import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ==================================================
# 1. KONFIGURASI HALAMAN
# ==================================================

st.set_page_config(
    page_title="Atlas Kependudukan Sulawesi Selatan",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palet: hijau struktur, abu beton, kapur, kuningan
HIJAU_TUA = "#0F3D2E"
HIJAU = "#1F6B4F"
HIJAU_MUDA = "#CFE3D8"
BETON = "#E6E9E4"
KAPUR = "#F5F6F2"
KUNINGAN = "#A6804A"
TINTA = "#16211C"
ABU = "#5E6B64"

# ==================================================
# 2. CSS
# ==================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, .stApp, [class*="css"] {{
    font-family: 'IBM Plex Sans', sans-serif;
    color: {TINTA};
}}
.stApp {{
    background-color: {KAPUR};
    background-image:
        linear-gradient(rgba(15,61,46,.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,61,46,.045) 1px, transparent 1px);
    background-size: 36px 36px;
}}
[data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background: transparent; }}
.block-container {{ padding: 1.6rem 3rem 2rem; max-width: 100%; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background-color: {HIJAU_TUA}; border-right: 4px solid {KUNINGAN}; }}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{ color: white; }}
[data-testid="stSidebar"] label {{ color: {HIJAU_MUDA} !important; font-weight: 500 !important; }}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{ background-color: {KAPUR}; border-radius: 3px; }}
[data-testid="stSidebar"] [data-baseweb="select"] * {{ color: {TINTA} !important; }}
[data-testid="stSidebar"] .stButton button {{
    border-radius: 3px; min-height: 44px; font-weight: 500; text-align: left;
    justify-content: flex-start; transition: background-color .15s ease;
}}
[data-testid="stSidebar"] .stButton button:focus-visible {{ outline: 2px solid {KUNINGAN}; outline-offset: 2px; }}

.brand {{ padding: 10px 4px 14px; border-bottom: 1px solid rgba(255,255,255,.18); margin-bottom: 14px; }}
.brand-name {{ font-family: 'Fraunces', serif; font-size: 22px; font-weight: 700; color: white; line-height: 1.15; }}
.brand-sub {{ color: {HIJAU_MUDA}; font-size: 13px; margin-top: 4px; }}
.side-note {{ color: {HIJAU_MUDA}; font-size: 12px; line-height: 1.6; }}

/* Hero bergaya kertas gambar teknik */
.hero {{
    background-color: {HIJAU_TUA};
    background-image:
        linear-gradient(rgba(255,255,255,.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px);
    background-size: 36px 36px;
    border-bottom: 5px solid {KUNINGAN};
    border-radius: 4px;
    padding: 38px 40px 32px;
    margin-bottom: 26px;
}}
.hero h1 {{
    font-family: 'Fraunces', serif; font-weight: 700; color: white;
    font-size: 40px; line-height: 1.12; margin: 0 0 10px; letter-spacing: -0.01em;
}}
.hero p {{ color: {HIJAU_MUDA}; font-size: 16px; margin: 0; max-width: 680px; line-height: 1.6; }}
.hero-meta {{ display: flex; gap: 28px; margin-top: 22px; flex-wrap: wrap; }}
.hero-meta div {{ color: white; font-size: 14px; border-left: 2px solid {KUNINGAN}; padding-left: 12px; }}
.hero-meta b {{ display: block; font-size: 20px; font-family: 'Fraunces', serif; }}

/* Judul bagian */
.section-title {{
    font-family: 'Fraunces', serif; font-size: 25px; font-weight: 700; color: {HIJAU_TUA};
    margin: 30px 0 4px; padding-top: 14px; border-top: 1px solid {ABU}55;
}}
.section-desc {{ color: {ABU}; font-size: 14.5px; margin-bottom: 14px; max-width: 760px; line-height: 1.6; }}

/* Kartu statistik */
div[data-testid="stMetric"] {{
    background: transparent; border: 1px solid #CBD3CB; border-top: 4px solid {HIJAU};
    padding: 16px 18px; border-radius: 3px;
}}
div[data-testid="stMetricLabel"] {{ color: {ABU}; }}
div[data-testid="stMetricValue"] {{ color: {HIJAU_TUA}; font-family: 'Fraunces', serif; font-weight: 700; }}

/* Kotak temuan */
.insight {{
    background: transparent; border: 1px solid #CBD3CB; border-left: 5px solid {KUNINGAN};
    padding: 16px 20px; border-radius: 3px; line-height: 1.75; font-size: 15px; margin-bottom: 10px;
}}
.insight b {{ color: {HIJAU_TUA}; }}

/* Tab */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BETON}; }}
.stTabs [data-baseweb="tab"] {{ font-weight: 500; padding: 8px 16px; }}
.stTabs [aria-selected="true"] {{ color: {HIJAU_TUA}; }}

