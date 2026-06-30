import tempfile

from src.readers.csv_reader import CSVReader


def test_csv_reader():

    csv_content = """full_name,email,phone,location,headline
Harikaran C,hari@gmail.com,+919876543210,Chennai,Software Engineer
"""

    with tempfile.NamedTemporaryFile(
        suffix=".csv",
        mode="w",
        delete=False,
    ) as file:

        file.write(csv_content)

        path = file.name

    candidate = CSVReader(path).extract_candidate()

    assert candidate.full_name.value == "Harikaran C"

    assert candidate.emails[0].value == "hari@gmail.com"

    assert candidate.phones[0].value == "+919876543210"