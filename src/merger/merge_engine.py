
from __future__ import annotations

from copy import deepcopy
from typing import Optional
from core.models import (
    Candidate,
    FieldValue,
)

class MergeEngine:
    @staticmethod
    def _choose_best(
        field1: Optional[FieldValue],
        field2: Optional[FieldValue],
    ) -> Optional[FieldValue]:
        if field1 is None:
            return deepcopy(field2)

        if field2 is None:
            return deepcopy(field1)

        confidence_gap = abs(
            field1.confidence - field2.confidence
        )

        if confidence_gap > 0.10:
            winner = (
                deepcopy(field1)
                if field1.confidence >= field2.confidence
                else deepcopy(field2)
            )
        else:

            value1 = field1.value
            value2 = field2.value

            if isinstance(value1, str) and isinstance(value2, str):

                value1 = value1.strip()
                value2 = value2.strip()

                if len(value1) > len(value2):
                    winner = deepcopy(field1)

                elif len(value2) > len(value1):
                    winner = deepcopy(field2)

                else:
                    winner = (
                        deepcopy(field1)
                        if field1.confidence >= field2.confidence
                        else deepcopy(field2)
                    )

            else:
                winner = (
                    deepcopy(field1)
                    if field1.confidence >= field2.confidence
                    else deepcopy(field2)
                )

        same = (
            str(field1.value).strip().lower()
            ==
            str(field2.value).strip().lower()
        )

        winner.confidence = MergeEngine._compute_merged_confidence(
            field1.confidence,
            field2.confidence,
            same_value=same,
                )
        winner.provenance = (
            deepcopy(field1.provenance)
            + deepcopy(field2.provenance)
        )

        seen = set()
        unique = []

        for prov in winner.provenance:

            key = (
                prov.source,
                prov.extraction_method,
                prov.original_value,
                prov.reader_name,
            )

            if key not in seen:
                seen.add(key)
                unique.append(prov)

        winner.provenance = unique
        return winner
    @staticmethod
    def _calculate_overall_confidence(
        candidate: Candidate,
    ) -> float:
       
        scores = []

        scalar_fields = [
            candidate.full_name,
            candidate.location,
            candidate.summary,
            candidate.headline,
            candidate.source_candidate_id,
        ]

        for field in scalar_fields:
            if field:
                scores.append(field.confidence)

        scores.extend(
            field.confidence
            for field in candidate.emails
        )

        scores.extend(
            field.confidence
            for field in candidate.phones
        )

        scores.extend(
            skill.name.confidence
            for skill in candidate.skills
        )

        if not scores:
            return 0.0

        return round(
            sum(scores) / len(scores),
            3,
        )
    @staticmethod
    def _merge_field_lists(list1, list2):
        merged = {}

        for field in list1 + list2:

            key = str(field.value).strip().lower()

            if key not in merged:
                merged[key] = deepcopy(field)
                continue

            existing = merged[key]

            # Keep higher confidence
            if field.confidence > existing.confidence:
                existing.value = field.value
            existing.confidence = MergeEngine._compute_merged_confidence(
                    existing.confidence,
                    field.confidence,
                    same_value=True,
                )
            # Merge provenance
            existing.provenance.extend(
                deepcopy(field.provenance)
            )

        return list(merged.values())
    @staticmethod
    def _merge_skills(skills1, skills2):
        """
        Merge skills while preserving provenance.
        """

        merged = {}

        for skill in skills1 + skills2:

            key = str(skill.name.value).strip().lower()

            if key not in merged:
                merged[key] = deepcopy(skill)
                continue

            existing = merged[key]
            if skill.name.confidence > existing.name.confidence:
                existing.category = skill.category

            existing.name.confidence = MergeEngine._compute_merged_confidence(
                existing.name.confidence,
                skill.name.confidence,
                same_value=True,
            )

            existing.name.provenance.extend(
                deepcopy(skill.name.provenance)
            )

        return list(merged.values())
    @staticmethod
    def _merge_links(links1, links2):
        """
        Merge links while preserving provenance.
        """

        merged = {}

        for link in links1 + links2:

            key = str(link.url.value).strip().lower()

            if key not in merged:
                merged[key] = deepcopy(link)
                continue

            existing = merged[key]
            if link.url.confidence > existing.url.confidence:
                existing.platform = link.platform
                existing.url.value = link.url.value
            existing.url.confidence = MergeEngine._compute_merged_confidence(
                existing.url.confidence,
                link.url.confidence,
                same_value=True,
            )

            existing.url.provenance.extend(
                deepcopy(link.url.provenance)
            )

        return list(merged.values())
        

    def merge(
        self,
        candidate1: Candidate,
        candidate2: Candidate,
    ) -> Candidate:
        
        merged = Candidate()

        merged.candidate_id = (
                candidate1.candidate_id
                if candidate1.candidate_id
                else candidate2.candidate_id
            )

        merged.source_candidate_id = self._choose_best(
            candidate1.source_candidate_id,
            candidate2.source_candidate_id,
        )


        merged.full_name = self._choose_best(
            candidate1.full_name,
            candidate2.full_name,
        )

        merged.location = self._choose_best(
            candidate1.location,
            candidate2.location,
        )

        merged.headline = self._choose_best(
            candidate1.headline,
            candidate2.headline,
        )

        merged.summary = self._choose_best(
            candidate1.summary,
            candidate2.summary,
        )


        if (
            candidate1.years_experience is None
            or (
                candidate2.years_experience is not None
                and candidate2.years_experience > candidate1.years_experience
            )
        ):
            merged.years_experience = candidate2.years_experience
        else:
            merged.years_experience = candidate1.years_experience


        merged.emails = self._merge_field_lists(
            candidate1.emails,
            candidate2.emails,
        )

        merged.phones = self._merge_field_lists(
            candidate1.phones,
            candidate2.phones,
        )

        merged.skills = self._merge_skills(
            candidate1.skills,
            candidate2.skills,
        )

        merged.links = self._merge_links(
            candidate1.links,
            candidate2.links,
        )


        if len(candidate2.experience) >= len(candidate1.experience):
            merged.experience = deepcopy(candidate2.experience)
        else:
            merged.experience = deepcopy(candidate1.experience)


        if len(candidate2.education) >= len(candidate1.education):
            merged.education = deepcopy(candidate2.education)
        else:
            merged.education = deepcopy(candidate1.education)


        
        merged.overall_confidence = self._calculate_overall_confidence(
                merged
            )

        return merged
    

    @staticmethod
    def _compute_merged_confidence(
        confidence1: float,
        confidence2: float,
        same_value: bool = True,
    ) -> float:
        if same_value:

            return min(
                1.0,
                max(confidence1, confidence2) + 0.05
            )

        return max(
            0.0,
            max(confidence1, confidence2) - 0.05
        )