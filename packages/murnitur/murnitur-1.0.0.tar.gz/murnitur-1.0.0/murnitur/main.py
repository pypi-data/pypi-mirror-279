import re
import json
import openlit as lit
from contextlib import contextmanager
from functools import wraps
from enum import Enum
from typing import List, Dict
from openlit.otel.tracing import trace as t
from openlit.semcov import SemanticConvetion
from opentelemetry.trace import SpanKind, Status, StatusCode, Span
from .tracer import setup_tracing
from .util import Util


class Config:
    environment: str
    app_name: str
    api_key: str = ""


class Prompt:
    messages = []
    id: str = ""
    name: str = ""

    def __init__(self, id: str, name: str, messages: List) -> None:
        self.id = id
        self.name = name
        self.messages = messages


class Preset:
    active_version: Prompt = None
    versions: List[Prompt] = []

    def __init__(self, preset):
        active = preset["PresetPrompts"][0]
        self.active_version = Prompt(
            id=active["id"], name=active["name"], messages=active["prompts"]
        )
        self.versions = [
            Prompt(id=curr["id"], name=curr["name"], messages=curr["prompts"])
            for curr in preset["PresetPrompts"]
        ]


class Environment(Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    STAGING = "staging"


class TracedSpan:
    def __init__(self, span):
        self._span: Span = span

    def log(self, name: str, payload: Dict):
        if self._span.is_recording():
            __trace = t.get_tracer_provider()
            with __trace.get_tracer(__name__).start_span(
                name=name,
                kind=SpanKind.CLIENT,
            ) as child:
                child.set_attribute("type", "log")
                child.set_attribute("log-data", json.dumps(payload, indent=4))

    def set_result(self, result):
        self._span.set_attribute(SemanticConvetion.GEN_AI_CONTENT_COMPLETION, result)

    def set_metadata(self, metadata: Dict):
        self._span.set_attributes(attributes=metadata)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._span.end()


@contextmanager
def tracer(name: str):
    __trace = t.get_tracer_provider()
    with __trace.get_tracer(__name__).start_as_current_span(
        name,
        kind=SpanKind.CLIENT,
    ) as span:
        yield TracedSpan(span)


def trace(wrapped):
    """
    Generates a telemetry wrapper for messages to collect metrics.
    """

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        __trace = t.get_tracer_provider()
        with __trace.get_tracer(__name__).start_as_current_span(
            name=wrapped.__name__,
            kind=SpanKind.CLIENT,
        ) as span:
            try:
                response = wrapped(*args, **kwargs)
                span.set_attribute(
                    SemanticConvetion.GEN_AI_CONTENT_COMPLETION, response
                )
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                response = None
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR))
                lit.logging.error(f"Error in {wrapped.__name__}: {e}", exc_info=True)

            # Adding function arguments as metadata
            try:
                span.set_attribute("function.args", str(args))
                span.set_attribute("function.kwargs", str(kwargs))
                span.set_attribute(
                    SemanticConvetion.GEN_AI_APPLICATION_NAME, Config.app_name
                )
                span.set_attribute(
                    SemanticConvetion.GEN_AI_ENVIRONMENT, Config.environment
                )
            except Exception as meta_exception:
                lit.logging.error(
                    f"Failed to set metadata for {wrapped.__name__}: {meta_exception}",
                    exc_info=True,
                )

            return response

    return wrapper


def log(name: str, payload: Dict):
    __trace = t.get_tracer_provider()
    with __trace.get_tracer(__name__).start_span(
        name=name,
        kind=SpanKind.CLIENT,
    ) as child:
        child.set_attribute("type", "log")
        child.set_attribute("log-data", json.dumps(payload, indent=4))


def set_api_key(api_key: str):
    Config.api_key = api_key


def get_api_key():
    return Config.api_key


def load_preset(name):
    code, content = Util().get_preset(name=name, api_key=Config.api_key)
    if content:
        return Preset(content)
    return None


def format_prompt(messages: List, params: Dict):
    def replace_match(match):
        variable_name = match.group(1)
        return str(params.get(variable_name, f"{{{{{variable_name}}}}}"))

    replaced_templates = []
    for template in messages:
        new_template = {}
        for key, value in template.items():
            if isinstance(value, str):
                new_value = re.sub(r"\{\{([\w-]+)\}\}", replace_match, value)
                new_template[key] = new_value
            else:
                new_template[key] = value
        replaced_templates.append(new_template)

    return replaced_templates


def init(project_name: str, environment: Environment = Environment.DEVELOPMENT):
    if len(Config.api_key.strip()) == 0:
        print("Please provide a valid API key!")
        return

    Config.app_name = project_name
    Config.environment = environment.value

    # Setup tracer
    tracer = setup_tracing(
        application_name=project_name,
        environment=environment.value,
        otlp_headers=f"x-murnix-trace-token={Config.api_key}",
        disable_batch=False,
        tracer=None,
    )

    lit.init(
        environment=environment.value,
        application_name=project_name,
        disable_metrics=True,
        tracer=tracer,
    )
