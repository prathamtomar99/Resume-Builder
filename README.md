# Resume Builder with LinkedIn Integration

This project is a Resume Builder web application that integrates with LinkedIn to extract user information, process it, and generate a formatted resume. It uses Selenium for web scraping, Flask for the web framework, and connects to a MySQL database for storing project-related data.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x (preferably Python 3.7 or later)
- Google Chrome (for Selenium and remote debugging)
- MySQL (for the database)

## Setup and Installation

Follow the steps below to get started with the project.

### Step 1: Install Dependencies

Open your terminal and execute the following commands to install the necessary packages:

```bash
pip install -r requirements.txt
```

### Step 2: Open Google Chrome with Remote Debugging

To use Selenium with Chrome, you need to open Chrome in remote debugging mode.

Run the following command in your terminal:

```bash
# For macOS
open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile

# For Windows
start chrome --remote-debugging-port=9222 --user-data-dir="C:\chrome-profile"
```

This will allow Selenium to interact with your Chrome browser.

### Step 3: Prepare the Project Files

Save the following files in the same folder:
- main.py
- .env

Create a `.env` file with the following content:

```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_DATABASE=resumebuilderdb
```

### Step 4: Run the Python Script

Once you've set everything up, you can run the application. To start the web app, use the following command:

```bash
python main.py
```

### Step 5: Interact with the Application

1. Go to http://127.0.0.1:5000/ in your browser.
2. Login to LinkedIn (the app will open LinkedIn in your browser).
3. Enter the LinkedIn URL of the profile you want to extract information from.
4. The app will extract the About section, parse the data, and generate a formatted resume.

### Step 6: View and Download the Generated Resume

Once the resume is generated, you can:
- View the resume by going to `/view`.
- Download the resume by going to `/download`.

## How It Works

1. **LinkedIn Extraction**: The application uses Selenium to open LinkedIn profiles and scrape the "About" section.
2. **Skills Extraction**: Using a custom agent (crewi_agent_extracter), the skills are extracted from the profile text.
3. **Database Querying**: The extracted skills are matched with a database of project descriptions (stored in MySQL), and relevant projects are fetched.
4. **Resume Generation**: The extracted information, along with the matched project descriptions, is used to generate a professional-looking resume in .docx format.

## Project Structure

```
/project-folder
    ├── main.py               # Main application file
    ├── .env                  # Environment variables
    ├── /templates
    │   ├── index.html        # Main form for user input
    │   ├── result.html       # Display result page
    ├── /static
    │   └── (static assets)
    ├── /linked_info_selenium.py  # Script for LinkedIn data extraction
    ├── /crewi_agent_extracter.py # Script for extracting agent content
    ├── /crew_agent_resume.py     # Script for generating the resume
    ├── /format_docx.py           # Script for formatting and saving the resume
    ├── /match_skills.py          # Script for matching skills
    ├── /sql_connect.py           # temprorary python file to debug sql connection
    ├── /requirements.txt         # requirements file
```

## Troubleshooting

### Chrome not opening with remote debugging

If the Chrome browser doesn't open with the remote debugging port, you might see an error. If that happens, make sure:

- Google Chrome is installed correctly.
- The path to your user data directory (`/tmp/chrome-profile` or `"C:\chrome-profile"`) is valid.
- No other processes are using port 9222.

### Database Connection Issues

Ensure that your MySQL server is running and accessible with the credentials provided in `.env`. If you encounter issues, check the following:

- MySQL server status: Ensure the server is running and accessible.
- Database and table existence: Ensure the database `resumebuilderdb` and its tables (skills, project, etc.) exist.

## License

This project is licensed under the MIT License - see the LICENSE file for details.