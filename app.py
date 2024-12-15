# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kb5HNex5QkZQY9CkLcAiz_Y0NruyUuga

NAME: SUYOG S. DHANDE
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Step 1: Title and Description
st.title("Hospital Readmission Prediction")
st.write("This application predicts the likelihood of patient readmission based on their medical history and demographics. Upload the dataset and use the sidebar to input patient details for prediction.")

if uploaded_file:
    # Step 3: Load and Display Dataset
    diabetic_data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Dataset:")
    st.dataframe(diabetic_data.head())

    # Step 4: Data Cleaning and Preprocessing
    st.write("### Preprocessing the Data")
    diabetic_data.replace('?', np.nan, inplace=True)
    diabetic_data.fillna(diabetic_data.mode().iloc[0], inplace=True)
    diabetic_data.drop(['encounter_id', 'patient_nbr', 'weight', 'payer_code', 'medical_specialty'], axis=1, inplace=True)

    # Encode categorical variables
    label_encoders = {}
    for column in diabetic_data.select_dtypes(include='object').columns:
        le = LabelEncoder()
        diabetic_data[column] = le.fit_transform(diabetic_data[column])
        label_encoders[column] = le

    st.write("Data cleaned and encoded successfully!")

    # Step 5: Train-Test Split
    X = diabetic_data.drop('readmitted', axis=1)
    y = diabetic_data['readmitted']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 6: Train the Model
    st.write("### Training the Model")
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    st.write("Model trained successfully!")

    # Display model evaluation metrics
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    st.write("### Model Performance Metrics")
    st.write(f"Accuracy: {model.score(X_test, y_test):.2f}")
    st.write(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.2f}")

    # Step 7: User Input for Prediction
    st.sidebar.header("Input Patient Details")
    st.write("### Enter Patient Details for Prediction")
    def user_input_features():
        features = {}
        for col in X.columns:
            if diabetic_data[col].nunique() <= 10:  # Categorical feature
                features[col] = st.sidebar.selectbox(col, diabetic_data[col].unique())
            else:  # Numerical feature
                features[col] = st.sidebar.slider(col, float(X[col].min()), float(X[col].max()), float(X[col].mean()))
        return pd.DataFrame([features])

    input_df = user_input_features()
    st.write("### Input Data for Prediction")
    st.dataframe(input_df)

    # Step 8: Prediction
    if st.button("Predict"):
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)[0][1]
        st.write(f"Prediction: {'Readmitted' if prediction[0] == 1 else 'Not Readmitted'}")
        st.write(f"Probability of Readmission: {probability:.2f}")

        # Display feature importances
        st.write("### Feature Importance")
        feature_importances = pd.Series(model.feature_importances_, index=X.columns)
        st.bar_chart(feature_importances.sort_values(ascending=False))
