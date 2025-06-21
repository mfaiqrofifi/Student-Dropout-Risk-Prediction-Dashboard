import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

model = joblib.load("model_xgboost_dropout.joblib")

st.set_page_config(page_title="Prediksi Dropout Mahasiswa", layout="wide")
st.title("Sistem Prediksi Risiko Dropout Mahasiswa")
st.markdown("Masukkan data lengkap mahasiswa untuk mengetahui kemungkinan dropout berdasarkan faktor akademik dan sosial.")

with st.sidebar:
    st.header("Keterangan Fitur")
    st.markdown("- 1 = Ya / Lunas / Pria \n- 0 = Tidak / Belum Lunas / Wanita")
    st.markdown("Semua input numerik dapat disesuaikan berdasarkan informasi mahasiswa.")

with st.form("prediction_form"):
    st.subheader("1. Data Pribadi & Sosial")
    col1, col2, col3 = st.columns(3)
    with col1:
        marital_status = st.selectbox("Status Pernikahan", options=[1, 2, 3], format_func=lambda x: {1: "Single", 2: "Married", 3: "Divorced"}.get(x))
        gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: "Pria" if x==1 else "Wanita")
        age_enroll = st.number_input("Usia Saat Mendaftar", min_value=15, max_value=70, value=18)
        nacionality = st.selectbox("Kebangsaan", options=[1, 2, 3])
    with col2:
        mothers_occupation = st.selectbox("Pekerjaan Ibu", options=[0, 1, 2, 3])
        fathers_occupation = st.selectbox("Pekerjaan Ayah", options=[0, 1, 2, 3])
        mothers_qualification = st.selectbox("Pendidikan Ibu", options=[1, 2, 3])
        fathers_qualification = st.selectbox("Pendidikan Ayah", options=[1, 2, 3])
    with col3:
        scholarship = st.selectbox("Penerima Beasiswa", options=[0, 1])
        displaced = st.selectbox("Mahasiswa Terpindahkan", options=[0, 1])
        special_needs = st.selectbox("Kebutuhan Khusus", options=[0, 1])
        international = st.selectbox("Mahasiswa Internasional", options=[0, 1])

    st.subheader("2. Akademik & Keuangan")
    col4, col5, col6 = st.columns(3)
    with col4:
        application_mode = st.selectbox("Mode Aplikasi", options=[1, 2, 3, 4, 5, 6])
        application_order = st.number_input("Urutan Pilihan Program Studi", min_value=1, max_value=20, value=1)
        admission_grade = st.number_input("Nilai Masuk", min_value=0.0, max_value=200.0, value=120.0)
        course = st.number_input("Kode Program Studi", min_value=8000, max_value=9999)
    with col5:
        prev_qualification = st.selectbox("Kualifikasi Sebelumnya", options=[1, 2, 3, 4, 5, 6])
        prev_grade = st.number_input("Nilai Kualifikasi Sebelumnya", min_value=0.0, max_value=20.0)
        daytime = st.selectbox("Waktu Kuliah", options=[1, 0], format_func=lambda x: "Pagi" if x==1 else "Sore")
        tuition_paid = st.selectbox("Uang Kuliah Lunas", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Belum")
    with col6:
        debtor = st.selectbox("Memiliki Utang", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        unemployment_rate = st.number_input("Tingkat Pengangguran (%)", min_value=0.0, max_value=50.0)
        inflation_rate = st.number_input("Tingkat Inflasi (%)", min_value=0.0, max_value=50.0)
        gdp = st.number_input("GDP Mahasiswa", min_value=0.0)

    st.subheader("3. Aktivitas Akademik Semester 1 & 2")
    sem_cols = st.columns(6)
    academic_data = {}
    for sem in ['1st', '2nd']:
        for typ in ['credited', 'enrolled', 'evaluations', 'approved', 'grade', 'without_evaluations']:
            label = f"Curricular_units_{sem}_sem_{typ}"
            index = ['1st', '2nd'].index(sem)*3 + ['credited', 'enrolled', 'evaluations', 'approved', 'grade', 'without_evaluations'].index(typ)%3
            academic_data[label] = sem_cols[index].number_input(label.replace("_", " ").title(), min_value=0.0)

    submitted = st.form_submit_button("Prediksi Sekarang")

if submitted:
    input_data = pd.DataFrame([{
        "Marital_status": marital_status,
        "Application_mode": application_mode,
        "Application_order": application_order,
        "Course": course,
        "Daytime_evening_attendance": daytime,
        "Previous_qualification": prev_qualification,
        "Previous_qualification_grade": prev_grade,
        "Nacionality": nacionality,
        "Mothers_qualification": mothers_qualification,
        "Fathers_qualification": fathers_qualification,
        "Mothers_occupation": mothers_occupation,
        "Fathers_occupation": fathers_occupation,
        "Admission_grade": admission_grade,
        "Displaced": displaced,
        "Educational_special_needs": special_needs,
        "Debtor": debtor,
        "Tuition_fees_up_to_date": tuition_paid,
        "Gender": gender,
        "Scholarship_holder": scholarship,
        "Age_at_enrollment": age_enroll,
        "International": international,
        "GDP": gdp,
        "Unemployment_rate": unemployment_rate,
        "Inflation_rate": inflation_rate,
        **academic_data
    }])

    input_data.insert(0, "id", 0)
    expected_features = model.get_booster().feature_names
    input_data = input_data[expected_features]

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("Hasil Prediksi: Mahasiswa diprediksi akan lulus.")
        st.info("Rekomendasi: Mahasiswa ini menunjukkan potensi untuk lulus. Tetap pantau dan dukung pencapaiannya.")
    else:
        st.error("Hasil Prediksi: Mahasiswa diprediksi akan dropout.")
        st.warning("Rekomendasi: Mahasiswa ini berisiko dropout. Berikan bimbingan akademik tambahan dan pantau performa semester awal secara ketat.")

    # Visualisasi akademik
    st.subheader("Visualisasi Performa Akademik")
    plot_data = input_data[[
        'Curricular_units_1st_sem_approved',
        'Curricular_units_2nd_sem_approved',
        'Curricular_units_1st_sem_enrolled',
        'Curricular_units_2nd_sem_enrolled'
    ]].melt(var_name='Aktivitas', value_name='Jumlah')

    plot_data['Aktivitas'] = plot_data['Aktivitas'].replace({
        'Curricular_units_1st_sem_approved': 'Disetujui S1',
        'Curricular_units_2nd_sem_approved': 'Disetujui S2',
        'Curricular_units_1st_sem_enrolled': 'Terdaftar S1',
        'Curricular_units_2nd_sem_enrolled': 'Terdaftar S2'
    })

    fig = px.bar(
        plot_data,
        x="Aktivitas",
        y="Jumlah",
        color="Aktivitas",
        title="Perbandingan Aktivitas Akademik Semester 1 dan 2"
    )
    st.plotly_chart(fig, use_container_width=True)
