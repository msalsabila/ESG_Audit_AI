
import streamlit as st
import io
from pypdf import PdfReader

# Library untuk membuat laporan PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape

if "teks_pdf" not in st.session_state:
    st.session_state["teks_pdf"] = ""
    


def buat_pdf_laporan(judul, isi):
    buffer = io.BytesIO()

    dokumen = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    gaya = getSampleStyleSheet()

    gaya["Title"].fontSize = 20
    gaya["Title"].textColor = colors.HexColor("#17365D")
    gaya["Title"].alignment = 1

    konten = []

    konten.append(Paragraph(escape(judul), gaya["Title"]))
    konten.append(Spacer(1, 12))

    konten.append(
        Paragraph(
            "ENVIRONMENTAL • SOCIAL • GOVERNANCE",
            gaya["Heading2"]
        )
    )

    konten.append(Spacer(1, 20))

    for baris in isi.split("\n"):
        if baris.strip():
            konten.append(
                Paragraph(
                    escape(baris),
                    gaya["BodyText"]
                )
            )
            konten.append(Spacer(1, 8))

    def nomor_halaman(canvas, dokumen):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(40, 25, "Laporan Audit ESG")
        canvas.drawRightString(555, 25, f"Halaman {dokumen.page}")
        canvas.restoreState()

    dokumen.build(
        konten,
        onFirstPage=nomor_halaman,
        onLaterPages=nomor_halaman
    )

    buffer.seek(0)
    return buffer.getvalue()

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
        "Unggah laporan tahunan atau laporan keberlanjutan "
        "perusahaan dalam format PDF."
    )

    dokumen = st.file_uploader(
        "Pilih dokumen perusahaan (PDF)",
        type=["pdf"]
    )

    if dokumen is not None:
        st.success("Dokumen berhasil diunggah!")
        st.write("Nama dokumen:", dokumen.name)

        try:
            pembaca = PdfReader(dokumen)

            st.write("Jumlah halaman:", len(pembaca.pages))

            teks_pdf = ""

            for nomor, halaman in enumerate(pembaca.pages, start=1):
                teks = halaman.extract_text() or ""
                teks_pdf += f"\n--- HALAMAN {nomor} ---\n"
                teks_pdf += teks
                
            st.session_state["teks_pdf"] = teks_pdf
        
            if teks_pdf.strip():
                st.subheader("Isi Dokumen PDF")

                if st.button("📄 Lihat Isi Dokumen"):
                    st.text_area(
                        "Teks yang berhasil dibaca",
                        teks_pdf,
                        height=400
                    )
            else:
                st.warning(
                    "Teks tidak ditemukan. PDF mungkin berupa hasil scan."
                )


        except Exception as e:
            st.error(f"Dokumen gagal dibaca: {e}")

elif menu == "Audit Lingkungan":
    st.title("🌳 Audit Lingkungan")
    st.write("Pemeriksaan informasi lingkungan berdasarkan dokumen perusahaan.")

    teks = st.session_state["teks_pdf"].lower()

    indikator = {
        "Emisi dan Gas Rumah Kaca": ["emisi", "gas rumah kaca", "karbon"],
        "Penggunaan Energi": ["energi", "listrik", "bahan bakar"],
        "Pengelolaan Air": ["air", "limbah cair", "penggunaan air"],
        "Pengelolaan Limbah": ["limbah", "sampah", "daur ulang"],
        "Keanekaragaman Hayati": ["keanekaragaman hayati", "deforestasi", "konservasi"]
    }

    if not teks:
        st.warning("Silakan unggah dokumen PDF terlebih dahulu.")
    else:
        for nama, kata_kunci in indikator.items():
            ditemukan = any(kata in teks for kata in kata_kunci)

            if ditemukan:
                st.success(f"{nama}: Informasi ditemukan")
            else:
                st.warning(f"{nama}: Informasi tidak ditemukan")

elif menu == "Audit Sosial":
    st.title("👥 Audit Sosial")
    st.write("Pemeriksaan informasi sosial berdasarkan dokumen perusahaan.")

    teks = st.session_state["teks_pdf"].lower()

    indikator = {
        "Ketenagakerjaan": ["karyawan", "tenaga kerja", "pekerja"],
        "Keselamatan dan Kesehatan Kerja (K3)": ["keselamatan kerja", "kesehatan kerja", "k3"],
        "Pelatihan dan Pengembangan": ["pelatihan", "pengembangan kompetensi"],
        "Hak Asasi Manusia": ["hak asasi manusia", "ham", "hak pekerja"],
        "Masyarakat": ["masyarakat", "pemberdayaan masyarakat", "program sosial"],
        "Kesetaraan dan Keberagaman": ["kesetaraan", "keberagaman", "diskriminasi"]
    }

    if not teks:
        st.warning("Silakan unggah dokumen PDF terlebih dahulu.")
    else:
        for nama, kata_kunci in indikator.items():
            ditemukan = any(kata in teks for kata in kata_kunci)

            if ditemukan:
                st.success(f"{nama}: Informasi ditemukan")
            else:
                st.warning(f"{nama}: Informasi tidak ditemukan")

elif menu == "Audit Tata Kelola":
    st.title("🏢 Audit Tata Kelola")
    st.write("Pemeriksaan informasi tata kelola berdasarkan dokumen perusahaan.")

    teks = st.session_state["teks_pdf"].lower()

    indikator = {
        "Struktur Tata Kelola": ["direksi", "dewan komisaris", "komisaris"],
        "Etika Bisnis": ["kode etik", "etika bisnis", "perilaku bisnis"],
        "Anti Korupsi": ["anti korupsi", "antikorupsi", "gratifikasi"],
        "Manajemen Risiko": ["manajemen risiko", "pengelolaan risiko"],
        "Kepatuhan": ["kepatuhan", "peraturan", "regulasi"],
        "Transparansi": ["transparansi", "keterbukaan informasi"],
        "Komite Audit": ["komite audit", "audit internal"]
    }

    if not teks:
        st.warning("Silakan unggah dokumen PDF terlebih dahulu.")
    else:
        for nama, kata_kunci in indikator.items():
            ditemukan = any(kata in teks for kata in kata_kunci)

            if ditemukan:
                st.success(f"{nama}: Informasi ditemukan")
            else:
                st.warning(f"{nama}: Informasi tidak ditemukan")

