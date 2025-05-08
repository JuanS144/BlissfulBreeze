from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from models.database import db
from datetime import date
bcrypt = Bcrypt()

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
            pay_rate=0,
            speciality='none'):
        
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
    @staticmethod
    def hash_password(password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        return hashed_pwd
    
    def check_password(self,password):
        return bcrypt.check_password_hash(self.password,password)
    
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

    def update_pay_rate(self):
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET pay_rate = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (self.pay_rate, self.user_id))
            db.commit()
        except Exception as e:
            print(f"Error updating pay rate: {e}")

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
            print(f"Error updating speciality: {e}")

    
    def update_admin(self):
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_user
                SET access_level = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (self.access_level, self.user_id))
            db.commit()  
        except Exception as e:
            print(f"Error updating user profile: {e}")


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
    
    @staticmethod
    def get_user_by_id(user_id):
        try:
            cursor = db.get_cursor()
            query = "SELECT * FROM salon_user WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
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
    def get_admins():
        try:
            cursor = db.get_cursor()
            query = """
                SELECT *
                FROM salon_user
                WHERE user_type = 'admin'
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
    def get_members():
        try:
            cursor = db.get_cursor()
            query = """
                SELECT *
                FROM salon_user
                WHERE access_level = 1"""
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


# ------------------- class Appointment -----------------
class Appointment:
    """
    Represents a hair salon appointment with attributes matching the salon_appointment table.
    Tracks appointments between consumers (clients) and providers (professionals).
    """
    salon_name = "Blissful Breeze"

    def __init__(self, appointment_id, consumer_id, provider_id, consumer_name, provider_name, 
                status="requested", approved=False, 
                date_appoint=date.today(), slot="9-10", venue="cmn_room",
                nber_services=1, consumer_report="", is_cancelled=False):
        
        self.appointment_id = appointment_id
        self.status = status
        self.approved = approved
        self.date_appoint = date_appoint
        self.slot = slot
        self.venue = venue
        
        # Consumer (client) and provider (professional) information
        self.consumer_id = consumer_id
        self.provider_id = provider_id
        self.consumer_name = consumer_name
        self.provider_name = provider_name
        self.nber_services = nber_services
        
        # Update and cancellation tracking
        self.is_cancelled = is_cancelled
        
        # Reports
        self.consumer_report = consumer_report

    def has_consumer_report(self):
        """Check if the appointment has a consumer report"""
        return self.consumer_report is not None and self.consumer_report.strip() != ''

    def is_cancelled(self):
        """Check if the appointment is cancelled"""
        return self.status == 'cancelled'

    def __str__(self):
        return f'Appointment #{self.appointment_id} - {self.date_appoint} {self.slot}, {self.consumer_name} with {self.provider_name}'
    
    @staticmethod
    def get_appointments():
        try:
            cursor = db.get_cursor()
            query = """
                SELECT * FROM salon_appointment
            """
            cursor.execute(query)
            appointments = cursor.fetchone()
            cursor.close()

            return appointments
        except Exception as e:
            print("Error getting appointments:", e)
            return None
        
    @staticmethod
    def get_appointment(appointment_id):
        try:
            cursor = db.get_cursor()
            query = """
                SELECT * FROM salon_appointment
                WHERE appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return Appointment(*result)
            else:
                print(f'Appointment {appointment_id} not found!')
                return None
        except Exception as e:
            print("Error getting appointment:", e)
            return None
    @staticmethod
    def update_appointment(appointment_id, updates):
        try:
            cursor = db.get_cursor()
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            values = list(updates.values()) + [appointment_id]
            query = f"UPDATE salon_appointment SET {set_clause} WHERE appointment_id = %s"
            cursor.execute(query, values)
            db.commit()
            cursor.close()
            print(f"Appointment {appointment_id} updated successfully.")
        except Exception as e:
            print("Error updating appointment:", e)
