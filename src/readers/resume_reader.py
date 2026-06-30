from __future__ import annotations
from ast import pattern
import re
import pdfplumber
from pathlib import Path
from utils.skill_loader import (
    load_skills,
    SKILL_CATEGORY,
)
from core.enums import (
    ExtractionMethod,
    LinkType,
    SkillCategory,
    SourceType,
)

from core.models import (
    Candidate,
    Education,
    Experience,
    FieldValue,
    Link,
    Location,
    Skill,
)

from readers.base_reader import BaseReader

from utils.reader_utils import (
    create_field_value,
    split_comma_separated,
)

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"(\+?\d[\d\s\-]{8,15}\d)"
LINKEDIN_REGEX = r"https?://(?:www\.)?linkedin\.com/in/[^\s]+"
GITHUB_REGEX = r"https?://(?:www\.)?github\.com/[^\s]+"


class ResumeReader(BaseReader):
   
    SKILLS = load_skills(
        Path(__file__).parent.parent / "data" / "skills.txt"
    )
    @property
    def source_type(self) -> SourceType:
        return SourceType.RESUME

    def _extract_text(self) -> str:
        

        self._validate_source()

        pages = []

        with pdfplumber.open(self.input_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:
                    pages.append(text)

        return "\n".join(pages)
    
    def _extract_email(
        self,
        text: str,
    ) -> str | None:
       
        match = re.search(EMAIL_REGEX, text)

        if match:
            return match.group()

        return None

    def _extract_phone(
        self,
        text: str,
    ) -> str | None:
        
        match = re.search(PHONE_REGEX, text)

        if match:
            return match.group()

        return None
    
    def _extract_name(
        self,
        text: str,
    ) -> str | None:
        
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return None

        candidates = lines[:10]

        best_name = None
        best_score = float("-inf")

        blacklist = {
            "resume",
            "curriculum vitae",
            "cv",
            "email",
            "phone",
            "mobile",
            "address",
            "linkedin",
            "github",
            "portfolio",
            "objective",
            "summary",
            "profile",
            "education",
            "experience",
            "skills",
            "projects",
            "internship",
            "software engineer",
            "software developer",
            "data scientist",
            "machine learning engineer",
            "full stack developer",
            "backend developer",
            "frontend developer",
        }

        for line in candidates:

            score = 0

            lower = line.lower()

            # Contact information is never a name
            if "@" in lower:
                continue

            if "http" in lower:
                continue

            if "linkedin" in lower:
                continue

            if "github" in lower:
                continue

            # Reject obvious headings
            if lower in blacklist:
                continue

            words = line.split()


            if 2 <= len(words) <= 4:
                score += 5

            if len(words) < 2:
                score -= 5
            if 4<len(words) <= 14:
                score+=3
            if len(words) > 14:
                score -= 5

      
            if all(
                word.replace(".", "").isalpha()
                for word in words
            ):
                score += 3

      
            if all(
                word[:1].isupper()
                for word in words
            ):
                score += 2

            # Penalize digits
            if any(
                char.isdigit()
                for char in line
            ):
                score -= 5

            # Earlier lines are more likely to contain the name
            score += max(0, 10 - candidates.index(line))

            if score > best_score:
                best_score = score
                best_name = line

        return best_name

    def _extract_links(
        self,
        text: str,
    ) -> list[Link]:

        links = []

        github = re.search(
            GITHUB_REGEX,
            text,
            re.IGNORECASE,
        )

        if github:

            links.append(

                Link(

                    platform=LinkType.GITHUB,

                    url=create_field_value(

                        github.group(),

                        self.source_type,

                        ExtractionMethod.REGEX,

                        reader_name=self.reader_name,

                    ),

                )

            )

        linkedin = re.search(
            LINKEDIN_REGEX,
            text,
            re.IGNORECASE,
        )

        if linkedin:

            links.append(

                Link(

                    platform=LinkType.LINKEDIN,

                    url=create_field_value(

                        linkedin.group(),

                        self.source_type,

                        ExtractionMethod.REGEX,

                        reader_name=self.reader_name,

                    ),

                )

            )

        return links

    def _extract_skills(
        self,
        text: str,
    ) -> list[Skill]:
        
        skills = []

        found = set()

        lower_text = text.lower()

        for canonical, aliases in self.SKILLS.items():

            for alias in aliases:

                pattern = r"\b" + re.escape(alias) + r"\b"

                if re.search(pattern, lower_text):

                    if canonical in found:
                        break

                    found.add(canonical)

                    skills.append(

                        Skill(

                            name=create_field_value(

                                value=canonical,

                                source=self.source_type,

                                extraction_method=ExtractionMethod.REGEX,

                                reader_name=self.reader_name,

                            ),

                            category=SKILL_CATEGORY.get(
                                canonical,
                                SkillCategory.OTHER,
                            ),

                        )

                    )

                    break

        return skills

    def _extract_section(
        self,
        text: str,
        headings: list[str],
    ) -> str:
        

        lines = text.splitlines()

        start = None

        normalized_headings = {
            heading.lower().strip()
            for heading in headings
        }

        for index, line in enumerate(lines):

            current = line.strip().lower()

            if current in normalized_headings:
                start = index + 1
                break

        if start is None:
            return ""

        # Common section headings found in resumes
        stop_headings = {

            "education",
            "academic background",
            "academics",

            "experience",
            "work experience",
            "professional experience",
            "employment",
            "internships",

            "projects",
            "personal projects",

            "skills",
            "technical skills",
            "key skills",

            "certifications",

            "achievements",
            "awards",

            "publications",

            "summary",
            "profile",
            "objective",

            "languages",

            "interests",

            "volunteering",
            "leadership",

            "contact",
        }

        section = []

        for line in lines[start:]:

            stripped = line.strip()

            if not stripped:
                continue

            if stripped.lower() in stop_headings:
                break

            section.append(stripped)

        return "\n".join(section)
    
    def _extract_education(
        self,
        text: str,
    ) -> list[Education]:

        section = self._extract_section(
            text,
            ["education"]
        )

        if not section:
            return []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        if not lines:
            return []

        institution = None
        degree = None

        for line in lines:

            lower = line.lower()

            if degree is None:

                if any(
                    keyword in lower
                    for keyword in [
                        "b.tech",
                        "b.e",
                        "m.tech",
                        "m.e",
                        "bachelor",
                        "master",
                        "phd",
                        "mba",
                        "b.sc",
                        "m.sc",
                    ]
                ):
                    degree = line
                    continue

            if institution is None:
                institution = line

        if institution is None:
            return []

        return [

            Education(

                institution=create_field_value(
                    institution,
                    self.source_type,
                    ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                ),

                degree=create_field_value(
                    degree,
                    self.source_type,
                    ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                ) if degree else None,

            )

        ]

    def _extract_experience(
        self,
        text: str,
    ) -> list[Experience]:

        section = self._extract_section(
            text,
            [
                "experience",
                "work experience",
                "professional experience",
                "employment",
                "internships",
            ]
        )

        if not section:
            return []

        lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            return []

        title = lines[0]
        company = lines[1]

        return [

            Experience(

                company=create_field_value(
                    company,
                    self.source_type,
                    ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                ),

                title=create_field_value(
                    title,
                    self.source_type,
                    ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                ),

            )

        ]
    
    def _extract_summary(
        self,
        text: str,
    ) -> FieldValue | None:
        """
        Extract candidate summary/objective/profile section.
        """

        section = self._extract_section(
            text,
            [
                "summary",
                "professional summary",
                "profile",
                "objective",
                "career objective",
                "professional profile",
            ],
        )

        if not section:
            return None

        return create_field_value(
            value=section,
            source=self.source_type,
            extraction_method=ExtractionMethod.REGEX,
            reader_name=self.reader_name,
        )
    def _extract_location(
        self,
        text: str,
    ) -> FieldValue | None:
        """
        Extract candidate location by matching city names.
        """

        city_file = (
            Path(__file__).parent.parent
            / "data"
            / "cities.txt"
        )

        with city_file.open(
            encoding="utf-8"
        ) as file:

            cities = [

                city.strip()

                for city in file

                if city.strip()

            ]

        lower_text = text.lower()

        for city in cities:

            if city.lower() in lower_text:

                location = Location(
                    city=city
                )

                return create_field_value(
                    value=location,
                    source=self.source_type,
                    extraction_method=ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                )

        return None
    
    def extract_candidate(self) -> Candidate:

        text = self._extract_text()

        candidate = Candidate()

        # Basic Information
        name = self._extract_name(text)
        if name:
            candidate.full_name = create_field_value(
                value=name,
                source=self.source_type,
                extraction_method=ExtractionMethod.REGEX,
                reader_name=self.reader_name,
            )

        email = self._extract_email(text)
        if email:
            candidate.emails.append(
                create_field_value(
                    value=email,
                    source=self.source_type,
                    extraction_method=ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                )
            )

        phone = self._extract_phone(text)
        if phone:
            candidate.phones.append(
                create_field_value(
                    value=phone,
                    source=self.source_type,
                    extraction_method=ExtractionMethod.REGEX,
                    reader_name=self.reader_name,
                )
            )

        # Optional Information
        candidate.location = self._extract_location(text)
        candidate.summary = self._extract_summary(text)

        # Collections
        candidate.links = self._extract_links(text)
        candidate.skills = self._extract_skills(text)
        candidate.education = self._extract_education(text)
        candidate.experience = self._extract_experience(text)

        return candidate