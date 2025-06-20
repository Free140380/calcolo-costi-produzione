
import streamlit as st

st.set_page_config(page_title="Calcolo Costi Produzione", layout="wide")

st.title("🧮 Calcolo Costi di Produzione")

# Input principali
nome_pezzo = st.text_input("Nome pezzo")
prezzo_nudo = st.number_input("Costo Nudo e Crudo (€)", min_value=0.0, format="%.3f")
pezzi_ora = st.number_input("Produzione (pezzi/ora)", min_value=1)
quantita = st.number_input("Quantità da produrre", min_value=1)
macchina = st.selectbox("Macchina utilizzata", ["CNC", "Giorgi"])

attrezzaggio = st.number_input("Ore attrezzaggio", min_value=0.0, format="%.2f")
lavaggio = st.number_input("Ore lavaggio", min_value=0.0, format="%.2f")
imballaggio = st.number_input("Ore imballaggio", min_value=0.0, format="%.2f")
brocciatura = st.number_input("Ore brocciatura", min_value=0.0, format="%.2f")
filettatura = st.number_input("Ore filettatura", min_value=0.0, format="%.2f")
assemblaggio1 = st.number_input("Ore assemblaggio 1", min_value=0.0, format="%.2f")
assemblaggio2 = st.number_input("Ore assemblaggio 2", min_value=0.0, format="%.2f")
chiusura = st.number_input("Ore chiusura pezzi", min_value=0.0, format="%.2f")

# Costi a pezzo
vibratura = st.number_input("Costo vibratura per pezzo", min_value=0.0, format="%.3f")
pulitura = st.number_input("Costo pulitura per pezzo", min_value=0.0, format="%.3f")
cromatura = st.number_input("Costo cromatura per pezzo", min_value=0.0, format="%.3f")
ricottura = st.number_input("Costo ricottura per pezzo", min_value=0.0, format="%.3f")
verniciatura = st.number_input("Costo verniciatura per pezzo", min_value=0.0, format="%.3f")

if st.button("Calcola"):
    ore_macchina = quantita / pezzi_ora
    costo_operatore = (
        attrezzaggio * 22 + lavaggio * 13 + imballaggio * 13 + brocciatura * 13 +
        filettatura * 13 + assemblaggio1 * 13 + assemblaggio2 * 13 + chiusura * 13
    )
    controllo_macchina = ((ore_macchina // 2) + 1) * 22

    energia = ore_macchina * 2.5  # stima energia €/h
    trasporto = 22  # fisso

    ammortamento = 0
    if macchina == "CNC":
        ammortamento = (80000 / (365 * 24)) * ore_macchina  # costo stimato ammortamento CNC

    costi_pezzo = (
        prezzo_nudo +
        (costo_operatore + controllo_macchina + energia + trasporto + ammortamento) / quantita +
        vibratura + pulitura + cromatura + ricottura + verniciatura
    )
    costi_pezzo += costi_pezzo * 0.20  # 10% imprevisti + 10% indiretti

    st.success(f"Costo totale per pezzo: **€{costi_pezzo:.3f}**")
    st.info("Consigli di prezzo (minimo, medio, massimo):")
    st.write(f"- Minimo: €{costi_pezzo * 1.10:.3f}")
    st.write(f"- Medio: €{costi_pezzo * 1.25:.3f}")
    st.write(f"- Massimo: €{costi_pezzo * 1.40:.3f}")
