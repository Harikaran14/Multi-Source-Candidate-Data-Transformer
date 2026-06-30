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
from pydantic import BaseModel


class ProjectionEngine:

    def __init__(
        self,
        config_path: str | Path,
    ):

        with open(config_path) as file:
            self.config = json.load(file)
        self.validate_config()
    def _resolve_path(
        self,
        candidate: Candidate,
        path: str,
    ):

        return getattr(candidate, path, None)
    
    def _serialize(self, value):
        """
        Recursively convert Pydantic models into JSON-serializable
        dictionaries while respecting include_confidence.
        """

        if value is None:
            return None

        # ---------- FieldValue ----------

        if isinstance(value, FieldValue):

            if self.config.get("include_confidence", False):

                return {
                    "value": self._serialize(value.value),
                    "confidence": value.confidence,
                }

            return self._serialize(value.value)

        # ---------- List ----------

        if isinstance(value, list):

            return [
                self._serialize(item)
                for item in value
            ]

        # ---------- Pydantic Model ----------

        if isinstance(value, BaseModel):

            result = {}

            for key, val in value.model_dump(exclude_none=True).items():

                result[key] = self._serialize(
                    getattr(value, key)
                )

            return result

        # ---------- Enum ----------

        if hasattr(value, "value"):

            return value.value

        return value
    def validate_config(self):

        required = {
            "include_confidence",
            "missing_strategy",
            "fields",
        }

        missing = required - self.config.keys()

        if missing:
            raise ValueError(
                f"Missing config keys: {missing}"
            )

        allowed = {
            "null",
            "omit",
            "error",
        }

        if (
            self.config["missing_strategy"]
            not in allowed
        ):
            raise ValueError(
                "Invalid missing strategy."
            )

        for field in self.config["fields"]:

            if "from" not in field:
                raise ValueError(
                    "'from' missing in projection field."
                )

            if "to" not in field:
                raise ValueError(
                    "'to' missing in projection field."
                )
    def _format_field(self, value):
        return self._serialize(value)
        
    def _format_list(self, values):
        return self._serialize(values)
    def _normalize(
        self,
        field_name: str,
        value,
    ):
        """
        Normalize projected values according to the field.
        """

        if value is None:
            return None

        # ---------------- Emails ----------------

        if field_name == "emails":

            for email in value:

                email.value = Normalizer.normalize_email(
                    email.value
                )

            return value

        # ---------------- Phones ----------------

        if field_name == "phones":

            for phone in value:

                phone.value = Normalizer.normalize_phone(
                    phone.value
                )

            return value

        # ---------------- Skills ----------------

        if field_name == "skills":

            for skill in value:

                skill.name.value = (
                    Normalizer.normalize_skill(
                        skill.name.value
                    )
                )

            return value

        # ---------------- Summary ----------------

        if field_name == "summary":

            value.value = Normalizer.normalize_text(
                value.value
            )

            return value

        # ---------------- Headline ----------------

        if field_name == "headline":

            value.value = Normalizer.normalize_text(
                value.value
            )

            return value

        # ---------------- Full Name ----------------

        if field_name == "full_name":

            value.value = Normalizer.normalize_text(
                value.value
            )

            return value

        # ---------------- Location ----------------

        if field_name == "location":

            if value.value.city:

                value.value.city = (
                    Normalizer.normalize_location(
                        value.value.city
                    )
                )

            if value.value.state:

                value.value.state = (
                    Normalizer.normalize_location(
                        value.value.state
                    )
                )

            if value.value.country:

                value.value.country = (
                    Normalizer.normalize_location(
                        value.value.country
                    )
                )

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
            if field.get("normalize", True):
                value = self._normalize(source, value)
            
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
                    value
                )

        return output