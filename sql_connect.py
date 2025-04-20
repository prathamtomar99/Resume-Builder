import mysql.connector

# Database se connection banana
connection = mysql.connector.connect(
    host="localhost",       # ya server ka address
    user="root",   # apna username
    password="89mnpopat", # apna password
    database="resumebuilderdb"  # jis database se data nikalna hai
)

# Cursor create karna
cursor = connection.cursor()

# SQL query likhna
query = "SELECT project_description FROM project WHERE resume_id IN (SELECT resume_id FROM skills WHERE skill_name = 'Java');"

# Query execute karna
cursor.execute(query)

# Data fetch karna
result = cursor.fetchall()

# Print karna
for row in result:
    print(row)

# Close karna connection
cursor.close()
connection.close()