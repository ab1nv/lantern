import pytest

from unittest.mock import AsyncMock, MagicMock
from lantern.leetcode import LeetCodeClient


@pytest.mark.asyncio
async def test_fetch_problem_data_success():
    client = LeetCodeClient()

    mock_response_data = {
        "data": {
            "question": {
                "questionFrontendId": "1",
                "title": "Two Sum",
                "difficulty": "Easy",
                "topicTags": [{"name": "Array"}, {"name": "Hash Table"}],
            }
        }
    }

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.post = MagicMock(return_value=mock_response)

    result = await client.fetch_problem_data(mock_session, "two-sum")

    assert result is not None
    assert result["question_id"] == "1"
    assert result["question_title"] == "Two Sum"
    assert result["difficulty"] == "Easy"
    assert "Array" in result["topic_tags"]


@pytest.mark.asyncio
async def test_fetch_problem_data_failure():
    client = LeetCodeClient()

    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.post = MagicMock(return_value=mock_response)

    result = await client.fetch_problem_data(mock_session, "invalid-slug")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_problem_data_invalid_response():
    client = LeetCodeClient()

    mock_response_data = {"data": {}}

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.post = MagicMock(return_value=mock_response)

    result = await client.fetch_problem_data(mock_session, "two-sum")

    assert result is None
