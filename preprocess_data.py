import pandas as pd
import numpy as np
import re
from load_data import get_data

data_dict = get_data()

hospital_data = data_dict['hospital_data']
location_data = data_dict['location_data']
payment_data = data_dict['payment_data']
service_data = data_dict['service_data']
operating_time = data_dict['operating_time']


def encode_care_system(care_system: str) -> int:
    if care_system == "Public":
        return 1

    if care_system == "Private":
        return 2

    else:
        return 0


# Create Matrix Factorization
def generate_factorized_matrix(data, column):
    points = set()
    for i, element in enumerate(data[column].values):
        element = re.sub('\.', ',', element)
        values = element.split(',')
        for value in values:
            try:
                value = int(value.strip())
                points.add(value)
            except:
                continue

    matrix = np.zeros((len(data), len(points)))
    for i, element in enumerate(data[column].values):
        element = re.sub('\.', ',', element)
        values = element.split(',')
        for value in values:
            try:
                value = int(value.strip())
                matrix[i, value] = 1
            except:
                continue

    return matrix, points


def get_matrices() -> dict:
    service_matrix, service_points = generate_factorized_matrix(hospital_data, 'Service Id')
    location_matrix, location_points = generate_factorized_matrix(hospital_data, 'Location ID')
    operating_time_matrix, op_time_points = generate_factorized_matrix(hospital_data, 'Operating time ID')
    payment_matrix, payment_points = generate_factorized_matrix(hospital_data, 'Payment ID')

    care_system = hospital_data['Care system'].apply(lambda x: encode_care_system(str(x)))
    ratings = hospital_data['rating'].fillna(0).values

    return {
        "service": [service_matrix, service_points],
        "location": [location_matrix, location_points],
        "operating_time": [operating_time_matrix, op_time_points],
        "payment": [payment_matrix, payment_points],
        "care system": np.array([care_system]),
        "ratings": np.array([ratings])
    }


def get_matrix(elements, data, size, name_col, id_col, is_op=False):
    matrix = np.zeros(size)
    for i, element in enumerate(elements):
        df = data.copy()
        try:
            if is_op:
                day_dict = {
                    0: "Monday",
                    1: "Tuesday",
                    2: "Wednesday",
                    3: "Thursday",
                    4: "Friday",
                    5: "Saturday",
                    6: "Sunday"
                }

                day = day_dict[i]
                df = df[df['Operation_Day'] == day]

            id = df[df[name_col] == element][id_col].values[0]
            matrix[id] = 1

        except:
            pass

    return matrix


def gen_hospital_matrix(service, location, op_time, care_system, payment, rating, points: list):
    print(service)
    service = get_matrix(service, service_data, len(points[0]), 'Service Name', 'Service Id')
    print(service)
    location = get_matrix(location, location_data, len(points[1]), 'Location Name', 'Location ID')

    op = get_matrix(op_time, operating_time, len(points[2]), 'Operation_Time', 'Time_of_operation_id', is_op=True)
    payment = get_matrix(payment, payment_data, len(points[3]), 'Payment Name', 'Payment ID')
    care_s = np.array([encode_care_system(care_system)])

    if rating == 'Any':
        rating = 0

    return np.concatenate([
        np.array([service]), [location], [op], [payment], care_s.reshape(-1, 1), np.array([rating]).reshape(-1, 1)
    ], axis=1)
