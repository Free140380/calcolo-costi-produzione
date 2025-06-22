import streamlit as st
from fpdf import FPDF
import os

# Aggiungi il font DejaVu
FONT_PATH = "DejaVuSans.ttf"  # Assicurati che sia nella stessa cartella

class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', '', 14)
        self.cell(0, 10, "Report Calcolo Costi Produzione", ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def crea_pdf(nome_pezzo, dettagli, risultati):
    pdf = PDF()
    pdf.add_font('DejaVu', '', FONT_PATH, uni=True)
    pdf.add_page()
    pdf.set_font('DejaVu', '', 12)

    pdf.cell(0, 10, f"Nome pezzo: {nome_pezzo}", ln=True)
    pdf.ln(5)

    for descrizione, valore in dettagli.items():
        pdf.multi_cell(0, 10, f"{descrizione}: {valore}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Costo unitario: {risultati['costo_unitario']:.4f} Euro", ln=True)
    pdf.cell(0, 10, f"Prezzo minimo suggerito: {risultati['prezzo_min']:.4f} Euro", ln=True)
    pdf.cell(0, 10, f"Prezzo medio suggerito: {risultati['prezzo_med']:.4f} Euro", ln=True)
    pdf.cell(0, 10, f"Prezzo massimo suggerito: {risultati['prezzo_max']:.4f} Euro", ln=True)
    pdf.cell(0, 10, f"Margine sul prezzo di vendita: {risultati['margine_valore']:.4f} Euro ({risultati['margine_percento']:.2f}%)", ln=True)

    file_path = f"Report_Costi_Produzione.pdf"
    pdf.output(file_path)
    return file_path

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="Calcolo Costi Produzione", layout="centered")
st.title("🔧 Calcolo Costi Produzione")

st.markdown("""
Compila i campi per calcolare il costo di produzione, prezzi suggeriti e margine.
""")

nome_pezzo = st.text_input("Nome pezzo", "Pomolo cromato")
costo_nudo = st.number_input("Costo Nudo e Crudo (Euro)", min_value=0.0, step=0.01)
pezzi_ora = st.number_input("Tempo Macchina (Pezzi/Ora)", min_value=1.0)
quantita = st.number_input("Pezzi da Produrre", min_value=1)
macchina = st.selectbox("Macchina utilizzata", ["CNC", "Giorgi"])
prezzo_vendita = st.number_input("Prezzo di vendita previsto (Euro)", min_value=0.0, step=0.01)

tempi = {
    "Attrezzaggio (h)": (st.number_input("Tempo Attrezzaggio (h)", 0.0), 22),
    "Lavaggio (h)": (st.number_input("Tempo Lavaggio (h)", 0.0), 13),
    "Imballaggio (h)": (st.number_input("Tempo Imballaggio (h)", 0.0), 13),
    "Brocciatura (h)": (st.number_input("Tempo Brocciatura (h)", 0.0), 13),
    "Filettatura (h)": (st.number_input("Tempo Filettatura (h)", 0.0), 13),
    "Assemblaggio 1 (h)": (st.number_input("Tempo Assemblaggio 1 (h)", 0.0), 13),
    "Assemblaggio 2 (h)": (st.number_input("Tempo Assemblaggio 2 (h)", 0.0), 13),
    "Chiusura pezzi (h)": (st.number_input("Tempo Chiusura Pezzi (h)", 0.0), 13),
}

costi_aggiuntivi = {
    "Vibratura": st.number_input("Costo Vibratura (Euro)", 0.0),
    "Pulitura": st.number_input("Costo Pulitura (Euro)", 0.0),
    "Cromatura": st.number_input("Costo Cromatura (Euro)", 0.0),
    "Ricottura": st.number_input("Costo Ricottura (Euro)", 0.0),
    "Verniciatura": st.number_input("Costo Verniciatura (Euro)", 0.0),
}

if st.button("🔍 Genera Costi e PDF"):
    # ---- Calcolo costi
    tempo_macchina = quantita / pezzi_ora
    tempo_attrezzaggio = tempi["Attrezzaggio (h)"][0]
                                                
    if macchina == "CNC":
        costo_operatore = (22 / 4) * tempo_attrezzaggio
        costo_ammortamento = 0.05 * tempo_macchina  # esempio base
    else:
        costo_operatore = 22 * tempo_attrezzaggio
        costo_ammortamento = 0

    costo_tempi = sum(t[0] * t[1] for t in tempi.values())
    costo_aggiuntivo = sum(costi_aggiuntivi.values())
    controllo_macchina = (8 / 2) * 22 if quantita else 0
    trasporto = 40 * 0.5  # es. 0.5 Euro/km medio con Doblò elettrico
    energia = 0.02 * quantita  # es. 0.02 Euro a pezzo

    costo_totale = (
        costo_nudo * quantita +
        costo_operatore +
        costo_ammortamento +
        costo_tempi +
        costo_aggiuntivo +
        controllo_macchina +
        trasporto +
        energia
    )

    costo_indiretto = 0.10 * costo_totale
    costo_imprevisti = 0.10 * costo_totale

    totale_finale = costo_totale + costo_indiretto + costo_imprevisti
    costo_unitario = totale_finale / quantita

    prezzo_min = costo_unitario * 1.20
    prezzo_med = costo_unitario * 1.40
    prezzo_max = costo_unitario * 1.60

    margine_valore = prezzo_vendita - costo_unitario
    margine_percento = (margine_valore / costo_unitario) * 100 if costo_unitario > 0 else 0

    # ---- Mostra risultati
    st.success(f"Costo unitario: {costo_unitario:.4f} Euro")
    st.info(f"Prezzo minimo suggerito: {prezzo_min:.4f} Euro")
    st.info(f"Prezzo medio suggerito: {prezzo_med:.4f} Euro")
    st.info(f"Prezzo massimo suggerito: {prezzo_max:.4f} Euro")
    st.warning(f"Margine sul prezzo di vendita: {margine_valore:.4f} Euro ({margine_percento:.2f}%)")

    # ---- PDF
    dettagli = {
        "Costo nudo totale": f"{costo_nudo} * {quantita} = {costo_nudo * quantita:.2f} Euro",
        "Tempo macchina": f"{quantita} / {pezzi_ora} = {tempo_macchina:.2f} h",
        "Costo operatore": f"= {costo_operatore:.2f} Euro",
        "Costo ammortamento": f"= {costo_ammortamento:.2f} Euro",
        "Costi lavorazioni": f"= {costo_tempi:.2f} Euro",
        "Costi extra (vibr., pulit., etc)": f"= {costo_aggiuntivo:.2f} Euro",
        "Controllo macchina": f"= {controllo_macchina:.2f} Euro",
        "Trasporto": f"= {trasporto:.2f} Euro",
        "Energia elettrica": f"= {energia:.2f} Euro",
        "Costi indiretti 10%": f"= {costo_indiretto:.2f} Euro",
        "Costi imprevisti 10%": f"= {costo_imprevisti:.2f} Euro",
        "Totale Finale": f"= {totale_finale:.2f} Euro",
    }

    risultati = {
        "costo_unitario": costo_unitario,
        "prezzo_min": prezzo_min,
        "prezzo_med": prezzo_med,
        "prezzo_max": prezzo_max,
        "margine_valore": margine_valore,
        "margine_percento": margine_percento,
    }

    pdf_path = crea_pdf(nome_pezzo, dettagli, risultati)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Scarica PDF Dettagliato", f, file_name=pdf_path, mime="application/pdf")
