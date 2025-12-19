import streamlit as st
import pandas as pd
import joblib
from animations import load_lottiefile, show_full_screen_animation

st.set_page_config(page_title="Cardio AI", layout="centered")

@st.cache_resource
def load_data():
    try:
        model = joblib.load('ml/heart_model.pkl')
        scaler = joblib.load('ml/scaler.pkl')
        return model, scaler
    except FileNotFoundError:
        st.error("Не знайдено файли 'heart_model.pkl' або 'scaler.pkl'.")
        return None, None

lottie_ambulance = load_lottiefile("anim/ambulancia.json")
lottie_healthcare = load_lottiefile("anim/healthCare.json")

model_columns = ['age', 'sex', 'dataset', 'cp', 'trestbps',
                 'chol', 'fbs', 'restecg', 'thalch', 'exang',
                 'oldpeak', 'slope', 'ca', 'thal']

st.title("Cardio AI: Діагностика")
st.markdown("Введіть клінічні показники пацієнта для аналізу ризику.")

model, scaler = load_data()

if model is not None:
    with st.form("medical_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Вік", 20, 100, 50)
            sex_option = st.selectbox("Стать", ["Чоловік", "Жінка"])
            sex = 1 if sex_option == "Чоловік" else 0
            
            cp_map = {"Типова стенокардія": 0, "Атипова стенокардія": 1, "Неангінальний біль": 2, "Безсимптомний": 3}
            cp_label = st.selectbox("Тип болю", list(cp_map.keys()))
            cp = cp_map[cp_label]
            
            trestbps = st.number_input("Тиск (мм рт.ст.)", 90, 220, 120)
            chol = st.number_input("Холестерин (мг/дл)", 100, 600, 200)
            fbs_option = st.selectbox("Цукор натщесерце > 120?", ["Ні", "Так"])
            fbs = 1 if fbs_option == "Так" else 0
            
            restecg_map = {"Норма": 0, "Аномалія ST-T": 1, "Гіпертрофія": 2}
            restecg_label = st.selectbox("ЕКГ спокою", list(restecg_map.keys()))
            restecg = restecg_map[restecg_label]

        with col2:
            thalch = st.number_input("Макс. пульс", 60, 220, 150)
            exang_option = st.selectbox("Стенокардія від навантаження?", ["Ні", "Так"])
            exang = 1 if exang_option == "Так" else 0
            oldpeak = st.number_input("Депресія ST (Oldpeak)", 0.0, 10.0, 0.0, step=0.1)
            
            slope_map = {"Вгору (Upsloping)": 0, "Плоский (Flat)": 1, "Вниз (Downsloping)": 2}
            slope_label = st.selectbox("Нахил ST", list(slope_map.keys()))
            slope = slope_map[slope_label]
            ca = st.slider("Кількість судин (0-3)", 0, 3, 0)
            thal_map = {"Невідомо/Інше": 0, "Норма": 1, "Фіксований дефект": 2, "Оборотний дефект": 3}
            thal_label = st.selectbox("Таласемія", list(thal_map.keys()))
            thal = thal_map[thal_label]

        submit = st.form_submit_button("🔍 Отримати прогноз", type="primary")

    if submit:
        input_dict = {
            'age': age, 'sex': sex, 'dataset': 1, 'cp': cp,
            'trestbps': trestbps, 'chol': chol, 'fbs': fbs,
            'restecg': restecg, 'thalch': thalch, 'exang': exang,
            'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
        }
        
        df_input = pd.DataFrame([input_dict])
        df_input = df_input[model_columns]

        try:
            X_scaled = scaler.transform(df_input)
            prediction = model.predict(X_scaled)[0]
            probability = model.predict_proba(X_scaled)[0][1]

            st.divider()

            if probability < 0.50:
                st.success("✅ Чудовий результат!")
                st.metric("Ймовірність хвороби", f"{probability:.1%}")
                st.write("Показники в нормі.")
                st.balloons()

            elif probability < 0.80:
                st.warning("⚠️ Середній ризик")
                st.metric("Ймовірність хвороби", f"{probability:.1%}")
                st.write("Слідкуйте за здоров'ям та консультуйтесь з лікарем при погіршенні показників.")
                if lottie_healthcare:
                    show_full_screen_animation(lottie_healthcare, centered=True)

            else:
                st.error("🚨 Високий ризик!")
                st.metric("Ймовірність хвороби", f"{probability:.1%}")
                st.write("Негайно зверніться до лікаря.")
                if lottie_ambulance:
                    show_full_screen_animation(lottie_ambulance, direction="left-to-right")

        except Exception as e:
            st.error(f"Помилка при розрахунку: {e}")
