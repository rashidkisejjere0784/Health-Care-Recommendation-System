import intellikit as ik
import numpy as np
from numpy.linalg import norm


def calculate_cosine_similarity(point, full_data, data_df, n=3):
    cosine_similarities = np.dot(full_data, point.T) / (norm(full_data, axis=1)[:, np.newaxis] * norm(point))
    top_choices = np.argsort(cosine_similarities.flatten())[-n:][::-1]
    top_names = data_df.iloc[top_choices]
    return top_names, top_choices


def get_recommendation_nn(full_data, data_point, data_df, service_len):
    """ Get the recommendation based on the Nearest Neighbors Algorithm. """
    full_data_services = full_data[:, :service_len]
    print(data_point[:, :service_len], full_data_services[:, :service_len])
    top_choices = calculate_cosine_similarity(data_point[:, :service_len], full_data_services, data_df, n=4)[1]

    filtered_data = full_data[top_choices]

    final_vector = data_point[:, service_len:]

    final_choices = calculate_cosine_similarity(final_vector, filtered_data[:, service_len:], data_df)[1]
    top_choices = top_choices[final_choices]

    return data_df.iloc[top_choices]
