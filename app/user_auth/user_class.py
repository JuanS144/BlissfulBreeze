from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from models.database import db
bcrypt = Bcrypt()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class User(UserMixin):
    def __init__(
            self, 
            user_id,
            user_name,
            email,
            password,
            active=True,
            user_type='client',
            access_level=1,
            user_image='default-user.png',
            phone_number='CSIT',
            address='CS',
            age=18,
            pay_rate=15.75,
            speciality='Hair-dresser'):
        
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.active = active
        self.user_type = user_type
        self.access_level = access_level
        self.user_image = user_image
        self.phone_number = phone_number
        self.address = address
        self.age = age
        self.pay_rate = pay_rate
        self.speciality = speciality

    def get_id(self):
        return str(self.user_id)
    
    def update_user(self):
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET user_image = %s, email = %s, user_name = %s, phone_number = %s, address = %s, age = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (self.user_image, self.email, self.user_name, self.phone_number, self.address, self.age, self.user_id))
            db.commit()  
        except Exception as e:
            print(f"Error updating user profile: {e}")

    def activate_user(self):
        """Activates a user both in memory and in the database"""
        try:
            # Update local object
            self.active = True
            
            # Update database
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET active = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (True, self.user_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error activating user: {e}")
            return False

    def deactivate_user(self):
        """Deactivates a user both in memory and in the database"""
        try:
            # Update local object
            self.active = False
            
            # Update database
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET active = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (False, self.user_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error deactivating user: {e}")
            return False

    @staticmethod
    def hash_password(password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        return hashed_pwd
    
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)
    
    @staticmethod
    def add_user(
        user_name,
        email,
        password,
        active=True,
        user_type='client',
        access_level=1,
        user_image='default-user.png',
        phone_number='CSIT',
        address='CS',
        age=18,
        pay_rate=15.75,
        speciality='Hair-dresser',
    ):
        try:
            cursor = db.get_cursor()
            password = User.hash_password(password)

            query = """
                INSERT INTO salon_user (
                    user_name, email, password, active, user_type, access_level,
                    user_image, phone_number, address, age, pay_rate, speciality
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                user_name, email, password, active, user_type, access_level,
                user_image, phone_number, address, age, pay_rate, speciality
            ))
            db.commit()
            cursor.close()
            print("User added successfully.")
        except Exception as e:
            print("Error adding user:", e)

    def update_speciality(self):
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET speciality = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (self.speciality, self.user_id))
            db.commit()  
        except Exception as e:
            print(f"Error updating user profile: {e}")
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            cursor = db.get_cursor()
            query = "SELECT * FROM salon_user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                user = User(
                    user_id=row[0],
                    active=row[1],
                    user_type=row[2],
                    access_level=row[3],
                    user_name=row[4],
                    email=row[5],
                    user_image=row[6],
                    password=row[7],
                    phone_number=row[8],
                    address=row[9],
                    age=row[10],
                    pay_rate=row[11],
                    speciality=row[12]
                )
                return user
            else:
                print(f'User {user_id} not found!')
                return None
        except Exception as e:
            print("Error retrieving user:", e)
            return None

    @staticmethod
    def get_user_by_username(username):
        try:
            cursor = db.get_cursor()
            query = """
                SELECT user_id, user_name, email, password, active, user_type, access_level,
                    user_image, phone_number, address, age, pay_rate, speciality
                FROM salon_user
                WHERE user_name = %s
            """
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return User(*result)
            else:
                print(f'User {username} not found!')
                return None
        except Exception as e:
            print("Error getting user:", e)
            return None
    
    @staticmethod
    def get_professionals():
        try:
            cursor = db.get_cursor()
            query = """
                SELECT *
                FROM salon_user
                WHERE user_type = 'professional'
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            if not results:
                print("No professionals found.")
                return []

            professionals = [
                User(
                    user_id=row[0],
                    active=row[1],
                    user_type=row[2],
                    access_level=row[3],
                    user_name=row[4],
                    email=row[5],
                    user_image=row[6],
                    password=row[7],
                    phone_number=row[8],
                    address=row[9],
                    age=row[10],
                    pay_rate=row[11],
                    speciality=row[12]
                )
                for row in results
            ]
            return professionals
        except Exception as e:
            print("Error getting professionals:", e)
            return None
        
    @staticmethod
    def get_username_from_id(user_id):
        try:
            cursor = db.get_cursor()
            query = """
                SELECT user_name
                FROM salon_user
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                print(f'User {user_id} not found!')
                return None
        except Exception as e:
            print("Error getting user name:", e)
            return None
        
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


