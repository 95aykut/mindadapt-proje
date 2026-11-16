import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="MindAdapt | Ortaokul Siber Psikoloji Ara?t?rmas?",
    page_icon="??",
    layout="centered"
)

# --- VER? DOSYASI AYARLARI ---
DATA_FILE = "mindadapt_ortaokul_verileri.csv"

# --- ORTAOKUL DUZEY?NE UYARLANMI? SORU HAVUZU ---
MINDADAPT_OOL_POOL = [
    # Boyut A: Bildirim Hassasiyeti
    {"id": "A_1_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Tabletimin veya telefonumun ekran? yand???nda hemen bakma iste?i duyar?m."},
    {"id": "A_1_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Ders cal???rken veya odev yaparken gelen bildirim sesleri dikkatimi da??t?r."},
    {"id": "A_1_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Arkada? gruplar?mdan art arda mesaj geldi?inde merak edip hemen acar?m."},
    {"id": "A_2_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Gelen bir mesaja bakt?ktan sonra kendimi ba?ka oyun veya uygulamalarda gezinirken bulurum."},
    {"id": "A_2_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Bilgisayarda odev yaparken ekranda beliren uyar?lar okudu?um soruyu unutturur."},
    {"id": "A_2_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Ders s?ras?nda telefonumu veya tabletimi gozumun onunden ay?rmakta zorlan?r?m."},
    {"id": "A_3_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Hic ses gelmese bile akl?ma 'acaba yeni bir ?ey payla?t?lar m??' du?uncesi gelir."},
    {"id": "A_3_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Cihaz?m ba?ka bir odada olsa bile akl?m surekli oradad?r, gidip kontrol etme ihtiyac? duyar?m."},
    {"id": "A_3_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Telefonuma yeni bir bildirim geldi?inde ona hemen bakmazsam dersime odaklanamam."},

    # Boyut B: Dijital Coklu Gorev
    {"id": "B_1_1", "boyut": "Dijital Coklu Gorev", "zorluk": 1, "metin": "Bilgisayarda ders cal???rken arka planda hep muzik veya video ac?k olsun isterim."},
    {"id": "B_1_2", "boyut": "Dijital Coklu Gorev", "zorluk": 1, "metin": "?nternette odev ararken ayn? anda bircok sekme (pencere) ac?k olur."},
    {"id": "B_1_3", "boyut": "Dijital Coklu Gorev", "zorluk": 1, "metin": "Televizyonda cizgi film veya video izlerken elimde telefonla da oynar?m."},
    {"id": "B_2_1", "boyut": "Dijital Coklu Gorev", "zorluk": 2, "metin": "E?itici bir video izlerken s?k s?k videoyu durdurup sosyal medyaya veya oyuna bakar?m."},
    {"id": "B_2_2", "boyut": "Dijital Coklu Gorev", "zorluk": 2, "metin": "Ara?t?rma yaparken kendimi birdenbire komik videolar izlerken bulurum."},
    {"id": "B_2_3", "boyut": "Dijital Coklu Gorev", "zorluk": 2, "metin": "Ayn? anda hem arkada??ma mesaj yaz?p hem ders yapmaya cal???nca ikisinde de kafam kar???r."},
    {"id": "B_3_1", "boyut": "Dijital Coklu Gorev", "zorluk": 3, "metin": "10-15 dakikal?k bir videoyu ba?ka hicbir yere bakmadan tek seferde bitirmekte zorlan?r?m."},
    {"id": "B_3_2", "boyut": "Dijital Coklu Gorev", "zorluk": 3, "metin": "Bir oyundan c?k?p saniyeler sonra fark?nda olmadan tekrar ayn? oyuna t?klad???m olur."},
    {"id": "B_3_3", "boyut": "Dijital Coklu Gorev", "zorluk": 3, "metin": "Tek bir ?eye odakland???mda cabuk s?k?l?r?m, hemen ba?ka bir ekrana gecmek isterim."},

    # Boyut C: Bili?sel Derinle?me Kayb?
    {"id": "C_1_1", "boyut": "Bili?sel Derinle?me", "zorluk": 1, "metin": "Ekranda uzun bir metin okurken sat?rlar? atlad???m? veya ba?a donmek zorunda kald???m? fark ederim."},
    {"id": "C_1_2", "boyut": "Bili?sel Derinle?me", "zorluk": 1, "metin": "Cok fazla ekran kar??s?nda kald???mda gozlerimde ve kafamda yorgunluk hissederim."},
    {"id": "C_1_3", "boyut": "Bili?sel Derinle?me", "zorluk": 1, "metin": "Uzun yaz?lar? okumak yerine resimli veya k?sa ozetleri tercih ederim."},
    {"id": "C_2_1", "boyut": "Bili?sel Derinle?me", "zorluk": 2, "metin": "Telefona bakt?ktan sonra yar?m b?rakt???m bir matematik sorusuna kafam? tekrar toplamak zor gelir."},
    {"id": "C_2_2", "boyut": "Bili?sel Derinle?me", "zorluk": 2, "metin": "K?sa videolar (Reels/TikTok/Shorts) izledikten sonra normal ders videolar? bana cok yava? gelir."},
    {"id": "C_2_3", "boyut": "Bili?sel Derinle?me", "zorluk": 2, "metin": "Bildirim yuzunden bolundu?um bir derse tekrar ayn? dikkatle donmem uzun surer."},
    {"id": "C_3_1", "boyut": "Bili?sel Derinle?me", "zorluk": 3, "metin": "Cok fazla ekran kulland?ktan sonra normal bir hikaye kitab?n? bile anlamakta zorlan?r?m."},
    {"id": "C_3_2", "boyut": "Bili?sel Derinle?me", "zorluk": 3, "metin": "Gun icinde surekli ekran de?i?tirmek beni o kadar yorar ki ak?am ders cal??mak istemem."},
    {"id": "C_3_3", "boyut": "Bili?sel Derinle?me", "zorluk": 3, "metin": "Zor bir problemi cozerken akl?mdaki say?lar? ve ad?mlar? bir arada tutmakta zorlan?r?m."}
]

