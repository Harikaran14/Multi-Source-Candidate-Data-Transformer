
from __future__ import annotations
from uuid import uuid4
from typing import Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from .enums import (
    SourceType,
    ExtractionMethod,
    LinkType,
    SkillCategory,
)

class Provenance(BaseModel):

    model_config = ConfigDict(extra="forbid")
    source: SourceType
    extraction_method: ExtractionMethod
    original_value: Optional[str] = None
    reader_name: Optional[str] = None
    confidence_at_source: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0
    )

class FieldValue(BaseModel):


    model_config = ConfigDict(extra="forbid")
    value: Any
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )
    provenance: List[Provenance] = Field(
        default_factory=list,
        description="History describing where this value originated."
    )

class Location(BaseModel):

    model_config = ConfigDict(extra="forbid")
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class Link(BaseModel):

    model_config = ConfigDict(extra="forbid")
    platform: LinkType
    url: FieldValue


class Skill(BaseModel):


    model_config = ConfigDict(extra="forbid")
    name: FieldValue
    category: Optional[SkillCategory] = None
    proficiency: Optional[str] = None
    years_of_experience: Optional[float] = Field(
        default=None,
        ge=0
    )
class Experience(BaseModel):
 

    model_config = ConfigDict(extra="forbid")
    company: FieldValue
    title: FieldValue
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[FieldValue] = None

class Education(BaseModel):

    model_config = ConfigDict(extra="forbid")
    institution: FieldValue
    degree: Optional[FieldValue] = None
    field_of_study: Optional[FieldValue] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[FieldValue] = None


class Candidate(BaseModel):
   
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Globally unique candidate identifier."
    )
    source_candidate_id: Optional[FieldValue] = None
    full_name: Optional[FieldValue] = None
    emails: List[FieldValue] = Field(
        default_factory=list
    )
    phones: List[FieldValue] = Field(
        default_factory=list
    )
    location: Optional[FieldValue] = None
    headline: Optional[FieldValue] = None
    summary: Optional[FieldValue] = None
    years_experience: Optional[float] = Field(
    default=None,
    ge=0
)
    links: List[Link] = Field(
        default_factory=list
    )
    skills: List[Skill] = Field(
        default_factory=list
    )
    experience: List[Experience] = Field(
        default_factory=list
    )
    education: List[Education] = Field(
        default_factory=list
    )
    overall_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )
