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
    st.markdown("- Ya = 1, Tidak = 0\n- Pria = 1, Wanita = 0")
    st.markdown("Lihat dokumentasi fitur di [GitHub Readme](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)")

with st.form("prediction_form"):
    st.subheader("1. Data Pribadi & Sosial")
    col1, col2, col3 = st.columns(3)
    with col1:
        marital_status = st.selectbox("Status Pernikahan", options=[1, 2, 3], format_func=lambda x: {1: "Lajang", 2: "Menikah", 3: "Cerai"}.get(x))
        gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: "Pria" if x==1 else "Wanita")
        age_enroll = st.number_input("Usia Saat Mendaftar", min_value=15, max_value=70, value=18)
        nacionality = st.selectbox("Kebangsaan", options=[1, 2, 3], format_func=lambda x: {1: "Indonesia", 2: "Asing", 3: "Lainnya"}.get(x))
    with col2:
        mothers_occupation = st.selectbox("Pekerjaan Ibu", options=[0, 1, 2, 3], format_func=lambda x: {0: "Tidak Bekerja", 1: "PNS", 2: "Wirausaha", 3: "Lainnya"}.get(x))
        fathers_occupation = st.selectbox("Pekerjaan Ayah", options=[0, 1, 2, 3], format_func=lambda x: {0: "Tidak Bekerja", 1: "PNS", 2: "Wirausaha", 3: "Lainnya"}.get(x))
        mothers_qualification = st.selectbox("Pendidikan Ibu", options=[1, 2, 3], format_func=lambda x: {1: "SMA", 2: "S1", 3: "S2/S3"}.get(x))
        fathers_qualification = st.selectbox("Pendidikan Ayah", options=[1, 2, 3], format_func=lambda x: {1: "SMA", 2: "S1", 3: "S2/S3"}.get(x))
    with col3:
        scholarship = st.selectbox("Penerima Beasiswa", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        displaced = st.selectbox("Mahasiswa Terpindahkan", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        special_needs = st.selectbox("Kebutuhan Khusus", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")
        international = st.selectbox("Mahasiswa Internasional", options=[0, 1], format_func=lambda x: "Ya" if x==1 else "Tidak")

    st.subheader("2. Akademik & Keuangan")
    col4, col5, col6 = st.columns(3)
    with col4:
        application_mode = st.selectbox("Jalur Pendaftaran", options=[1, 2, 3, 4, 5, 6], format_func=lambda x: {1: "Reguler", 2: "Undangan", 3: "Beasiswa", 4: "Mandiri", 5: "Internasional", 6: "Lainnya"}.get(x))
        application_order = st.number_input("Urutan Pilihan Studi", min_value=1, max_value=20, value=1)
        admission_grade = st.number_input("Nilai Masuk", min_value=0.0, max_value=200.0, value=120.0)
        course = st.number_input("Kode Program Studi", min_value=8000, max_value=9999)
    with col5:
        prev_qualification = st.selectbox("Kualifikasi Sebelumnya", options=[1, 2, 3, 4, 5, 6], format_func=lambda x: f"Tingkat {x}")
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
    label_dict = {
        "credited": "SKS Diakui",
        "enrolled": "SKS Diambil",
        "evaluations": "Evaluasi",
        "approved": "SKS Lulus",
        "grade": "Rata-rata Nilai",
        "without_evaluations": "Tanpa Evaluasi"
    }
    for sem in ['1', '2']:
        for typ in label_dict.keys():
            label = f"Curricular_units_{sem}st_sem_{typ}" if sem == '1' else f"Curricular_units_{sem}nd_sem_{typ}"
            display_label = f"Semester {sem} - {label_dict[typ]}"
            index = ['1', '2'].index(sem)*3 + list(label_dict.keys()).index(typ)%3
            academic_data[label] = sem_cols[index].number_input(display_label, min_value=0.0)

    submitted = st.form_submit_button("Prediksi Sekarang")

if submitted:
    input_data = pd.DataFrame([{**{
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
        "Inflation_rate": inflation_rate
    }, **academic_data}])

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

    st.subheader("Visualisasi Performa Akademik")
    plot_data = input_data[[
        'Curricular_units_1st_sem_approved',
        'Curricular_units_2nd_sem_approved',
        'Curricular_units_1st_sem_enrolled',
        'Curricular_units_2nd_sem_enrolled'
    ]].melt(var_name='Aktivitas', value_name='Jumlah')

    plot_data['Aktivitas'] = plot_data['Aktivitas'].replace({
        'Curricular_units_1st_sem_approved': 'Lulus Smt 1',
        'Curricular_units_2nd_sem_approved': 'Lulus Smt 2',
        'Curricular_units_1st_sem_enrolled': 'Ambil Smt 1',
        'Curricular_units_2nd_sem_enrolled': 'Ambil Smt 2'
    })

    fig = px.bar(
        plot_data,
        x="Aktivitas",
        y="Jumlah",
        color="Aktivitas",
        title="Perbandingan Aktivitas Akademik Semester 1 dan 2"
    )
    st.plotly_chart(fig, use_container_width=True)