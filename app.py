import streamlit as st
import pandas as pd
import pickle

# --- Modeli yükle ---
with open("catboost_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🌍 Bireysel Karbon Emisyonu Tahmin Aracı")
st.write("Seçilen yaşam alışkanlıklarına göre karbon emisyonunu tahmin eder.")

# --- Kullanıcı girdi arayüzü ---
def user_input():
    data = {
        "Transport": st.selectbox("Transport", ["walk/bicycle", "public", "private"]),
        "Vehicle_Type": st.selectbox("Vehicle Type", ["None", "diesel", "electric", "hybrid", "lpg", "petrol", "public_cost"]),
        "Frequency_of_Traveling_by_Air": st.selectbox("Air Travel", ["never", "rarely", "frequently", "very frequently"]),
        "Heating_Energy_Source": st.selectbox("Heating Source", ["electricity", "natural gas", "wood", "coal"]),
        "Energy_efficiency": st.selectbox("Energy Efficiency", ["Yes", "Sometimes", "No"]),
        "Waste_Bag_Size": st.selectbox("Waste Bag Size", ["small", "medium", "large", "extra large"]),
        "How_Many_New_Clothes_Monthly": st.slider("New Clothes per Month", 0, 20, 2),
        "Diet": st.selectbox("Diet", ["vegan", "vegetarian", "pescatarian", "omnivore"]),
    }
    return pd.DataFrame([data])

df_input = user_input()

# --- Eşik değerler (senin datasetine göre) ---
q33, q66 = 1700, 2483

def segment_emission(value):
    if value < q33:
        return "🟢 Düşük", 0.3
    elif value < q66:
        return "🟡 Orta", 0.65
    else:
        return "🔴 Yüksek", 1.0

# --- Tahmin ve Görselleştirme ---
if st.button("Tahmin Et"):
    prediction = model.predict(df_input)[0]
    segment, ratio = segment_emission(prediction)

    st.metric(label="🌱 Tahmin Edilen Emisyon", value=f"{prediction:.2f}")
    st.metric(label="📊 Segment", value=segment)

    st.write("### Emisyon Seviyesi")
    st.progress(ratio)

