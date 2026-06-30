from __future__ import annotations

import argparse
import json
import logging
import sys

from pipeline.pipeline import CandidatePipeline
from pathlib import Path



logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Candidate Profile Ingestion Engine"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to candidate CSV file",
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Path to candidate resume PDF",
    )

    parser.add_argument(
        "--projection",
        default="../config/recruiter_projection.json",
        help="Projection configuration JSON",
    )

    parser.add_argument(
        "--output",
        default="../output/output.json",
        help="Output JSON file",
    )

    return parser.parse_args()


def main():

    args = parse_arguments()
    

    logger.info("Starting Candidate Ingestion Pipeline...")

    try:

        pipeline = CandidatePipeline(
            projection_config=args.projection
        )

        result = pipeline.run(
            csv_path=args.csv,
            resume_path=args.resume,
        )
        output_path = Path(args.output)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open("w", encoding="utf-8") as file:

            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Output written to %s",
            args.output,
        )

    except Exception as e:

        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()