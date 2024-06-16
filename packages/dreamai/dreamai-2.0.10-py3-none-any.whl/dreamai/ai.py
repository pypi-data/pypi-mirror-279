import inspect
from enum import Enum
from typing import Callable, Optional, Type

import instructor
import tiktoken
from pydantic import BaseModel, create_model
from tenacity import Retrying, stop_after_attempt, wait_random


class ModelName(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_4O = "gpt-4o"
    GPT_4 = "gpt-4-turbo"
    HAIKU = "claude-3-haiku-20240307"
    SONNET = "claude-3-sonnet-20240229"
    OPUS = "claude-3-opus-20240229"
    GEMINI = "models/gemini-1.5-latest"
    GEMINI_FLASH = "models/gemini-1.5-flash-latest"
    MISTRAL = "anyscale/mistralai/Mistral-7B-Instruct-v0.1"
    MIXTRAL = "anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1"


MODEL = ModelName.GPT_3
ATTEMPTS = 2
MAX_TOKENS = 2048
TEMPERATURE = 0.3


def create_tool_model(func: Callable) -> Type[BaseModel]:
    sig = inspect.signature(func)
    fields = {}
    for name, parameter in sig.parameters.items():
        if parameter.annotation is not inspect.Parameter.empty and name != "return":
            is_required = parameter.default == inspect.Parameter.empty
            fields[name] = (
                parameter.annotation,
                ... if is_required else parameter.default,
            )
    model_name = "".join([s.title() for s in func.__name__.split("_")]) + "Tool"
    return create_model(model_name, **fields)


def count_gpt_tokens(text: str, model: ModelName = MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def chat_message(role: str, content: str) -> dict[str, str]:
    return {"role": role, "content": content}


def system_message(content: str) -> dict[str, str]:
    return chat_message(role="system", content=content)


def user_message(content: str) -> dict[str, str]:
    return chat_message(role="user", content=content)


def assistant_message(content: str) -> dict[str, str]:
    return chat_message(role="assistant", content=content)


def merge_same_role_messages(messages: list[dict]) -> list[dict]:
    if not messages:
        return []
    new_messages = []
    last_message = None
    for message in messages:
        if last_message is None:
            last_message = message
        elif last_message["role"] == message["role"]:
            last_message["content"] += "\n\n" + message["content"]
        else:
            new_messages.append(last_message)
            last_message = message
    if last_message is not None:
        new_messages.append(last_message)
    return new_messages


def oai_response(response) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return response


def claude_response(response) -> str:
    try:
        return response.content[0].text
    except Exception:
        return response


def ai_retry_attempts(attempts: int = 3):
    return (
        Retrying(wait=wait_random(min=1, max=40), stop=stop_after_attempt(attempts))
        if attempts > 1
        else 1
    )


def ask_cld_or_oai(
    ask_cld: instructor.Instructor,
    ask_oai: instructor.Instructor,
    messages: list[dict[str, str]],
    system: str = "",
    model: ModelName = MODEL,
    response_model: Optional[type] = None,
    attempts: int = ATTEMPTS,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE,
    validation_context: dict = {},
    ask_kwargs: dict = {},
):
    ask_kwargs["model"] = model
    ask_kwargs["max_retries"] = attempts
    ask_kwargs["max_tokens"] = max_tokens
    ask_kwargs["temperature"] = temperature
    ask_kwargs["response_model"] = response_model
    ask_kwargs["validation_context"] = validation_context
    # print(f"ASK_KWARGS:\n{ask_kwargs}")
    try:
        if "gpt" in ask_kwargs["model"].lower():
            if system:
                messages.insert(0, system_message(system))
            res = ask_oai.create(
                messages=messages,  # type: ignore
                **ask_kwargs,
            )
            if response_model is None:
                return oai_response(res)
            return res
        else:
            res = ask_cld.create(
                system=system,
                messages=merge_same_role_messages(messages),  # type: ignore
                **ask_kwargs,
            )
            if response_model is None:
                return claude_response(res)
            return res
    except Exception as e:
        print(f"Error in ask_cld_or_oai. Messages: {messages}")
        print(e)
        return None
