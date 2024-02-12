import streamlit as st
import pandas as pd
import plotly.express as px

st.image('images/black-logo.png')


st.markdown("### ShipTrack")

st.markdown(
"""
Flowers and glowers are highly perishable products that require specific conditions to maintain their freshness and must reach the end consumer as quickly as possible to maximize both customer satisfaction and company profits. In this application, **ShipTrack**, we provide a preliminary analysis based on test data, showing the quantity of product received and calculating average losses incurred by the time it spends in storage without being sold, using a simple linear test function. Additionally, we display upcoming orders for our product. This analysis represents just the initial scope of what could evolve into effective monitoring of product inflows and outflows, aimed at minimizing losses and boosting sales campaigns.
"""
)


# ======== Data manipulation ========

shipments_flowers = pd.read_csv('views/shipments_flowers.csv')
type_damage = pd.read_csv('views/flowers_type_damage.csv')
orders_flowers = pd.read_csv('views/orders_flowers.csv')

# Set datetime types 

shipments_flowers.shipment_date = pd.to_datetime(shipments_flowers.shipment_date).dt.date
orders_flowers.order_date = pd.to_datetime(orders_flowers.order_date).dt.date

# Additional variables 

orders_flowers['total_cost'] = orders_flowers.quantity * orders_flowers.cost_cad



# chart_2
chart_2 = orders_flowers[['order_date', 'total_cost']
                         ].groupby(['order_date']).sum().reset_index()


# chart_4 
chart_4 = shipments_flowers[['shipment_date', 'inventory_gross_value', 'money_lost_damage']
                            ].groupby(['shipment_date']).sum().reset_index()
chart_4['not_lost_money'] = chart_4.inventory_gross_value - chart_4.money_lost_damage
side_a = chart_4.set_index('shipment_date')['money_lost_damage'].to_frame().rename(columns = {'money_lost_damage': 'money'}).reset_index()
side_a['money_status'] = 'lost'
side_b = chart_4.set_index('shipment_date')['not_lost_money'].to_frame().rename(columns = {'not_lost_money': 'money'}).reset_index()
side_b['money_status'] = 'not_lost'
refactory_chart_4 = [side_a, side_b]
chart_4a = pd.concat(refactory_chart_4)

# chart_5
type_damage['quantity_damage'] = type_damage.quantity - type_damage.quantity_no_damage
side_a1 = type_damage.set_index('flower_name')['quantity_no_damage'].to_frame().rename(columns={'quantity_no_damage':'quantity'}).reset_index()
side_a1['flower_status'] = 'not_lost'
side_b1 = type_damage.set_index('flower_name')['quantity_damage'].to_frame().rename(columns={'quantity_damage':'quantity'}).reset_index()
side_b1['flower_status'] = 'lost'
refactory_chart_5 = [side_b1, side_a1]
chart_5 = pd.concat(refactory_chart_5)


# ========= Plotly charts ===========
fig_2 = px.bar(chart_2, x='order_date', y='total_cost', 
               color_discrete_sequence=px.colors.qualitative.Light24)
fig_2.update_traces(marker_color=px.colors.qualitative.Light24[1])
fig_2.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                            ))
fig_4 = px.bar(chart_4a, x='shipment_date', y='money', color='money_status',
               color_discrete_sequence=px.colors.qualitative.Light24)
fig_4.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                            ))

fig_5 = px.bar(chart_5, x='quantity', y='flower_name', color='flower_status',
               color_discrete_sequence=px.colors.qualitative.Light24)
fig_5.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                            ))
# ========= Display in streamlit =======

st.divider()

st.markdown("#### First, how much product is damaged? ")

# st.plotly_chart(fig_2)
st.markdown("- Damage to the product measured by the daily shipments received in terms of money (CAD).")
st.plotly_chart(fig_4, use_container_width=True)
st.markdown("- Damage to the product measured by the types of flowers in terms of money (CAD).")
st.plotly_chart(fig_5, use_container_width=True)

st.markdown("#### Total balance CAD")
col1, col2 = st.columns(2)

total_investment = shipments_flowers.inventory_gross_value.sum()
total_lost = round(shipments_flowers.money_lost_damage.sum())



with col1:
    st.markdown("Total Investment")
    st.markdown(f"### ${total_investment:,}")

with col2:
    st.markdown("Average Losses by Damage")
    st.markdown(f"### ${total_lost:,}")

st.divider()
# ========== Display in streamlit ==========

st.markdown("#### Now lets see our orders and shipping by flower type")

flower = st.multiselect('Select a flower type',
                      ['alstromelia', 
                       'bouquet_rose_white', 
                       'bouquet_rose_red', 
                       'bouquet_rose_yellow',
                       'bouquet_rose_orange', 
                       'pom', 
                       'tulip', 
                       'hydrangea', 
                       'carnation', 
                       'minicarnation',
                       'spiders', 
                       'spray rose', 
                       'gypsophilia'])

# ========== More data Manipulation =========

# chart_1 
chart_1 = orders_flowers[['order_date', 'flower_name', 'quantity']
                         ].groupby(['order_date', 'flower_name']).sum().reset_index()

chart_1 = chart_1[chart_1.flower_name.isin(flower)]

# chart_3 
chart_3 = shipments_flowers[['shipment_date', 'flower_name', 'quantity']
                            ].groupby(['shipment_date', 'flower_name']).sum().reset_index()
chart_3 = chart_3[chart_3.flower_name.isin(flower)]

fig_1 = px.bar(chart_1, x='order_date', y='quantity', color='flower_name', 
               color_discrete_sequence=px.colors.qualitative.Light24)
fig_1.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                            ))

fig_3 = px.bar(chart_3, x='shipment_date', y='quantity', color='flower_name', 
               color_discrete_sequence=px.colors.qualitative.Light24)
fig_3.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                            ))

# ========= Display in streamlit ==========

st.markdown("- Orders of flower bouquets and glowers measured by the quantity of bouquets to be delivered.")
st.plotly_chart(fig_1, use_container_width=True)
st.markdown("- Shipments received of flower bouquets and glowers measured by the quantity of bouquets received.")
st.plotly_chart(fig_3, use_container_width=True)