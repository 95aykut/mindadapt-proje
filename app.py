import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime
import plotly.graph_objects as go

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="MindAdapt | Ortaokul Siber Psikoloji Araştırması",
    page_icon="🧠",
    layout="centered"
)

# --- VERİ DOSYASI AYARLARI ---
DATA_FILE = "mindadapt_ortaokul_verileri.csv"

# --- ORTAOKUL DÜZEYİNE UYARLANMIŞ SORU HAVUZU ---
MINDADAPT_OOL_POOL = [
    # Boyut A: Bildirim Hassasiyeti
    {"id": "A_1_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Tabletimin veya telefonumun ekranı yandığında hemen bakma isteği duyarım."},
    {"id": "A_1_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Ders çalışırken veya ödev yaparken gelen bildirim sesleri dikkatimi dağıtır."},
    {"id": "A_1_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 1, "metin": "Arkadaş gruplarımdan art arda mesaj geldiğinde merak edip hemen açarım."},
    {"id": "A_2_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Gelen bir mesaja baktıktan sonra kendimi başka oyun veya uygulamalarda gezinirken bulurum."},
    {"id": "A_2_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Bilgisayarda ödev yaparken ekranda beliren uyarılar okuduğum soruyu unutturur."},
    {"id": "A_2_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 2, "metin": "Ders sırasında telefonumu veya tabletimi gözümün önünden ayırmakta zorlanırım."},
    {"id": "A_3_1", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Hiç ses gelmese bile aklıma 'acaba yeni bir şey paylaştılar mı?' düşüncesi gelir."},
    {"id": "A_3_2", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Cihazım başka bir odada olsa bile aklım sürekli oradadır, gidip kontrol etme ihtiyacı duyarım."},
    {"id": "A_3_3", "boyut": "Bildirim Hassasiyeti", "zorluk": 3, "metin": "Telefonuma yeni bir bildirim geldiğinde ona hemen bakmazsam dersime odaklanamam."},

    # Boyut B: Dijital Çoklu Görev
    {"id": "B_1_1", "boyut": "Dijital Çoklu Görev", "zorluk": 1, "metin": "Bilgisayarda ders çalışırken arka planda hep müzik veya video açık olsun isterim."},
    {"id": "B_1_2", "boyut": "Dijital Çoklu Görev", "zorluk": 1, "metin": "İnternette ödev ararken aynı anda birçok sekme (pencere) açık olur."},
    {"id": "B_1_3", "boyut": "Dijital Çoklu Görev", "zorluk": 1, "metin": "Televizyonda çizgi film veya video izlerken elimde telefonla da oynarım."},
    {"id": "B_2_1", "boyut": "Dijital Çoklu Görev", "zorluk": 2, "metin": "Eğitici bir video izlerken sık sık videoyu durdurup sosyal medyaya veya oyuna bakarım."},
    {"id": "B_2_2", "boyut": "Dijital Çoklu Görev", "zorluk": 2, "metin": "Araştırma yaparken kendimi birdenbire komik videolar izlerken bulurum."},
    {"id": "B_2_3", "boyut": "Dijital Çoklu Görev", "zorluk": 2, "metin": "Aynı anda hem arkadaşıma mesaj yazıp hem ders yapmaya çalışınca ikisinde de kafam karışır."},
    {"id": "B_3_1", "boyut": "Dijital Çoklu Görev", "zorluk": 3, "metin": "10-15 dakikalık bir videoyu başka hiçbir yere bakmadan tek seferde bitirmekte zorlanırım."},
    {"id": "B_3_2", "boyut": "Dijital Çoklu Görev", "zorluk": 3, "metin": "Bir oyundan çıkıp saniyeler sonra farkında olmadan tekrar aynı oyuna tıkladığım olur."},
    {"id": "B_3_3", "boyut": "Dijital Çoklu Görev", "zorluk": 3, "metin": "Tek bir şeye odaklandığımda çabuk sıkılırım, hemen başka bir ekrana geçmek isterim."},

    # Boyut C: Bilişsel Derinleşme Kaybı
    {"id": "C_1_1", "boyut": "Bilişsel Derinleşme", "zorluk": 1, "metin": "Ekranda uzun bir metin okurken satırları atladığımı veya başa dönmek zorunda kaldığımı fark ederim."},
    {"id": "C_1_2", "boyut": "Bilişsel Derinleşme", "zorluk": 1, "metin": "Çok fazla ekran karşısında kaldığımda gözlerimde ve kafamda yorgunluk hissederim."},
    {"id": "C_1_3", "boyut": "Bilişsel Derinleşme", "zorluk": 1, "metin": "Uzun yazıları okumak yerine resimli veya kısa özetleri tercih ederim."},
    {"id": "C_2_1", "boyut": "Bilişsel Derinleşme", "zorluk": 2, "metin": "Telefona baktıktan sonra yarım bıraktığım bir matematik sorusuna kafamı tekrar toplamak zor gelir."},
    {"id": "C_2_2", "boyut": "Bilişsel Derinleşme", "zorluk": 2, "metin": "Kısa videolar (Reels/TikTok/Shorts) izledikten sonra normal ders videoları bana çok yavaş gelir."},
    {"id": "C_2_3", "boyut": "Bilişsel Derinleşme", "zorluk": 2, "metin": "Bildirim yüzünden bölündüğüm bir derse tekrar aynı dikkatle dönmem uzun sürer."},
    {"id": "C_3_1", "boyut": "Bilişsel Derinleşme", "zorluk": 3, "metin": "Çok fazla ekran kullandıktan sonra normal bir hikaye kitabını bile anlamakta zorlanırım."},
    {"id": "C_3_2", "boyut": "Bilişsel Derinleşme", "zorluk": 3, "metin": "Gün içinde sürekli ekran değiştirmek beni o kadar yorar ki akşam ders çalışmak istemem."},
    {"id": "C_3_3", "boyut": "Bilişsel Derinleşme", "zorluk": 3, "metin": "Zor bir problemi çözerken aklımdaki sayıları ve adımları bir arada tutmakta zorlanırım."}
]

# Standart Ölçek Maddeleri (12 Soru)
STANDART_OOL_POOL = [
    {"id": "STD_1", "boyut": "Standart", "zorluk": 2, "metin": "Ders çalışırken tabletimin veya telefonumun sesini kapatmam gereksiz gelir."},
    {"id": "STD_2", "boyut": "Standart", "zorluk": 2, "metin": "Önemli bir konuyu anlamaya çalışırken sosyal medya mesajları dikkatimi dağıtır."},
    {"id": "STD_3", "boyut": "Standart", "zorluk": 2, "metin": "Bilgisayarda ödev yaparken aynı anda farklı oyun veya siteleri açık tutarım."},
    {"id": "STD_4", "boyut": "Standart", "zorluk": 2, "metin": "Telefonumdan ses gelmese bile cebime alıp sık sık kontrol ederim."},
    {"id": "STD_5", "boyut": "Standart", "zorluk": 2, "metin": "Ekranlara baktıktan sonra okuduğum ders konusunu anlamakta zorlanırım."},
    {"id": "STD_6", "boyut": "Standart", "zorluk": 2, "metin": "Video izlerken aynı anda başka dijital şeylerle de ilgilenirim."},
    {"id": "STD_7", "boyut": "Standart", "zorluk": 2, "metin": "Gelen mesajlara hemen cevap vermezsem huzursuz olurum."},
    {"id": "STD_8", "boyut": "Standart", "zorluk": 2, "metin": "Dijital cihazlar yanımdayken ödevimi bitirmem çok daha uzun sürer."},
    {"id": "STD_9", "boyut": "Standart", "zorluk": 2, "metin": "İnternette ödev ararken ilgisiz başka sayfalara dalıp giderim."},
    {"id": "STD_10", "boyut": "Standart", "zorluk": 2, "metin": "Kısa videolar izledikten sonra uzun dersleri dinlemekte sıkılırım."},
    {"id": "STD_11", "boyut": "Standart", "zorluk": 2, "metin": "Masamda telefon dururken aklım sürekli ondadır."},
    {"id": "STD_12", "boyut": "Standart", "zorluk": 2, "metin": "Gün içinde dijital ekranlar yüzünden zihinsel olarak çabuk yorulurum."}
]

def select_next_adaptive_question(asked_ids, history):
    available = [q for q in MINDADAPT_OOL_POOL if q["id"] not in asked_ids]
    if not available:
        return None
    dimensions = ["Bildirim Hassasiyeti", "Dijital Çoklu Görev", "Bilişsel Derinleşme"]
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

# --- GİZLİ ARAŞTIRMACI PANELİ (ŞİFRE KORUMALI) ---
with st.sidebar:
    st.header("🔬 Araştırmacı Paneli")
    st.caption("20+20 = 40 Öğrenci Deney Kontrolü")
    
    # Şifre metin kutusu
    teacher_password = st.text_input("Öğretmen Şifresi", type="password", key="teacher_pass_input")
    
    # Enter derdi olmasın diye net bir giriş butonu ekledik
    giris_button = st.button("Giriş Yap 🔑")
    
    # Şifre doğru mu kontrolü (Şifre: Aykut.45)
    if giris_button and teacher_password == "Aykut.45":
        st.session_state["ogretmen_giris"] = True

    # Eğer buton tıklandıysa veya oturum açıldıysa paneli göster
    if st.session_state.get("ogretmen_giris", False) or teacher_password == "2204Bilsim":
        st.success("🔒 Yetkili Girişi Sağlandı")
        if os.path.exists(DATA_FILE):
            try:
                df_all = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
            except UnicodeDecodeError:
                try:
                    df_all = pd.read_csv(DATA_FILE, encoding="cp1254")
                except Exception:
                    df_all = pd.read_csv(DATA_FILE, encoding="latin-1", errors="replace")
            
            st.metric("Toplam Katılımcı", df_all["Katilimci_Kodu"].nunique())
            st.metric("Toplam Yanıt", len(df_all))
            csv_data = df_all.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 Tüm Verileri İndir (CSV)",
                data=csv_data,
                file_name=f"MindAdapt_Ortaokul_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            if st.button("🗑️ Verileri Sıfırla"):
                os.remove(DATA_FILE)
                st.rerun()
        else:
            st.info("Henüz veri kaydedilmedi.")
    else:
        if teacher_password:
            st.error("❌ Hatalı şifre!")
        st.info("Verileri görmek ve indirmek için şifreyi girip 'Giriş Yap' butonuna basınız.")

# --- EKRAN 1: ÖĞRENCİ GİRİŞİ ---
if st.session_state.step == "intro":
    st.title("🧠 MindAdapt: Dijital Odaklanma Çalışması")
    st.markdown("Merhaba sevgili öğrencimiz! Bu çalışma, dijital cihazları kullanırken odaklanma durumumuzu incelemek için yapılmaktadır.")
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            p_id = st.text_input("Öğrenci Kodunuz *", placeholder="Örn: OGR-01")
            grade = st.selectbox("Sınıf Düzeyi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"])
        with col2:
            group_type = st.selectbox("Deney Grubunuz *", ["Grup A (1. Oturum)", "Grup B (1. Oturum)"])
            test_mode = st.selectbox("Test Türü *", ["MindAdapt (AI Adaptif - 7 Soru)", "Standart Ölçek (12 Soru)"])
            gender = st.selectbox("Cinsiyet", ["Kız", "Erkek", "Belirtmek İstemiyorum"])
        submitted = st.form_submit_button("Teste Başla ▶️", use_container_width=True)
        if submitted:
            if not p_id.strip():
                st.error("Lütfen öğrenci kodunuzu yazınız.")
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
    options = {1: "1 — Hiçbir zaman", 2: "2 — Nadiren", 3: "3 — Bazen", 4: "4 — Sık sık", 5: "5 — Her zaman"}
    choice = st.radio("Sana en uygun olanı seç:", options=list(options.keys()), format_func=lambda x: options[x], index=None, key=f"radio_{q['id']}_{current_idx}")
    st.write("")
    if st.button("Cevapla ve Devam Et ⏭️", use_container_width=True):
        if choice is None:
            st.warning("Lütfen bir seçenek işaretle.")
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

# --- EKRAN 3: SONUÇ ---
elif st.session_state.step == "result":
    st.balloons()
    st.success("🎉 Katılımın için çok teşekkür ederiz! Cevapların güvenle kaydedildi.")
    df_hist = pd.DataFrame(st.session_state.history)
    avg_score = df_hist["puan"].mean()
    c1, c2, c3 = st.columns(3)
    c1.metric("Çözülen Soru", f"{len(df_hist)} Soru")
    c2.metric("Toplam Süre", f"{st.session_state.total_time:.1f} sn")
    c3.metric("Ortalama Puan", f"{avg_score:.2f} / 5.00")
    if "MindAdapt" in st.session_state.test_mode:
        st.subheader("📊 Dijital Odaklanma Profilin")
        dim_means = df_hist.groupby("boyut")["puan"].mean().reindex(["Bildirim Hassasiyeti", "Dijital Çoklu Görev", "Bilişsel Derinleşme"], fill_value=0)
        fig = go.Figure(data=go.Scatterpolar(r=dim_means.values, theta=dim_means.index, fill='toself', line_color='#2563EB'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, height=320)
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 Not: Bu çalışma tamamen bilimsel farkındalık içindir.")
    if st.button("Yeni Öğrenci Girişi 🔄", use_container_width=True):
        st.session_state.step = "intro"
        st.rerun()
