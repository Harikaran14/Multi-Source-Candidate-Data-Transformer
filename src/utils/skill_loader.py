from pathlib import Path


def load_skills(file_path: str | Path) -> dict[str, list[str]]:

    file_path = Path(file_path)

    skills = {}

    with file_path.open(
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            canonical, aliases = line.split("|")

            skills[canonical] = [

                alias.strip().lower()

                for alias in aliases.split(",")

            ]

    return skills