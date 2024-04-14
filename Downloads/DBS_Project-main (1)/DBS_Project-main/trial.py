from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Connect to the PostgreSQL database
url = "postgresql://databaseproject_owner:@ep-frosty-unit-a196xe4o.ap-southeast-1.aws.neon.tech/databaseproject?sslmode=require"
connection = psycopg2.connect(url)

# SQL queries

#Projects Table
INSERT_PROJECT_QUERY = "INSERT INTO Projects (ProjectName, Description, CreatorUserID, DueDate) VALUES (%s, %s, %s, %s) RETURNING ProjectID;"
SELECT_PROJECT_QUERY = "SELECT * FROM Projects WHERE ProjectID = %s;"
UPDATE_PROJECT_QUERY = "UPDATE Projects SET ProjectName = %s, Description = %s, DueDate = %s WHERE ProjectID = %s;"
DELETE_PROJECT_QUERY = "DELETE FROM Projects WHERE ProjectID = %s;"
#Users Table
INSERT_USER_QUERY = "INSERT INTO Users (Username, Email, Password, JoiningDate) VALUES (%s, %s, %s, %s) RETURNING UserID;"
SELECT_USER_QUERY = "SELECT * FROM Users WHERE UserID = %s;"
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("Username")
    email = data.get("Email")
    password = data.get("Password")
    joining_date_str = data.get("JoiningDate")
    try:
        joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        joining_date = datetime.now(timezone.utc).date()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER_QUERY, (username, email, password, joining_date))
            user_id = cursor.fetchone()[0]

    return jsonify({"UserID": user_id}), 201