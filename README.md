# Multi-Source Candidate Data Transformer

> A modular candidate ingestion pipeline that transforms heterogeneous candidate data into a unified canonical profile with provenance tracking, confidence-based conflict resolution, validation, and configurable output projections.

---

## Overview

Recruiters and hiring platforms often receive candidate information from multiple sources such as resumes, recruiter spreadsheets, ATS exports, LinkedIn profiles, and GitHub profiles. These sources may contain duplicate, incomplete, or conflicting information.

This project implements a modular pipeline that:

- Ingests candidate information from multiple sources.
- Converts every source into a common canonical representation.
- Merges candidate profiles intelligently.
- Tracks provenance for every extracted field.
- Computes confidence scores.
- Validates and normalizes candidate data.
- Produces configurable JSON outputs for different consumers.

---

## Features

### Multi-Source Ingestion

Currently implemented

- Recruiter CSV Reader
- Resume PDF Reader

Extensible architecture for

- LinkedIn Reader
- GitHub Reader
- ATS Reader
- Manual Input Reader

---

### Canonical Candidate Model

All readers produce the same internal `Candidate` object.

```text
Candidate
├── candidate_id
├── full_name
├── emails
├── phones
├── location
├── headline
├── summary
├── skills
├── experience
├── education
├── links
├── years_experience
└── overall_confidence
```

Every extracted field is represented using

```text
FieldValue
├── value
├── confidence
└── provenance
```

This allows the system to preserve both the extracted value and its origin.

---

## Architecture

```text
CSV --------\
              \
               Readers
              /
Resume ------/

        │

Extraction

        │

Canonical Candidate Model

        │

Merge Engine

        │

Validation & Normalization

        │

Projection Engine

        │

JSON Output
```

---

## Project Structure

```text
src/
│
├── core/
│   ├── models.py
│   └── enums.py
│
├── readers/
│   ├── base_reader.py
│   ├── csv_reader.py
│   └── resume_reader.py
│
├── merger/
│   └── merge_engine.py
│
├── projection/
│   └── projection_engine.py
│
├── validation/
│   └── validator.py
│
├── utils/
│   ├── normalizer.py
│   ├── reader_utils.py
│   └── skill_loader.py
│
├── pipeline/
│   └── pipeline.py
│
└── main.py
```

---

# Pipeline

## 1. Reader Layer

Each reader is responsible only for extracting data from a specific source.

Implemented readers

- CSVReader
- ResumeReader

Readers convert heterogeneous inputs into a common `Candidate` model.

---

## 2. Merge Engine

The merge engine combines multiple candidate profiles into a single canonical profile.

Responsibilities

- Conflict resolution
- Duplicate removal
- Provenance merging
- Confidence computation

### Scalar Fields

Example

```
CSV

Harikaran C

Resume

Harikaran Chandrasekaran
```

Higher confidence wins.

If confidence scores are similar, the more informative value is selected.

---

### Collection Fields

Collections are normalized and deduplicated.

- Emails
- Phones
- Skills
- Links

---

## Confidence Strategy

Initial confidence

| Source | Confidence |
|----------|------------|
| Recruiter CSV | 0.95 |
| Resume Regex | 0.85 |

When multiple sources agree

```
confidence = max(conf1, conf2) + 0.05
```

When conflicting values are found

```
confidence = max(conf1, conf2) - 0.05
```

Overall confidence

```
Average confidence of all populated fields
```

---

## Provenance Tracking

Every extracted field stores its origin.

Example

```json
{
  "source": "resume",
  "reader": "ResumeReader",
  "extraction_method": "regex",
  "original_value": "Harikaran C"
}
```

This enables complete traceability throughout the pipeline.

---

## Validation & Normalization

Before projection, candidate data is normalized and validated.

### Normalization

- Lowercase emails
- E.164 phone format
- Remove whitespace

### Validation

- Required fields
- Email format
- Phone format
- Confidence range

---

## Projection Engine

The projection engine is fully configuration driven.

Supported capabilities

- Field selection
- Field renaming
- Confidence inclusion
- Missing value handling

Example

```json
{
  "path": "candidate_name",
  "from": "full_name",
  "include_confidence": true
}
```

The same canonical candidate can generate multiple output formats without changing application code.

Examples

- Recruiter JSON
- ATS JSON
- Minimal API Response

---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python3 main.py \
    --csv sample_data/candidate.csv \
    --resume sample_data/resume.pdf \
    --projection config/recruiter_projection.json \
    --output output/recruiter.json
```

---

## Output

Generated JSON

```text
output/
    recruiter.json
```

---

# Example Output

```json
{
  "candidate_name": {
    "value": "Harikaran C",
    "confidence": 1.0
  },
  "emails": [...],
  "skills": [...],
  "education": [...],
  "overall_confidence": 0.867
}
```

---

# Design Decisions

### Canonical Intermediate Representation

Instead of directly transforming each source into the final output, every reader produces the same `Candidate` model.

Benefits

- Easy to extend
- Decouples readers from output formats
- Simplifies merge logic

---

### Modular Architecture

Every component has a single responsibility.

- Readers
- Merge Engine
- Validator
- Projection Engine

This makes the system easier to maintain and extend.

---

### Configuration-Driven Output

Projection is runtime configurable.

New output schemas can be created without modifying source code.

---

# Assumptions

- Resume contains machine-readable text.
- Candidate identity is determined using available identifying information.
- Confidence values are heuristic scores rather than ML predictions.
- One recruiter CSV row corresponds to one candidate.

---

# Limitations

Current implementation does not include

- OCR for scanned resumes
- LinkedIn Reader
- GitHub Reader
- Embedded PDF hyperlink extraction
- Semantic parsing using LLMs

These components can be integrated without changing the existing architecture.

---

# Future Improvements

- OCR support
- LinkedIn integration
- GitHub integration
- ATS reader
- ML-based confidence estimation
- Better experience and education parsing
- Embedding-based candidate matching

---

# Technologies Used

- Python 3
- Pydantic
- pdfplumber
- Regex
- JSON
- CSV

---

# Author

**Harikaran C**

B.Tech Information Technology

SSN College of Engineering

---


This project was built as part of the Eightfold Engineering Internship Assignment to demonstrate modular software design, data modeling, configurable transformations, provenance tracking, and confidence-based candidate profile merging.
