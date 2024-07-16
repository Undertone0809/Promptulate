"""
TODO add test: test pne's llm, test litellm llm
"""

from typing import Generator, Optional, Union

import pytest

import promptulate as pne
from promptulate import chat
from promptulate.llms import BaseLLM
from promptulate.pydantic_v1 import BaseModel, Field
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    UserMessage,
)


class StreamLLM(BaseLLM):
    def _predict(
        self, messages: MessageSet, *args, **kwargs
    ) -> Optional[type(BaseMessage)]:
        messages: list = [
            AssistantMessage(content="This", additional_kwargs={}),
            AssistantMessage(content="is", additional_kwargs={}),
            AssistantMessage(content="fake", additional_kwargs={}),
            AssistantMessage(content="message", additional_kwargs={}),
        ]

        for message in messages:
            yield message


class FakeLLM(BaseLLM):
    llm_type: str = "fake"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, instruction: str, *args, **kwargs):
        return "fake response"

    def _predict(
        self, messages: MessageSet, *args, **kwargs
    ) -> Union[BaseMessage, Generator]:
        content = "fake response"
        if "Output format" in messages.messages[-1].content:
            content = """{"city": "Shanghai", "temperature": 25}"""
        return AssistantMessage(content=content, additional_kwargs={})


def mock_tool():
    """This is mock tool"""
    return "mock tool"


class LLMResponse(BaseModel):
    city: str = Field(description="city name")
    temperature: float = Field(description="temperature")


def test_init():
    llm = FakeLLM()

    # not model and custom_llm
    with pytest.raises(ValueError) as e:
        chat("hello")
        assert str(e.value) == "model or custom_llm must be provided."

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        chat(messages="hello", custom_llm=llm, output_schema=LLMResponse, stream=True)

    # stream and tools and not exist at the same time.
    with pytest.raises(ValueError):
        chat("hello", custom_llm=llm, tools=[mock_tool], stream=True)

    # It is not allowed to pass MessageSet or List[Dict] type messages when using tools.
    with pytest.raises(ValueError):
        chat(
            MessageSet(messages=[UserMessage(content="hello")]),
            custom_llm=llm,
            tools=[mock_tool],
        )
        chat([], custom_llm=llm, tools=[mock_tool])

    with pytest.raises(ValueError) as e:
        chat("hello", model="gpt-3.5-turbo", custom_llm=llm)
        assert (
            str(e.value) == "model and custom_llm can't be provided at the same time."
        )

    with pytest.raises(ValueError) as e:
        chat("hello", model_config={"model": "gpt-3.5-turbo"}, custom_llm=llm)
        assert (
            str(e.value)
            == "model_config and custom_llm can't be provided at the same time."
        )


def test_custom_llm_chat():
    llm = FakeLLM()

    # test general chat
    answer = chat("hello", custom_llm=llm)
    assert answer == "fake response"

    # test messages is MessageSet
    messages = MessageSet(
        messages=[UserMessage(content="hello"), AssistantMessage(content="fake")]
    )
    answer = chat(messages, custom_llm=llm)
    assert answer == "fake response"

    # test messages is list
    messages = [{"content": "Hello, how are you?", "role": "user"}]
    answer = chat(messages, custom_llm=llm)
    assert answer == "fake response"


def test_custom_llm_chat_response():
    llm = FakeLLM()

    # test original response
    answer = chat("hello", custom_llm=llm, return_raw_response=True)
    assert isinstance(answer, BaseMessage)
    assert answer.content == "fake response"

    # test formatter response
    answer = chat(
        "what's weather tomorrow in shanghai?",
        output_schema=LLMResponse,
        custom_llm=llm,
    )
    assert isinstance(answer, LLMResponse)
    assert getattr(answer, "city", None) == "Shanghai"
    assert getattr(answer, "temperature", None) == 25

    # test formatter response with examples
    examples = [
        LLMResponse(city="Shanghai", temperature=25),
        LLMResponse(city="Beijing", temperature=30),
    ]
    answer = chat(
        "what's weather tomorrow in shanghai?",
        output_schema=LLMResponse,
        examples=examples,
        custom_llm=llm,
    )
    assert isinstance(answer, LLMResponse)
    assert getattr(answer, "city", None) == "Shanghai"
    assert getattr(answer, "temperature", None) == 25


def test_stream():
    class LLMResponse(BaseModel):
        data: Optional[str] = None

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        pne.chat("hello", stream=True, output_schema=LLMResponse)


def test_streaming():
    llm = StreamLLM()

    # test stream output
    answer_stream = pne.chat(
        "what's weather tomorrow in shanghai?",
        custom_llm=llm,
        stream=True,
    )

    # check if the answer is a stream of response
    answer: list = []
    for item in answer_stream:
        answer.append(item)

    assert len(answer) == 4
    assert answer[0].content == "This"
    assert answer[1].content == "is"
    assert answer[2].content == "fake"
    assert answer[3].content == "message"
