import streamlit as st
import datetime

st.set_page_config(page_title="Mobile Recharge Ledger", layout="centered")

# Initialize session state
if "ledger" not in st.session_state:
    st.session_state.ledger = {}

def add_user(mobile_number, initial_balance):
    ledger = st.session_state.ledger
    if mobile_number not in ledger:
        ledger[mobile_number] = {
            "balance": initial_balance,
            "history": []
        }
        st.success(f"User {mobile_number} added with balance ₹{initial_balance}")
    else:
        st.warning("User already exists!")

def recharge(mobile_number, amount):
    ledger = st.session_state.ledger
    if mobile_number in ledger:
        ledger[mobile_number]["balance"] += amount
        ledger[mobile_number]["history"].append({
            "type": "Recharge",
            "amount": amount,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(f"Recharged ₹{amount} to {mobile_number}. New balance: ₹{ledger[mobile_number]['balance']}")
    else:
        st.error("Mobile number not found!")

def deduct_balance(mobile_number, amount, reason):
    ledger = st.session_state.ledger
    if mobile_number in ledger:
        if ledger[mobile_number]["balance"] >= amount:
            ledger[mobile_number]["balance"] -= amount
            ledger[mobile_number]["history"].append({
                "type": "Deduction",
                "amount": amount,
                "reason": reason,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success(f"Deducted ₹{amount} for {reason}. New balance: ₹{ledger[mobile_number]['balance']}")
        else:
            st.warning("Insufficient balance!")
    else:
        st.error("Mobile number not found!")

def show_ledger(mobile_number):
    ledger = st.session_state.ledger
    if mobile_number in ledger:
        st.subheader(f"Ledger for {mobile_number}")
        st.write(f"**Current Balance:** ₹{ledger[mobile_number]['balance']}")
        st.markdown("---")
        for entry in reversed(ledger[mobile_number]["history"]):
            if entry["type"] == "Recharge":
                st.write(f"🟢 {entry['date']} | Recharge | +₹{entry['amount']}")
            else:
                st.write(f"🔴 {entry['date']} | Deduction | -₹{entry['amount']} | Reason: {entry['reason']}")
    else:
        st.error("Mobile number not found!")

# Streamlit UI
st.title("📱 Mobile Recharge Ledger")

tab1, tab2, tab3, tab4 = st.tabs(["Add User", "Recharge", "Deduct Balance", "View Ledger"])

with tab1:
    st.header("➕ Add New User")
    mobile = st.text_input("Enter Mobile Number", key="add_mobile")
    initial_balance = st.number_input("Initial Balance (₹)", min_value=0, step=1, key="init_bal")
    if st.button("Add User"):
        if mobile.strip():
            add_user(mobile.strip(), initial_balance)
        else:
            st.warning("Enter a valid mobile number.")

with tab2:
    st.header("🔋 Recharge")
    mobile = st.text_input("Enter Mobile Number", key="recharge_mobile")
    amount = st.number_input("Recharge Amount (₹)", min_value=1, step=1, key="recharge_amt")
    if st.button("Recharge"):
        if mobile.strip():
            recharge(mobile.strip(), amount)
        else:
            st.warning("Enter a valid mobile number.")

with tab3:
    st.header("💸 Deduct Balance")
    mobile = st.text_input("Enter Mobile Number", key="deduct_mobile")
    amount = st.number_input("Deduction Amount (₹)", min_value=1, step=1, key="deduct_amt")
    reason = st.text_input("Reason", key="deduct_reason")
    if st.button("Deduct"):
        if mobile.strip():
            deduct_balance(mobile.strip(), amount, reason if reason else "Usage")
        else:
            st.warning("Enter a valid mobile number.")

with tab4:
    st.header("📄 View Ledger")
    mobile = st.text_input("Enter Mobile Number", key="ledger_mobile")
    if st.button("Show Ledger"):
        if mobile.strip():
            show_ledger(mobile.strip())
        else:
            st.warning("Enter a valid mobile number.")
