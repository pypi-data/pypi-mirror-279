import random
from collections.abc import Callable
from typing import List, Optional, Union

import pandas as pd
import quattro
from sammo.base import EvaluationScore, Runner
from sammo.compactbars import CompactProgressBars
from sammo.components import Output
from sammo.data import DataTable
from sammo.dataformatters import PlainFormatter
from sammo.instructions import (
    FewshotExamples,
    InputData,
    MetaPrompt,
    Paragraph,
    Section,
)
from sammo.mutators import (
    BagOfMutators,
    InduceInstructions,
    Paraphrase,
    ReplaceParameter,
)
from sammo.runners import BaseRunner, LLMResult
from sammo.search import BeamSearch
from sammo.utils import serialize_json

from ..llms.llm import NDLLM
from ..llms.provider import NDLLMProvider


class InititialCandidates:
    def __init__(
        self, dtrain: DataTable, initial_prompt: Optional[str] = None
    ):
        self.dtrain = dtrain
        self.initial_prompt = initial_prompt if initial_prompt else ""

    def __call__(self):
        example_formatter = PlainFormatter(
            all_labels=self.dtrain.outputs.unique(), orient="item"
        )

        instructions = MetaPrompt(
            [
                Paragraph(
                    self.initial_prompt,
                    id="instructions",
                ),
                Paragraph("\n"),
                Paragraph("", id="few_shot"),
                Paragraph(InputData()),
            ],
            render_as="raw",
            data_formatter=example_formatter,
        )

        return Output(
            instructions.with_extractor("raise"),
            minibatch_size=1,
            on_error="empty_result",
        )


class TargetLLMRunner(BaseRunner):
    def __init__(
        self, llm: NDLLMProvider, api_key: Optional[str] = None, **kwargs
    ):
        super().__init__(**kwargs)
        self.llm = llm
        self.client = NDLLM(api_key=api_key)

    async def generate_text(
        self,
        prompt: str,
        priority: int = 0,
        **kwargs,
    ) -> LLMResult:
        request = dict(
            messages=[{"role": "user", "content": prompt}],
        )
        fingerprint = serialize_json(
            {"generative_model_id": self._model_id, **request}
        )
        return await self._execute_request(request, fingerprint, priority)

    async def _call_backend(self, request: dict) -> dict:
        result, _, _ = self.client.chat.completions.create(
            messages=request["messages"], model=[self.llm]
        )
        return {"response": result.content}

    def _to_llm_result(
        self, request: dict, json_data: dict, fingerprint: str | bytes
    ):
        return LLMResult(
            json_data["response"],
        )


class NDBeamSearch(BeamSearch):
    async def afit_transform(
        self,
        dataset: DataTable,
    ) -> DataTable:
        self._reset()
        self._mutator.update_priors(self._action_stats)
        self._mutator.objective = self._objective
        initial_candidates = await self._mutator.get_initial_candidates(
            self._runner, self._n_initial_candidates
        )

        colbar = CompactProgressBars()

        active_set = await self.evaluate(
            [c.candidate for c in initial_candidates],
            self._runner,
            self._objective,
            dataset,
            colbar,
            True,
        )
        active_set = self.argsort(
            [
                {**x, "action": c.action, "prev_actions": [c.action]}
                for c, x in zip(initial_candidates, active_set)
            ]
        )
        self.log(-1, active_set)
        active_set = self._update_active_set(active_set, active_set)
        rng = random.Random(42)

        depth_pbar = colbar.get("Optimization step", total=self._depth)
        for d in range(self._depth):
            # Mutate candidates in parallel
            mutation_tasks = list()

            candidates_for_mutation = self._pick_candidates_for_mutation(
                active_set, rng
            )
            async with quattro.TaskGroup() as g:
                for i, x in enumerate(candidates_for_mutation):
                    task = g.create_task(
                        self._mutator.mutate(
                            x["candidate"],
                            dataset,
                            self._runner,
                            n_mutations=self._n_mutations,
                            random_state=d
                            * self._beam_width
                            * self._n_mutations
                            + i,
                        )
                    )
                    mutation_tasks.append(task)

            # Prune mutation set if necessary
            mutations = list()
            for parent, mutation_task in zip(
                candidates_for_mutation, mutation_tasks
            ):
                offspring = mutation_task.result()
                mutations += [x.with_parent(parent) for x in offspring]

            if self._max_evals:
                n_evals = len(self._state["fit"])
                if len(mutations) + n_evals > self._max_evals:
                    mutations = mutations[: self._max_evals - n_evals]

            if not mutations:
                break

            # Evaluate candidates in parallel
            scored_mutations = await self.evaluate(
                [m.candidate for m in mutations],
                self._runner,
                self._objective,
                dataset,
                colbar,
                False,
            )
            scored_mutations = [
                {
                    **m_scored,
                    "prev_actions": [m.action] + m.parent["prev_actions"],
                    "action": m.action,
                }
                for m, m_scored in zip(mutations, scored_mutations)
            ]
            self.log(d, scored_mutations)
            if self._add_previous:
                scored_mutations += active_set

            active_set = self._update_active_set(active_set, scored_mutations)

            depth_pbar.update()

        colbar.finalize()
        self._update_priors()
        self._state["fit_costs"] = self._runner.costs.to_dict()
        return self._updated_best()

    async def evaluate(
        self,
        candidates: list[Output],
        runner: Runner,
        objective: Callable[[DataTable, DataTable], EvaluationScore],
        dataset: DataTable,
        colbar: CompactProgressBars,
        initialize: bool,
    ) -> list[dict]:
        if not candidates:
            return list()

        subtasks_total = sum([m.n_minibatches(dataset) for m in candidates])
        if initialize:
            subtasks_cb = colbar.get(
                "Initializing", total=subtasks_total
            ).update
        else:
            subtasks_cb = colbar.get("Subtasks", total=subtasks_total).update

        evaluation_tasks = list()
        async with quattro.TaskGroup() as g:
            for i, candidate in enumerate(candidates):
                task = g.create_task(
                    candidate.arun(runner, dataset, subtasks_cb, i)
                )
                evaluation_tasks.append(task)

        scored_mutations = list()
        for candidate, y_pred in zip(candidates, evaluation_tasks):
            scored_mutations.append(
                self._candidate_record(
                    candidate, dataset, y_pred.result(), objective=objective
                )
            )

        return scored_mutations


