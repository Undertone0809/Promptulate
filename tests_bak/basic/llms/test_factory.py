from unittest import mock

import pytest

import promptulate as pne


def test_init_litellm():
    import litellm

    with pytest.raises(litellm.exceptions.APIConnectionError) as e:
        model = pne.LLMFactory.build(model_name="claude-2")
        model("hello")

        assert (
            str(e.value)
            == "Missing Anthropic API Key - A call is being made to anthropic but no key is set either in the environment variables or via params"  # noqa
        )


# TODO: remove test other type llm
# def test_init_zhipu():
#     with pytest.raises(KeyError) as e:
#         model = pne.LLMFactory.build(model_name="zhipu/glm4")
#         model("hello")
#         assert (
#             str(e.value)
#             == "ValueError: ZHIPUAI_API_KEY is not provided. Please set your key."
#         )


# @pytest.fixture
# def llm_factory():
#     return pne.LLMFactory.build("zhipu/glm4")


# @pytest.fixture
# def mock_response():
#     mock_resp = mock.Mock()
#     mock_resp.status_code = 200
#     mock_resp.json.return_value = {
#         "choices": [{"message": {"content": "[start] This is a test [end]"}}]
#     }
#     return mock_resp


# @mock.patch("requests.post")
# def test_call(mock_post, llm_factory, mock_response):
#     # Use the mock response
#     mock_post.return_value = mock_response

#     llm_factory.set_private_api_key("my key.hello")
#     prompt = """
#     Please strictly output the following content.
#     ```
#     [start] This is a test [end]
#     ```
#     """
#     result = llm_factory(prompt)
#     assert result is not None
#     assert "[start] This is a test [end]" in result
