import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from hwrag.refiner.filter import Filter

filters = [
    Filter.from_dict(
        {
            "subclass_name": "ScoreFilter",
        }
    ),
    Filter.from_dict(
        {
            "subclass_name": "NoFilter",
        }
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("filter", filters)
async def test_filter(filter: Filter, mock_documennts_with_score):
    from hwrag.refiner.filter import NoFilter, ScoreFilter

    documents = mock_documennts_with_score
    if isinstance(filter, NoFilter):
        new_documents = filter.invoke(documents)
        assert isinstance(documents, list)
        assert len(documents) == len(new_documents)
    if isinstance(filter, ScoreFilter):
        documents = filter.invoke(documents, 4)
        assert isinstance(documents, list)
        assert len(documents) <= 4


if __name__ == "__main__":
    pytest.main()
