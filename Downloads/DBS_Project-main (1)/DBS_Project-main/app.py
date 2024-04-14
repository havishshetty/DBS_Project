from flask import Flask, request, jsonify,render_template ,redirect, url_for
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Connect to the PostgreSQL database

url = "postgresql://project_owner:8fqFmW4bLHvU@ep-polished-butterfly-a5hy3sqw.us-east-2.aws.neon.tech/project?sslmode=require"
connection = psycopg2.connect(url)

# SQL queries

# #Projects Table
# INSERT_PROJECT_QUERY = "INSERT INTO Projects (ProjectName, Description, CreatorUserID, DueDate) VALUES (%s, %s, %s, %s) RETURNING ProjectID;"
# SELECT_PROJECT_QUERY = "SELECT * FROM Projects WHERE ProjectID = %s;"
# UPDATE_PROJECT_QUERY = "UPDATE Projects SET ProjectName = %s, Description = %s, DueDate = %s WHERE ProjectID = %s;"
# DELETE_PROJECT_QUERY = "DELETE FROM Projects WHERE ProjectID = %s;"
# #Users Table
# INSERT_USER_QUERY = "INSERT INTO Users (Username, Email, Password, JoiningDate) VALUES (%s, %s, %s, %s) RETURNING UserID;"
# SELECT_USER_QUERY = "SELECT * FROM Users WHERE UserID = %s;"
# UPDATE_USER_QUERY = "UPDATE Users SET Username = %s, Email = %s, Password = %s, JoiningDate = %s WHERE UserID = %s;"
# DELETE_USER_QUERY = "DELETE FROM Users WHERE UserID = %s;"
# #Tasks Table
# INSERT_TASK_QUERY = "INSERT INTO Tasks (Title, Description, DueDate, Status, AssigneeUserID, ProjectID) VALUES (%s, %s, %s, %s, %s, %s) RETURNING TaskID;"
# SELECT_TASK_QUERY = "SELECT * FROM Tasks WHERE TaskID = %s;"
# UPDATE_TASK_QUERY = "UPDATE Tasks SET Title = %s, Description = %s, DueDate = %s, Status = %s, AssigneeUserID = %s, ProjectID = %s WHERE TaskID = %s;"
# DELETE_TASK_QUERY = "DELETE FROM Tasks WHERE TaskID = %s;"
# #Label Table
# INSERT_LABEL_QUERY = "INSERT INTO Labels (LabelName, ProjectID) VALUES (%s, %s) RETURNING LabelID;"
# SELECT_LABEL_QUERY = "SELECT * FROM Labels WHERE LabelID = %s;"
# UPDATE_LABEL_QUERY = "UPDATE Labels SET LabelName = %s, ProjectID = %s WHERE LabelID = %s;"
# DELETE_LABEL_QUERY = "DELETE FROM Labels WHERE LabelID = %s;"
# #TaskProgress Table
# INSERT_TASK_PROGRESS_QUERY = "INSERT INTO TaskProgress (TaskName, TaskID, LabelID) VALUES (%s, %s, %s) RETURNING TaskProgressID;"
# SELECT_TASK_PROGRESS_QUERY = "SELECT * FROM TaskProgress WHERE TaskProgressID = %s;"
# UPDATE_TASK_PROGRESS_QUERY = "UPDATE TaskProgress SET TaskName = %s, TaskID = %s, LabelID = %s WHERE TaskProgressID = %s;"
# DELETE_TASK_PROGRESS_QUERY = "DELETE FROM TaskProgress WHERE TaskProgressID = %s;"
# #Roles Table
# INSERT_ROLE_QUERY = "INSERT INTO Roles (UserID, ProjectID, RoleName, Description) VALUES (%s, %s, %s, %s);"
# SELECT_ROLE_QUERY = "SELECT * FROM Roles WHERE UserID = %s AND ProjectID = %s;"
# UPDATE_ROLE_QUERY = "UPDATE Roles SET RoleName = %s, Description = %s WHERE UserID = %s AND ProjectID = %s;"
# DELETE_ROLE_QUERY = "DELETE FROM Roles WHERE UserID = %s AND ProjectID = %s;"
# #Comments Table
# INSERT_COMMENT_QUERY = "INSERT INTO Comments (CommentText, TaskID, UserID) VALUES (%s, %s, %s) RETURNING CommentID;"
# SELECT_COMMENT_QUERY = "SELECT * FROM Comments WHERE CommentID = %s;"
# UPDATE_COMMENT_QUERY = "UPDATE Comments SET CommentText = %s WHERE CommentID = %s;"
# DELETE_COMMENT_QUERY = "DELETE FROM Comments WHERE CommentID = %s;"
# #Attachments Table
# INSERT_ATTACHMENT_QUERY = "INSERT INTO Attachments (FileName, FilePath, TaskID, UserID) VALUES (%s, %s, %s, %s) RETURNING AttachmentID;"
# SELECT_ATTACHMENT_QUERY = "SELECT * FROM Attachments WHERE AttachmentID = %s;"
# UPDATE_ATTACHMENT_QUERY = "UPDATE Attachments SET FileName = %s, FilePath = %s WHERE AttachmentID = %s;"
# DELETE_ATTACHMENT_QUERY = "DELETE FROM Attachments WHERE AttachmentID = %s;"
# #Permissions Table
# INSERT_PERMISSION_QUERY = "INSERT INTO Permissions (UserID, Action) VALUES (%s, %s) RETURNING PermissionID;"
# SELECT_PERMISSION_QUERY = "SELECT * FROM Permissions WHERE PermissionID = %s;"
# UPDATE_PERMISSION_QUERY = "UPDATE Permissions SET Action = %s WHERE PermissionID = %s;"
# DELETE_PERMISSION_QUERY = "DELETE FROM Permissions WHERE PermissionID = %s;"
# #Notifications Table
# INSERT_NOTIFICATION_QUERY = "INSERT INTO Notifications (UserID, Message) VALUES (%s, %s) RETURNING NotificationID;"
# SELECT_NOTIFICATION_QUERY = "SELECT * FROM Notifications WHERE NotificationID = %s;"
# UPDATE_NOTIFICATION_QUERY = "UPDATE Notifications SET Message = %s WHERE NotificationID = %s;"
# DELETE_NOTIFICATION_QUERY = "DELETE FROM Notifications WHERE NotificationID = %s;"


