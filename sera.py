import streamlit as st
import pandas as pd

# 1. Definiamo la tabella dei valori e le ore corrispondenti
TABELLA_ORE = {
    "M1r": 5.5,
    "M2r": 4.5,
    "Pr": 4.5,
    "Pdlr": 3.0,
    "P": 5.0,
    "F": 5.0
}

# 2. Creiamo l'interfaccia visiva
st.set_page_config(page_title="Calcolatore Ore", page_icon="🕒")
st.title("Calcolatore Ore - Turno Sera 🌙")
st.write("Trascina e rilascia qui il tuo file Excel per calcolare le ore automaticamente.")

# Ecco il Drag and Drop nativo di Streamlit
file_caricato = st.file_uploader("Carica il file Excel (.xlsx o .xls)", type=['xlsx', 'xls'])

# 3. Cosa succede quando l'utente inserisce un file
if file_caricato is not None:
    try:
        # Leggiamo l'Excel. header=None serve a rispettare le righe esatte
        df = pd.read_excel(file_caricato, header=None)
        
        # In Python si conta da 0. La riga 5 di Excel è l'indice 4.
        riga_5 = df.iloc[4] 
        
        colonna_sera = None
        
        # Cerchiamo la parola "sera" nella riga 5
        for col_indice, valore in riga_5.items():
            if str(valore).strip().lower() == "sera":
                colonna_sera = col_indice
                break
        
        if colonna_sera is None:
            st.error("⚠️ Errore: Non ho trovato la parola 'sera' nella riga 5 dell'Excel. Controlla il file e riprova.")
        else:
            # Prendiamo i dati dalla riga 6 in poi (indice 5 in Python) per la colonna corretta
            dati_sotto_sera = df.iloc[5:, colonna_sera]
            
            somma_totale = 0.0
            
            # Calcoliamo la somma traducendo le sigle
            for valore in dati_sotto_sera:
                valore_pulito = str(valore).strip()
                if valore_pulito in TABELLA_ORE:
                    somma_totale += TABELLA_ORE[valore_pulito]
            
            # Mostriamo il risultato con una grafica accattivante
            st.success("✅ File letto con successo!")
            st.metric(label="Totale Ore Calcolate", value=f"{somma_totale} ore")
            
    except Exception as e:
        st.error(f"❌ C'è stato un problema nella lettura del file: {e}")