# Standart Olcek Maddeleri (12 Soru)
STANDART_OOL_POOL = [
    {"id": "STD_1", "boyut": "Standart", "zorluk": 2, "metin": "Ders cal???rken tabletimin veya telefonumun sesini kapatmam gereksiz gelir."},
    {"id": "STD_2", "boyut": "Standart", "zorluk": 2, "metin": "Onemli bir konuyu anlamaya cal???rken sosyal medya mesajlar? dikkatimi da??t?r."},
    {"id": "STD_3", "boyut": "Standart", "zorluk": 2, "metin": "Bilgisayarda odev yaparken ayn? anda farkl? oyun veya siteleri ac?k tutar?m."},
    {"id": "STD_4", "boyut": "Standart", "zorluk": 2, "metin": "Telefonumdan ses gelmese bile cebime al?p s?k s?k kontrol ederim."},
    {"id": "STD_5", "boyut": "Standart", "zorluk": 2, "metin": "Ekranlara bakt?ktan sonra okudu?um ders konusunu anlamakta zorlan?r?m."},
    {"id": "STD_6", "boyut": "Standart", "zorluk": 2, "metin": "Video izlerken ayn? anda ba?ka dijital ?eylerle de ilgilenirim."},
    {"id": "STD_7", "boyut": "Standart", "zorluk": 2, "metin": "Gelen mesajlara hemen cevap vermezsem huzursuz olurum."},
    {"id": "STD_8", "boyut": "Standart", "zorluk": 2, "metin": "Dijital cihazlar yan?mdayken odevimi bitirmem cok daha uzun surer."},
    {"id": "STD_9", "boyut": "Standart", "zorluk": 2, "metin": "?nternette odev ararken ilgisiz ba?ka sayfalara dal?p giderim."},
    {"id": "STD_10", "boyut": "Standart", "zorluk": 2, "metin": "K?sa videolar izledikten sonra uzun dersleri dinlemekte s?k?l?r?m."},
    {"id": "STD_11", "boyut": "Standart", "zorluk": 2, "metin": "Masamda telefon dururken akl?m surekli ondad?r."},
    {"id": "STD_12", "boyut": "Standart", "zorluk": 2, "metin": "Gun icinde dijital ekranlar yuzunden zihinsel olarak cabuk yorulurum."}
]

