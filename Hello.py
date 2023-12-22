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

st.sidebar.markdown("[Monthly PM2.5 Levels Over Time](#monthly-pm25-levels-over-time)")
st.sidebar.markdown("[Correlation Between Different Pollutants](#correlation-between-different-pollutants)")

# Main Section 1
st.header('1. Bagaimana distribusi tingkat PM2.5 pada bulan dan tahun berbeda dalam kumpulan data?', anchor='monthly-pm25-levels-over-time')
monthly_pm25 = df.groupby('month_year')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots()
ax.plot(monthly_pm25['month_year'], monthly_pm25['PM2.5'])

# Show one label for every 6 months
labels = ax.get_xticklabels()
selected_labels = [label if i % 6 == 0 else '' for i, label in enumerate(labels)]
ax.set_xticklabels(selected_labels, rotation=45)

plt.title('Monthly PM2.5 Levels Over Time')
plt.tight_layout()

st.pyplot(fig)

# Answer for Question 1
with st.expander('Analisis pertanyaan 1'):
    st.write('Dari line plot yang sudah dibuat, kita dapat melihat bahwa rata-rata tingkat PM2.5 bulanan menunjukkan pola musiman yang jelas, dengan tingkat yang lebih tinggi pada bulan-bulan musim dingin dan tingkat yang lebih rendah pada musim panas. Ada juga tren peningkatan secara umum selama bertahun-tahun, yang menunjukkan bahwa kualitas udara semakin buruk.')

# Main Section 2
st.header('2. Bagaimana tingkat polutan yang berbeda (PM2.5, PM10, SO2, NO2, CO, O3) berkorelasi satu sama lain?', anchor='correlation-between-different-pollutants')
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
corr_matrix = df[pollutants].corr()
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, ax=ax)
st.pyplot(fig)

# Answer for Question 2
with st.expander('Analisis pertanyaan 2'):
    st.write('Dari heatmap yang telah dibuat, terlihat bahwa PM2.5 dan PM10 memiliki korelasi positif yang kuat yang menunjukkan bahwa keduanya cenderung meningkat dan menurun secara bersamaan. Di sisi lain, O3 dan CO memiliki korelasi negatif, menunjukkan bahwa semakin tinggi kadar O3 maka semakin rendah kadar NO2, dan sebaliknya. Korelasi yang paling lemah terdapat pada NO2 dan O3 yang menunjukkan tidak adanya hubungan yang jelas antara kedua polutan tersebut.')