from pprint import pprint

from readers.csv_reader import CSVReader
from readers.resume_reader import ResumeReader
from merger.merge_engine import MergeEngine
from projection.projection_engine import ProjectionEngine

# Read CSV
csv_candidate = CSVReader(
    "../sample_data/candidate.csv"
).extract_candidate()

# Read Resume
resume_candidate = ResumeReader(
    "../sample_data/resume.pdf"
).extract_candidate()

# Merge
merged = MergeEngine().merge(
    csv_candidate,
    resume_candidate,
)

print("\n================ MERGED =================\n")

# Projection
projection = ProjectionEngine(
    "../config/recruiter_projection.json"
)

result = projection.project(merged)

print("\n================ PROJECTED =================\n")
pprint(result)