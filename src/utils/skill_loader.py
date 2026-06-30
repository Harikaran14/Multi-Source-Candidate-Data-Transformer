from pathlib import Path

from core.enums import SkillCategory


SKILL_CATEGORY = {

    # ---------------- Programming Languages ----------------

    "Python": SkillCategory.PROGRAMMING_LANGUAGE,
    "Java": SkillCategory.PROGRAMMING_LANGUAGE,
    "C": SkillCategory.PROGRAMMING_LANGUAGE,
    "C++": SkillCategory.PROGRAMMING_LANGUAGE,
    "C#": SkillCategory.PROGRAMMING_LANGUAGE,
    "JavaScript": SkillCategory.PROGRAMMING_LANGUAGE,
    "TypeScript": SkillCategory.PROGRAMMING_LANGUAGE,
    "Go": SkillCategory.PROGRAMMING_LANGUAGE,
    "Rust": SkillCategory.PROGRAMMING_LANGUAGE,
    "Swift": SkillCategory.PROGRAMMING_LANGUAGE,
    "Kotlin": SkillCategory.PROGRAMMING_LANGUAGE,
    "PHP": SkillCategory.PROGRAMMING_LANGUAGE,
    "Ruby": SkillCategory.PROGRAMMING_LANGUAGE,
    "Scala": SkillCategory.PROGRAMMING_LANGUAGE,
    "R": SkillCategory.PROGRAMMING_LANGUAGE,
    "MATLAB": SkillCategory.PROGRAMMING_LANGUAGE,

    # ---------------- Frameworks ----------------

    "React": SkillCategory.FRAMEWORK,
    "Angular": SkillCategory.FRAMEWORK,
    "Vue.js": SkillCategory.FRAMEWORK,
    "Next.js": SkillCategory.FRAMEWORK,
    "Redux": SkillCategory.FRAMEWORK,
    "Node.js": SkillCategory.FRAMEWORK,
    "Express.js": SkillCategory.FRAMEWORK,
    "Flask": SkillCategory.FRAMEWORK,
    "Django": SkillCategory.FRAMEWORK,
    "FastAPI": SkillCategory.FRAMEWORK,
    "Spring Boot": SkillCategory.FRAMEWORK,
    "ASP.NET": SkillCategory.FRAMEWORK,
    "Laravel": SkillCategory.FRAMEWORK,

    # ---------------- Databases ----------------

    "MySQL": SkillCategory.DATABASE,
    "PostgreSQL": SkillCategory.DATABASE,
    "SQLite": SkillCategory.DATABASE,
    "MongoDB": SkillCategory.DATABASE,
    "Redis": SkillCategory.DATABASE,
    "Oracle": SkillCategory.DATABASE,
    "SQL Server": SkillCategory.DATABASE,

    # ---------------- Cloud ----------------

    "AWS": SkillCategory.CLOUD,
    "Azure": SkillCategory.CLOUD,
    "Google Cloud": SkillCategory.CLOUD,

    # ---------------- DevOps ----------------

    "Docker": SkillCategory.DEVOPS,
    "Kubernetes": SkillCategory.DEVOPS,
    "Git": SkillCategory.DEVOPS,
    "GitHub": SkillCategory.DEVOPS,
    "GitLab": SkillCategory.DEVOPS,
    "Terraform": SkillCategory.DEVOPS,
    "Ansible": SkillCategory.DEVOPS,
    "Jenkins": SkillCategory.DEVOPS,
    "Linux": SkillCategory.DEVOPS,
    "Nginx": SkillCategory.DEVOPS,
    "Apache": SkillCategory.DEVOPS,

    # ---------------- AI / ML ----------------

    "TensorFlow": SkillCategory.TOOL,
    "PyTorch": SkillCategory.TOOL,
    "Keras": SkillCategory.TOOL,
    "Scikit-learn": SkillCategory.TOOL,
    "OpenCV": SkillCategory.TOOL,
    "Pandas": SkillCategory.TOOL,
    "NumPy": SkillCategory.TOOL,
    "Matplotlib": SkillCategory.TOOL,
    "Seaborn": SkillCategory.TOOL,
    "XGBoost": SkillCategory.TOOL,
    "LightGBM": SkillCategory.TOOL,
    "CatBoost": SkillCategory.TOOL,

    # ---------------- Others ----------------

    "Spark": SkillCategory.TOOL,
    "PySpark": SkillCategory.TOOL,
    "Kafka": SkillCategory.TOOL,
    "Airflow": SkillCategory.TOOL,
    "REST API": SkillCategory.TOOL,
    "GraphQL": SkillCategory.TOOL,
    "gRPC": SkillCategory.TOOL,
    "Firebase": SkillCategory.TOOL,
    "Supabase": SkillCategory.TOOL,
    "Postman": SkillCategory.TOOL,
    "Figma": SkillCategory.TOOL,

    # ---------------- AI ----------------

    "Machine Learning": SkillCategory.TOOL,
    "Deep Learning": SkillCategory.TOOL,
    "Computer Vision": SkillCategory.TOOL,
    "Natural Language Processing": SkillCategory.TOOL,
    "Generative AI": SkillCategory.TOOL,
    "LLM": SkillCategory.TOOL,
    "LangChain": SkillCategory.TOOL,
    "LlamaIndex": SkillCategory.TOOL,
    "Ollama": SkillCategory.TOOL,
    "FAISS": SkillCategory.TOOL,
    "ChromaDB": SkillCategory.TOOL,
    "Pinecone": SkillCategory.TOOL,
    "Milvus": SkillCategory.TOOL,
    "Weaviate": SkillCategory.TOOL,
    "RAG": SkillCategory.TOOL,
    "Prompt Engineering": SkillCategory.TOOL,
    "Agentic AI": SkillCategory.TOOL,
    "MCP": SkillCategory.TOOL,
}


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