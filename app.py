import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('diabetes_model.joblib')  # Make sure this file exists

# App title
st.title("Diabetes Prediction App 🩺")
st.markdown("Enter patient details to predict diabetes risk:")

# Input form
with st.form("patient_details"):
    col1, col2 = st.columns(2)
    
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
        glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=100)
        blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=70)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
    
    with col2:
        insulin = st.number_input("Insulin (IU/mL)", min_value=0, max_value=1000, value=80)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0, step=0.1)
        diabetes_pedigree = st.number_input("Diabetes Pedigree", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    
    submit_button = st.form_submit_button("Predict Diabetes")

# Prediction logic
if submit_button:
    # Create input DataFrame (must match training data features EXACTLY)
    input_data = pd.DataFrame({
        'Pregnancies': [pregnancies],
        'Glucose': [glucose],
        'BloodPressure': [blood_pressure],
        'SkinThickness': [skin_thickness],
        'Insulin': [insulin],
        'BMI': [bmi],
        'DiabetesPedigreeFunction': [diabetes_pedigree],
        'Age': [age]
    })
    
    # Predict
    try:
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0][1] * 100  # Probability of diabetes
        
        # Display results
        st.subheader("Prediction Result")
        if prediction == 1:
            st.error(f"⚠️ High Risk of Diabetes ({proba:.1f}% probability)")
            st.warning("Consult a doctor for further evaluation")
        else:
            st.success(f"✅ Low Risk of Diabetes ({proba:.1f}% probability)")
            st.balloons()
            
        # Show interpretation
        st.markdown("**Interpretation:**")
        if proba < 30:
            st.info("Healthy range - maintain current lifestyle")
        elif proba < 70:
            st.warning("Moderate risk - consider lifestyle changes")
        else:
            st.error("High risk - medical consultation recommended")
            
    except Exception as e:
        st.error(f"Prediction failed: {str(e)}")

# Add some info
st.sidebar.markdown("""
**About this app:**
- Predicts diabetes risk using logistic regression
- Trained on Pima Indians Diabetes Dataset
- For educational purposes only
""")