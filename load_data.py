import pandas as pd

def get_data() -> dict:
    hospital_data = pd.read_csv("Hospital Data - Hospital.csv")
    location_data = pd.read_csv("Hospital Data - Location.csv")
    payment_data = pd.read_csv("Hospital Data - Payment system.csv")
    service_data = pd.read_csv("Hospital Data - Services.csv")
    operating_time = pd.read_csv("Hospital Data - Time Of Operation.csv")
    full_hospital_data = pd.read_csv("Hospital Data.csv")

    return {
        "hospital_data": hospital_data,
        "location_data": location_data,
        "payment_data": payment_data,
        "service_data": service_data,
        "operating_time": operating_time,
        "full_hospital_data": full_hospital_data
    }