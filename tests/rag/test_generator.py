from unittest.mock import MagicMock, patch

import pytest

from ragxiv.rag import LLMGenerator, answer_to_dict


@pytest.mark.parametrize(
    "token_limit, mocked_answer, check_result",
    [
        # over token limit
        (500000, "", False),
        # normal answer
        (512, "Mocked response", True),
    ],
)
def test_llm_generator_generate_mocked(
    token_limit: int, mocked_answer: str, check_result: bool
):
    """Tests the `_check_tokens_limit` and `generate` methods of the `LLMGenerator` class."""
    # Mock OllamaLLM + AutoTokenizer
    with (
        patch("ragxiv.rag.generator.OllamaLLM") as mock_llm_cls,
        patch("ragxiv.rag.generator.AutoTokenizer") as mock_tokenizer_cls,
    ):
        # --- Mock the tokenizer ---
        mock_tokenizer = MagicMock()
        mock_tokenizer.return_value = {"input_ids": list(range(token_limit))}
        mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer

        # --- Mock the LLM ---
        mock_llm = MagicMock()
        mock_llm.model = "deepseek-r1"
        mock_llm.invoke.return_value = mocked_answer
        mock_llm_cls.return_value = mock_llm

        # Generates a mocked prompt and answer from the LLM
        generator = LLMGenerator(model="deepseek-r1", text="mock input")
        prompt = "Extract all computational methods."
        assert generator._check_tokens_limit(prompt=prompt) == check_result
        assert generator.generate(prompt=prompt) == mocked_answer


@pytest.mark.parametrize(
    "answer, result",
    [
        # no list of dictionaries
        ("no list of dictionaries found", []),
        # successful
        (
            '[\n    {"answer": "This is the answer."}\n]',
            [{"answer": "This is the answer."}],
        ),
    ],
)
def test_answer_to_dict(answer: str, result: list[dict]):
    """Tests the `answer_to_dict` utility function."""
    assert answer_to_dict(answer=answer) == result
