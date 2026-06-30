import json
import tempfile

from src.projection.projection_engine import ProjectionEngine

from src.core.models import Candidate

from src.utils.reader_utils import create_field_value

from src.core.enums import (
    SourceType,
    ExtractionMethod,
)


def test_projection():

    config = {

        "include_confidence": False,

        "missing_strategy": "null",

        "fields": [

            {

                "from": "full_name",

                "to": "name",

                "normalize": True,

            }

        ]

    }

    with tempfile.NamedTemporaryFile(
        suffix=".json",
        mode="w",
        delete=False,
    ) as file:

        json.dump(
            config,
            file,
        )

        path = file.name

    candidate = Candidate()

    candidate.full_name = create_field_value(

        "Harikaran",

        SourceType.CSV,

        ExtractionMethod.CSV_MAPPING,

    )

    projection = ProjectionEngine(path)

    result = projection.project(candidate)

    assert result["name"] == "Harikaran"