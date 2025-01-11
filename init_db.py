from ext import app, db
from models import Service, User, Course, Post, Software

with app.app_context():
    
    db.drop_all()
    db.create_all()
    
    admin_user = User(
        username="admin",
        email = "admin@geocyber.ge",
        name="Admin",
        surname="Admin",
        password="adminpass",
        role="Admin"
    )

    # Add the admin user to the session and commit
    admin_user.save()