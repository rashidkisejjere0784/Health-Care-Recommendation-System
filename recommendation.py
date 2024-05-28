from preprocess_data import get_matrices, gen_hospital_matrix
import intellikit as ik
import numpy as np
import pandas as pd
from recommendation_algorithms import get_recommendation_nn


def get_recommendation(services, location, payment_method, rating, operating_time, care_system):
    data_df = pd.read_csv("Hospital Data.csv")
    matrices = get_matrices()
    service_matrix = matrices['service']
    location_matrix = matrices['location']
    payment_matrix = matrices['payment']
    operating_time_matrix = matrices['operating_time']
    care_system_matrix = matrices['care system']
    rating_matrix = matrices['ratings']

    full_encoded_matrix = np.concatenate([service_matrix[0], location_matrix[0], operating_time_matrix[0],
                                          payment_matrix[0], care_system_matrix.reshape(-1, 1),
                                          rating_matrix.reshape(-1, 1)], axis=1)

    hospital_matrix = gen_hospital_matrix(service=services, location=location, op_time=operating_time,
                                          payment=payment_method, care_system=care_system, rating=rating,
                                          points=[service_matrix[1], location_matrix[1], operating_time_matrix[1],
                                                  payment_matrix[1]]
                                          )

    recommendation = get_recommendation_nn(full_data=full_encoded_matrix, data_point=hospital_matrix, data_df=data_df,
                                           service_len=len(service_matrix[0]))

    return recommendation
