import os
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt
from backend.models import db, User
from backend.api import (
    User_Login, AddSubject, User_Signup, AddChapter, AddQuiz,
    AddQuestion, Export_Details, Start_Quiz, User_Results,
    Admin_Summary, Admin_Users, Admin_Profile, User_Profile
)
from app import bcrypt

from backend.config import cache
from dotenv import load_dotenv
load_dotenv()
from flask_mail import Mail, Message
mail=Mail()
def create_app():
    app = Flask(__name__, static_folder="frontend/dist", template_folder="frontend/dist")
    
    # Load config (this already sets up your mail variables)
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object("backend.config.ProductionConfig")
    else:
        app.config.from_object("backend.config.LocalConfig")

    print("--- MAIL DEBUG INFO ---")
    print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    # For security, let's only print the length of the password
    password = app.config.get('MAIL_PASSWORD')
    print(f"MAIL_PASSWORD LENGTH: {len(password) if password else 0}")
    print("-----------------------")
    # --------------------------
    mail.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    return app
def admin_setup():
    admin = User.query.filter_by(Is_admin=True).first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password=bcrypt.generate_password_hash('vm123').decode('utf-8'),
            dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            full_name='Admin User',
            Is_admin=True,
            gender='Male',
            phone='1234567890',
            address='123 Admin St, Admin City, Admin Country',
            status='Active',
            qualification='Admin'
        )
        db.session.add(admin)
        db.session.commit()

app = create_app()
api = Api(app)
CORS(app)
jwt = JWTManager(app)

with app.app_context():
    # celery = celery_init_app(app)  # optional
    db.create_all()
    admin_setup()
@app.route("/send-test-email")
def send_test_email():
     # --- ADD THIS DEBUG BLOCK ---
    print("--- SENDING TEST EMAIL ---")
    print(f"Using Username: {app.config.get('MAIL_USERNAME')}")
    password = app.config.get('MAIL_PASSWORD')
    print(f"Using Password of Length: {len(password) if password else 0}")
    print("--------------------------")
    # ----
    try:
        # Create the message object
        msg = Message(
            subject="Hello from Flask on Render!",
            # The sender is automatically read from your app's config
            recipients=["vanshmittal021@gmail.com"] # <-- CHANGE THIS to your email
        )
        msg.body = "This is a test email sent from your deployed Flask application."
        
        # Send the email
        mail.send(msg)
        return "✅ Test email sent successfully!"
    except Exception as e:
        # This will print the exact error to your Render logs for debugging
        print(f"Error sending email: {str(e)}")
        return f"❌ Failed to send email: {str(e)}"

# API routes
api.add_resource(User_Login, '/login')
api.add_resource(AddSubject,'/add_subject/get', '/add_subject/post','/edit_subject/<int:sub_id>','/delete_subject/<int:sub_id>')
api.add_resource(User_Signup, '/signup')
api.add_resource(AddChapter, '/add_chapter/get', '/add_chapter/<int:subject_id>', '/edit_chapter/<int:chapter_id>','/delete_chapter/<int:chapter_id>','/get_chapters')
api.add_resource(AddQuiz,  '/add_quiz', '/edit_quiz/<int:quiz_id>', '/delete_quiz/<int:quiz_id>','/get_quiz')
api.add_resource(AddQuestion,'/add_question/<int:quiz_id>', '/edit_question/<int:question_id>', '/delete_question/<int:question_id>','/get_questions/<int:quiz_id>')
api.add_resource(Export_Details, '/export_details')
api.add_resource(Start_Quiz, '/start_quiz/<int:quiz_id>')
api.add_resource(User_Results, '/user_results')
api.add_resource(Admin_Summary, '/admin_summary')
api.add_resource(Admin_Users, '/admin_users')
api.add_resource(Admin_Profile, '/admin/profile')
api.add_resource(User_Profile, '/user/profile')

# Lightweight health check for uptime monitors (keeps Render free tier awake).
# Does no DB/cache work so external pings stay cheap.
@app.route("/health")
def health():
    return {"status": "ok"}, 200

# Catch-all route to serve Vue
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
    
 
    
if __name__ == "__main__":
    app.run(debug=True)