from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .model import SalonAppointment, SalonUser  # replace with correct import if needed
from . import api   
from models.database import db

@api.route('/appointments', methods=['GET'])
def get_appointments():
    conn = db.db_conn()
    appointments = SalonAppointment.get_appointments(conn)
    return jsonify([a.to_dict() for a in appointments]), 200


@api.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    conn = db.db_conn()
    appointment = SalonAppointment.get_appointment_by_id(conn, appointment_id)
    if not appointment:
        return jsonify({"msg": "Appointment not found"}), 404
    return jsonify(appointment.to_dict()), 200


@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    conn = db.db_conn()
    data = request.get_json()
    user_id = get_jwt_identity()

    # For simplicity, assume the logged-in user is the consumer.
    consumer = SalonUser.get_user_by_id(conn, user_id)
    provider = SalonUser.get_user_by_id(conn, data['provider_id'])

    if not consumer or not provider:
        return jsonify({"msg": "User(s) not found"}), 404

    created = SalonAppointment.create_appointment(
        conn,
        consumer_id=consumer.id,
        provider_id=provider.id,
        slot=data['slot'],
        venue=data['venue'],
        date_appoint=data['date_appoint'],
        consumer_name=consumer.username,
        provider_name=provider.username,
        nber_services=data.get('nber_services', 1)
    )
    if created:
        return jsonify({"msg": "Appointment created"}), 201
    return jsonify({"msg": "Failed to create appointment"}), 400


@api.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    conn = db.db_conn()
    user_id = int(get_jwt_identity())
    appointment = SalonAppointment.get_appointment_by_id(conn, appointment_id)

    if not appointment or appointment.consumer_id != user_id:
        return jsonify({"msg": "Unauthorized or not found"}), 403

    data = request.get_json()
    updated = SalonAppointment.update_appointment(
        conn,
        appointment_id,
        status=data.get('status'),
        approved=data.get('approved'),
        consumer_report=data.get('consumer_report'),
        provider_report=data.get('provider_report')
    )
    if updated:
        return jsonify({"msg": "Appointment updated"}), 200
    return jsonify({"msg": "Failed to update appointment"}), 400


@api.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    conn = db.db_conn()
    user_id = int(get_jwt_identity())
    appointment = SalonAppointment.get_appointment_by_id(conn, appointment_id)

    # Assume is_admin() checks a user's access level
    is_admin = SalonUser.get_user_by_id(conn, user_id).access_level == 'admin'

    if not appointment or (appointment.consumer_id != user_id and not is_admin):
        return jsonify({"msg": "Unauthorized or not found"}), 403

    deleted = SalonAppointment.delete_appointment(conn, appointment_id)
    if deleted:
        return jsonify({"msg": "Appointment deleted"}), 200
    return jsonify({"msg": "Failed to delete"}), 400