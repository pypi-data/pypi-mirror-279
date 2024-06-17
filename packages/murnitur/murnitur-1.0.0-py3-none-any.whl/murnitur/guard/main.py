import requests
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict, Optional, List, Literal, Union
from .lib import check_pii, detect_tone, detect_injection, detect_toxicity, detect_bias

Value = Union[str, int, List[str]]


class Payload(TypedDict):
    input: Optional[str]
    output: Optional[str]


class Rule(TypedDict):
    metric: Literal[
        "pii", "input_pii", "toxicity", "input_tone", "tone", "bias", "prompt_injection"
    ]
    operator: Literal[
        "equal",
        "not_equal",
        "contains",
        "greater_than",
        "less_than",
        "greater_than_equal",
        "less_than_equal",
        "any",
        "all",
    ]
    value: Value


class Action(TypedDict):
    type: Literal["OVERRIDE", "FLAG"]
    fallback: str


class RuleSet(TypedDict):
    rules: List[Rule]
    action: Action


class Guard:
    executor = ThreadPoolExecutor(max_workers=5)

    @staticmethod
    def send_interception_to_backend(data, api_key: str):
        if api_key is not None:
            try:
                response = requests.post(
                    "https://api.murnitur.ai/api/interceptions",
                    json=data,
                    headers={"x-murnix-trace-token": api_key},
                )
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to send interception: {e}")

    @staticmethod
    def __preprocess_rules(rulesets: List[RuleSet]):
        processed_rules = []
        for ruleset in rulesets:
            processed_rules.append(
                {
                    "rules": [
                        {
                            "metric": rule["metric"],
                            "operator": rule["operator"],
                            "value": (
                                rule["value"]
                                if isinstance(rule["value"], list)
                                else [rule["value"]]
                            ),
                        }
                        for rule in ruleset["rules"]
                    ],
                    "action": ruleset["action"],
                }
            )
        return processed_rules

    @staticmethod
    def shield(
        payload: Payload,
        rulesets: List[RuleSet],
        murnitur_key: Optional[str] = None,
        openai_key: Optional[str] = None,
        group: Optional[str] = None,
        model: Optional[str] = "gpt-3.5-turbo",
    ):
        """
        Shields the payload based on provided rulesets.

        Args:
            payload (dict): The input data to be checked.
            rulesets (list): A list of rules defining how to check the payload.
            murnitur_key (str): API key for Murnitur services.
            group (str, optional): Group name for categorization. Default is "untitled".
            openai_key (str, optional): API key for OpenAI services.
            model (str, optional): Model for OpenAI services. Default is "gpt-3.5-turbo"

        Returns:
            str: Response message after applying the rules.
        """
        try:
            preprocessed_rulesets = Guard.__preprocess_rules(rulesets)

            for ruleset in preprocessed_rulesets:
                action_type = ruleset["action"]["type"]
                fallback = ruleset["action"]["fallback"]

                for rule in ruleset["rules"]:
                    metric = rule["metric"]
                    operator = rule["operator"]
                    rule_value = rule["value"]

                    if metric in ("pii", "input_pii"):
                        pii_value = payload.get(
                            "output" if metric == "pii" else "input", ""
                        )
                        if check_pii(pii_value, operator, rule_value):
                            submit_interception(
                                payload,
                                fallback,
                                action_type,
                                rule,
                                ruleset,
                                metric,
                                group,
                                murnitur_key,
                            )
                            return (
                                fallback
                                if action_type == "OVERRIDE"
                                else f"Message flagged: {fallback}"
                            )

                    elif metric in ("tone", "input_tone"):
                        tone_value = payload.get(
                            "output" if metric == "tone" else "input", ""
                        )
                        if detect_tone(tone_value, operator, rule_value):
                            submit_interception(
                                payload,
                                fallback,
                                action_type,
                                rule,
                                ruleset,
                                metric,
                                group,
                                murnitur_key,
                            )
                            return (
                                fallback
                                if action_type == "OVERRIDE"
                                else f"Message flagged: {fallback}"
                            )

                    elif metric == "prompt_injection":
                        input_value = payload.get("input", "")
                        if detect_injection(
                            input_value, operator, rule_value, openai_key, model
                        ):
                            submit_interception(
                                payload,
                                fallback,
                                action_type,
                                rule,
                                ruleset,
                                metric,
                                group,
                                murnitur_key,
                            )
                            return (
                                fallback
                                if action_type == "OVERRIDE"
                                else f"Message flagged: {fallback}"
                            )

                    elif metric == "toxicity":
                        input_value = payload.get("input", "")
                        output_value = payload.get("output", "")
                        if detect_toxicity(
                            input_value,
                            output_value,
                            operator,
                            rule_value[0],
                            openai_key,
                            model,
                        ):
                            submit_interception(
                                payload,
                                fallback,
                                action_type,
                                rule,
                                ruleset,
                                metric,
                                group,
                                murnitur_key,
                            )
                            return (
                                fallback
                                if action_type == "OVERRIDE"
                                else f"Message flagged: {fallback}"
                            )

                    elif metric == "bias":
                        input_value = payload.get("input", "")
                        output_value = payload.get("output", "")
                        if detect_bias(
                            input_value,
                            output_value,
                            operator,
                            rule_value[0],
                            openai_key,
                            model,
                        ):
                            submit_interception(
                                payload,
                                fallback,
                                action_type,
                                rule,
                                ruleset,
                                metric,
                                group,
                                murnitur_key,
                            )
                            return (
                                fallback
                                if action_type == "OVERRIDE"
                                else f"Message flagged: {fallback}"
                            )

            return payload.get("output", "")

        except Exception as e:
            raise e


def submit_interception(
    payload, fallback, action_type, rule, ruleset, metric, group=None, murnitur_key=None
):
    """
    Submits an interception to the backend for processing asynchronously.

    Args:
        payload (dict): The input data to be intercepted.
        fallback (str): The fallback message.
        action_type (str): The action type, e.g., "OVERRIDE".
        rule (dict): The rule that triggered the interception.
        ruleset (dict): The ruleset containing the rule.
        group (str, optional): Group name for categorization. Default is None.
        murnitur_key (str, optional): API key for Murnitur services. Default is None.

    Returns:
        Future: A future object representing the execution of the interception.
    """
    group = group or "untitled"

    interception_data = {
        "group": group,
        "interception": {
            "input": payload.get("input"),
            "output": payload.get("output"),
            "metric": metric,
            "response": (
                fallback
                if action_type == "OVERRIDE"
                else f"Message flagged: {fallback}"
            ),
            "rule": rule,
            "action": ruleset["action"],
        },
    }

    return Guard.executor.submit(
        Guard.send_interception_to_backend, data=interception_data, api_key=murnitur_key
    )
