import streamlit as st
from streamlit_navigation_bar import st_navbar
from load_data import get_data
import numpy as np
from recommendation import get_recommendation

page = st_navbar(["Home", "Get Recommendation", "About", "Settings", "Contribute"])

if page == "Home":
    st.title("Hospital Recommendation System")
    st.write("First of its kind Uganda based healthcare recommendation system")

if page == "Get Recommendation":
    if 'selected_services' not in st.session_state:
        st.session_state['step'] = 0

    st.subheader("Select Features")
    services = get_data()['service_data']
    locations = get_data()['location_data']
    payment_data = get_data()['payment_data']
    operating_time = get_data()['operating_time']

    col_count = 4

    services_list = services['Service Name'].values
    location_list = ['Any'] + locations['Location Name'].to_list()

    if 'selected_services' in st.session_state:
        if len(st.session_state['selected_services']) != 0:
            st.markdown("#### Selected Services (tap to remove)")
            selected_cols = st.columns(len(st.session_state['selected_services']))
            for idx, service in enumerate(st.session_state['selected_services']):
                with selected_cols[idx]:
                    if st.button(service, key=f"selected_{service}"):
                        st.session_state['selected_services'].remove(service)

                        if len(st.session_state['selected_services']) == 0:
                            st.session_state['step'] = 0

                        st.rerun()

    if 'location' in st.session_state:
        if len(st.session_state['location']) != 0:
            st.markdown("#### Selected Locations (tap to remove)")
            selected_cols = st.columns(len(st.session_state['location']))
            for idx, location in enumerate(st.session_state['location']):
                with selected_cols[idx]:
                    if st.button(location):
                        st.session_state['location'].remove(location)

                        if len(st.session_state['location']) == 0:
                            st.session_state['step'] = 1

                        st.rerun()

    if 'payment' in st.session_state:
        if len(st.session_state['payment']) != 0:
            st.markdown("#### Selected payments (tap to remove)")
            selected_cols = st.columns(len(st.session_state['payment']))
            for idx, payment in enumerate(st.session_state['payment']):
                with selected_cols[idx]:
                    if st.button(payment):
                        st.session_state['payment'].remove(payment)

                        if len(st.session_state['payment']) == 0:
                            st.session_state['step'] = 2

                        st.rerun()
    if 'care_system' in st.session_state:
        st.write(f"### Selected Care System - {st.session_state['care_system']}")

    if 'operating_time' in st.session_state:
        if len(st.session_state['operating_time']) != 0:
            st.markdown("#### Selected Operating time")
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            selected_cols = st.columns(len(st.session_state['operating_time']))
            for idx, operating in enumerate(st.session_state['operating_time']):
                with selected_cols[idx]:
                    st.write(days[idx])
                    st.write(operating)

    if 'rating' in st.session_state:
        st.write(f"### Selected rating - {st.session_state['rating']}")

    col1, col2 = st.columns([1, 1])
    with col1:
        confirm = st.button("Next", type='primary')
        if confirm:
            st.session_state['step'] = int(st.session_state['step']) + 1

    with col2:
        back = st.button("Back")
        if back:
            st.session_state['step'] = int(st.session_state['step']) - 1 if st.session_state['step'] > 0 else 0

    st.divider()

    # Define the number of columns and calculate the number of rows needed
    if st.session_state['step'] == 0:
        row_counts = len(services_list) // col_count + (1 if len(services_list) % col_count != 0 else 0)

        # Display services as buttons in a grid
        for i in range(row_counts):
            cols = st.columns(col_count)
            for j in range(col_count):
                service_index = i * col_count + j
                if service_index < len(services_list):
                    with cols[j]:
                        if st.button(services_list[service_index]):
                            if 'selected_services' not in st.session_state:
                                st.session_state['selected_services'] = []

                            if service_index not in st.session_state['selected_services']:
                                st.session_state['selected_services'].append(services_list[service_index])
                                st.rerun()

    if st.session_state['step'] == 1:
        location = st.multiselect("Select a location", location_list)

        st.session_state['location'] = location

    if st.session_state['step'] == 2:
        st.subheader("Select a Payment Method")
        payment_list = payment_data['Payment'].values[:-1]
        payment = st.multiselect("Select a payment method", payment_list)

        st.session_state['payment'] = payment

    if st.session_state['step'] == 3:
        st.subheader("Select a care system Method")
        care_system = st.selectbox("Select a care system method",['Any', 'Public', 'Private'])
        st.session_state['care_system'] = care_system

    if st.session_state['step'] == 4:
        st.subheader("Select an Operating Time")
        operating_time = get_data()['operating_time']
        operating_time_list = ["Any"] + list(operating_time['Operation_Time'].unique())
        days = operating_time['Operation_Day'].unique()[:-1]
        Values = list(np.zeros(len(days)))
        for i, day in enumerate(days):
            value = st.selectbox(f"Select Operating Time on {day}", options=operating_time_list[:-1])
            Values[i] = value

        st.session_state['operating_time'] = Values

    if st.session_state['step'] == 5:
        st.subheader("Select Rating")
        rating = st.selectbox("Rating", options=["Any", 1, 2, 3, 4, 5])
        st.session_state['rating'] = rating

    if st.session_state['step'] == 6:
        st.subheader("Recommendations")
        recommendations = get_recommendation(st.session_state['selected_services'],
                                             st.session_state['location'],
                                             st.session_state['payment'],
                                             st.session_state['rating'],
                                             st.session_state['operating_time'],
                                             st.session_state['care_system'])

        for index, hospital in recommendations.iterrows():
            with st.expander(f"## {hospital['Hospital']}"):
                st.write(f"### {hospital['Location']}")
                st.write(f"**Services Offered:** {hospital['cleaned services']}")
                st.write(f"**Payment Options:** {hospital['payment']}")
                st.write(f"**Care System:** {hospital['Care system']}")
                st.write(f"**Rating:** {hospital['rating']}")

                # Show website as a clickable link
                st.write(f"**Website:** [{hospital['website']}]({hospital['website']})")

                st.subheader("Opening Hours")
                days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for day in days_of_week:
                    st.write(f"**{day}:** {hospital[day]}")


if page == "About":
    st.write("@ 2024 Pollicy")

if page == "Settings":
    st.subheader("Select an algorithm to use")

if page == "Contribute":
    st.write("## The Smart healthcare system highly depends on data.. Contribute by helping in the recording of more "
             "healthcare facilities in Uganda")

    st.write("### Login in to Contribute")
    st.write("# Coming soon...")
