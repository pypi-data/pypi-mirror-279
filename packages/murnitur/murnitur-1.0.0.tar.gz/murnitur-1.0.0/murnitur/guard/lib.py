import re
import os
from typing import Union, List
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ToxicityMetric, BiasMetric
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .prompt_injection import PromptInjectionDetector

analyzer = SentimentIntensityAnalyzer()

pii_patterns = {
    "address": r"\d{1,5}\s\w{1,2}\.\s(\b\w+\b\s){1,2}\w+\.",
    "date": r"\d{1,2}/\d{1,2}/\d{4}",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "financial_info": r"\b(?:\d[ -]*?){13,16}\b",
    "phone_number": re.compile(
        r"(?:\+?\d{1,3})?[-.\s]?(\(?\d{2,4}\)?)?[-.\s]?\d{3,4}[-.\s]?\d{4,9}"
    ),
    "ssn": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",
}


def evaluate_rule(
    value: Union[int, str], operator: str, payload_value: Union[str, int]
) -> bool:
    operators = {
        "equal": lambda x, y: x == y,
        "not_equal": lambda x, y: x != y,
        "contains": lambda x, y: y in x,
        "greater_than": lambda x, y: x > y,
        "less_than": lambda x, y: x < y,
        "greater_than_equal": lambda x, y: x >= y,
        "less_than_equal": lambda x, y: x <= y,
        "any": lambda x, y: any(item in y for item in x),
        "all": lambda x, y: all(item in y for item in x),
    }

    if isinstance(payload_value, str) and operator in (
        "greater_than",
        "less_than",
        "greater_than_equal",
        "less_than_equal",
    ):
        try:
            payload_value = int(payload_value)
        except ValueError:
            return False

    return operators[operator](payload_value, value)


def check_pii(payload: str, operator: str, value: Union[str, List[str]]) -> bool:
    if operator == "contains":
        return any(
            re.findall(pii_patterns[pattern], payload)
            for pattern in value
            if pattern in pii_patterns
        )
    elif operator == "any":
        return any(
            re.findall(pii_patterns[pattern], payload)
            for pattern in value
            if pattern in pii_patterns
        )
    elif operator == "all":
        return all(
            re.findall(pii_patterns[pattern], payload)
            for pattern in value
            if pattern in pii_patterns
        )


def detect_tone(payload: str, operator: str, value: Union[str, List[str]]) -> bool:
    def detect(text):
        sentiment = analyzer.polarity_scores(text)
        compound_score = sentiment["compound"]

        tones = []

        if compound_score >= 0.05:
            if sentiment["pos"] > 0.6:
                tones.append("joy")
            if sentiment["pos"] > 0.4:
                tones.append("love")
            if "joy" not in tones and "love" not in tones:
                tones.append("positive")
        elif compound_score <= -0.05:
            if sentiment["neg"] > 0.6:
                tones.append("anger")
            if sentiment["neg"] > 0.4:
                tones.append("annoyance")
            if sentiment["neg"] > 0.2:
                tones.append("sadness")
            if (
                "anger" not in tones
                and "annoyance" not in tones
                and "sadness" not in tones
            ):
                tones.append("negative")
        else:
            tones.append("neutral")

        return tones, sentiment

    tones, _ = detect(payload)
    if isinstance(value, str):
        value = [value]
    if operator == "equal" or operator == "contains" or operator == "any":
        return any(tone in value for tone in tones)
    elif operator == "not_equal":
        return any(tone not in value for tone in tones)


def detect_injection(
    payload: str, operator: str, value: Union[str, List[str]], api_key: str, model: str
) -> bool:

    injection_score = PromptInjectionDetector(
        api_key=api_key, model=model
    ).detect_prompt_injection(payload)
    if injection_score:
        injection_type = injection_score["type"]

        if isinstance(value, str):
            value = [value]
        if operator == "equal" or operator == "contains":
            return injection_type in value
        elif operator == "not_equal":
            return injection_type not in value


def detect_toxicity(
    input: str, output: str, operator: str, value: int, api_key: str, model: str
) -> bool:
    os.environ["OPENAI_API_KEY"] = api_key
    test_case = LLMTestCase(input=input, actual_output=output)
    metric = ToxicityMetric(
        model=model, include_reason=True, async_mode=False, strict_mode=True
    )
    result = metric.measure(test_case)
    res = evaluate_rule(value, operator, result)
    return res


def detect_bias(
    input: str, output: str, operator: str, value: int, api_key: str, model: str
) -> bool:
    os.environ["OPENAI_API_KEY"] = api_key
    test_case = LLMTestCase(input=input, actual_output=output)
    metric = BiasMetric(
        model=model, include_reason=True, async_mode=False, strict_mode=True
    )
    result = metric.measure(test_case)
    res = evaluate_rule(value, operator, result)
    return res
