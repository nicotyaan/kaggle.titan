import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Titanic Dashboard", layout="wide")

st.title("🚢 Titanic Survival Dashboard")

# -------------------------
# データ読み込み
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
    )
    return df

df = load_data()

# -------------------------
# サイドバー（フィルター）
# -------------------------
st.sidebar.header("Filter Options")

selected_sex = st.sidebar.multiselect(
    "Select Sex",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)

selected_class = st.sidebar.multiselect(
    "Select Passenger Class",
    options=df["Pclass"].unique(),
    default=df["Pclass"].unique()
)

filtered_df = df[
    (df["Sex"].isin(selected_sex)) &
    (df["Pclass"].isin(selected_class))
]

# -------------------------
# KPI表示
# -------------------------
col1, col2, col3 = st.columns(3)

survival_rate = filtered_df["Survived"].mean()
total_passengers = len(filtered_df)
avg_age = filtered_df["Age"].mean()

col1.metric("Total Passengers", total_passengers)
col2.metric("Survival Rate", f"{survival_rate:.2%}")
col3.metric("Average Age", f"{avg_age:.1f}")

st.divider()

# -------------------------
# Survival Rate by Sex
# -------------------------
st.subheader("Survival Rate by Sex")

sex_chart = alt.Chart(filtered_df).mark_bar().encode(
    x="Sex:N",
    y="mean(Survived):Q",
    color="Sex:N",
    tooltip=["Sex", alt.Tooltip("mean(Survived):Q", format=".2%")]
).properties(height=400)

st.altair_chart(sex_chart, use_container_width=True)

# -------------------------
# Age Distribution
# -------------------------
st.subheader("Age Distribution")

age_hist = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Age:Q", bin=alt.Bin(maxbins=30)),
    y="count()",
    color="Survived:N",
    tooltip=["count()"]
).properties(height=400)

st.altair_chart(age_hist, use_container_width=True)

# -------------------------
# Heatmap (Pclass × Sex)
# -------------------------
st.subheader("Survival Rate by Class and Sex")

heatmap = alt.Chart(filtered_df).mark_rect().encode(
    x="Pclass:O",
    y="Sex:N",
    color=alt.Color("mean(Survived):Q", scale=alt.Scale(scheme="blues")),
    tooltip=["Pclass", "Sex", alt.Tooltip("mean(Survived):Q", format=".2%")]
).properties(height=400)

st.altair_chart(heatmap, use_container_width=True)

# -------------------------
# Raw Data Toggle
# -------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)