elif menu == "Analisis Dokumen AI":
    st.title("🤖 Analisis Dokumen ESG")
    st.write("Ringkasan pemeriksaan dokumen berdasarkan aspek ESG.")

    teks = st.session_state["teks_pdf"].lower()

    indikator_esg = {
        "Environmental": {
            "Emisi dan Gas Rumah Kaca": ["emisi", "gas rumah kaca", "karbon"],
            "Penggunaan Energi": ["energi", "listrik", "bahan bakar"],
            "Pengelolaan Air": ["air", "limbah cair", "penggunaan air"],
            "Pengelolaan Limbah": ["limbah", "sampah", "daur ulang"],
            "Keanekaragaman Hayati": ["keanekaragaman hayati", "deforestasi", "konservasi"]
        },
        "Social": {
            "Ketenagakerjaan": ["karyawan", "tenaga kerja", "pekerja"],
            "Keselamatan dan Kesehatan Kerja": ["keselamatan kerja", "kesehatan kerja", "k3"],
            "Pelatihan dan Pengembangan": ["pelatihan", "pengembangan kompetensi"],
            "Hak Asasi Manusia": ["hak asasi manusia", "ham", "hak pekerja"],
            "Masyarakat": ["masyarakat", "pemberdayaan masyarakat", "program sosial"],
            "Kesetaraan dan Keberagaman": ["kesetaraan", "keberagaman", "diskriminasi"]
        },
        "Governance": {
            "Struktur Tata Kelola": ["direksi", "dewan komisaris", "komisaris"],
            "Etika Bisnis": ["kode etik", "etika bisnis", "perilaku bisnis"],
            "Anti Korupsi": ["anti korupsi", "antikorupsi", "gratifikasi"],
            "Manajemen Risiko": ["manajemen risiko", "pengelolaan risiko"],
            "Kepatuhan": ["kepatuhan", "peraturan", "regulasi"],
            "Transparansi": ["transparansi", "keterbukaan informasi"],
            "Komite Audit": ["komite audit", "audit internal"]
        }
    }

    if not teks:
        st.warning("Silakan unggah dokumen PDF terlebih dahulu.")
    else:
        total = 0
        ditemukan_total = 0

        for aspek, daftar in indikator_esg.items():
            st.subheader(aspek)

            for nama, kata_kunci in daftar.items():
                total += 1
                ditemukan = any(kata in teks for kata in kata_kunci)

                if ditemukan:
                    ditemukan_total += 1
                    st.success(f"{nama}: Informasi ditemukan")
                else:
                    st.warning(f"{nama}: Informasi tidak ditemukan")

        persentase = (ditemukan_total / total) * 100

        st.divider()
        st.subheader("Ringkasan Hasil Pemeriksaan")

        kolom1, kolom2, kolom3 = st.columns(3)

        kolom1.metric("Total Indikator", total)
        kolom2.metric("Informasi Ditemukan", ditemukan_total)
        kolom3.metric("Cakupan Indikator", f"{persentase:.1f}%")

        st.info(
            "Hasil ini merupakan pemeriksaan awal berdasarkan "
            "pencocokan kata kunci dalam dokumen, bukan penilaian "
            "mutlak atas kinerja ESG perusahaan."
        )


