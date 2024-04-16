import requests
from pprint import pprint

base_url = "http://127.0.0.1:5000" #replace with your local ip given by flask from the output when you run the main.py file
#Run the main.py file before running this test file
#Also to test open up another terminal in the same directory and run the test_apis.py file

# Test Get Doctors
def test_get_doctors():
    response = requests.get(f"{base_url}/doctors")
    print("Get Doctors:")
    pprint(response.json())

# Test Get Appointments for a Doctor
def test_get_appointments(doctor_id, date):
    response = requests.get(f"{base_url}/appointments/{doctor_id}?date={date}")
    print(f"Get Appointments for Doctor {doctor_id} on {date}:")
    pprint(response.json())

# Test Delete an Appointment
def test_delete_appointment(appointment_id):
    response = requests.delete(f"{base_url}/appointments/{appointment_id}")
    print(f"Delete Appointment {appointment_id}:")
    pprint(response.json())

# Test Add a New Appointment
def test_add_appointment(doctor_id, date_time, patient_first_name, patient_last_name, kind):
    appointment_data = {
        "doctor_id": doctor_id,
        "date_time": date_time,
        "patient_first_name": patient_first_name,
        "patient_last_name": patient_last_name,
        "kind": kind
    }
    response = requests.post(f"{base_url}/appointments", json=appointment_data)
    print("Add New Appointment:")
    pprint(response.json())

# Run tests
if __name__ == "__main__":
    test_get_doctors()
    test_get_appointments(doctor_id=1, date="2024-04-16")
    test_add_appointment(
        doctor_id=1,
        date_time="2024-04-16T09:00",
        patient_first_name="John",
        patient_last_name="Doe",
        kind="New Patient"
    )
    # Ensure to use a valid appointment_id; for demo, assuming the new appointment's id is 4
    test_delete_appointment(appointment_id=4)