/* Tombol unduh */
.stDownloadButton button {{
    background-color: {HIJAU_TUA}; color: white; border-radius: 3px; font-weight: 500; border: none;
}}
.stDownloadButton button:hover {{ background-color: {KUNINGAN}; color: white; }}

[data-testid="stDataFrame"] {{ border: 1px solid #CBD3CB; border-radius: 3px; }}

.footer {{
    text-align: center; color: {ABU}; font-size: 13px;
    padding: 22px 0 8px; margin-top: 36px; border-top: 1px solid {BETON};
}}
@media (max-width: 700px) {{
    .hero {{ padding: 26px 20px; }}
    .hero h1 {{ font-size: 28px; }}
}}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. MEMBACA DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[1]
FILE_DATA = BASE_DIR / "dataset" / "Data_Kependudukan_Bersih.csv"

KOLOM = "Jumlah_Penduduk_Ribu_Jiwa"
WILAYAH = "Kabupaten/Kota"


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)

    for kolom in [WILAYAH, "Tahun", KOLOM]:
        if kolom not in data.columns:
            raise ValueError(f"Kolom {kolom} tidak ditemukan dalam dataset.")

    data["Tahun"] = pd.to_numeric(data["Tahun"], errors="coerce")
    data[KOLOM] = pd.to_numeric(data[KOLOM], errors="coerce")
    data = data.dropna(subset=[WILAYAH, "Tahun", KOLOM])
    data["Tahun"] = data["Tahun"].astype(int)
    return data


try:
    df = load_data(str(FILE_DATA))
except Exception as error:
    st.error(f"Dataset tidak bisa dibaca: {error}")
    st.info("Simpan file Data_Kependudukan_Bersih.csv di folder dataset, lalu muat ulang halaman.")
    st.stop()

if df.empty:
    st.error("Dataset kosong, tidak ada data yang bisa ditampilkan.")
    st.stop()

# ==================================================
# 4. FUNGSI BANTU
# ==================================================


def tata_grafik(fig, tinggi=420):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=tinggi,
        font=dict(family="IBM Plex Sans", color=TINTA),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig.update_xaxes(gridcolor="#D5DBD4", linecolor=ABU)
    fig.update_yaxes(gridcolor="#D5DBD4", linecolor=ABU)
    return fig


def judul(teks, deskripsi=""):
    st.markdown(f'<div class="section-title">{teks}</div>', unsafe_allow_html=True)
    if deskripsi:
        st.markdown(f'<div class="section-desc">{deskripsi}</div>', unsafe_allow_html=True)


def fmt(angka, desimal=2):
    # format Indonesia: titik ribuan, koma desimal
    teks = f"{angka:,.{desimal}f}"
    return teks.replace(",", "X").replace(".", ",").replace("X", ".")


# ==================================================
# 5. SIDEBAR
# ==================================================

if "menu_aktif" not in st.session_state:
    st.session_state.menu_aktif = "Ringkasan"

st.sidebar.markdown("""
<div class="brand">
    <div class="brand-name">Atlas Kependudukan<br>Sulawesi Selatan</div>
    <div class="brand-sub">Dashboard analisis jumlah penduduk</div>
</div>
""", unsafe_allow_html=True)

menu_list = [
    ("Profil Kependudukan", "🏠"),
    ("Data Kependudukan", "📋"),
    ("Analisis Perkembangan", "📈"),
    ("Tentang Aplikasi", "ℹ️"),
]

for i, (nama_menu, ikon) in enumerate(menu_list):
    aktif = st.session_state.menu_aktif == nama_menu
    latar = KAPUR if aktif else HIJAU
    teks = HIJAU_TUA if aktif else "white"
    st.sidebar.markdown(f"""
    <style>
    div.st-key-nav_{i} button {{
        background-color: {latar}; color: {teks};
        border: 1px solid {"#FFFFFF" if aktif else HIJAU_MUDA + "55"};
    }}
    div.st-key-nav_{i} button p {{ color: {teks} !important; }}
    div.st-key-nav_{i} button:hover {{ background-color: {HIJAU_MUDA}; color: {HIJAU_TUA}; }}
    div.st-key-nav_{i} button:hover p {{ color: {HIJAU_TUA} !important; }}
    </style>
    """, unsafe_allow_html=True)

    if st.sidebar.button(f"{ikon}  {nama_menu}", key=f"nav_{i}", width="stretch"):
        st.session_state.menu_aktif = nama_menu
        st.rerun()

menu = st.session_state.menu_aktif

st.sidebar.markdown("---")
st.sidebar.markdown("**Filter data**")

daftar_tahun = sorted(df["Tahun"].unique())
tahun_pilihan = st.sidebar.selectbox(
    "Tahun pengamatan", daftar_tahun, index=len(daftar_tahun) - 1
)

daftar_wilayah = ["Semua Kabupaten/Kota"] + sorted(df[WILAYAH].unique())
wilayah_pilihan = st.sidebar.selectbox("Kabupaten/Kota", daftar_wilayah)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f'<div class="side-note">Sumber data: BPS Provinsi Sulawesi Selatan<br>'
    f'Periode {min(daftar_tahun)}–{max(daftar_tahun)}</div>',
    unsafe_allow_html=True,
)

