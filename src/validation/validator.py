from __future__ import annotations

import re

from core.models import Candidate


class CandidateValidator:
    """
    Validates the canonical Candidate object before projection.
    """

    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_REGEX = re.compile(
        r"^\+?\d{10,15}$"
    )

    @classmethod
    def validate(cls, candidate: Candidate) -> list[str]:

        errors = []

        # ---------- Name ----------

        if (
            candidate.full_name is None
            or not str(candidate.full_name.value).strip()
        ):
            errors.append("Candidate name is missing.")

        # ---------- Emails ----------

        for email in candidate.emails:

            if not cls.EMAIL_REGEX.match(email.value):
                errors.append(
                    f"Invalid email: {email.value}"
                )

        # ---------- Phones ----------

        for phone in candidate.phones:

            if not cls.PHONE_REGEX.match(phone.value):
                errors.append(
                    f"Invalid phone: {phone.value}"
                )

        # ---------- Confidence ----------

        if not (
            0.0
            <= candidate.overall_confidence
            <= 1.0
        ):
            errors.append(
                "Overall confidence must lie between 0 and 1."
            )

        return errors