#Login Endpoint

@app.route('/')
def login():
    return render_template('login_page.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login_submit():
    data=request.get_json()
    username = data.get("username")
    password = data.get("password")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
    if user:
        return redirect(url_for('home'))
    else:
        return render_template('login_page.html', error='Wrong username or password')



# #Project Endpoints
# @app.route("/api/projects", methods=["POST"])
# def create_project():
#     data = request.get_json()
#     project_name = data.get("ProjectName")
#     description = data.get("Description")
#     creator_user_id = data.get("CreatorUserID")
#     due_date_str = data.get("DueDate")
#     try:
#         due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         due_date = None
    
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_PROJECT_QUERY, (project_name, description, creator_user_id, due_date))
#             project_id = cursor.fetchone()[0]
    
#     return jsonify({"ProjectID": project_id}), 201

# @app.route("/api/projects/<int:project_id>", methods=["GET"])
# def get_project(project_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_PROJECT_QUERY, (project_id,))
#             project = cursor.fetchone()
#             if project:
#                 return jsonify({
#                     "ProjectID": project[0],
#                     "ProjectName": project[1],
#                     "Description": project[2],
#                     "CreatorUserID": project[3],
#                     "DueDate": project[4].isoformat() if project[4] else None
#                 })
#             else:
#                 return jsonify({"message": "Project not found"}), 404

# @app.route("/api/projects/<int:project_id>", methods=["PUT"])
# def update_project(project_id):
#     data = request.get_json()
#     project_name = data.get("ProjectName")
#     description = data.get("Description")
#     due_date_str = data.get("DueDate")
#     try:
#         due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         due_date = None

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_PROJECT_QUERY, (project_name, description, due_date, project_id))
    
#     return jsonify({"message": "Project updated successfully"}), 200

# @app.route("/api/projects/<int:project_id>", methods=["DELETE"])
# def delete_project(project_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_PROJECT_QUERY, (project_id,))
    
#     return jsonify({"message": "Project deleted successfully"}), 200

# #User Endpoints

# @app.route("/api/users", methods=["POST"])
# def create_user():
#     data = request.get_json()
#     username = data.get("Username")
#     email = data.get("Email")
#     password = data.get("Password")
#     joining_date_str = data.get("JoiningDate")
#     try:
#         joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         joining_date = datetime.now(timezone.utc).date()

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_USER_QUERY, (username, email, password, joining_date))
#             user_id = cursor.fetchone()[0]

#     return jsonify({"UserID": user_id}), 201

