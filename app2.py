import streamlit as st

st.set_page_config(
    page_title="Student Feedback System",
    page_icon="📝",
    layout="wide"
)

st.title("🎓 Student Feedback Management System")
st.write("Welcome to the Student Feedback Management System!")

name = st.text_input("Enter your name")
rating = st.slider("Rate your experience", 1, 5, 3)
feedback = st.text_area("Enter your feedback")

if st.button("Submit Feedback"):
    if name.strip() and feedback.strip():
        st.success("Thank you for your feedback!")
        st.write("Name:", name)
        st.write("Rating:", rating, "/5")
        st.write("Feedback:", feedback)
    else:
        st.warning("Please enter your name and feedback.")
