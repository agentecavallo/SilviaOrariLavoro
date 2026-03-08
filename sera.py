import streamlit as st

# 1. Definiamo la tabella dei valori
TABELLA_ORE = {
    "m1r": 5.5,
    "m2r": 4.5,
    "pr": 4.5,
    "pdlr": 3.0,
    "p": 5.0,
    "f": 5.0
}

# 2. Interfaccia visiva
# 🕰️ QUI HO RIMESSO L'OROLOGIO ANALOGICO!
st.set_page_config(page_title="Calcolatore Ore", page_icon="🕰️")
st.title("Calcolatore Ore - Turni CUP")

# --- INSERIMENTO FIRMA ---
try:
    st.image("michelone.jpg", width=60)
except FileNotFoundError:
    st.error("⚠️ Attenzione: Non riesco a trovare il file 'michelone.jpg'.")
except Exception as e:
    st.error(f"⚠️ Errore con l'immagine: {e}")
# -------------------------

st.write("Niente più calcoli astrusi con possibilità di errore!")

# 3. Creiamo un box di testo dimezzato (height=150)
testo_incollato = st.text_area("dopo aver copiato tutta la colobba sul file excel su Google Drive incollala qui sotto:", height=150, placeholder="Incolla qui l'intera colonna dei tuoi turni mensili")

# 4. Pulsante per far partire il calcolo
if st.button("Calcola Ore", type="primary"):
    
    # Controlliamo che l'utente abbia incollato qualcosa
    if testo_incollato.strip() == "":
        st.warning("⚠️ Incolla i dati nel riquadro prima di cliccare su Calcola!")
    else:
        somma_totale = 0.0
        turni_trovati = 0
        
        # Dividiamo il testo incollato riga per riga
        righe = testo_incollato.split('\n')
        
        for riga in righe:
            # Puliamo la riga e trasformiamo in minuscolo
            valore_pulito = riga.strip().lower()
            
            # Se la sigla incollata è nella nostra tabella, sommiamo le ore
            if valore_pulito in TABELLA_ORE:
                somma_totale += TABELLA_ORE[valore_pulito]
                turni_trovati += 1
                
        # Mostriamo il risultato
        st.success("✅ Calcolo completato!")
        st.metric(label="Totale Ore Calcolate", value=f"{somma_totale} ore")
        st.write(f"*(Ho riconosciuto e sommato {turni_trovati} turni validi dalla tua selezione)*")
