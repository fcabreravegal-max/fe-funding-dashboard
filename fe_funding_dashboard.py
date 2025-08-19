
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fossil East Funding Dashboard", layout="wide")

st.title("📊 Fossil East Weekly Funding Dashboard")

# --- Input: Load data ---
@st.cache_data
def load_data():
    funding = {
        'Week 33': 3846532.96,
        'Week 34': 2573307.29,
        'Week 35': 7400115.44,
        'Week 36': 6394681.15
    }
    cash = {
        'Fossil India': 3604544.06,
        'Mexico': 3043151.43,
        'USA': 3518904.48,
        'Canada': 2783539.54,
        'Germany': 2167734.07
    }
    ic_ap = {'Fossil India': 9952350.11}
    return funding, cash, ic_ap

funding_needs, available_cash, interco_ap = load_data()

# --- Week Selection ---
selected_week = st.selectbox("Select Week", list(funding_needs.keys()))
need = funding_needs[selected_week]
st.metric(label="Fossil East Funding Need", value=f"${need:,.2f}")

# --- Strategy Selection ---
st.subheader("💡 Choose Funding Sources")

use_ic_ap = st.checkbox("Use Intercompany AP Offset from India ($9.95M)", value=True)
selected_sources = st.multiselect(
    "Select Entities to Fund via Cash Transfer",
    options=list(available_cash.keys()),
    default=["Fossil India", "Mexico"]
)

# --- Allocation Simulation ---
remaining = need
funding_details = []

if use_ic_ap and interco_ap["Fossil India"] > 0:
    ic_ap_used = min(interco_ap["Fossil India"], remaining)
    funding_details.append(("Fossil India (IC AP)", ic_ap_used))
    remaining -= ic_ap_used

for entity in selected_sources:
    if remaining <= 0:
        break
    cash_available = available_cash.get(entity, 0)
    amount = min(cash_available, remaining)
    funding_details.append((f"{entity} (Cash)", amount))
    remaining -= amount

# --- Results ---
st.subheader("🧾 Funding Breakdown")

df = pd.DataFrame(funding_details, columns=["Source", "Amount (USD)"])
df["Amount (USD)"] = df["Amount (USD)"].map("${:,.2f}".format)
st.dataframe(df, use_container_width=True)

st.metric(label="Remaining Unfunded", value=f"${remaining:,.2f}")
