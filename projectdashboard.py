import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Hi Britto ❤ ^_^ ", layout="wide")


st.markdown("""
    <style>
    .main {
        background-color: #FF0000;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


st.title(" Student Analytics Dashboard")


file = "REEDITED STUDENT DETAILS.xlsx"

sheet1 = pd.read_excel(file, sheet_name=0)
sheet2 = pd.read_excel(file, sheet_name=1)

sheet1.columns = sheet1.columns.str.strip()
sheet2.columns = sheet2.columns.str.strip()





sheet2['JOD'] = pd.to_datetime(sheet2['JOD'], dayfirst=True)
sheet2 = sheet2.sort_values('JOD')
sheet2['MonthYear'] = sheet2['JOD'].dt.strftime('%b %Y')


total_students = len(sheet1)

total_courses = sheet1['Course'].nunique()






total_students = len(sheet1)

total_courses = sheet1['Course'].nunique()


col1, col2, col3 = st.columns(3)

col1.metric("Students", total_students)
col2.metric(" Courses", total_courses)



sheet2['MonthYear'] = sheet2['JOD'].dt.to_period('M')
rev = sheet2.groupby('MonthYear')['Fee'].sum().reset_index()
rev['MonthYear'] = rev['MonthYear'].astype(str)


fig1 = px.line(
    rev,   
    x='MonthYear',
    y='Fee',
    markers=True,
    color_discrete_sequence=['#00FFAA']
)

fig1.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)
fig1.update_traces(line=dict(width=3))

st.plotly_chart(fig1, use_container_width=True)
















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


sheet2['Fee'] = pd.to_numeric(sheet2['Fee'], errors='coerce')
sheet2 = sheet2.dropna(subset=['Fee'])

sheet2['JOD'] = pd.to_datetime(sheet2['JOD'], dayfirst=True)


sheet2['MonthYear'] = sheet2['JOD'].dt.to_period('M')
monthly = sheet2.groupby('MonthYear')['Fee'].sum().reset_index()


monthly['MonthYear'] = monthly['MonthYear'].astype(str)


monthly['Smoothed'] = monthly['Fee'].rolling(window=2).mean()


monthly['Smoothed'].fillna(monthly['Fee'], inplace=True)


last_value = monthly['Smoothed'].iloc[-1]


forecast = [last_value * (1 + 0.05*i) for i in range(1,4)]


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


new_count = sheet3['New Joiner'].count()
repeat_count = sheet3['Repeated students'].count()
ref_count = sheet3['Reference Student'].count()

import pandas as pd

counts = pd.DataFrame({
    'Type': ['New', 'Repeated', 'Reference'],
    'Count': [new_count, repeat_count, ref_count]
})




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







