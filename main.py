from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

#Creating dummy data for the flask app as a base in the database
def populate_dummy_data():
    if Doctor.query.first() is None:
        doc1 = Doctor(first_name='John', last_name='Johnson')
        doc2 = Doctor(first_name='Connor', last_name='McGreggor')
        doc3 = Doctor(first_name='Josh', last_name='Peck')

        db.session.add_all([doc1, doc2, doc3])
        db.session.commit()

        appointments = [
            Appointment(patient_first_name='Hunter', patient_last_name='Smith', date_time=datetime(2024, 4, 16, 8, 0), kind='New Patient', doctor=doc1),
            Appointment(patient_first_name='Christian', patient_last_name='Smith', date_time=datetime(2024, 4, 16, 8, 30), kind='Follow-up', doctor=doc2),
        ]

        db.session.add_all(appointments)
        db.session.commit()


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_first_name = db.Column(db.String(50), nullable=False)
    patient_last_name = db.Column(db.String(50), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    kind = db.Column(db.String(50), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)


@app.route('/doctors', methods=['GET'])
def get_doctors():
    print("Fetching doctors from the database")
    doctors = Doctor.query.all()
    json = jsonify([{'id': doc.id, 'first_name': doc.first_name, 'last_name': doc.last_name} for doc in doctors])
    print(str(json))
    return json


def appointment_time_is_valid(date_time):
    """Check if the appointment time is on a 15-minute interval."""
    return date_time.minute % 15 == 0 and date_time.second == 0


@app.route('/appointments/<int:doctor_id>', methods=['GET'])
def get_appointments(doctor_id):
    date = request.args.get('date')
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).filter(db.func.date(Appointment.date_time) == date_obj.date()).all()
    return jsonify([{'id': app.id, 'patient_first_name': app.patient_first_name, 'patient_last_name': app.patient_last_name, 'time': app.date_time.strftime('%Y-%m-%dT%H:%M'), 'kind': app.kind} for app in appointments])

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'}), 200


@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    
    try:
        date_time = datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date format, should be YYYY-MM-DDTHH:MM'}), 400
    
    if not appointment_time_is_valid(date_time):
        return jsonify({'error': 'Invalid appointment time, should be at a 15-minute interval'}), 400

    existing_appointments = Appointment.query.filter_by(doctor_id=data['doctor_id'], date_time=date_time).count()
    if existing_appointments >= 3:
        return jsonify({'error': 'A doctor can have no more than 3 appointments at the same time'}), 400

    new_appointment = Appointment(
        patient_first_name=data['patient_first_name'],
        patient_last_name=data['patient_last_name'],
        date_time=date_time,
        kind=data['kind'],
        doctor_id=data['doctor_id']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'id': new_appointment.id}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_dummy_data()
    app.run(debug=True)


