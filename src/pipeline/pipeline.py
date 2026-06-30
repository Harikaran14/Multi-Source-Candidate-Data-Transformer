
from enum import Enum

class SourceType(str, Enum):
    RESUME = "resume"
    CSV = "csv"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    ATS = "ats"
    MANUAL = "manual"


class ExtractionMethod(str, Enum):

    REGEX = "regex"
    PDF_PARSER = "pdf_parser"
    CSV_MAPPING = "csv_mapping"
    API = "api"
    MANUAL = "manual"
    MERGED = "merged"


class LinkType(str, Enum):


    GITHUB = "github"
    LINKEDIN = "linkedin"
    PORTFOLIO = "portfolio"
    WEBSITE = "website"
    OTHER = "other"