import streamlit as st

# Custom CSS to change the color of the button with a specific ID
st.markdown(
    """
     <style>
    .special-button button {
        background-color: green;
        color: white;
        border-radius: 12px;  /* Adjust the radius to get the desired roundness */
        padding: 0.5em 1em;   /* Optional: Adjust padding for better appearance */
        border: none;        /* Optional: Remove border */
        cursor: pointer;     /* Optional: Add pointer cursor */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to create a button with a unique ID
def special_button(label, key=None):
    # Use st.markdown to create an HTML button with a unique class
    button_id = key if key else label
    custom_button = st.markdown(f"""
        <div class="special-button">
            <button id="{button_id}">{label}</button>
        </div>
        <script>
            document.getElementById("{button_id}").onclick = function() {{
                window.location.reload();
            }}
        </script>
    """, unsafe_allow_html=True)
    return st.session_state.get(button_id, False)