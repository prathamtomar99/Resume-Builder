from flask import Flask, render_template, request, send_file, redirect, url_for
from linked_info_selenium import extract_about_from_linkedin
from crewi_agent_extracter import get_content_crew
from crew_agent_resume import get_resume_crew
from format_docx import save_resume_to_docx
from bs4 import BeautifulSoup
import mysql.connector
import os
from match_skills import get_skills

# Database se connection banana
connection = mysql.connector.connect(
    host="localhost",       # ya server ka address
    user="root",   # apna username
    password="89mnpopat", # apna password
    database="resumebuilderdb"  # jis database se data nikalna hai
)

# Cursor create karna
cursor = connection.cursor()


app = Flask(__name__)
RESUME_FILE = "formatted_resume.docx"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        linkedin_url = request.form.get("linkedin_url")

        # extract data from linkenin 
        link = linkedin_url
        data = extract_about_from_linkedin(link)
        soup = BeautifulSoup(data, 'html.parser')

        # Extract just the text
        data = soup.get_text(separator=' ', strip=True)
        print("Extracted DATA Line no. 38")
        print(data)

        # get skills from agent
        skills = get_content_crew(data)
        print("data recieed at line 43")
        print(skills)

        skills_str = str(skills.output) if hasattr(skills, 'output') else str(skills)
        print("Line no. ")
        print(skills_str)

        skills_list = get_skills(skills_str)
        print("Line no. 51")
        print(skills_list)

        str_data_sql=""
        try:    
            for i in skills_list:
                print(i)
                try:
                    query = f"SELECT project_description FROM project WHERE resume_id IN (SELECT resume_id FROM skills WHERE skill_name = {i});"
                    # Query execute karna
                    cursor.execute(query)
                    # Data fetch karna
                    result = cursor.fetchall()
                    # Print karna
                    for row in result:
                        str_data_sql+=row
                        print(row)
                except Exception as e:
                    continue
        except Exception as e:
            print("error occured at l no. 67")

        #execute query here
        # resume_data = run_query_here
        resume_data = str_data_sql
        resume_content = get_resume_crew(resume_data=resume_data,profile=data,skill = skills_str)
        save_resume_to_docx(resume_content)

        return redirect(url_for("result"))
    return render_template("index.html")

@app.route("/result")
def result():
    if os.path.exists(RESUME_FILE):
        return render_template("result.html")
    else:
        return "Resume not found.", 404

@app.route("/view")
def view_file():
    if os.path.exists(RESUME_FILE):
        return send_file(RESUME_FILE)
    return "File not found.", 404

@app.route("/download")
def download_file():
    if os.path.exists(RESUME_FILE):
        response = send_file(RESUME_FILE, as_attachment=True)
        os.remove(RESUME_FILE)
        return response
    return "File not found.", 404

if __name__ == "__main__":
    app.run(debug=True)

cursor.close()
connection.close()