elif menu == "Temuan Audit":
    st.title("📋 Temuan dan Rekomendasi Audit ESG")
    st.write(
        "Daftar hasil pemeriksaan dan rekomendasi "
        "perbaikan berdasarkan dokumen perusahaan."
    )

    teks = st.session_state["teks_pdf"].lower()

    indikator_esg = {
        "Environmental": {
            "Emisi dan Gas Rumah Kaca": (
                ["emisi", "gas rumah kaca", "karbon"],
                "Periksa kelengkapan data emisi dan upaya pengurangan gas rumah kaca."
            ),
            "Penggunaan Energi": (
                ["energi", "listrik", "bahan bakar"],
                "Periksa pencatatan konsumsi energi dan program efisiensi energi."
            ),
            "Pengelolaan Air": (
                ["air", "limbah cair", "penggunaan air"],
                "Periksa data penggunaan air dan pengelolaan limbah cair."
            ),
            "Pengelolaan Limbah": (
                ["limbah", "sampah", "daur ulang"],
                "Periksa prosedur pengelolaan dan pengurangan limbah."
            ),
            "Keanekaragaman Hayati": (
                ["keanekaragaman hayati", "deforestasi", "konservasi"],
                "Periksa kebijakan perlindungan lingkungan dan keanekaragaman hayati."
            )
        },
        "Social": {
            "Ketenagakerjaan": (
                ["karyawan", "tenaga kerja", "pekerja"],
                "Periksa kebijakan ketenagakerjaan dan pemenuhan hak pekerja."
            ),
            "Keselamatan dan Kesehatan Kerja": (
                ["keselamatan kerja", "kesehatan kerja", "k3"],
                "Periksa penerapan program keselamatan dan kesehatan kerja."
            ),
            "Pelatihan dan Pengembangan": (
                ["pelatihan", "pengembangan kompetensi"],
                "Periksa program pelatihan dan pengembangan kompetensi karyawan."
            ),
            "Hak Asasi Manusia": (
                ["hak asasi manusia", "ham", "hak pekerja"],
                "Periksa kebijakan perlindungan hak asasi manusia."
            ),
            "Masyarakat": (
                ["masyarakat", "pemberdayaan masyarakat", "program sosial"],
                "Periksa pelaksanaan program tanggung jawab sosial masyarakat."
            ),
            "Kesetaraan dan Keberagaman": (
                ["kesetaraan", "keberagaman", "diskriminasi"],
                "Periksa kebijakan kesetaraan dan pencegahan diskriminasi."
            )
        },
        "Governance": {
            "Struktur Tata Kelola": (
                ["direksi", "dewan komisaris", "komisaris"],
                "Periksa kelengkapan informasi struktur dan tanggung jawab tata kelola."
            ),
            "Etika Bisnis": (
                ["kode etik", "etika bisnis", "perilaku bisnis"],
                "Periksa penerapan kode etik dan kebijakan perilaku bisnis."
            ),
            "Anti Korupsi": (
                ["anti korupsi", "antikorupsi", "gratifikasi"],
                "Periksa kebijakan pencegahan korupsi dan gratifikasi."
            ),
            "Manajemen Risiko": (
                ["manajemen risiko", "pengelolaan risiko"],
                "Periksa penerapan identifikasi dan pengelolaan risiko."
            ),
            "Kepatuhan": (
                ["kepatuhan", "peraturan", "regulasi"],
                "Periksa informasi kepatuhan terhadap peraturan yang berlaku."
            ),
            "Transparansi": (
                ["transparansi", "keterbukaan informasi"],
                "Periksa keterbukaan informasi dan transparansi perusahaan."
            ),
            "Komite Audit": (
                ["komite audit", "audit internal"],
                "Periksa fungsi dan pelaksanaan pengawasan audit internal."
            )
        }
    }

    if not teks:
        st.warning("Silakan unggah dokumen PDF terlebih dahulu.")
    else:
        hasil_temuan = []

        for aspek, daftar in indikator_esg.items():
            for nama, data in daftar.items():
                kata_kunci, rekomendasi = data
                ditemukan = [
                    kata for kata in kata_kunci if kata in teks
                ]

                if ditemukan:
                    status = "Informasi ditemukan"
                    rekomendasi_hasil = (
                        "Verifikasi kecukupan bukti dan kesesuaian "
                        "informasi dengan indikator ESG."
                    )
                else:
                    status = "Informasi tidak ditemukan"
                    rekomendasi_hasil = rekomendasi

                hasil_temuan.append({
                    "Aspek ESG": aspek,
                    "Indikator": nama,
                    "Status": status,
                    "Kata Kunci": ", ".join(ditemukan) if ditemukan else "-",
                    "Rekomendasi": rekomendasi_hasil
                })

        total_temuan = len(hasil_temuan)
        perlu_diperiksa = sum(
            1 for item in hasil_temuan
            if item["Status"] == "Informasi tidak ditemukan"
        )

        kolom1, kolom2 = st.columns(2)

        kolom1.metric("Total Indikator", total_temuan)
        kolom2.metric("Perlu Pemeriksaan Lanjutan", perlu_diperiksa)

        st.subheader("Daftar Temuan dan Rekomendasi")

        for aspek in ["Environmental", "Social", "Governance"]:
            st.markdown(f"### {aspek}")

            data_aspek = [
                item for item in hasil_temuan
                if item["Aspek ESG"] == aspek
            ]

            for item in data_aspek:
                with st.expander(item["Indikator"]):
                    st.write("**Status:**", item["Status"])
                    st.write("**Kata kunci:**", item["Kata Kunci"])
                    st.write("**Rekomendasi:**", item["Rekomendasi"])

        st.info(
            "Catatan: Hasil ini merupakan indikasi awal berdasarkan "
            "pencocokan kata kunci, bukan temuan audit yang telah "
            "terverifikasi. Setiap hasil perlu diperiksa kembali "
            "oleh auditor."
        )


