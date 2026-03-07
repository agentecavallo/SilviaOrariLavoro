import streamlit as st
import pandas as pd
import re

# 1. Definiamo la tabella dei valori
TABELLA_ORE = {
    "M1r": 5.5,
    "M2r": 4.5,
    "Pr": 4.5,
    "Pdlr": 3.0,
    "P": 5.0,
    "F": 5.0
}

# Funzione per trasformare il link di Drive in un link di download diretto
def crea_link_download_diretto(url_condivisione):
    # Cerca l'ID del file dentro il link di Google Drive
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url_condivisione)
    if match:
        id_file = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={id_file}"
    return None

# Funzione per elaborare i dati (così non ripetiamo il codice)
def calcola_ore(df):
    riga_5 = df.iloc[4] 
    colonna_sera = None
    
    for col_indice, valore in riga_5.items():
        if str(valore).strip().lower() == "sera":
            colonna_sera = col_indice
            break
    
    if colonna_sera is None:
        st.error("⚠️ Errore: Non ho trovato la parola 'sera' nella riga 5 dell'Excel.")
        return
        
    dati_sotto_sera = df.iloc[5:, colonna_sera]
    somma_totale = 0.0
    
    for valore in dati_sotto_sera:
        valore_pulito = str(valore).strip()
        if valore_pulito in TABELLA_ORE:
            somma_totale += TABELLA_ORE[valore_pulito]
            
    st.success("✅ File letto con successo!")
    st.metric(label="Totale Ore Calcolate", value=f"{somma_totale} ore")

# 2. Interfaccia visiva
st.set_page_config(page_title="Calcolatore Ore", page_icon="🕒")
st.title("Calcolatore Ore - Turno Sera 🌙")

# Creiamo due "schede" per dare due opzioni all'utente
tab1, tab2 = st.tabs(["🔗 Incolla Link Drive", "📁 Carica File Excel"])

with tab1:
    st.write("Incolla qui il link di condivisione del file Google Drive. Assicurati che il file sia impostato su 'Chiunque abbia il link'.")
    link_drive = st.text_input("Link Google Drive:")
    
    if st.button("Calcola da Link"):
        if link_drive:
            link_diretto = crea_link_download_diretto(link_drive)
            if link_diretto:
                try:
                    # pandas può leggere un file Excel direttamente da un link web!
                    df = pd.read_excel(link_diretto, header=None)
                    calcola_ore(df)
                except Exception as e:
                    st.error(f"❌ Impossibile leggere il file dal link. Verifica che il link sia corretto e pubblico. Errore: {e}")
            else:
                st.warning("⚠️ Link non valido. Assicurati di copiare il link di condivisione completo.")
        else:
            st.warning("⚠️ Inserisci un link prima di premere il pulsante.")

with tab2:
    st.write("Oppure trascina/seleziona il file dal tuo dispositivo.")
    file_caricato = st.file_uploader("Carica il file Excel", type=['xlsx', 'xls'])
    if file_caricato is not None:
        try:
            df = pd.read_excel(file_caricato, header=None)
            calcola_ore(df)
        except Exception as e:
            st.error(f"❌ C'è stato un problema nella lettura del file: {e}")
