import streamlit as st
import pandas as pd

st.image('images/black-logo.png')


st.markdown("### Data Docs​​")

st.markdown(
"""
This page serves as a documentation hub, offering insights into the underlying structure and data driving our application. From an entity-relationship diagram illustrating the database schema to a peek into the raw data powering the visualizations showcased on the page, this documentation provides a comprehensive overview of the system's architecture and the rich dataset at its core. By understanding these foundational elements, users can gain a deeper appreciation for the application's functionality and the data-driven insights it delivers.
"""
)

st.markdown("""#### ER diagram of the database""")
st.image("images/bloomstar_diagram.png")

st.markdown("#### Data")
st.markdown("- Customers table")
st.dataframe(pd.read_csv("data/customers.csv"))
st.markdown("- Flowers table")
st.dataframe(pd.read_csv("data/flowers.csv"))
st.markdown("- Orders table")
st.dataframe(pd.read_csv("data/orders.csv"))
st.markdown("- Shipments table")
st.dataframe(pd.read_csv("data/shipments.csv"))

st.markdown("#### Views")
st.markdown("- Flowers Type Damage")
st.dataframe(pd.read_csv("views/flowers_type_damage.csv"))
st.markdown("- Order Flowers")
st.dataframe(pd.read_csv("views/orders_flowers.csv"))
st.markdown("- Shipment Flowers")
st.dataframe(pd.read_csv("views/shipments_flowers.csv"))