def select_next_adaptive_question(asked_ids, history):
    available = [q for q in MINDADAPT_OOL_POOL if q["id"] not in asked_ids]
    if not available:
        return None
    dimensions = ["Bildirim Hassasiyeti", "Dijital Coklu Gorev", "Bili?sel Derinle?me"]
    if len(history) < 3:
        target_dim = dimensions[len(history)]
        candidates = [q for q in available if q["boyut"] == target_dim and q["zorluk"] == 2]
        return candidates[0] if candidates else available[0]
    dim_scores = {d: [] for d in dimensions}
    for h in history:
        dim_scores[h["boyut"]].append(h["puan"])
    best_dim = dimensions[0]
    max_priority = -1
    for d in dimensions:
        scores = dim_scores[d]
        count = len(scores)
        mean_val = np.mean(scores) if scores else 2.5
        std_val = np.std(scores) if count > 1 else 1.5
        priority = (std_val * 1.2) + (mean_val / 5.0) - (count * 0.45)
        if priority > max_priority:
            max_priority = priority
            best_dim = d
    last_score_in_dim = dim_scores[best_dim][-1] if dim_scores[best_dim] else 3
    if last_score_in_dim >= 4:
        target_diff = 3
    elif last_score_in_dim <= 2:
        target_diff = 1
    else:
        target_diff = 2
    candidates = [q for q in available if q["boyut"] == best_dim and q["zorluk"] == target_diff]
    if not candidates:
        candidates = [q for q in available if q["boyut"] == best_dim]
    if not candidates:
        candidates = available
    return candidates[0]

def save_results(participant_id, grade, gender, group_type, test_type, history, total_duration):
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mean_score = round(np.mean([h["puan"] for h in history]), 2)
    for idx, item in enumerate(history, 1):
        rows.append({
            "Tarih": timestamp,
            "Katilimci_Kodu": participant_id,
            "Sinif": grade,
            "Cinsiyet": gender,
            "Deney_Grubu": group_type,
            "Test_Modu": test_type,
            "Soru_Sirasi": idx,
            "Soru_ID": item["id"],
            "Alt_Boyut": item["boyut"],
            "Verilen_Puan": item["puan"],
            "Tepki_Suresi_Sn": round(item["sure"], 3),
            "Toplam_Sure_Sn": round(total_duration, 2),
            "Ortalama_Puan": mean_score
        })
    df_new = pd.DataFrame(rows)
    if os.path.exists(DATA_FILE):
        df_new.to_csv(DATA_FILE, mode="a", header=False, index=False, encoding="utf-8-sig")
    else:
        df_new.to_csv(DATA_FILE, mode="w", header=True, index=False, encoding="utf-8-sig")

if "step" not in st.session_state:
    st.session_state.step = "intro"
if "history" not in st.session_state:
    st.session_state.history = []
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "q_start_time" not in st.session_state:
    st.session_state.q_start_time = None
if "test_start_time" not in st.session_state:
    st.session_state.test_start_time = None

# --- G?ZL? ARA?TIRMACI PANEL? (??FRE KORUMALI) ---
with st.sidebar:
    st.header("?? Ara?t?rmac? Paneli")
    st.caption("20+20 = 40 O?renci Deney Kontrolu")
    teacher_password = st.text_input("O?retmen ?ifresi", type="password")
    if teacher_password == "2204Bilsim":
        st.success("?? Yetkili Giri?i Sa?land?")
        if os.path.exists(DATA_FILE):
            df_all = pd.read_csv(DATA_FILE)
            st.metric("Toplam Kat?l?mc?", df_all["Katilimci_Kodu"].nunique())
            st.metric("Toplam Yan?t", len(df_all))
            csv_data = df_all.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="?? Tum Verileri ?ndir (CSV)",
                data=csv_data,
                file_name=f"MindAdapt_Ortaokul_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            if st.button("??? Verileri S?f?rla"):
                os.remove(DATA_FILE)
                st.rerun()
        else:
            st.info("Henuz veri kaydedilmedi.")
    else:
        st.info("Verileri gormek ve indirmek icin o?retmen ?ifresini giriniz.")

