import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data  
def load_data():
    df = pd.read_csv('data/PRSA_Data_Gucheng_20130301-20170228.csv')
    df['wd'] = df['wd'].ffill()
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df['PM2.5'] = pd.to_numeric(df['PM2.5'], errors='coerce')
    df['month_year'] = df['date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Main title
st.title('Air Quality Analysis')

# Sidebar
st.sidebar.title('Air Quality Analysis')

st.sidebar.markdown("[Tingkat PM2.5 Bulanan](#monthly-pm25-levels-over-time)")
st.sidebar.markdown("[Korelasi Antar Polutan](#correlation-between-different-pollutants)")

# Main Section 1
st.header('What is the PM2.5 level distribution like over the months and years?', anchor='monthly-pm25-levels-over-time')
monthly_pm25 = df.groupby('month_year')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots()
ax.plot(monthly_pm25['month_year'], monthly_pm25['PM2.5'])

# Show one label for every 6 months
labels = ax.get_xticklabels()
selected_labels = [label if i % 6 == 0 else '' for i, label in enumerate(labels)]
ax.set_xticklabels(selected_labels, rotation=45)

plt.title('PM2.5 Levels per Month')
plt.tight_layout()

st.pyplot(fig)

# Answer for Question 1
with st.expander('Analysis'):
    st.write('From the line plot, we can see that the average monthly PM2.5 levels show a clear seasonal pattern, with higher levels in the winter months and lower levels in the summer. There has also been a general upward trend over the years, indicating that air quality is getting worse.')

# Main Section 2
st.header('How do the levels of different pollutants (PM2.5, PM10, SO2, NO2, CO, O3) correlate with each other?', anchor='correlation-between-different-pollutants')
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
corr_matrix = df[pollutants].corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, ax=ax)
st.pyplot(fig)

# Answer for Question 2
with st.expander('Analysis'):
    st.write('From the heatmap, we can see that PM2.5 and PM10 have a strong positive correlation, indicating that they tend to increase and decrease simultaneously. On the other hand, O3 and CO have a negative correlation, indicating that the higher the O3 levels, the lower the NO2 levels, and vice versa. The weakest correlation is found in NO2 and O3, which shows that there is no clear relationship between these two pollutants.')