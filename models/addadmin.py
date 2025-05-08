from app.user_auth.user_class import User  # Adjust the import path accordingly
from models.database import db
db.delete_users_by_username_pattern("David")
User.add_user(
    user_name="David",
    user_type="admin",
    email="david@example.com",
    access_level=4,
    password="securepassword123"
)
