import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# Load model
model = joblib.load('model_rf.joblib')

# Preprocessing
def preprocess(data_input):
    df = pd.read_csv('student_data_filtered.csv')
    df = df.drop(columns=['Status'], axis=1)
    df = pd.concat([df, data_input], ignore_index=True)

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    return df_scaled[-1].reshape(1, -1)

# Mappings
gender_map = {'Male': 1, 'Female': 0}
marital_map = {
    'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4,
    'Facto Union': 5, 'Legally Seperated': 6
}
application_map = {
    '1st Phase - General Contingent': 1,
    '1st Phase - Special Contingent (Azores Island)': 5,
    '1st Phase - Special Contingent (Madeira Island)': 16,
    '2nd Phase - General Contingent': 17,
    '3rd Phase - General Contingent': 18,
    'Ordinance No. 612/93': 2,
    'Ordinance No. 854-B/99': 10,
    'Ordinance No. 533-A/99, Item B2 (Different Plan)': 26,
    'Ordinance No. 533-A/99, Item B3 (Other Institution)': 27,
    'International Student (Bachelor)': 15,
    'Over 23 Years Old': 39,
    'Transfer': 42,
    'Change of Course': 43,
    'Holders of Other Higher Courses': 7,
    'Short Cycle Diploma Holders': 53,
    'Technological Specialization Diploma Holders': 44,
    'Change of Institution/Course': 51,
    'Change of Institution/Course (International)': 57,
}

# UI
st.title("🎓 Student Graduation Prediction")

with st.form("student_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("Gender", ['Male', 'Female'])
        age = st.number_input("Age at Enrollment", 17, 70, 20)
        marital = st.selectbox("Marital Status", list(marital_map.keys()))
        application = st.selectbox("Application Mode", list(application_map.keys()))
        prev_grade = st.number_input("Previous Qualification Grade", 0, 200)
        admission_grade = st.number_input("Admission Grade", 0, 200)
        scholarship = st.checkbox("Scholarship")
        tuition = st.checkbox("Tuition Up to Date")
        displaced = st.checkbox("Displaced")
        debtor = st.checkbox("Debtor")

    with col2:
        u1_enrolled = st.number_input("1st Sem Enrolled Units", 0, 26)
        u1_approved = st.number_input("1st Sem Approved Units", 0, 26)
        u1_grade = st.number_input("1st Sem Grade", 0, 20)
        u2_enrolled = st.number_input("2nd Sem Enrolled Units", 0, 23)
        u2_eval = st.number_input("2nd Sem Evaluations", 0, 33)
        u2_approved = st.number_input("2nd Sem Approved Units", 0, 20)
        u2_grade = st.number_input("2nd Sem Grade", 0, 20)
        u2_no_eval = st.number_input("2nd Sem No Evaluations", 0, 12)

    submitted = st.form_submit_button("🔍 Predict")

if submitted:
    data = [[
        marital_map[marital], application_map[application], prev_grade,
        admission_grade, int(displaced), int(debtor), int(tuition),
        gender_map[gender], int(scholarship), age,
        u1_enrolled, u1_approved, u1_grade,
        u2_enrolled, u2_eval, u2_approved, u2_grade, u2_no_eval
    ]]

    columns = [
        'Marital_status', 'Application_mode', 'Previous_qualification_grade',
        'Admission_grade', 'Displaced', 'Debtor', 'Tuition_fees_up_to_date',
        'Gender', 'Scholarship_holder', 'Age_at_enrollment',
        'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_approved',
        'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved',
        'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations'
    ]

    input_df = pd.DataFrame(data, columns=columns)
    final_input = preprocess(input_df)
    prediction = model.predict(final_input)[0]

    if prediction == 1:
        st.success("🎓 Prediction: **Graduate**")
    else:
        st.error("📉 Prediction: **Dropout**")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2025 | Developed by <strong>Siti Robiiatul Adawiyyah</strong></p>", unsafe_allow_html=True)