# @app.route("/api/users/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_USER_QUERY, (user_id,))
#             user = cursor.fetchone()
#             if user:
#                 return jsonify({
#                     "UserID": user[0],
#                     "Username": user[1],
#                     "Email": user[2],
#                     "Password": user[3],
#                     "JoiningDate": user[4].isoformat() if user[4] else None
#                 })
#             else:
#                 return jsonify({"message": "User not found"}), 404

# @app.route("/api/users/<int:user_id>", methods=["PUT"])
# def update_user(user_id):
#     data = request.get_json()
#     username = data.get("Username")
#     email = data.get("Email")
#     password = data.get("Password")
#     joining_date_str = data.get("JoiningDate")
#     try:
#         joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         joining_date = None

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_USER_QUERY, (username, email, password, joining_date, user_id))

#     return jsonify({"message": "User updated successfully"}), 200

# @app.route("/api/users/<int:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_USER_QUERY, (user_id,))

#     return jsonify({"message": "User deleted successfully"}), 200


# #Task Endpoints
# @app.route("/api/tasks", methods=["POST"])
# def create_task():
#     data = request.get_json()
#     title = data.get("Title")
#     description = data.get("Description")
#     due_date_str = data.get("DueDate")
#     try:
#         due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         due_date = None
#     status = data.get("Status")
#     assignee_user_id = data.get("AssigneeUserID")
#     project_id = data.get("ProjectID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_TASK_QUERY, (title, description, due_date, status, assignee_user_id, project_id))
#             task_id = cursor.fetchone()[0]

#     return jsonify({"TaskID": task_id}), 201

# @app.route("/api/tasks/<int:task_id>", methods=["GET"])
# def get_task(task_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_TASK_QUERY, (task_id,))
#             task = cursor.fetchone()
#             if task:
#                 return jsonify({
#                     "TaskID": task[0],
#                     "Title": task[1],
#                     "Description": task[2],
#                     "DueDate": task[3].isoformat() if task[3] else None,
#                     "Status": task[4],
#                     "AssigneeUserID": task[5],
#                     "ProjectID": task[6]
#                 })
#             else:
#                 return jsonify({"message": "Task not found"}), 404

# @app.route("/api/tasks/<int:task_id>", methods=["PUT"])
# def update_task(task_id):
#     data = request.get_json()
#     title = data.get("Title")
#     description = data.get("Description")
#     due_date_str = data.get("DueDate")
#     try:
#         due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
#     except (ValueError, TypeError):
#         due_date = None
#     status = data.get("Status")
#     assignee_user_id = data.get("AssigneeUserID")
#     project_id = data.get("ProjectID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_TASK_QUERY, (title, description, due_date, status, assignee_user_id, project_id, task_id))

#     return jsonify({"message": "Task updated successfully"}), 200

# @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_TASK_QUERY, (task_id,))

#     return jsonify({"message": "Task deleted successfully"}), 200

# #Label Endpoints
# @app.route("/api/labels", methods=["POST"])
# def create_label():
#     data = request.get_json()
#     label_name = data.get("LabelName")
#     project_id = data.get("ProjectID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_LABEL_QUERY, (label_name, project_id))
#             label_id = cursor.fetchone()[0]

#     return jsonify({"LabelID": label_id}), 201

# @app.route("/api/labels/<int:label_id>", methods=["GET"])
# def get_label(label_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_LABEL_QUERY, (label_id,))
#             label = cursor.fetchone()
#             if label:
#                 return jsonify({
#                     "LabelID": label[0],
#                     "LabelName": label[1],
#                     "ProjectID": label[2]
#                 })
#             else:
#                 return jsonify({"message": "Label not found"}), 404

# @app.route("/api/labels/<int:label_id>", methods=["PUT"])
# def update_label(label_id):
#     data = request.get_json()
#     label_name = data.get("LabelName")
#     project_id = data.get("ProjectID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_LABEL_QUERY, (label_name, project_id, label_id))

#     return jsonify({"message": "Label updated successfully"}), 200

# @app.route("/api/labels/<int:label_id>", methods=["DELETE"])
# def delete_label(label_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_LABEL_QUERY, (label_id,))

#     return jsonify({"message": "Label deleted successfully"}), 200

# #TaskProgress Endpoints
# @app.route("/api/task-progress", methods=["POST"])
# def create_task_progress():
#     data = request.get_json()
#     task_name = data.get("TaskName")
#     task_id = data.get("TaskID")
#     label_id = data.get("LabelID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_TASK_PROGRESS_QUERY, (task_name, task_id, label_id))
#             task_progress_id = cursor.fetchone()[0]

