
import streamlit as st

st.set_page_config(
    page_title="Sistem Audit ESG Berbasis AI",
    page_icon="🌱",
    layout="wide"
)

# Identitas aplikasi
st.sidebar.title("🌱 ESG AUDIT AI")
st.sidebar.caption("Sistem Audit Berbasis Kecerdasan Buatan")
st.sidebar.markdown("---")

# Menu navigasi
menu = st.sidebar.radio(
    "MENU NAVIGASI",
    [
        "Beranda",
        "Unggah Dokumen",
        "Audit Lingkungan",
        "Audit Sosial",
        "Audit Tata Kelola",
        "Analisis Dokumen AI",
        "Temuan Audit",
        "Laporan Audit"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Versi 1.0 | Proyek Akademik")

# Halaman Beranda
if menu == "Beranda":
    st.title("🌱 Sistem Audit ESG Berbasis AI")
    st.subheader("Selamat Datang di Dashboard ESG Audit AI")

    st.write(
        "Aplikasi ini membantu proses analisis dokumen "
        "perusahaan berdasarkan aspek lingkungan, sosial, "
        "dan tata kelola."
    )

    st.info(
        "Silakan pilih menu di sebelah kiri untuk memulai "
        "proses audit ESG."
    )

    kolom1, kolom2, kolom3 = st.columns(3)

    with kolom1:
        st.success("🌳 AUDIT LINGKUNGAN")

    with kolom2:
        st.warning("👥 AUDIT SOSIAL")

    with kolom3:
        st.info("🏢 AUDIT TATA KELOLA")

# Halaman lainnya
elif menu == "Unggah Dokumen":
    st.title("📂 Unggah Dokumen Perusahaan")

    st.write(
        "Silakan unggah dokumen perusahaan "
        "yang akan digunakan dalam proses audit ESG."
    )

    dokumen = st.file_uploader(
        "Pilih dokumen perusahaan (PDF)",
        type=["pdf"]
    )

    if dokumen is not None:
        st.success("Dokumen berhasil diunggah!")

        st.write("Nama dokumen:", dokumen.name)

        st.write(
            "Ukuran dokumen:",
            round(dokumen.size / 1024, 2),
            "KB"
        )

elif menu == "Audit Lingkungan":
    st.title("🌳 Audit Lingkungan")
    st.write("Halaman pemeriksaan aspek lingkungan.")

elif menu == "Audit Sosial":
    st.title("👥 Audit Sosial")
    st.write("Halaman pemeriksaan aspek sosial.")

elif menu == "Audit Tata Kelola":
    st.title("🏢 Audit Tata Kelola")
    st.write("Halaman pemeriksaan tata kelola perusahaan.")

elif menu == "Analisis Dokumen AI":
    st.title("🤖 Analisis Dokumen dengan AI")
    st.write("Halaman analisis isi dokumen perusahaan.")

elif menu == "Temuan Audit":
    st.title("📋 Temuan Audit")
    st.write("Halaman hasil temuan pemeriksaan ESG.")

elif menu == "Laporan Audit":
    st.title("📑 Laporan Audit")
    st.write("Halaman penyusunan laporan hasil audit ESG.")
