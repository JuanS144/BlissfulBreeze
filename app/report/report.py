from datetime import date

class Report:
    def __init__(self, report_id, appointment_id, status='inactive', date_report=None, feedback_professional=None, feedback_client=None):
        self.report_id = report_id
        self.appointment_id = appointment_id
        self.status = status
        self.date_report = date_report or date.today()
        self.feedback_professional = feedback_professional
        self.feedback_client = feedback_client

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "appointment_id": self.appointment_id,
            "status": self.status,
            "date_report": self.date_report.isoformat(),
            "feedback_professional": self.feedback_professional,
            "feedback_client": self.feedback_client
        }

    @staticmethod
    def from_row(row):
        return Report(
            report_id=row[0],
            appointment_id=row[1],
            status=row[2],
            date_report=row[3],
            feedback_professional=row[4],
            feedback_client=row[5]
        )
    
    # ---------- DB Methods ----------
    @staticmethod
    def get_by_id(conn, report_id):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM salon_report WHERE report_id = %s", (report_id,))
            row = cur.fetchone()
            return Report.from_row(row) if row else None

    @staticmethod
    def get_all(conn):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM salon_report")
            rows = cur.fetchall()
            return [Report.from_row(row) for row in rows]

    @staticmethod
    def create(conn, report):
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO salon_report (appointment_id, status, date_report, feedback_professional, feedback_client)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING report_id
            """, (
                report.appointment_id,
                report.status,
                report.date_report,
                report.feedback_professional,
                report.feedback_client
            ))
            report_id = cur.fetchone()[0]
            conn.commit()
            report.report_id = report_id
            return report_id

    @staticmethod
    def update(conn, report):
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE salon_report
                SET appointment_id = %s,
                    status = %s,
                    date_report = %s,
                    feedback_professional = %s,
                    feedback_client = %s
                WHERE report_id = %s
            """, (
                report.appointment_id,
                report.status,
                report.date_report,
                report.feedback_professional,
                report.feedback_client,
                report.report_id
            ))
            conn.commit()

    @staticmethod
    def delete(conn, report_id):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM salon_report WHERE report_id = %s", (report_id,))
            conn.commit()

    @staticmethod
    def get_by_appointment_id(conn, appointment_id):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM salon_report WHERE appointment_id = %s", (appointment_id,))
            row = cur.fetchone()
            return Report.from_row(row) if row else None
        
    @staticmethod
    def validate_appointment_ownership(conn, appointment_id, user_id):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM salon_appointment 
                WHERE appointment_id = %s AND (consumer_id = %s OR provider_id = %s)
            """, (appointment_id, user_id, user_id))
            count = cur.fetchone()[0]
            return count > 0
        
        # ...existing code...

    @staticmethod
    def get_available_appointments(conn, user_id=None, is_admin=False):
        """Get appointments that don't have reports yet"""
        with conn.cursor() as cur:
            if is_admin:
                cur.execute("""
                    SELECT a.appointment_id, 
                           CONCAT('Appointment #', a.appointment_id, ' - ', a.consumer_name, ' with ', a.provider_name) 
                    FROM salon_appointment a 
                    LEFT JOIN salon_report r ON a.appointment_id = r.appointment_id 
                    WHERE r.report_id IS NULL
                """)
            else:
                cur.execute("""
                    SELECT a.appointment_id, 
                           CONCAT('Appointment #', a.appointment_id, ' - ', a.consumer_name, ' with ', a.provider_name) 
                    FROM salon_appointment a 
                    LEFT JOIN salon_report r ON a.appointment_id = r.appointment_id 
                    WHERE r.report_id IS NULL 
                    AND (a.consumer_id = %s OR a.provider_id = %s)
                """, (user_id, user_id))
            return cur.fetchall()

    @staticmethod
    def get_user_reports(conn, user_id):
        """Get all reports for a specific user"""
        reports = []
        all_reports = Report.get_all(conn)
        for report in all_reports:
            if Report.validate_appointment_ownership(conn, report.appointment_id, user_id):
                reports.append(report)
        return reports