#     return jsonify({"TaskProgressID": task_progress_id}), 201

# @app.route("/api/task-progress/<int:task_progress_id>", methods=["GET"])
# def get_task_progress(task_progress_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_TASK_PROGRESS_QUERY, (task_progress_id,))
#             task_progress = cursor.fetchone()
#             if task_progress:
#                 return jsonify({
#                     "TaskProgressID": task_progress[0],
#                     "TaskName": task_progress[1],
#                     "TaskID": task_progress[2],
#                     "LabelID": task_progress[3]
#                 })
#             else:
#                 return jsonify({"message": "Task progress not found"}), 404

# @app.route("/api/task-progress/<int:task_progress_id>", methods=["PUT"])
# def update_task_progress(task_progress_id):
#     data = request.get_json()
#     task_name = data.get("TaskName")
#     task_id = data.get("TaskID")
#     label_id = data.get("LabelID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_TASK_PROGRESS_QUERY, (task_name, task_id, label_id, task_progress_id))

#     return jsonify({"message": "Task progress updated successfully"}), 200

# @app.route("/api/task-progress/<int:task_progress_id>", methods=["DELETE"])
# def delete_task_progress(task_progress_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_TASK_PROGRESS_QUERY, (task_progress_id,))

#     return jsonify({"message": "Task progress deleted successfully"}), 200

# #Roles Endpoint
# @app.route("/api/roles", methods=["POST"])
# def create_role():
#     data = request.get_json()
#     user_id = data.get("UserID")
#     project_id = data.get("ProjectID")
#     role_name = data.get("RoleName")
#     description = data.get("Description")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_ROLE_QUERY, (user_id, project_id, role_name, description))

#     return jsonify({"message": "Role created successfully"}), 201

# @app.route("/api/roles/<int:user_id>/<int:project_id>", methods=["GET"])
# def get_role(user_id, project_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_ROLE_QUERY, (user_id, project_id))
#             role = cursor.fetchone()
#             if role:
#                 return jsonify({
#                     "UserID": role[0],
#                     "ProjectID": role[1],
#                     "RoleName": role[2],
#                     "Description": role[3]
#                 })
#             else:
#                 return jsonify({"message": "Role not found"}), 404

# @app.route("/api/roles/<int:user_id>/<int:project_id>", methods=["PUT"])
# def update_role(user_id, project_id):
#     data = request.get_json()
#     role_name = data.get("RoleName")
#     description = data.get("Description")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_ROLE_QUERY, (role_name, description, user_id, project_id))

#     return jsonify({"message": "Role updated successfully"}), 200

# @app.route("/api/roles/<int:user_id>/<int:project_id>", methods=["DELETE"])
# def delete_role(user_id, project_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_ROLE_QUERY, (user_id, project_id))

#     return jsonify({"message": "Role deleted successfully"}), 200

# #Comment Endpoint
# @app.route("/api/comments", methods=["POST"])
# def create_comment():
#     data = request.get_json()
#     comment_text = data.get("CommentText")
#     task_id = data.get("TaskID")
#     user_id = data.get("UserID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_COMMENT_QUERY, (comment_text, task_id, user_id))
#             comment_id = cursor.fetchone()[0]

#     return jsonify({"CommentID": comment_id}), 201

# @app.route("/api/comments/<int:comment_id>", methods=["GET"])
# def get_comment(comment_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_COMMENT_QUERY, (comment_id,))
#             comment = cursor.fetchone()
#             if comment:
#                 return jsonify({
#                     "CommentID": comment[0],
#                     "CommentText": comment[1],
#                     "TaskID": comment[2],
#                     "UserID": comment[3]
#                 })
#             else:
#                 return jsonify({"message": "Comment not found"}), 404

# @app.route("/api/comments/<int:comment_id>", methods=["PUT"])
# def update_comment(comment_id):
#     data = request.get_json()
#     comment_text = data.get("CommentText")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_COMMENT_QUERY, (comment_text, comment_id))

#     return jsonify({"message": "Comment updated successfully"}), 200

# @app.route("/api/comments/<int:comment_id>", methods=["DELETE"])
# def delete_comment(comment_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_COMMENT_QUERY, (comment_id,))

