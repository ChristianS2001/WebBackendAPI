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

def populate_dummy_data():
    # Check if there are any doctors already in the database
    if Doctor.query.first() is None:
        # Create dummy doctors
        doc1 = Doctor(first_name='Julius', last_name='Hibbert')
        doc2 = Doctor(first_name='Algernop', last_name='Krieger')
        doc3 = Doctor(first_name='Nick', last_name='Riviera')

        db.session.add_all([doc1, doc2, doc3])
        db.session.commit()

        # Create dummy appointments for each doctor
        appointments = [
            Appointment(patient_first_name='Sterling', patient_last_name='Archer', date_time=datetime(2024, 4, 16, 8, 0), kind='New Patient', doctor=doc1),
            Appointment(patient_first_name='Cyril', patient_last_name='Figgis', date_time=datetime(2024, 4, 16, 8, 30), kind='Follow-up', doctor=doc2),
            # ... add more dummy appointments ...
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
    kind = db.Column(db.String(50), nullable=False)  # 'New Patient' or 'Follow-up'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)


@app.route('/doctors', methods=['GET'])
def get_doctors():
    print("Fetching doctors from the database")
    doctors = Doctor.query.all()
    json = jsonify([{'id': doc.id, 'first_name': doc.first_name, 'last_name': doc.last_name} for doc in doctors])
    print(str(json))
    return json


@app.route('/appointments/<int:doctor_id>', methods=['GET'])
def get_appointments(doctor_id):
    date = request.args.get('date')  # Expected format 'YYYY-MM-DD'
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
    new_appointment = Appointment(
        patient_first_name=data['patient_first_name'],
        patient_last_name=data['patient_last_name'],
        date_time=datetime.strptime(data['date_time'], '%Y-%m-%dT%H:%M'),
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


