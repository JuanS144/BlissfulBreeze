from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import os
import psycopg2
from config import Config 

bcrypt = Bcrypt()

class SalonUser(UserMixin):
    def __init__(self, connection, user_id, active, user_type, access_level, user_name, email,
                 password, phone_number, address, age, pay_rate,
                 speciality, user_image='default-user.png'):
        self.id = user_id
        self.__connection = connection
        self.active = active
        self.user_type = user_type
        self.access_level = access_level
        self.username = user_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.address = address
        self.age = age
        self.pay_rate = pay_rate
        self.speciality = speciality
        self.image_file = user_image

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "active": self.active,
            "user_type": self.user_type,
            "access_level": self.access_level,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "age": self.age,
            "pay_rate": self.pay_rate,
            "speciality": self.speciality,
            "image_file": self.image_file
        }
    
    @staticmethod
    def get_user_by_username(connection, user_name):
        qry = "SELECT * FROM salon_user WHERE user_name = %s"
        with connection.cursor() as curr:
            curr.execute(qry, (user_name,))
            res = curr.fetchone()
            return SalonUser(connection, *res) if res else None
        
    @staticmethod
    def get_user_by_id(connection, user_id):
        qry = "SELECT * FROM salon_user WHERE user_id = %s"
        with connection.cursor() as curr:
            curr.execute(qry, (user_id,))
            res = curr.fetchone()
            return SalonUser(connection ,*res) if res else None
        
    @staticmethod    
    def get_users(connection, condition="TRUE"):
        qry = f"SELECT * FROM salon_user WHERE {condition}"
        with connection.cursor() as curr:
            curr.execute(qry)
            return [SalonUser(connection, *row) for row in curr.fetchall()]
        
    @staticmethod
    def update_user(connection, user_id, user_name, email, phone_number, address):
        qry = """
            UPDATE salon_user SET user_name = %s, email = %s,
            phone_number = %s, address = %s WHERE user_id = %s
        """
        with connection.cursor() as curr:
            try:
                curr.execute(qry, (user_name, email, phone_number, address, user_id))
                connection.commit()
                return True
            except Exception as e:
                print(f"Update error: {e}")
                connection.rollback()
                return False
            
    @staticmethod
    def delete_user(connection, user_id):
        qry = "DELETE FROM salon_user WHERE user_id = %s"
        with connection.cursor() as curr:
            try:
                curr.execute(qry, (user_id,))
                connection.commit()
                return True
            except Exception as e:
                print(f"Delete error: {e}")
                return False
    
class SalonAppointment:
    def __init__(self, connection, appointment_id, status, approved, date_appoint, slot,
                 venue, consumer_id, provider_id, consumer_name, provider_name,
                 nber_services=1, user_update_intitiator=None,
                 user_cancel_intitiator=None, consumer_report=None,
                 provider_report=None):
        self.id = appointment_id
        self.__connection = connection
        self.status = status
        self.approved = approved
        self.date_appoint = date_appoint
        self.slot = slot
        self.venue = venue
        self.consumer_id = consumer_id
        self.provider_id = provider_id
        self.consumer_name = consumer_name
        self.provider_name = provider_name
        self.nber_services = nber_services
        self.user_update_intitiator = user_update_intitiator
        self.user_cancel_intitiator = user_cancel_intitiator
        self.consumer_report = consumer_report
        self.provider_report = provider_report

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "approved": self.approved,
            "date_appoint": self.date_appoint.isoformat() if hasattr(self.date_appoint, "isoformat") else self.date_appoint,
            "slot": self.slot,
            "venue": self.venue,
            "consumer_id": self.consumer_id,
            "provider_id": self.provider_id,
            "consumer_name": self.consumer_name,
            "provider_name": self.provider_name,
            "nber_services": self.nber_services,
            "user_update_intitiator": self.user_update_intitiator,
            "user_cancel_intitiator": self.user_cancel_intitiator,
            "consumer_report": self.consumer_report,
            "provider_report": self.provider_report
        }
    
    # === APPOINTMENT OPERATIONS ===
    @staticmethod
    def create_appointment(connection, consumer_id, provider_id, slot, venue, date_appoint,
                           consumer_name, provider_name, nber_services=1):
        qry = """
            INSERT INTO salon_appointment (
                consumer_id, provider_id, slot, venue, date_appoint,
                consumer_name, provider_name, nber_services
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as curr:
            try:
                curr.execute(qry, (consumer_id, provider_id, slot, venue, date_appoint,
                                   consumer_name, provider_name, nber_services))
                connection.commit()
                return True
            except Exception as e:
                print(f"Create appointment error: {e}")
                connection.rollback()
                return False

    @staticmethod
    def get_appointments(connection, condition="TRUE"):
        qry = f"SELECT * FROM salon_appointment WHERE {condition}"
        with connection.cursor() as curr:
            curr.execute(qry)
            return [SalonAppointment(connection, *row) for row in curr.fetchall()]

    @staticmethod
    def get_appointment_by_id(connection, appointment_id):
        qry = "SELECT * FROM salon_appointment WHERE appointment_id = %s"
        with connection.cursor() as curr:
            curr.execute(qry, (appointment_id,))
            res = curr.fetchone()
            return SalonAppointment(connection, *res) if res else None

    @staticmethod
    def update_appointment(connection, appointment_id, status=None, approved=None,
                           consumer_report=None, provider_report=None):
        fields = []
        values = []
        if status is not None:
            fields.append("status = %s")
            values.append(status)
        if approved is not None:
            fields.append("approved = %s")
            values.append(approved)
        if consumer_report is not None:
            fields.append("consumer_report = %s")
            values.append(consumer_report)
        if provider_report is not None:
            fields.append("provider_report = %s")
            values.append(provider_report)
        if not fields:
            return False

        qry = f"UPDATE salon_appointment SET {', '.join(fields)} WHERE appointment_id = %s"
        values.append(appointment_id)

        with connection.cursor() as curr:
            try:
                curr.execute(qry, values)
                connection.commit()
                return True
            except Exception as e:
                print(f"Update appointment error: {e}")
                connection.rollback()
                return False

    @staticmethod
    def delete_appointment(connection, appointment_id):
        qry = "DELETE FROM salon_appointment WHERE appointment_id = %s"
        with connection.cursor() as curr:
            try:
                curr.execute(qry, (appointment_id,))
                connection.commit()
                return True
            except Exception as e:
                print(f"Delete appointment error: {e}")
                connection.rollback()
                return False