from datetime import timedelta, datetime
from random import randint

from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()


# Function to generate a random date and time within a specific range
def random_datetime(start_datetime, end_datetime):
    return start_datetime + timedelta(
        days=randint(0, 100),
        hours=randint(0, 23),
        minutes=randint(0, 59),
        seconds=randint(0, 59),
    )

symptomsProvider = DynamicProvider(
    provider_name="symptoms",
    elements=["Fever", "Headache", "Fatigue", "Cough", "Sore throat", "Shortness of breath",
              "Muscle aches", "Nausea", "Vomiting", "Diarrhea"],
)

medicationsProvider = DynamicProvider(
    provider_name="medications",
    elements=[ "Aspirin", "Ibuprofen", "Acetaminophen (Paracetamol)", "Naproxen",
               "Loratadine", "Diphenhydramine (Benadryl)", "Ranitidine", "Omeprazole",
               "Loperamide", "Simethicone", "Famotidine", "Dextromethorphan (DXM)",
               "Guaifenesin", "Vitamin C (Ascorbic Acid)", "Melatonin"]
)

activitiesProvider = DynamicProvider(
    provider_name="activities",
    elements=["Wake up", "Brush teeth", "Take a shower", "Eat breakfast",
              "Go to work/school", "Lunch", "Complete assignments/tasks",
              "Exercise", "Dinner", "Relax and unwind", "Read", "Watch TV or movies",
              "Socialize with friends or family", "Prepare for bed", "Sleep"]
)
fake.add_provider(symptomsProvider)
fake.add_provider(medicationsProvider)
fake.add_provider(activitiesProvider)

# Function to generate sample data for a given schema
def generate_data(schema_type, num_samples):
    data = []
    current_datetime = datetime(2023, 1, 1, 0, 0, 0)  # Starting date and time
    end_datetime = datetime(2023, 8, 31, 23, 59, 59)  # Ending date and time

    for _ in range(num_samples):
        date_time = random_datetime(current_datetime, end_datetime)
        if schema_type == "Symptom":
            name = fake.symptoms()
        elif schema_type == "Medication":
            name = fake.medications()
        elif schema_type == "Activity":
            name = fake.activities()
        else:
            name = fake.word()
        description = fake.sentence()

        if schema_type == "Symptom":
            data.append({"date": date_time, "name": name, "type": "Symptom", "description": description})
        elif schema_type == "Activity":
            data.append({"date": date_time, "name": name, "type": "Activity", "description": description})
        elif schema_type == "Medication":
            data.append({"date": date_time, "name": name, "type": "Medication", "description": description})

        current_datetime = date_time

    return data
