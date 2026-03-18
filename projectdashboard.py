import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Hi Britto ❤ ^_^ ", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
    <style>
    .main {
        background-color: #FF0000;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title(" Student Analytics Dashboard")

# ---------------- LOAD DATA ----------------
file = "REEDITED STUDENT DETAILS.xlsx"

sheet1 = pd.read_excel(file, sheet_name=0)
sheet2 = pd.read_excel(file, sheet_name=1)

sheet1.columns = sheet1.columns.str.strip()
sheet2.columns = sheet2.columns.str.strip()

# ---------------- DATE FIX ----------------
sheet2['JOD'] = pd.to_datetime(sheet2['JOD'], dayfirst=True)
sheet2 = sheet2.sort_values('JOD')
sheet2['MonthYear'] = sheet2['JOD'].dt.strftime('%b %Y')

# ---------------- KPI ----------------
total_students = len(sheet1)
total_revenue = sheet2['Fee'].sum()
avg_fee = sheet2['Fee'].mean()

col1, col2, col3 = st.columns(3)

col1.metric(" Students", total_students)
col2.metric(" Revenue", f"₹ {total_revenue}")
col3.metric(" Avg Fee", f"₹ {round(avg_fee,2)}")

st.divider()

# ---------------- REVENUE TREND ----------------
st.subheader(" Monthly Revenue Trend")

rev = sheet2.groupby('MonthYear')['Fee'].sum().reset_index()

fig1 = px.line(
    rev, x='MonthYear', y='Fee',
    markers=True,
    color_discrete_sequence=['#00FFAA']
)

fig1.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- COURSE ANALYSIS ----------------
st.subheader(" Course Distribution")

course_count = sheet1['Course'].value_counts().reset_index()
course_count.columns = ['Course', 'Count']

fig2 = px.bar(
    course_count,
    x='Course',
    y='Count',
    text='Count',
    color='Course',
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig2.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- TRAINER ----------------
if 'Trainer' in sheet1.columns:
    st.subheader("Trainer Performance")

    trainer_count = sheet1['Trainer'].value_counts().reset_index()
    trainer_count.columns = ['Trainer', 'Count']

    fig3 = px.bar(
        trainer_count,
        x='Trainer',
        y='Count',
        text='Count',
        color='Trainer',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig3.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- TIMING ----------------
if 'Timing' in sheet1.columns:
    st.subheader(" Peak Timing")

    timing_count = sheet1['Timing'].value_counts().reset_index()
    timing_count.columns = ['Timing', 'Count']

    fig4 = px.bar(
        timing_count,
        x='Timing',
        y='Count',
        text='Count',
        color='Timing',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig4.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.subheader(" Revenue Forecast (Smoothed)")

# ---------------- PREPARE DATA ----------------
sheet2['Fee'] = pd.to_numeric(sheet2['Fee'], errors='coerce')
sheet2 = sheet2.dropna(subset=['Fee'])

sheet2['JOD'] = pd.to_datetime(sheet2['JOD'], dayfirst=True)

# Monthly revenue
sheet2['MonthYear'] = sheet2['JOD'].dt.to_period('M')
monthly = sheet2.groupby('MonthYear')['Fee'].sum().reset_index()

# Convert to datetime for plotting
monthly['MonthYear'] = monthly['MonthYear'].astype(str)

# ---------------- SMOOTHING ----------------
monthly['Smoothed'] = monthly['Fee'].rolling(window=2).mean()

# Fill first value
monthly['Smoothed'].fillna(monthly['Fee'], inplace=True)

# ---------------- FORECAST ----------------
last_value = monthly['Smoothed'].iloc[-1]

# simple future forecast (flat + slight growth)
forecast = [last_value * (1 + 0.05*i) for i in range(1,4)]

# Future months
import pandas as pd
future_months = pd.period_range(
    start=pd.Period(monthly['MonthYear'].iloc[-1]) + 1,
    periods=3,
    freq='M'
).astype(str)

# ---------------- PLOT ----------------
import plotly.graph_objects as go

fig = go.Figure()

# Actual
fig.add_trace(go.Scatter(
    x=monthly['MonthYear'],
    y=monthly['Fee'],
    mode='lines+markers',
    name='Actual',
    line=dict(color='#00FFAA')
))

# Smoothed
fig.add_trace(go.Scatter(
    x=monthly['MonthYear'],
    y=monthly['Smoothed'],
    mode='lines',
    name='Trend',
    line=dict(color='#FFD700', dash='dash')
))

# Forecast
fig.add_trace(go.Scatter(
    x=future_months,
    y=forecast,
    mode='lines+markers',
    name='Forecast',
    line=dict(color='#FF4B4B')
))

fig.update_layout(
    title=" Revenue Forecast (Smoothed Trend)",
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- OUTPUT ----------------
forecast_df = pd.DataFrame({
    "Month": future_months,
    "Forecast Revenue": forecast
})

st.write(" Forecasted Revenue:")
st.dataframe(forecast_df)





st.subheader("Course Analysis")

sheet3 = pd.read_excel(file, sheet_name="Sheet3")
st.write(sheet3.columns)

st.subheader(" Student Type Distribution (Sheet3)")

# Count values (ignore empty cells)
new_count = sheet3['New Joiner'].count()
repeat_count = sheet3['Repeated students'].count()
ref_count = sheet3['Reference Student'].count()

# Create dataframe
import pandas as pd

counts = pd.DataFrame({
    'Type': ['New', 'Repeated', 'Reference'],
    'Count': [new_count, repeat_count, ref_count]
})

# ---------------- CHART ----------------
import plotly.express as px

fig = px.pie(
    counts,
    names='Type',
    values='Count',
    color='Type',
    color_discrete_map={
        'New': '#3399FF',
        'Repeated': '#FF4B4B',
        'Reference': '#00FFAA'
    },
    title="Student Distribution - Sheet3"
)

fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)












st.subheader("Intern Analysis")

sheet4 = pd.read_excel(file, sheet_name="Sheet4")
st.write(sheet4.columns)


new_count = sheet4['New Joiner'].count()
repeat_count = sheet4['Repeated students'].count()
ref_count = sheet4['Reference Student'].count()


counts = pd.DataFrame({
     'Type': ['New', 'Repeated', 'Reference'],
    'Count': [new_count, repeat_count, ref_count]
})
fig = px.pie(
    counts,
    names='Type',
    values='Count',
    color='Type',
    color_discrete_map={
        'New': '#3399FF',
        'Repeated': '#FF4B4B',
        'Reference': '#00FFAA'
    },
    title="Student Distribution - Sheet4"
)


fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)







