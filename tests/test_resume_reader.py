from src.readers.resume_reader import ResumeReader


def test_resume_reader():

    reader = ResumeReader("dummy.pdf")

    reader._extract_text = lambda: """
Harikaran C

Email: hari@gmail.com

Phone: +91 9876543210

Skills:
Python
React
MongoDB
"""

    candidate = reader.extract_candidate()

    assert candidate.full_name is not None

    assert len(candidate.skills) >= 3

    assert candidate.emails