# ==================================================
# 6. PENGOLAHAN DATA
# ==================================================

tahun_awal, tahun_akhir = int(df["Tahun"].min()), int(df["Tahun"].max())

data_tahun = (
    df.groupby("Tahun")[KOLOM].sum().reset_index().sort_values("Tahun")
)

data_pilihan = df[df["Tahun"] == tahun_pilihan].copy()
total_pilihan = data_pilihan[KOLOM].sum()
data_pilihan["Kontribusi_Persen"] = data_pilihan[KOLOM] / total_pilihan * 100
data_pilihan["Peringkat"] = data_pilihan[KOLOM].rank(ascending=False, method="min").astype(int)

data_perbandingan = data_pilihan.sort_values(KOLOM, ascending=False)

data_filter = data_perbandingan.copy()
if wilayah_pilihan != "Semua Kabupaten/Kota":
    data_filter = data_filter[data_filter[WILAYAH] == wilayah_pilihan]

perkembangan = data_tahun.copy()
perkembangan["Perubahan_Penduduk"] = perkembangan[KOLOM].diff()
perkembangan["Persentase_Perubahan"] = perkembangan[KOLOM].pct_change() * 100
perkembangan["Tren"] = perkembangan["Perubahan_Penduduk"].apply(
    lambda x: "Meningkat" if x > 0 else ("Menurun" if x < 0 else "Tetap")
)
perkembangan.loc[perkembangan["Perubahan_Penduduk"].isna(), "Tren"] = "-"

# Matriks wilayah x tahun dan laju pertumbuhan tahunan majemuk (CAGR)
matriks = df.pivot_table(index=WILAYAH, columns="Tahun", values=KOLOM, aggfunc="sum")
jumlah_tahun = tahun_akhir - tahun_awal
cagr = None
if jumlah_tahun > 0 and tahun_awal in matriks.columns and tahun_akhir in matriks.columns:
    awal_w = matriks[tahun_awal]
    akhir_w = matriks[tahun_akhir]
    valid = (awal_w > 0) & (akhir_w > 0)
    cagr = (((akhir_w[valid] / awal_w[valid]) ** (1 / jumlah_tahun) - 1) * 100)
    cagr = cagr.rename("Laju_Pertumbuhan_per_Tahun").reset_index().sort_values(
        "Laju_Pertumbuhan_per_Tahun", ascending=False
    )

awal_total = data_tahun.iloc[0][KOLOM]
akhir_total = data_tahun.iloc[-1][KOLOM]
perubahan_total = akhir_total - awal_total
persen_total = perubahan_total / awal_total * 100 if awal_total else 0

# ==================================================
# 7. HERO
# ==================================================

