from crewai import Agent
import os
from litellm import completion
from crewai import Task
from crewai import LLM
from crewai import Crew, Process
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")

# Set environment variable for LLM
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY if GEMINI_API_KEY else ""

# Initialize LLM
try:
    llm = LLM(model="gemini/gemini-1.5-flash")
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Error initializing LLM: {str(e)}")
    llm = None

technical_skills = (
    "JavaScript, Python, Java, C++, C#, Ruby, PHP, Swift, Kotlin, Go, Rust, TypeScript, SQL, MATLAB, R, "
    "React.js, Angular, Vue.js, Node.js, Express, Django, Flask, Spring, Hibernate, Laravel, Ruby on Rails, "
    ".NET, Git, GitHub, GitLab, Bitbucket, Android (Java, Kotlin), iOS (Swift, Objective-C), React Native, "
    "Flutter, AWS, Microsoft Azure, Google Cloud Platform (GCP), MySQL, PostgreSQL, MongoDB, Firebase, "
    "Oracle DB, NoSQL, SQLite, Docker, Kubernetes, Jenkins, Terraform, CI/CD Pipelines, JUnit, Mocha, "
    "Selenium, Cypress, TDD, BDD, HTML5, CSS3, CSS Grid, Flexbox, Web Accessibility (WCAG, ARIA), Apache, Nginx"
)

# Define the information extraction agent
technical_skill_extractor_unstructured = Agent(
    role=(
        "You are an expert in extracting **technical and non-technical skills** from user profiles or text data. "
        "Your task is to identify and return only the **relevant skills**, ignoring unrelated details, advertisements, "
        "or general background information."
    ),
    goal=(
        "Return a **concise, structured, and accurate** list of skills (technical and non-technical) from the input data. "
        "Ensure the extracted skills are categorized where possible and relevant to the subject matter."
    ),
    verbose=False,
    memory=True,
    llm=llm,
    backstory=(
        "This agent was developed to streamline skill extraction from various sources. "
        "Designed to enhance research efficiency, it focuses on identifying **core competencies** "
        "while eliminating noise. "
        f"Some of the technical skills well known to you are: {technical_skills}."
    ),
)

# Agent to format and structure the extracted skills
formatted_skill_extractor_structured = Agent(
    role=(
        "You are an expert in extracting and formatting **technical and non-technical skills** from the given data. "
        "Your job is to identify and return them in a **structured Python list format**, ignoring unrelated content."
    ),
    goal=(
        "Return a **clean, structured list** of skills from the input data. "
        "Make sure the skills are clearly formatted and categorized properly where applicable."
    ),
    verbose=False,
    memory=True,
    llm=llm,
    backstory=(
        "This agent was designed to efficiently extract and organize both technical and soft skills "
        "from various sources. It enhances readability by structuring the output in a usable format. "
        f"Some technical skills you know: {technical_skills}."
    ),
    output_format="""
    ["Python", "Java", "C++", "JavaScript", "Rust", "Go", "HTML", "CSS", "React", "Node.js", "Flutter", "Swift","Kotlin", "SQL", "PostgreSQL", "MongoDB", "Git", "GitHub", "TensorFlow", "AWS", "Azure", "Docker", "Kubernetes", "Communication", "Teamwork", "Problem-solving", "Leadership"]
    """,
)

# Define the tasks
unstructured_skills_task = Task(
    description="Extract technical and non-technical skills from {data}.",
    expected_output="A list of only relevant technical and non-technical skills.",
    agent=technical_skill_extractor_unstructured,
)

structured_skills_task = Task(
    description="Format the extracted skills from {data} into a Python list Give a single list containing both technical and non technical . the output format should be like [skill1,skill2...]",
    expected_output="Clean, Python list of categorized skills.",
    agent=formatted_skill_extractor_structured,
)

# Create the crew with agents and tasks
crew1 = Crew(
    agents=[technical_skill_extractor_unstructured, formatted_skill_extractor_structured],
    tasks=[unstructured_skills_task, structured_skills_task],
    process=Process.sequential
)

# Function to extract and return structured skills from a user's data
def get_content_crew(data):
    try:
        result = crew1.kickoff(inputs={"data": data, "skills": technical_skills})
        return result
    except Exception as e:
        logger.error(f"Error in get_content_crew: {str(e)}")
        return f"Error processing content: {str(e)}"

# # example data
# data="I am a fervent machine learning enthusiast with an endless thirst for the newest technological advancements pursuing B.Tech in Artificial Intelligence and Data Science. In addition to coding, I enjoy working with groups to plan interesting technical events, speeches, and workshops that unite the tech community. For the past seven years, I've had the honor of hosting many (tech and non tech) shows, which has helped me hone my communication abilities and establish relationships with various audiences. I take on challenges because of my unwavering confidence and persistence, always looking for ways to advance and innovate.Currently, I am a part of the Artificial Intelligence team at IEEE SB VIT, Pune, where we are trying to create an innovative project that involves AI and ML. I am learning more about machine learning, Natural Language Processing and Data Structure and Algorithms. Together, let's connect and investigate the exciting worlds of learning, cooperation, and technology."
# print(get_content_crew(data))