elif menu == "Laporan Audit":
    st.title("📑 Laporan Audit ESG")
    st.write("Ringkasan hasil pemeriksaan dokumen berdasarkan indikator ESG.")

    teks = st.session_state.get("teks_pdf", "")

    if not teks.strip():
        st.warning("Silakan unggah dokumen PDF terlebih dahulu pada menu Unggah Dokumen.")

    else:
        # Identitas pemeriksaan
        st.subheader("1. Identitas Pemeriksaan")

        nama_perusahaan = st.text_input("Nama Perusahaan")
        nama_dokumen = st.text_input("Nama Dokumen")
        tanggal = st.date_input("Tanggal Pemeriksaan")

        # Indikator ESG
        indikator_esg = {
            "Lingkungan": {
                "Emisi dan Gas Rumah Kaca": ["emisi", "gas rumah kaca", "karbon"],
                "Penggunaan Energi": ["energi", "listrik", "bahan bakar"],
                "Pengelolaan Air": ["air", "limbah cair", "penggunaan air"],
                "Pengelolaan Limbah": ["limbah", "sampah", "daur ulang"],
                "Keanekaragaman Hayati": ["keanekaragaman hayati", "deforestasi", "konservasi"]
            },
            "Sosial": {
                "Ketenagakerjaan": ["karyawan", "tenaga kerja", "pekerja"],
                "Keselamatan dan Kesehatan Kerja": ["keselamatan kerja", "kesehatan kerja", "k3"],
                "Pelatihan dan Pengembangan": ["pelatihan", "pengembangan kompetensi"],
                "Hak Asasi Manusia": ["hak asasi manusia", "ham", "hak pekerja"],
                "Masyarakat": ["masyarakat", "pemberdayaan masyarakat", "program sosial"],
                "Kesetaraan dan Keberagaman": ["kesetaraan", "keberagaman", "diskriminasi"]
            },
            "Tata Kelola": {
                "Struktur Tata Kelola": ["direksi", "dewan komisaris", "komisaris"],
                "Etika Bisnis": ["kode etik", "etika bisnis", "perilaku bisnis"],
                "Anti Korupsi": ["anti korupsi", "antikorupsi", "gratifikasi"],
                "Manajemen Risiko": ["manajemen risiko", "pengelolaan risiko"],
                "Kepatuhan": ["kepatuhan", "peraturan", "regulasi"],
                "Transparansi": ["transparansi", "keterbukaan informasi"],
                "Komite Audit": ["komite audit", "audit internal"]
            }
        }

        # Pemeriksaan indikator
        hasil = {}
        total = 0
        ditemukan = 0

        for aspek, indikator in indikator_esg.items():
            hasil[aspek] = {}

            for nama, kata_kunci in indikator.items():
                total += 1

                status = any(
                    kata.lower() in teks.lower()
                    for kata in kata_kunci
                )

                hasil[aspek][nama] = status

                if status:
                    ditemukan += 1

        belum = total - ditemukan
        cakupan = (ditemukan / total) * 100

        # Ringkasan audit
        st.divider()
        st.subheader("2. Ringkasan Hasil Audit")

        kolom1, kolom2, kolom3 = st.columns(3)

        kolom1.metric("Total Indikator", total)
        kolom2.metric("Terdeteksi", ditemukan)
        kolom3.metric("Belum Terdeteksi", belum)

        st.progress(cakupan / 100)
        st.write(f"**Cakupan informasi ESG: {cakupan:.1f}%**")

        # Hasil per aspek
        st.divider()
        st.subheader("3. Hasil Pemeriksaan per Aspek")

        ringkasan = []

        for aspek, indikator in hasil.items():
            jumlah = len(indikator)
            jumlah_ada = sum(indikator.values())

            ringkasan.append({
                "Aspek": aspek,
                "Total Indikator": jumlah,
                "Terdeteksi": jumlah_ada,
                "Belum Terdeteksi": jumlah - jumlah_ada
            })

        st.dataframe(ringkasan, use_container_width=True, hide_index=True)

        # Rincian temuan
        st.divider()
        st.subheader("4. Temuan dan Rekomendasi")

        for aspek, indikator in hasil.items():
            with st.expander(f"Hasil Pemeriksaan {aspek}"):
                for nama, status in indikator.items():
                    if status:
                        st.write(f"✅ **{nama}** — Kata kunci terdeteksi.")
                    else:
                        st.write(f"⚠️ **{nama}** — Informasi belum terdeteksi.")
                        st.caption(
                            "Rekomendasi: Periksa kembali dokumen dan "
                            "lengkapi informasi serta bukti pendukung terkait indikator ini."
                        )

        # Kesimpulan
        st.divider()
        st.subheader("5. Kesimpulan Audit")

        st.write(
            f"Berdasarkan pemeriksaan awal terhadap dokumen, "
            f"ditemukan {ditemukan} dari {total} indikator ESG "
            f"dengan cakupan informasi sebesar {cakupan:.1f}%. "
            f"Terdapat {belum} indikator yang belum terdeteksi "
            f"dan perlu ditinjau lebih lanjut."
        )

        st.info(
            "Catatan: Hasil ini merupakan pemeriksaan awal berbasis "
            "pencocokan kata kunci, bukan kesimpulan audit atau verifikasi "
            "kepatuhan ESG secara menyeluruh."
        )

        # Membuat laporan PDF
        st.divider()
        st.subheader("6. Unduh Laporan")

        if st.button("📄 Buat Laporan PDF", type="primary"):
            if not nama_perusahaan.strip():
                st.error("Silakan isi nama perusahaan terlebih dahulu.")
            elif not nama_dokumen.strip():
                st.error("Silakan isi nama dokumen terlebih dahulu.")
            else:
                isi_laporan = [
                    f"Nama Perusahaan: {nama_perusahaan}",
                    f"Nama Dokumen: {nama_dokumen}",
                    f"Tanggal Pemeriksaan: {tanggal}",
                    "",
                    "RINGKASAN HASIL AUDIT",
                    f"Total indikator: {total}",
                    f"Indikator terdeteksi: {ditemukan}",
                    f"Indikator belum terdeteksi: {belum}",
                    f"Cakupan informasi ESG: {cakupan:.1f}%",
                    "",
                    "HASIL PEMERIKSAAN PER ASPEK"
                ]

                for aspek, indikator in hasil.items():
                    jumlah = len(indikator)
                    jumlah_ada = sum(indikator.values())

                    isi_laporan.append(
                        f"{aspek}: {jumlah_ada} dari {jumlah} indikator terdeteksi"
                    )

                isi_laporan.extend(["", "RINCIAN TEMUAN DAN REKOMENDASI"])

                for aspek, indikator in hasil.items():
                    isi_laporan.append(aspek.upper())

                    for nama, status in indikator.items():
                        if status:
                            isi_laporan.append(
                                f"{nama}: Kata kunci terdeteksi."
                            )
                        else:
                            isi_laporan.append(
                                f"{nama}: Belum terdeteksi. "
                                "Rekomendasi: Lengkapi informasi dan bukti pendukung."
                            )

                isi_laporan.extend([
                    "",
                    "KESIMPULAN",
                    f"Ditemukan {ditemukan} dari {total} indikator ESG "
                    f"dengan cakupan {cakupan:.1f}%.",
                    "",
                    "Catatan: Pemeriksaan awal berbasis pencocokan kata kunci "
                    "dan bukan verifikasi kepatuhan ESG secara menyeluruh."
                ])

                pdf = buat_pdf_laporan(
                    "LAPORAN HASIL AUDIT ESG",
                    "\n".join(isi_laporan)
                )

                st.download_button(
    label="⬇️ Unduh Laporan Audit PDF",
    data=pdf,
    file_name="Laporan_Audit_ESG.pdf",
    mime="application/pdf",
    key="download_laporan_esg"
)