st.markdown(f"""
<div class="hero">
    <h1>Jumlah penduduk Sulawesi Selatan, wilayah demi wilayah</h1>
    <p>Pantau sebaran dan perkembangan penduduk {df[WILAYAH].nunique()} kabupaten/kota
    pada {tahun_awal}–{tahun_akhir}, dari tingkat provinsi sampai tiap wilayah.</p>
    <div class="hero-meta">
        <div><b>{fmt(total_pilihan, 0)} ribu</b>penduduk provinsi, {tahun_pilihan}</div>
        <div><b>{df[WILAYAH].nunique()}</b>kabupaten/kota</div>
        <div><b>{len(daftar_tahun)} tahun</b>data pengamatan</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 8. MENU RINGKASAN
# ==================================================

if menu == "Ringkasan":

    # Pertumbuhan dibanding tahun sebelumnya
    delta_teks = None
    sebelumnya = data_tahun[data_tahun["Tahun"] == tahun_pilihan - 1]
    if not sebelumnya.empty:
        selisih = total_pilihan - sebelumnya.iloc[0][KOLOM]
        delta_teks = f"{fmt(selisih)} ribu vs {tahun_pilihan - 1}"

    terbesar_w = data_perbandingan.iloc[0]
    terkecil_w = data_perbandingan.iloc[-1]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(f"Total penduduk {tahun_pilihan}", f"{fmt(total_pilihan)} ribu", delta_teks)
    k2.metric("Rata-rata per wilayah", f"{fmt(data_pilihan[KOLOM].mean())} ribu")
    k3.metric("Wilayah terbanyak", terbesar_w[WILAYAH], f"{fmt(terbesar_w['Kontribusi_Persen'])}% dari provinsi", delta_color="off")
    k4.metric("Wilayah tersedikit", terkecil_w[WILAYAH], f"{fmt(terkecil_w['Kontribusi_Persen'])}% dari provinsi", delta_color="off")

    # Tren
    if wilayah_pilihan == "Semua Kabupaten/Kota":
        judul("Perkembangan jumlah penduduk provinsi",
              "Jumlah seluruh kabupaten/kota pada setiap tahun. Titik berwarna kuningan menandai tahun yang dipilih.")
        tren = data_tahun
    else:
        judul(f"Perkembangan jumlah penduduk {wilayah_pilihan}",
              "Tren satu wilayah sesuai filter di sidebar. Titik berwarna kuningan menandai tahun yang dipilih.")
        tren = df[df[WILAYAH] == wilayah_pilihan].sort_values("Tahun")

    fig_line = px.area(tren, x="Tahun", y=KOLOM, markers=True,
                       color_discrete_sequence=[HIJAU],
                       labels={KOLOM: "Jumlah penduduk (ribu jiwa)"})
    fig_line.update_traces(
        line=dict(width=3), marker=dict(size=9),
        fillcolor="rgba(31,107,79,0.12)",
        hovertemplate="Tahun %{x}<br>%{y:,.2f} ribu jiwa<extra></extra>",
    )
    titik = tren[tren["Tahun"] == tahun_pilihan]
    fig_line.add_trace(go.Scatter(
        x=titik["Tahun"], y=titik[KOLOM], mode="markers", showlegend=False,
        marker=dict(size=16, color=KUNINGAN, line=dict(width=2, color="white")),
        hoverinfo="skip",
    ))
    fig_line.update_xaxes(dtick=1)
    st.plotly_chart(tata_grafik(fig_line, 380), width="stretch")

    # Perbandingan wilayah
    judul(f"Peringkat wilayah menurut jumlah penduduk, {tahun_pilihan}",
          "Batang disusun dari yang terbanyak. Wilayah yang dipilih di sidebar ditandai warna kuningan.")

    tab_bar, tab_tree = st.tabs(["Peringkat", "Komposisi"])

    with tab_bar:
        urut = data_perbandingan.sort_values(KOLOM, ascending=True).copy()
        urut["Warna"] = urut[WILAYAH].apply(
            lambda w: KUNINGAN if w == wilayah_pilihan else HIJAU
        )
        fig_bar = go.Figure(go.Bar(
            x=urut[KOLOM], y=urut[WILAYAH], orientation="h",
            marker_color=urut["Warna"],
            customdata=urut["Kontribusi_Persen"],
            hovertemplate="%{y}<br>%{x:,.2f} ribu jiwa (%{customdata:.2f}%)<extra></extra>",
        ))
        fig_bar.update_xaxes(title="Jumlah penduduk (ribu jiwa)")
        st.plotly_chart(tata_grafik(fig_bar, max(420, 26 * len(urut))), width="stretch")

    with tab_tree:
        fig_tree = px.treemap(
            data_perbandingan, path=[WILAYAH], values=KOLOM, color=KOLOM,
            color_continuous_scale=[HIJAU_MUDA, HIJAU, HIJAU_TUA],
        )
        fig_tree.update_traces(
            hovertemplate="%{label}<br>%{value:,.2f} ribu jiwa<extra></extra>",
            textfont=dict(family="IBM Plex Sans", size=14),
        )
        fig_tree.update_layout(coloraxis_showscale=False)
        st.plotly_chart(tata_grafik(fig_tree, 460), width="stretch")
        st.caption("Luas kotak menunjukkan porsi tiap wilayah terhadap total penduduk provinsi.")

    # Temuan
    judul("Temuan utama")

    if perubahan_total > 0:
        kondisi = "bertambah"
    elif perubahan_total < 0:
        kondisi = "berkurang"
    else:
        kondisi = "tidak berubah"

    tiga_besar = data_perbandingan.head(3)
    porsi_tiga = tiga_besar["Kontribusi_Persen"].sum()
    nama_tiga = ", ".join(tiga_besar[WILAYAH].tolist())

    st.markdown(f"""
    <div class="insight">
    Pada <b>{tahun_awal}–{tahun_akhir}</b>, jumlah penduduk provinsi <b>{kondisi}</b>
    sebesar <b>{fmt(abs(perubahan_total))} ribu jiwa</b> ({fmt(abs(persen_total))}%).
    </div>
    <div class="insight">
    Pada {tahun_pilihan}, tiga wilayah terbanyak (<b>{nama_tiga}</b>) menampung
    <b>{fmt(porsi_tiga)}%</b> penduduk provinsi.
    </div>
    """, unsafe_allow_html=True)

    if cagr is not None and not cagr.empty:
        tercepat = cagr.iloc[0]
        terlambat = cagr.iloc[-1]
        st.markdown(f"""
        <div class="insight">
        Laju pertumbuhan tahunan tertinggi ada di <b>{tercepat[WILAYAH]}</b>
        ({fmt(tercepat['Laju_Pertumbuhan_per_Tahun'])}% per tahun), dan terendah di
        <b>{terlambat[WILAYAH]}</b> ({fmt(terlambat['Laju_Pertumbuhan_per_Tahun'])}% per tahun).
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# 9. MENU DATA KEPENDUDUKAN
# ==================================================

elif menu == "Data Kependudukan":

    judul("Data kependudukan",
          f"Tahun {tahun_pilihan}, wilayah: {wilayah_pilihan}. Ubah filter di sidebar untuk memperbarui tabel.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Baris ditampilkan", fmt(len(data_filter), 0))
    c2.metric("Jumlah wilayah", fmt(data_filter[WILAYAH].nunique(), 0))
    c3.metric("Total penduduk", f"{fmt(data_filter[KOLOM].sum())} ribu")

    tampil = data_filter.rename(columns={
        KOLOM: "Jumlah Penduduk (ribu jiwa)",
        "Kontribusi_Persen": "Kontribusi (%)",
    })
    st.dataframe(
        tampil.style.format({
            "Jumlah Penduduk (ribu jiwa)": "{:,.2f}",
            "Kontribusi (%)": "{:.2f}",
        }),
        width="stretch", hide_index=True,
    )

    csv_data = data_filter.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Unduh data CSV", data=csv_data,
        file_name=f"data_kependudukan_{tahun_pilihan}.csv", mime="text/csv",
    )

