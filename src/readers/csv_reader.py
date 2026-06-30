

from __future__ import annotations
import csv
from core.enums import (
    ExtractionMethod,
    SourceType,
)
from core.models import (
    Candidate,
    Experience,
    FieldValue,
    Location,
)
from readers.base_reader import BaseReader
from utils.reader_utils import (
    create_field_value,
    is_missing,
)


class CSVReader(BaseReader):
    
    @property
    def source_type(self) -> SourceType:
        return SourceType.CSV

    def _load_csv(self) -> dict[str, str]:
        self._validate_source()

        with self.input_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            rows = list(reader)

        if len(rows) == 0:
            raise ValueError("CSV file is empty.")

        if len(rows) > 1:
            raise ValueError(
                "CSVReader expects exactly one candidate."
            )

        return rows[0]

    def _create_field(
        self,
        value: str | None,
    ) -> FieldValue | None:
        if is_missing(value):
            return None

        return create_field_value(
            value=value.strip(),
            source=self.source_type,
            extraction_method=ExtractionMethod.CSV_MAPPING,
            reader_name=self.reader_name,
        )

    def _create_location(
        self,
        city: str | None,
    ) -> FieldValue | None:
        
        if is_missing(city):
            return None

        location = Location(
            city=city.strip()
        )

        return create_field_value(
            value=location,
            source=self.source_type,
            extraction_method=ExtractionMethod.CSV_MAPPING,
            reader_name=self.reader_name,
        )

    def extract_candidate(self) -> Candidate:
        

        row = self._load_csv()

        candidate = Candidate()


        candidate.source_candidate_id = self._create_field(
            row.get("source_candidate_id")
        )

        candidate.full_name = self._create_field(
            row.get("name") or row.get("full_name")
        )


        email = self._create_field(
            row.get("email")
        )

        if email:
            candidate.emails.append(email)


        phone = self._create_field(
            row.get("phone")
        )

        if phone:
            candidate.phones.append(phone)

        candidate.location = self._create_location(
            row.get("current_location") or row.get("location")
        )

        years = row.get("years_experience")

        if not is_missing(years):
            try:
                candidate.years_experience = float(years)
            except ValueError:
                pass


        company = self._create_field(
            row.get("current_company")
        )

        title = self._create_field(
            row.get("title")
        )

        if company is not None and title is not None:

            experience = Experience(
                company=company,
                title=title,
            )

            candidate.experience.append(experience)

        return candidate