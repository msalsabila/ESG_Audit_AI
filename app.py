import streamlit as st

st.set_page_config(
    page_title="Sistem Audit ESG Berbasis AI",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 SISTEM AUDIT ESG BERBASIS AI")

st.subheader(
    "Aplikasi Analisis Dokumen Lingkungan, Sosial, dan Tata Kelola"
)

st.write(
    "Selamat datang di Sistem Audit ESG Berbasis AI. "
    "Aplikasi ini membantu pengguna menganalisis dokumen perusahaan "
    "berdasarkan aspek lingkungan, sosial, dan tata kelola."
)

st.info(
    "Silakan unggah dokumen perusahaan untuk memulai proses analisis ESG."
)

st.markdown("### Aspek Audit ESG")

kolom1, kolom2, kolom3 = st.columns(3)

with kolom1:
    st.success("🌳 LINGKUNGAN")

with kolom2:
    st.warning("👥 SOSIAL")

with kolom3:
    st.info("🏢 TATA KELOLA")

st.markdown("---")

st.caption("Sistem Audit ESG Berbasis AI | Untuk Keperluan Akademik")