# ==================================================
# 10. MENU ANALISIS PERKEMBANGAN
# ==================================================

elif menu == "Analisis Perkembangan":

    judul("Analisis perkembangan penduduk",
          "Perubahan dihitung dari jumlah seluruh kabupaten/kota pada setiap tahun.")

    data_perubahan = perkembangan.dropna(subset=["Perubahan_Penduduk"])

    if not data_perubahan.empty:
        naik = data_perubahan.loc[data_perubahan["Perubahan_Penduduk"].idxmax()]
        turun = data_perubahan.loc[data_perubahan["Perubahan_Penduduk"].idxmin()]
        rata = data_perubahan["Persentase_Perubahan"].mean()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Perubahan total", f"{fmt(perubahan_total)} ribu", f"{fmt(persen_total)}%")
        m2.metric("Rata-rata per tahun", f"{fmt(rata)}%")
        m3.metric("Kenaikan terbesar", f"{fmt(naik['Perubahan_Penduduk'])} ribu", f"Tahun {int(naik['Tahun'])}", delta_color="off")
        m4.metric("Kenaikan terkecil", f"{fmt(turun['Perubahan_Penduduk'])} ribu", f"Tahun {int(turun['Tahun'])}", delta_color="off")

    tab1, tab2, tab3 = st.tabs(["Per tahun", "Per wilayah", "Peta panas"])

    with tab1:
        st.dataframe(
            perkembangan.rename(columns={
                KOLOM: "Jumlah Penduduk (ribu jiwa)",
                "Perubahan_Penduduk": "Perubahan (ribu jiwa)",
                "Persentase_Perubahan": "Perubahan (%)",
            }).style.format({
                "Jumlah Penduduk (ribu jiwa)": "{:,.2f}",
                "Perubahan (ribu jiwa)": "{:,.2f}",
                "Perubahan (%)": "{:.2f}%",
            }),
            width="stretch", hide_index=True,
        )
        fig_growth = px.bar(
            data_perubahan, x="Tahun", y="Persentase_Perubahan",
            color_discrete_sequence=[HIJAU],
            labels={"Persentase_Perubahan": "Perubahan (%)"},
            title="Persentase perubahan penduduk provinsi per tahun",
        )
        fig_growth.update_xaxes(dtick=1)
        st.plotly_chart(tata_grafik(fig_growth, 360), width="stretch")

    with tab2:
        if cagr is not None and not cagr.empty:
            st.caption(
                f"Laju pertumbuhan tahunan majemuk tiap wilayah, {tahun_awal}–{tahun_akhir}."
            )
            urut_c = cagr.sort_values("Laju_Pertumbuhan_per_Tahun", ascending=True)
            fig_c = go.Figure(go.Bar(
                x=urut_c["Laju_Pertumbuhan_per_Tahun"], y=urut_c[WILAYAH], orientation="h",
                marker_color=[KUNINGAN if v < 0 else HIJAU for v in urut_c["Laju_Pertumbuhan_per_Tahun"]],
                hovertemplate="%{y}<br>%{x:.2f}% per tahun<extra></extra>",
            ))
            fig_c.update_xaxes(title="Pertumbuhan per tahun (%)")
            st.plotly_chart(tata_grafik(fig_c, max(420, 26 * len(urut_c))), width="stretch")
        else:
            st.info("Data belum cukup untuk menghitung laju pertumbuhan per wilayah.")

    with tab3:
        st.caption("Warna semakin gelap berarti jumlah penduduk semakin besar.")
        fig_heat = px.imshow(
            matriks.sort_values(tahun_akhir, ascending=False) if tahun_akhir in matriks.columns else matriks,
            aspect="auto", color_continuous_scale=[BETON, HIJAU, HIJAU_TUA],
            labels=dict(x="Tahun", y="Kabupaten/Kota", color="Ribu jiwa"),
        )
        fig_heat.update_xaxes(dtick=1)
        st.plotly_chart(tata_grafik(fig_heat, max(460, 24 * len(matriks))), width="stretch")

    st.markdown(f"""
    <div class="insight">
    Selama <b>{tahun_awal}–{tahun_akhir}</b>, jumlah penduduk provinsi berubah sebesar
    <b>{fmt(perubahan_total)} ribu jiwa</b> ({fmt(persen_total)}%).
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# 11. MENU TENTANG APLIKASI
# ==================================================

elif menu == "Tentang Aplikasi":

    judul("Tentang aplikasi")

    a, b = st.columns(2)
    with a:
        st.markdown("""
**Fungsi**

Aplikasi ini menampilkan, mengolah, dan memvisualisasikan jumlah penduduk
kabupaten/kota di Provinsi Sulawesi Selatan.

**Yang bisa dilakukan**

1. Melihat ringkasan dan temuan utama per tahun.
2. Membandingkan jumlah penduduk antarwilayah.
3. Menelusuri tren dan laju pertumbuhan tiap wilayah.
4. Menyaring data dan mengunduhnya sebagai CSV.
        """)
    with b:
        st.markdown(f"""
**Data**

- Sumber: Badan Pusat Statistik (BPS) Provinsi Sulawesi Selatan
- Periode: {tahun_awal}–{tahun_akhir}
- Satuan: ribu jiwa
- Cakupan: {df[WILAYAH].nunique()} kabupaten/kota

**Metode**

- Pembersihan data
- Analisis deskriptif
- Perubahan tahunan dan laju pertumbuhan majemuk
- Visualisasi interaktif

**Teknologi**

Python, Streamlit, Pandas, Plotly
        """)

# ==================================================
# 12. FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    <b>Atlas Kependudukan Sulawesi Selatan</b><br>
    Dibangun dengan Python, Streamlit, Pandas, dan Plotly. Sumber data: BPS Provinsi Sulawesi Selatan.
</div>
""", unsafe_allow_html=True)