import re

# Master list of skills (stored in original form)
master_skills = [
    # Core Software/Programming
    "Java", "Kotlin", "Python", "JavaScript", "Node.js", "HTML", "CSS", "React.js",
    "Vue.js", "Angular", "Express.js", "Django", "Flask", "Spring Boot",
    "C", "C++", "C#", "Go", "Rust", "TypeScript", "PHP", "SQL",

    # Databases & Backend
    "PostgreSQL", "MySQL", "MongoDB", "Firebase", "SQLite", "Oracle DB", "Redis",
    "Supabase", "GraphQL", "REST APIs", "Microservices",

    # DevOps & Tools
    "Git", "GitHub", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Nginx",
    "Terraform", "Ansible", "Linux", "Bash", "Shell Scripting",

    # Mobile & Cross-platform
    "Android Development", "iOS Development", "React Native", "Flutter", "Swift",

    # Machine Learning / AI
    "Machine Learning", "Deep Learning", "Computer Vision", "Natural Language Processing",
    "LLMs", "Transformers", "Scikit-learn", "TensorFlow", "PyTorch", "Keras",
    "OpenCV", "NLTK", "SpaCy", "Hugging Face", "MLFlow",

    # Data Engineering / Analytics
    "Data Analysis", "Data Visualization", "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "Power BI", "Tableau", "Excel", "Apache Spark", "Hadoop", "Airflow", "ETL",

    # Cloud Platforms
    "AWS", "Google Cloud", "Azure", "Heroku", "Cloudflare",

    # Engineering Tools & Tech (Non-software)
    "MATLAB", "Simulink", "AutoCAD", "SolidWorks", "ANSYS", "LTspice", 
    "LabVIEW", "Proteus", "PLC Programming", "Embedded Systems", 
    "Internet of Things (IoT)", "SCADA", "Arduino", "Raspberry Pi", 
    "PCB Design", "3D Printing",

    # Networking & Security
    "Computer Networks", "Network Security", "Cybersecurity", "Wireshark", "Cryptography",
    "Ethical Hacking", "Firewalls", "VPN",

    # Core Engineering Domains
    "Thermodynamics", "Fluid Mechanics", "Heat Transfer", "Structural Analysis",
    "CAD", "CAM", "Mechanics of Materials", "Manufacturing Processes",

    # Soft Skills / Management
    "Teamwork/Collaboration", "Project Coordination/Management", "Problem-solving",
    "Time Management", "Communication", "Adaptability", "Leadership", "Creativity",
    "Critical Thinking", "Public Speaking", "Presentation Skills", "Conflict Resolution",

    # Domain-Specific
    "Robotics", "Automation", "Control Systems", "Mechatronics", "Power Systems",
    "Renewable Energy", "Civil Engineering", "Geotechnical Engineering",
    "Transportation Engineering", "Environmental Engineering",

    "Agile", "Scrum", "Design Thinking", "UI/UX", "UI","UX","Figma", "Canva",
    "Technical Writing", "Documentation", "Research", "Patent Writing"
]


# Also store a lowercase version for matching
normalized_master = {skill.lower(): skill for skill in master_skills}

def extract_matching_skills(raw_text):
    # Extract quoted or unquoted words/phrases
    raw_matches = re.findall(r'"(.*?)"|[\w\-/+.]+', raw_text)
    
    cleaned_matches = [item.strip().lower() for item in raw_matches if item.strip()]
    
    # Check against normalized skills
    matched = []
    for word in cleaned_matches:
        if word in normalized_master:
            matched.append(normalized_master[word])  # Preserve original formatting

    return matched

def get_skills(text_input):
    skills = extract_matching_skills(text_input)
    return skills