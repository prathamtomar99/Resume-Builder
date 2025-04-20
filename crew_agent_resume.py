from crewai import Crew, Agent, Task
from dotenv import load_dotenv
import logging
import os
from crewai import LLM

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- LLM SETUP ---
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

# --- AGENTS DEFINITION ---

# 1. Information Collector Agent
info_collector = Agent(
    role="Information Collector",
    goal="Efficiently gather all necessary details for resume creation from the prebuild resumes :{resume}",
    backstory="A highly skilled data analyst specializing in extracting structured and unstructured information. "
              "Expert in identifying missing details and asking relevant questions to ensure a comprehensive resume.",
    verbose=False,
    memory=True,
    allow_delegation=True,
    llm=llm
)

# 2. Resume Writer Agent
resume_writer = Agent(
    role="Resume Writer",
    goal="Craft a compelling, structured, and ATS-optimized resume take reference from {resume}",
    backstory="A professional resume writer with years of experience in creating high-impact resumes tailored to various industries. "
              "Expert in using powerful action verbs and ensuring clarity and professionalism.",
    verbose=False,
    llm=llm,
    memory=True
)

# 3. Proofreader & Enhancer Agent
proofreader = Agent(
    role="Proofreader & Enhancer",
    goal="Ensure the resume is error-free, well-structured, and polished",
    backstory="A meticulous editor with an eye for detail, grammar, and clarity. "
              "Excels at refining content, removing redundancies, and enhancing readability to make the resume stand out.",
    verbose=False,
    memory=True,
    llm=llm
)

# 4. Formatting Agent
formatter = Agent(
    role="Resume Formatter",
    goal="Apply a visually appealing and professional format to the resume",
    backstory="An experienced designer specializing in resume aesthetics, layout optimization, and readability enhancement. "
              "Ensures that the resume is both ATS-friendly and visually impressive.",
    verbose=False,
    memory=True,
    llm=llm
)

# --- TASKS DEFINITION ---

# Task 1: Collect Resume Information
collect_info_task = Task(
    description="Collect essential resume details, including personal information, work experience, skills, education, and notable achievements from the Linkedin Profile data : {profile}. Also take a look the {skills} person is having, and make accordingly. "
                "Ensure completeness and request clarification when needed." "You can include of what club the person was a member or any info u get, make a good resume",
    expected_output="A well-structured dataset containing all necessary resume information.",
    agent=info_collector
)

# Task 2: Write the Resume Content
write_resume_task = Task(
    description="Transform collected information into a compelling, well-organized resume. "
                "Ensure the content is engaging, professional, and optimized for Applicant Tracking Systems (ATS).",
    expected_output="A well-written resume draft with clear sections and impactful content.",
    agent=resume_writer,
    context=[collect_info_task]
)

# Task 3: Proofread & Enhance Content
proofread_task = Task(
    description="Review and refine the resume content to eliminate grammar errors, improve clarity, and enhance readability. "
                "Ensure that the writing style is professional, concise, and error-free.",
    expected_output="A polished, grammatically correct, and well-structured resume.",
    agent=proofreader,
    context=[write_resume_task]
)

# Task 4: Format the Resume
format_resume_task = Task(
    description="Apply an appropriate resume layout and styling to ensure readability and professionalism. "
                "Ensure the document follows standard formatting guidelines and is optimized for digital and print formats.",
    expected_output="A professionally formatted resume ready for job applications.",
    agent=formatter,
    context=[proofread_task]
)

crew = Crew(
    agents=[info_collector, resume_writer, proofreader, formatter],
    tasks=[collect_info_task, write_resume_task, proofread_task, format_resume_task]
)

def get_resume_crew(resume_data,profile,skill):
    result =  crew.kickoff(inputs={'resume': resume_data,'profile':profile,'skills':skill})
    for i in result:
        return i[1].replace("```","")
    