class PromptOptimizer:
    """
    Implementation of PromptOptimizer class, used to optimize prompts.
    """

    llm_providers: List[NDLLMProvider]
    """The list of LLM providers that you want to optimize the prompt for."""

    objective: Callable
    """The objective function to maximize."""

    rate_limit: int
    """The number of LLM calls per second. By default this is 2."""

    max_retries: int
    """The maximum number of retries if an LLM call fails. By default this is 1."""

    timeout: float
    """The wait time in seconds before an LLM call times out. By default this is 60 seconds."""

    api_key: Optional[str]
    """
    API key required for making calls to NotDiamond.
    You can get an API key via our dashboard: https://app.notdiamond.ai
    If an API key is not set, it will check for NOTDIAMOND_API_KEY in .env file.
    """

    def __init__(
        self,
        llm_providers: Union[List[NDLLMProvider], List[str]],
        objective: Callable,
        rate_limit: int = 2,
        max_retries: int = 1,
        timeout: float = 60,
        api_key: Optional[str] = None,
    ):
        self.llm_providers = NDLLM._parse_llm_providers_data(llm_providers)
        self.objective = objective
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.timeout = timeout
        self.api_key = api_key

        self.best_provider_prompt = None

        self.depth = 3
        self.mutations_per_beam = 2
        self.n_initial_candidates = 4
        self.beam_width = 4

    def optimize(
        self,
        dataset: pd.DataFrame,
        input_column: str,
        output_column: str,
        initial_prompt: Optional[str] = None,
    ):
        """
        Method to run the optimizer on the provided dataset.

        Parameters:
            dataset (pandas.DataFrame): The optimizer dataset in a pandas DataFrame.
            input_column (str): The column in the DataFrame corresponding to the
                              input prompt.
            output_column (str): The column in the DataFrame corresponding to the
                               output prompt.
            initial_prompt (Optional[str]): An initial prompt to use for the optimizer.
        Raises:
            ValueError("The dataset must be in a pandas dataframe."): When the dataset is not
                                                                      a pandas DataFrame.
            ValueError(f"Input column {input_column} not in dataframe."): When the specified
                                                         input column is not in the DataFrame.
            ValueError(f"Output column {input_column} not in dataframe."): When the specified
                                                        output column is not in the DataFrame.
        """
        if not isinstance(dataset, pd.DataFrame):
            raise ValueError("The dataset must be in a pandas dataframe.")

        if input_column not in dataset.columns:
            raise ValueError(f"Input column {input_column} not in dataframe.")

        if output_column not in dataset.columns:
            raise ValueError(
                f"Output column {output_column} not in dataframe."
            )

        try:
            d_train = DataTable.from_pandas(
                dataset, input_fields=input_column, output_fields=output_column
            )
        except Exception as e:
            raise ValueError(f"Error loading dataset: {str(e)}")

        mutation_operators = BagOfMutators(
            InititialCandidates(d_train, initial_prompt),
            InduceInstructions({"id": "instructions"}, d_train),
            Paraphrase({"id": "instructions"}),
            ReplaceParameter(
                {"id": "few_shot"},
                choices=Section(
                    "Examples",
                    FewshotExamples(d_train.sample(3, seed=43)),
                    id="few_shot",
                ),
            ),
            sample_for_init_candidates=False,
        )

        def objective_fn(
            y_true: DataTable, y_pred: DataTable
        ) -> EvaluationScore:
            y_targets = y_true.outputs.normalized_values()
            y_predictions = y_pred.outputs.normalized_values()
            score = self.objective(y_targets, y_predictions)
            return EvaluationScore(score)

        self.best_provider_prompt = {}
        for provider in self.llm_providers:
            model_id = f"{provider.provider}/{provider.model}"
            print(f"Optimizing prompt for {model_id}...")

            runner = TargetLLMRunner(
                provider,
                api_key=self.api_key,
                api_config={"api_key": provider.api_key},
                model_id=model_id,
                rate_limit=self.rate_limit,
                max_retries=self.max_retries,
                timeout=self.timeout,
            )

            optimizer = NDBeamSearch(
                runner=runner,
                mutator=mutation_operators,
                objective=objective_fn,
                maximize=True,
                depth=self.depth,
                mutations_per_beam=self.mutations_per_beam,
                n_initial_candidates=self.n_initial_candidates,
                beam_width=self.beam_width,
                add_previous=True,
            )

            try:
                optimizer.fit(d_train)
            except Exception:
                raise RuntimeError(
                    "An error ocurred while optimizing the prompt."
                )

            self.best_provider_prompt[model_id] = {
                "prompt": optimizer.best_prompt._child._child._child._child[
                    0
                ].content[
                    0
                ],  # FIXME make this more dynamic
                "score": optimizer.best_score,
                "initial_score": optimizer._state["fit"][0]["objective"],
            }

    @property
    def optimized_prompt(self):
        """
        Return a dictionary of the best prompts found for each provider.
        The keys are the provider strings and the item is a dictionary containing "prompt", "score", and "initial_score".
        """
        if not self.best_provider_prompt:
            raise ValueError("Need to run optimizer first.")
        return self.best_provider_prompt
