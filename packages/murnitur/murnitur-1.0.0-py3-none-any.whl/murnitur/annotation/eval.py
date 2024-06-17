import os
from ..util import Util
from typing import List, Dict, Optional
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import (
    AnswerRelevancyMetric,
    HallucinationMetric,
    BiasMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ToxicityMetric,
    SummarizationMetric,
)
from .pii import PIIMetric


class Evaluation:

    def __init__(
        self, openai_key: str, murnitur_key: str, model: str = "gpt-3.5-turbo"
    ):
        os.environ["OPENAI_API_KEY"] = openai_key
        self.model = model
        self.api_key = murnitur_key

        pii_metric = PIIMetric(threshold=0.1)
        hallucination_metric = HallucinationMetric(
            threshold=0.3, model=model, strict_mode=True
        )
        answer_relevancy_metric = AnswerRelevancyMetric(
            threshold=0.5, model=model, strict_mode=True
        )
        faithfullness_metric = FaithfulnessMetric(model=model, strict_mode=True)
        bias_metric = BiasMetric(model=model, strict_mode=True)
        context_relevancy_metric = ContextualRelevancyMetric(
            model=model, strict_mode=True
        )
        context_precision_metric = ContextualPrecisionMetric(
            model=model, strict_mode=True
        )
        toxicity_metric = ToxicityMetric(model=model, strict_mode=True)
        summarization_metric = SummarizationMetric(model=model, strict_mode=True)

        self.all_metrics = {
            "hallucination": hallucination_metric,
            "faithfulness": faithfullness_metric,
            "relevancy": answer_relevancy_metric,
            "bias": bias_metric,
            "context-relevancy": context_relevancy_metric,
            "context-precision": context_precision_metric,
            "toxicity": toxicity_metric,
            "summarization": summarization_metric,
            "pii": pii_metric,
        }

    def run_suite(
        self,
        metrics: List[str],
        dataset: List[Dict],
        save_output: Optional[bool] = True,
        async_mode: Optional[bool] = True,
    ) -> List[Dict]:
        try:
            eval_dataset = EvaluationDataset(
                test_cases=[
                    LLMTestCase(
                        input=c["input"],
                        actual_output=c["output"],
                        context=c["context"],
                        retrieval_context=c["retrieval_context"],
                        expected_output=c["ground_truth"],
                    )
                    for c in dataset
                ]
            )
            result = self.__evaluate_outputs__(
                dataset=eval_dataset, metrics=metrics, async_mode=async_mode
            )
            if save_output:
                Util().send_metrics(
                    metrics=result,
                    runs=metrics,
                    headers={"x-murnix-trace-token": self.api_key},
                )
            return result
        except Exception as e:
            print(f"Error occured: {e}")

    def __evaluate_outputs__(
        self, dataset: EvaluationDataset, metrics: list[str], async_mode: bool
    ):
        allowed_metrics = []
        for m in metrics:
            if m in self.all_metrics:
                allowed_metrics.append(self.all_metrics[m])
        result = evaluate(
            dataset,
            allowed_metrics,
            write_cache=False,
            use_cache=False,
            print_results=False,
            run_async=async_mode,
            show_indicator=False,
        )
        output = []
        for r in result:
            metrics = [
                {
                    "name": m.__name__,
                    "cost": m.evaluation_cost,
                    "model": m.evaluation_model,
                    "threshold": m.threshold,
                    "score": m.score,
                    "reason": m.reason,
                    "error": m.error,
                    "success": m.success,
                }
                for m in r.metrics
            ]

            output.append(
                {
                    "input": r.input,
                    "success": r.success,
                    "output": r.actual_output,
                    "ground_truth": r.expected_output,
                    "context": r.context[0] if r.context is not None else "",
                    "retrieval_context": (
                        r.retrieval_context[0]
                        if r.retrieval_context is not None
                        else ""
                    ),
                    "metrics": metrics,
                }
            )

        return output
