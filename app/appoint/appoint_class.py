from datetime import date
from models.database import db
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
    def cancel_appointment(appointment_id):
        """
        Change status of an appointment to cancelled.
        """
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_appointment 
                SET status = %s
                WHERE appointment_id = %s
            """
            cursor.execute(query, ("cancelled", appointment_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False 

    @staticmethod
    def get_appointments(user_id, access_level):
        try:
            cursor = db.get_cursor()

            # If user is admin_appoint, retrieve all existing appointments
            if access_level == 2 or access_level == 4:
                query = """
                    SELECT * FROM salon_appointment
                """
                cursor.execute(query)
            else:
            # otherwise get the appointments for a specific user
                query = """
                    SELECT * FROM salon_appointment WHERE consumer_id = %s
                """
                cursor.execute(query, (user_id,))

            rows = cursor.fetchall()
            cursor.close()

            appointments = []
            for row in rows:
                appointment = Appointment(
                    appointment_id=row[0],
                    status=row[1],
                    approved=row[2],
                    date_appoint=row[3],
                    slot=row[4],
                    venue=row[5],
                    consumer_id=row[6],
                    provider_id=row[7],
                    consumer_name=row[8],
                    provider_name=row[9],
                    nber_services=row[10],
                    consumer_report=row[11] if len(row) > 11 else None
                )
                appointments.append(appointment)

            return appointments
        except Exception as e:
            print("Error getting appointments:", e)
            return []

    @staticmethod
    def get_appointment(appointment_id):
        """
        Retrieve a single appointment by ID.
        """
        try:
            cursor = db.get_cursor()
            query = """
                SELECT * FROM salon_appointment
                WHERE appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                # Create appointment with named parameters
                return Appointment(
                    appointment_id=row[0],
                    status=row[1],
                    approved=row[2],
                    date_appoint=row[3],
                    slot=row[4],
                    venue=row[5],
                    consumer_id=row[6],
                    provider_id=row[7],
                    consumer_name=row[8],
                    provider_name=row[9],
                    nber_services=row[10],
                    consumer_report=row[11] if len(row) > 11 else None
                )
            return None
        except Exception as e:
            print(f"Error retrieving appointment {appointment_id}: {e}")
            return None
        
    @staticmethod
    def update_appointment(appointment_id, date_appoint, slot, venue, nber_services, consumer_report):
        """
        Update appointment information in the salon_appointment table.
        """
        try:
            cursor = db.get_cursor()
            query = """
                UPDATE salon_appointment 
                SET date_appoint = %s, slot = %s, venue = %s, nber_services = %s, consumer_report = %s
                WHERE appointment_id = %s
            """
            cursor.execute(query, (date_appoint, slot, venue, nber_services, consumer_report, appointment_id))
            db.commit()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
            return False

    @staticmethod
    def add_appointment(appointment):
        """
        Add an appointment to the database.

        Args:
            appointment (Appointment): The Appointment object to add.
        """
        try:
            cursor = db.get_cursor()
            query = '''
            INSERT INTO salon_appointment (
                status, approved, date_appoint, slot, venue,
                consumer_id, provider_id, consumer_name, provider_name,
                nber_services, consumer_report
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING appointment_id
            '''
            cursor.execute(query, (
                appointment.status,
                appointment.approved,
                appointment.date_appoint,
                appointment.slot,
                appointment.venue,
                appointment.consumer_id,
                appointment.provider_id,
                appointment.consumer_name,
                appointment.provider_name,
                appointment.nber_services,
                appointment.consumer_report
            ))
            
            # Get the newly created appointment's ID
            appointment_id = cursor.fetchone()[0]
            appointment.appointment_id = appointment_id  # Update the object with the new ID
            
            db.commit()
            cursor.close()
            
            print(f"Appointment added successfully with ID: {appointment_id}")
            return appointment_id
        except Exception as e:
            print("Error adding appointment:", e)
            return None
