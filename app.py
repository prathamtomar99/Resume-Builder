from linked_info_selenium import extract_about_from_linkedin
from crewi_agent_extracter import get_content_crew
from crew_agent_resume import get_resume_crew
from format_docx import save_resume_to_docx
import logging
from bs4 import BeautifulSoup

logging.basicConfig(
    filename="app_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a",
    force=True,  # Ensures logging resets correctly
)

logger = logging.getLogger()

# Example log messages
logging.info("Application started")
for handler in logger.handlers:
    handler.flush()
    handler.close()

# extract data from linkenin 
link = "https://www.linkedin.com/in/sujal-thakur-317257287/"
data = extract_about_from_linkedin(link)
soup = BeautifulSoup(data, 'html.parser')

# Extract just the text
data = soup.get_text(separator=' ', strip=True)
logging.info(f"SELENIUM DATA LINE NO. 21: {data}")
skills = get_content_crew(data)
logging.info(f"CREW SKILLS LINE NO. 23: {data}")

try:
    for i in skills:
        print(i[1])
        logging.info(f"SKILLS SET LINE NO. 28: {i[1]}")
        temp = i[1].split("\n")[1]
        temp = temp.split("]")[0]
        temp = temp.split("[")[1]
        temp = temp.split(",")
        t = [i.replace("'","").strip() for i in temp]
        skills_list = t
        logging.info(f"SKILLS LIST LINE NO. 35: {skills_list}")
        break
except Exception as e:
    print("Error Occured")

# skills_list 
s = "'" + "','".join(skills_list) + "'"
logging.info("string formed in Line no. 48 is :",s)

#execute query here
# resume_data = run_query_here
resume_data = ""
resume_content = get_resume_crew(resume_data=resume_data,profile=data,skill = skills_list)
logging.info(f"SKILLS LIST LINE NO. 43: {resume_content}")
save_resume_to_docx(resume_content)

print("Logs have been written to 'app_logs.txt'")