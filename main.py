import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Fraud Detection", layout="centered")

st.title("Fraud Transaction Risk Assessment")

model = joblib.load("fraud_voting_model.joblib")
encoder = joblib.load("type_encoder.joblib")

step = st.number_input("Step (hour)", min_value=0, value=350)
amount = st.number_input("Transaction Amount", min_value=0.0, value=180000.0)

oldbalanceOrg = st.number_input("Old Balance (Origin)", min_value=0.0, value=185000.0)
newbalanceOrig = st.number_input("New Balance (Origin)", min_value=0.0, value=5000.0)

oldbalanceDest = st.number_input("Old Balance (Destination)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Destination)", min_value=0.0, value=180000.0)

transaction_type = st.selectbox(
    "Transaction Type",
    ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"],
    index=4
)

deltaOrig = oldbalanceOrg - newbalanceOrig
deltaDest = newbalanceDest - oldbalanceDest
log_amount = np.log1p(amount)

type_encoded = encoder.transform(
    pd.DataFrame({"type": [transaction_type]})
)[0][0]


input_df = pd.DataFrame([{
    "step": step,
    "type": type_encoded,
    "amount": amount,
    "oldbalanceOrg": oldbalanceOrg,
    "newbalanceOrig": newbalanceOrig,
    "oldbalanceDest": oldbalanceDest,
    "newbalanceDest": newbalanceDest,
    "isFlaggedFraud": 0,
    "isMerchantDest": 0,
    "deltaOrig": deltaOrig,
    "deltaDest": deltaDest,
    "log_amount": log_amount
}])

if st.button("Assess Risk"):
    prob = model.predict_proba(input_df)[0][1]

    st.subheader(f"Fraud Risk Score: {prob:.2f}")

    if prob >= 0.6:
        st.error("HIGH RISK TRANSACTION")
    elif prob >= 0.3:
        st.warning("MEDIUM RISK TRANSACTION")
    else:
        st.success("LOW RISK TRANSACTION")

    with st.expander("Input Features"):
        st.write(input_df)
