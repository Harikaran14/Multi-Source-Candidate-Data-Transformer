"""
normalizer.py

Utility functions used by the Projection Engine to
normalize output values.
"""

from __future__ import annotations

import re


class Normalizer:

    @staticmethod
    def normalize_email(email: str) -> str:
        """
        Normalize email addresses.
        """
        return email.strip().lower()

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone numbers.

        Example:
            +91 98765-43210
            -> +919876543210
        """

        phone = re.sub(r"[^\d+]", "", phone)

        if phone.startswith("91") and not phone.startswith("+91"):
            phone = "+" + phone

        return phone

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Remove extra whitespace.
        """

        return " ".join(text.split())

    @staticmethod
    def normalize_skill(skill: str) -> str:
        """
        Skills are already canonicalized by ResumeReader.
        """

        return skill.strip()

    @staticmethod
    def normalize_location(location: str) -> str:
        """
        Normalize location strings.
        """

        return location.title()