import requests
from pprint import pprint

base_url = "" #replace with your local ip given by flask from the output when you run the main.py file
#Run the main.py file before running this test file
#Also to test open up another terminal in the same directory and run the test_apis.py file

#Test Get Doctors
def test_get_doctors():
    response = requests.get(f"{base_url}/doctors")
    print("Get Doctors:")
    pprint(response.json())

#Test Get All Appointments for a Specific Doctor on a Specific Day
def test_get_appointments_for_doctor_on_day(doctor_id, date):
    response = requests.get(f"{base_url}/appointments/{doctor_id}?date={date}")
    print(f"Get All Appointments for Doctor {doctor_id} on {date}:")
    pprint(response.json())

#Test Delete an Appointment
def test_delete_appointment(appointment_id):
    response = requests.delete(f"{base_url}/appointments/{appointment_id}")
    print(f"Delete Appointment {appointment_id}:")
    pprint(response.json())

#Test Add a New Appointment
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
    return response.json()

#Test Adding an Appointment at Invalid Time
def test_add_appointment_invalid_time(doctor_id, date_time):
    print(f"Testing adding an appointment with invalid time {date_time}:")
    response = test_add_appointment(
        doctor_id=doctor_id,
        date_time=date_time,
        patient_first_name="Invalid",
        patient_last_name="Time",
        kind="New Patient"
    )
    pprint(response)

#Test Adding Too Many Appointments at the Same Time
def test_add_too_many_appointments_same_time(doctor_id, date_time):
    print(f"Testing adding too many appointments at the same time {date_time}:")
    #Assume doctor_id 1 is a valid doctor and we have already two appointments at 09:00
    count = 0
    responses = []
    for i in range(4):  #Attempt to add 4 appointments at the same time
        count+=1
        response = test_add_appointment(
            doctor_id=doctor_id,
            date_time=date_time,
            patient_first_name=f"TooMany{i}",
            patient_last_name="Appointments",
            kind="New Patient"
        )
        responses.append(response)
        if count != 4:
            print("This is the" + str(count) + "th appointment scheduled")
        elif count == 4:
            print("This is the" + str(count) + "th appointment scheduled")
            print("Now that we have reached 4 appointments at the same time we should see a fail here" + str(response))
    return responses

#Run tests
if __name__ == "__main__":
    test_get_doctors()

    #Test getting all appointments for a specific doctor on a specific day
    print("\n--- Testing getting all appointments for a specific doctor on a specific day ---")
    test_get_appointments_for_doctor_on_day(doctor_id=1, date="2024-04-16")

    #Testing valid appointment addition
    print("\n--- Testing valid appointment addition ---")
    added_appointment_response = test_add_appointment(
        doctor_id=1,
        date_time="2024-04-16T09:15",
        patient_first_name="John",
        patient_last_name="Doe",
        kind="New Patient"
    )
    
    #Extract the ID of the newly added appointment for deletion test
    added_appointment_id = added_appointment_response.get('id', None)
    
    #Testing invalid time (not at 15-minute intervals)
    print("\n--- Testing invalid time addition ---")
    test_add_appointment_invalid_time(
        doctor_id=1,
        date_time="2024-04-16T09:07"
    )
    
    print("\n--- Adding an appointment to be deleted ---")
    #Make sure this is a time slot that exists and is free for the doctor to avoid the 'no more than 3 appointments' error
    valid_appointment_for_deletion = test_add_appointment(
        doctor_id=1,
        date_time="2024-04-16T09:45",
        patient_first_name="Delete",
        patient_last_name="Me",
        kind="New Patient"
    )

    #Testing too many appointments at the same time
    print("\n--- Testing too many appointments at the same time ---")
    too_many_responses = test_add_too_many_appointments_same_time(
        doctor_id=4,
        date_time="2024-04-16T09:15"
    )

    #Test deletion of the appointment added for deletion
    if valid_appointment_for_deletion and 'id' in valid_appointment_for_deletion:
        print("\n--- Deleting the test appointment ---")
        appointment_id_to_delete = valid_appointment_for_deletion['id']
        test_delete_appointment(appointment_id=appointment_id_to_delete)
    else:
        print("Could not add an appointment for deletion test; no valid appointment ID returned from add operation.")
