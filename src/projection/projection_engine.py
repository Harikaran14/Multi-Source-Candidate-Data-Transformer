from __future__ import annotations

import json
from pathlib import Path
from utils.normalizer import Normalizer
from core.models import (
    Candidate,
    FieldValue,
    Skill,
    Link,
)

class ProjectionEngine:

    def __init__(
        self,
        config_path: str | Path,
    ):

        with open(config_path) as file:
            self.config = json.load(file)

    def _resolve_path(
        self,
        candidate: Candidate,
        path: str,
    ):

        return getattr(candidate, path, None)
    
    def _format_field(
        self,
        value,
    ):

        include_confidence = self.config.get(
            "include_confidence",
            False,
        )

        if value is None:
            return None

        if isinstance(value, FieldValue):

            if include_confidence:

                return {

                    "value": value.value,

                    "confidence": value.confidence,

                }

            return value.value

        return value
    
    def _format_list(
        self,
        values,
    ):

        formatted = []

        for value in values:

            if isinstance(value, FieldValue):

                formatted.append(
                    self._format_field(value)
                )

            elif isinstance(value, Skill):

                formatted.append(

                    {

                        "name":

                            self._format_field(
                                value.name
                            ),

                        "category":

                            value.category.value
                            if value.category
                            else None,

                    }

                )

            elif isinstance(value, Link):

                formatted.append(

                    {

                        "platform":

                            value.platform.value,

                        "url":

                            self._format_field(
                                value.url
                            ),

                    }

                )

            else:

                formatted.append(value)

        return formatted

    def _normalize(self, value):

        if value is None:
            return None

        if isinstance(value, FieldValue):

            if isinstance(value.value, str):

                value.value = Normalizer.normalize_text(
                    value.value
                )

            return value

        if isinstance(value, Skill):

            value.name.value = Normalizer.normalize_skill(
                value.name.value
            )

            return value

        if isinstance(value, Link):

            if value.platform.value == "github":
                value.url.value = value.url.value.lower()

            elif value.platform.value == "linkedin":
                value.url.value = value.url.value.lower()

            return value

        return value

    def project(
        self,
        candidate: Candidate,
    ):

        output = {}

        strategy = self.config.get(
            "missing_strategy",
            "null",
        )

        for field in self.config["fields"]:

            source = field["from"]

            target = field["to"]

            value = self._resolve_path(
                candidate,
                source,
            )

            if value is None:

                if strategy == "omit":
                    continue

                if strategy == "error":
                    raise ValueError(
                        f"{source} missing."
                    )

                output[target] = None

                continue

            if isinstance(value, list):

                output[target] = self._format_list(
                    value
                )

            else:

                output[target] = self._format_field(
                    self._normalize(value)
                )

        return output