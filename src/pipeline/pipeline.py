from readers.csv_reader import CSVReader
from readers.resume_reader import ResumeReader

from merger.merge_engine import MergeEngine

from projection.projection_engine import ProjectionEngine

from validation.validator import CandidateValidator


class CandidatePipeline:

    def __init__(self, projection_config):

        self.merger = MergeEngine()

        self.projection = ProjectionEngine(
            projection_config
        )

    def run(
        self,
        csv_path,
        resume_path,
    ):

        csv_candidate = CSVReader(
            csv_path
        ).extract_candidate()

        resume_candidate = ResumeReader(
            resume_path
        ).extract_candidate()

        merged = self.merger.merge(
            csv_candidate,
            resume_candidate,
        )

        errors = CandidateValidator.validate(
            merged
        )

        if errors:
            raise ValueError(
                "\n".join(errors)
            )

        return self.projection.project(
            merged
        )