# --- EKRAN 1: O?RENC? G?R??? ---
if st.session_state.step == "intro":
    st.title("?? MindAdapt: Dijital Odaklanma Cal??mas?")
    st.markdown("Merhaba sevgili o?rencimiz! Bu cal??ma, dijital cihazlar? kullan?rken odaklanma durumumuzu incelemek icin yap?lmaktad?r.")
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            p_id = st.text_input("O?renci Kodunuz *", placeholder="Orn: OGR-01")
            grade = st.selectbox("S?n?f Duzeyi", ["5. S?n?f", "6. S?n?f", "7. S?n?f", "8. S?n?f"])
        with col2:
            group_type = st.selectbox("Deney Grubunuz *", ["Grup A (1. Oturum)", "Grup B (1. Oturum)"])
            test_mode = st.selectbox("Test Turu *", ["MindAdapt (AI Adaptif - 7 Soru)", "Standart Olcek (12 Soru)"])
            gender = st.selectbox("Cinsiyet", ["K?z", "Erkek", "Belirtmek ?stemiyorum"])
        submitted = st.form_submit_button("Teste Ba?la ??", use_container_width=True)
        if submitted:
            if not p_id.strip():
                st.error("Lutfen o?renci kodunuzu yaz?n?z.")
            else:
                st.session_state.p_id = p_id.strip().upper()
                st.session_state.grade = grade
                st.session_state.group_type = group_type
                st.session_state.test_mode = test_mode
                st.session_state.gender = gender
                st.session_state.history = []
                st.session_state.test_start_time = time.time()
                if "Standart" in test_mode:
                    st.session_state.current_q = STANDART_OOL_POOL[0]
                else:
                    st.session_state.current_q = select_next_adaptive_question([], [])
                st.session_state.q_start_time = time.time()
                st.session_state.step = "test"
                st.rerun()

# --- EKRAN 2: TEST UYGULAMA ---
elif st.session_state.step == "test":
    is_standard = "Standart" in st.session_state.test_mode
    max_questions = len(STANDART_OOL_POOL) if is_standard else 7
    current_idx = len(st.session_state.history) + 1
    st.progress((current_idx - 1) / max_questions)
    st.caption(f"Grup: **{st.session_state.group_type}** | Soru **{current_idx} / {max_questions}**")
    q = st.session_state.current_q
    st.markdown(f"### {q['metin']}")
    st.write("")
    options = {1: "1 ¡X Hicbir zaman", 2: "2 ¡X Nadiren", 3: "3 ¡X Bazen", 4: "4 ¡X S?k s?k", 5: "5 ¡X Her zaman"}
    choice = st.radio("Sana en uygun olan? sec:", options=list(options.keys()), format_func=lambda x: options[x], index=None, key=f"radio_{q['id']}_{current_idx}")
    st.write("")
    if st.button("Cevapla ve Devam Et ??", use_container_width=True):
        if choice is None:
            st.warning("Lutfen bir secenek i?aretle.")
        else:
            elapsed = time.time() - st.session_state.q_start_time
            st.session_state.history.append({"id": q["id"], "boyut": q["boyut"], "zorluk": q["zorluk"], "puan": choice, "sure": elapsed})
            if len(st.session_state.history) >= max_questions:
                total_time = time.time() - st.session_state.test_start_time
                save_results(st.session_state.p_id, st.session_state.grade, st.session_state.gender, st.session_state.group_type, st.session_state.test_mode, st.session_state.history, total_time)
                st.session_state.total_time = total_time
                st.session_state.step = "result"
                st.rerun()
            else:
                if is_standard:
                    st.session_state.current_q = STANDART_OOL_POOL[len(st.session_state.history)]
                else:
                    asked = [h["id"] for h in st.session_state.history]
                    st.session_state.current_q = select_next_adaptive_question(asked, st.session_state.history)
                st.session_state.q_start_time = time.time()
                st.rerun()

# --- EKRAN 3: SONUC ---
elif st.session_state.step == "result":
    st.balloons()
    st.success("?? Kat?l?m?n icin cok te?ekkur ederiz! Cevaplar?n guvenle kaydedildi.")
    df_hist = pd.DataFrame(st.session_state.history)
    avg_score = df_hist["puan"].mean()
    c1, c2, c3 = st.columns(3)
    c1.metric("Cozulen Soru", f"{len(df_hist)} Soru")
    c2.metric("Toplam Sure", f"{st.session_state.total_time:.1f} sn")
    c3.metric("Ortalama Puan", f"{avg_score:.2f} / 5.00")
    if "MindAdapt" in st.session_state.test_mode:
        st.subheader("?? Dijital Odaklanma Profilin")
        dim_means = df_hist.groupby("boyut")["puan"].mean().reindex(["Bildirim Hassasiyeti", "Dijital Coklu Gorev", "Bili?sel Derinle?me"], fill_value=0)
        fig = go.Figure(data=go.Scatterpolar(r=dim_means.values, theta=dim_means.index, fill='toself', line_color='#2563EB'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=320)
        st.plotly_chart(fig, use_container_width=True)
        st.info("?? Not: Bu cal??ma tamamen bilimsel fark?ndal?k icindir.")
    if st.button("Yeni O?renci Giri?i ??", use_container_width=True):
        st.session_state.step = "intro"
        st.rerun()