#     return jsonify({"message": "Comment deleted successfully"}), 200
# #Attachment Table
# @app.route("/api/attachments", methods=["POST"])
# def create_attachment():
#     data = request.get_json()
#     file_name = data.get("FileName")
#     file_path = data.get("FilePath")
#     task_id = data.get("TaskID")
#     user_id = data.get("UserID")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_ATTACHMENT_QUERY, (file_name, file_path, task_id, user_id))
#             attachment_id = cursor.fetchone()[0]

#     return jsonify({"AttachmentID": attachment_id}), 201

# @app.route("/api/attachments/<int:attachment_id>", methods=["GET"])
# def get_attachment(attachment_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_ATTACHMENT_QUERY, (attachment_id,))
#             attachment = cursor.fetchone()
#             if attachment:
#                 return jsonify({
#                     "AttachmentID": attachment[0],
#                     "FileName": attachment[1],
#                     "FilePath": attachment[2],
#                     "TaskID": attachment[3],
#                     "UserID": attachment[4]
#                 })
#             else:
#                 return jsonify({"message": "Attachment not found"}), 404

# @app.route("/api/attachments/<int:attachment_id>", methods=["PUT"])
# def update_attachment(attachment_id):
#     data = request.get_json()
#     file_name = data.get("FileName")
#     file_path = data.get("FilePath")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_ATTACHMENT_QUERY, (file_name, file_path, attachment_id))

#     return jsonify({"message": "Attachment updated successfully"}), 200

# @app.route("/api/attachments/<int:attachment_id>", methods=["DELETE"])
# def delete_attachment(attachment_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_ATTACHMENT_QUERY, (attachment_id,))

#     return jsonify({"message": "Attachment deleted successfully"}), 200

# #Permissions Endpoints
# @app.route("/api/permissions", methods=["POST"])
# def create_permission():
#     data = request.get_json()
#     user_id = data.get("UserID")
#     action = data.get("Action")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_PERMISSION_QUERY, (user_id, action))
#             permission_id = cursor.fetchone()[0]

#     return jsonify({"PermissionID": permission_id}), 201

# @app.route("/api/permissions/<int:permission_id>", methods=["GET"])
# def get_permission(permission_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_PERMISSION_QUERY, (permission_id,))
#             permission = cursor.fetchone()
#             if permission:
#                 return jsonify({
#                     "PermissionID": permission[0],
#                     "UserID": permission[1],
#                     "Action": permission[2]
#                 })
#             else:
#                 return jsonify({"message": "Permission not found"}), 404

# @app.route("/api/permissions/<int:permission_id>", methods=["PUT"])
# def update_permission(permission_id):
#     data = request.get_json()
#     action = data.get("Action")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_PERMISSION_QUERY, (action, permission_id))

#     return jsonify({"message": "Permission updated successfully"}), 200

# @app.route("/api/permissions/<int:permission_id>", methods=["DELETE"])
# def delete_permission(permission_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_PERMISSION_QUERY, (permission_id,))

#     return jsonify({"message": "Permission deleted successfully"}), 200

# #Notifications Endpoints
# @app.route("/api/notifications", methods=["POST"])
# def create_notification():
#     data = request.get_json()
#     user_id = data.get("UserID")
#     message = data.get("Message")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(INSERT_NOTIFICATION_QUERY, (user_id, message))
#             notification_id = cursor.fetchone()[0]

#     return jsonify({"NotificationID": notification_id}), 201

# @app.route("/api/notifications/<int:notification_id>", methods=["GET"])
# def get_notification(notification_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(SELECT_NOTIFICATION_QUERY, (notification_id,))
#             notification = cursor.fetchone()
#             if notification:
#                 return jsonify({
#                     "NotificationID": notification[0],
#                     "UserID": notification[1],
#                     "Message": notification[2]
#                 })
#             else:
#                 return jsonify({"message": "Notification not found"}), 404

# @app.route("/api/notifications/<int:notification_id>", methods=["PUT"])
# def update_notification(notification_id):
#     data = request.get_json()
#     message = data.get("Message")

#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(UPDATE_NOTIFICATION_QUERY, (message, notification_id))

#     return jsonify({"message": "Notification updated successfully"}), 200

# @app.route("/api/notifications/<int:notification_id>", methods=["DELETE"])
# def delete_notification(notification_id):
#     with connection:
#         with connection.cursor() as cursor:
#             cursor.execute(DELETE_NOTIFICATION_QUERY, (notification_id,))

#     return jsonify({"message": "Notification deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)