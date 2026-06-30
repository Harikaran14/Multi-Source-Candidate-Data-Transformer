from src.merger.merge_engine import MergeEngine

from src.core.models import Candidate

from src.utils.reader_utils import create_field_value

from src.core.enums import (
    SourceType,
    ExtractionMethod,
)


def test_merge_email():

    c1 = Candidate()

    c2 = Candidate()

    c1.emails.append(

        create_field_value(

            "hari@gmail.com",

            SourceType.CSV,

            ExtractionMethod.CSV_MAPPING,

        )

    )

    c2.emails.append(

        create_field_value(

            "hari@gmail.com",

            SourceType.RESUME,

            ExtractionMethod.REGEX,

        )

    )

    merged = MergeEngine().merge(
        c1,
        c2,
    )

    assert len(merged.emails) == 1

    assert len(
        merged.emails[0].provenance
    ) >= 2