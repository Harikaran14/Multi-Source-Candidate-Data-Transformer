from __future__ import annotations

import re

from core.models import Candidate
from utils.normalizer import Normalizer


class CandidateValidator:
    """
    Validates the canonical Candidate object.

    Validation includes:
    - Required fields
    - Email format
    - Phone format
    - Confidence score range

    Email addresses and phone numbers are normalized before
    validation so that the canonical Candidate object always
    contains standardized values.
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

        # ---------- Full Name ----------

        if (
            candidate.full_name is None
            or not str(candidate.full_name.value).strip()
        ):
            errors.append("Candidate name is missing.")

        # ---------- Emails ----------

        for email in candidate.emails:

            normalized_email = Normalizer.normalize_email(
                str(email.value)
            )

            # Keep canonical model normalized
            email.value = normalized_email

            if not cls.EMAIL_REGEX.fullmatch(normalized_email):
                errors.append(
                    f"Invalid email: {normalized_email}"
                )

        # ---------- Phones ----------

        for phone in candidate.phones:

            normalized_phone = Normalizer.normalize_phone(
                str(phone.value)
            )

            # Keep canonical model normalized
            phone.value = normalized_phone

            if not cls.PHONE_REGEX.fullmatch(normalized_phone):
                errors.append(
                    f"Invalid phone: {normalized_phone}"
                )

        # ---------- Confidence ----------

        if not (
            0.0 <= candidate.overall_confidence <= 1.0
        ):
            errors.append(
                "Overall confidence must lie between 0 and 1."
            )

        return errors