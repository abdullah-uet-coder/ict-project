import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(
    page_title="AutoCareIQ",
    page_icon="🚗",
    layout="wide"
)

CSV_FILE = "vehicles.csv"

# Create CSV if missing
if not os.path.exists(CSV_FILE):
    pd.DataFrame(
        columns=["Owner", "Vehicle", "Year", "Mileage"]
    ).to_csv(CSV_FILE, index=False)

st.title("🚗 AutoCareIQ")
st.caption("Smart Vehicle Health & Maintenance Management System")

tab1, tab2, tab3, tab4 = st.tabs([
    "Vehicle Profile",
    "Health & Maintenance",
    "Expenses",
    "Saved Vehicles"
])

# ----------------------------
# TAB 1
# ----------------------------
with tab1:

    st.header("Vehicle Registration")

    owner = st.text_input("Owner Name")

    vehicle = st.text_input("Vehicle Name")

    year = st.number_input(
        "Model Year",
        min_value=1990,
        max_value=datetime.now().year,
        value=2020
    )

    mileage = st.number_input(
        "Current Mileage",
        min_value=0,
        value=50000
    )

    if st.button("Save Vehicle"):

        new_data = pd.DataFrame({
            "Owner": [owner],
            "Vehicle": [vehicle],
            "Year": [year],
            "Mileage": [mileage]
        })

        existing = pd.read_csv(CSV_FILE)

        updated = pd.concat(
            [existing, new_data],
            ignore_index=True
        )

        updated.to_csv(CSV_FILE, index=False)

        st.success("Vehicle Saved Successfully!")

# ----------------------------
# TAB 2
# ----------------------------
with tab2:

    st.header("Vehicle Health Analysis")

    vehicle_age = datetime.now().year - year

    health_score = (
        100
        - (vehicle_age * 2)
        - (mileage / 10000)
    )

    health_score = max(0, health_score)

    st.metric(
        "Health Score",
        f"{health_score:.0f}/100"
    )

    if health_score >= 80:
        st.success("Excellent Condition")
    elif health_score >= 60:
        st.warning("Fair Condition")
    else:
        st.error("Poor Condition")

    st.subheader("Maintenance Reminder")

    last_oil_change = st.number_input(
        "Mileage at Last Oil Change",
        min_value=0,
        value=45000
    )

    service_gap = mileage - last_oil_change

    st.write(
        f"Distance Since Service: {service_gap:,} km"
    )

    if service_gap >= 5000:
        st.error("⚠ Oil Change Required")
    else:
        st.success("✅ Oil Change OK")

    st.subheader("Breakdown Risk")

    battery_age = st.slider(
        "Battery Age (Years)",
        0, 10, 2
    )

    tire_age = st.slider(
        "Tire Age (Years)",
        0, 10, 3
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        risk = "High" if battery_age > 3 else "Low"
        st.metric("Battery Risk", risk)

    with col2:
        risk = "High" if tire_age > 5 else "Low"
        st.metric("Tire Risk", risk)

    with col3:
        risk = "High" if mileage > 100000 else "Low"
        st.metric("Engine Risk", risk)

# ----------------------------
# TAB 3
# ----------------------------
with tab3:

    st.header("Expense Dashboard")

    fuel = st.number_input(
        "Fuel Cost (PKR)",
        min_value=0,
        value=10000
    )

    maintenance = st.number_input(
        "Maintenance Cost (PKR)",
        min_value=0,
        value=5000
    )

    repair = st.number_input(
        "Repair Cost (PKR)",
        min_value=0,
        value=2000
    )

    total = fuel + maintenance + repair

    st.metric(
        "Total Expense",
        f"PKR {total:,.0f}"
    )

    expense_df = pd.DataFrame({
        "Category": [
            "Fuel",
            "Maintenance",
            "Repair"
        ],
        "Cost": [
            fuel,
            maintenance,
            repair
        ]
    })

    fig = px.pie(
        expense_df,
        names="Category",
        values="Cost",
        title="Expense Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# TAB 4
# ----------------------------
with tab4:

    st.header("Saved Vehicles")

    data = pd.read_csv(CSV_FILE)

    st.dataframe(
        data,
        use_container_width=True
    )

    st.write(
        f"Total Vehicles Registered: {len(data)}"
    )
