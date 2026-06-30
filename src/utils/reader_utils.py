
from __future__ import annotations
from typing import Any
from core.enums import ExtractionMethod, SourceType
from core.models import FieldValue, Provenance

DEFAULT_CONFIDENCE = {
    SourceType.CSV: 0.95,
    SourceType.RESUME: 0.85,
    SourceType.GITHUB: 0.90,
    SourceType.LINKEDIN: 0.90,
    SourceType.ATS: 0.95,
    SourceType.MANUAL: 1.00,
}


def create_field_value(
    value: Any,
    source: SourceType,
    extraction_method: ExtractionMethod,
    confidence: float | None = None,
    reader_name: str | None = None,
) -> FieldValue:
 

    if confidence is None:
        confidence = DEFAULT_CONFIDENCE.get(source, 0.80)

    provenance = Provenance(
        source=source,
        extraction_method=extraction_method,
        original_value=str(value),
        reader_name=reader_name,
    )

    return FieldValue(
        value=value,
        confidence=confidence,
        provenance=[provenance],
    )


def split_comma_separated(value: str | None) -> list[str]:
   

    if value is None:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def is_missing(value: Any) -> bool:

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    return False