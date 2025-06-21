import streamlit as st

st.set_page_config(page_title="Calcolo Costi Produzione", layout="wide")

st.title("🧮 Calcolo Costi Produzione")

# Input dell'utente
col1, col2 = st.columns(2)

with col1:
    nome_pezzo = st.text_input("Nome pezzo")
    costo_nudo = st.number_input("Costo nudo e crudo (€)", min_value=0.0, format="%.4f")
    pezzi_ora = st.number_input("Produzione macchina (pezzi/ora)", min_value=1)
    quantita = st.number_input("Quantità da produrre", min_value=1)
    macchina = st.selectbox("Macchina utilizzata", ["CNC", "Giorgi"])

with col2:
    attrezzaggio_h = st.number_input("Tempo attrezzaggio (ore)", min_value=0.0, format="%.2f")
    lavaggio_h = st.number_input("Tempo lavaggio (ore)", min_value=0.0, format="%.2f")
    imballaggio_h = st.number_input("Tempo imballaggio (ore)", min_value=0.0, format="%.2f")
    controllo_h = quantita / (8 * 2) * 1  # 1 ora ogni 2 ore in turno di 8h

# Costi lavorazioni
st.subheader("Costi extra (opzionali)")
col3, col4, col5 = st.columns(3)

with col3:
    vibratura = st.number_input("Costo vibratura (€)", min_value=0.0, format="%.4f")
    pulitura = st.number_input("Costo pulitura (€)", min_value=0.0, format="%.4f")

with col4:
    cromatura = st.number_input("Costo cromatura (€)", min_value=0.0, format="%.4f")
    ricottura = st.number_input("Costo ricottura (€)", min_value=0.0, format="%.4f")

with col5:
    verniciatura = st.number_input("Costo verniciatura (€)", min_value=0.0, format="%.4f")

# Costi orari fissi
operatore_22 = 22
operatore_13 = 13

# Costi diretti
tempo_lavorazione_tot = quantita / pezzi_ora
costo_macchina = tempo_lavorazione_tot * (0.75 if macchina == "CNC" else 0)  # ammortamento solo CNC
costo_attrezzaggio = attrezzaggio_h * operatore_22
costo_lavaggio = lavaggio_h * operatore_13
costo_imballaggio = imballaggio_h * operatore_13
costo_controllo = controllo_h * operatore_22

# Costi extra su ogni pezzo
costo_extra_unit = vibratura + pulitura + cromatura + ricottura + verniciatura

# Totale costi
totale = (
    quantita * costo_nudo +
    costo_attrezzaggio +
    costo_lavaggio +
    costo_imballaggio +
    costo_macchina +
    costo_controllo +
    costo_extra_unit * quantita
)

# Costi indiretti e imprevisti
costo_totale_finale = totale * 1.20  # +10% costi indiretti +10% imprevisti
prezzo_unitario = costo_totale_finale / quantita

# Output
st.markdown("---")
st.subheader("📊 Risultati")
st.markdown(f"**Totale Costi:** € {totale:,.2f}")
st.markdown(f"**Totale con costi indiretti e imprevisti (20%):** € {costo_totale_finale:,.2f}")
st.markdown(f"**Costo unitario:** € {prezzo_unitario:,.4f}")
