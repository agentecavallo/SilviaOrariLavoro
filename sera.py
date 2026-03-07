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
st.set_page_config(page_title="Calcolatore Ore", page_icon="🕒")
st.title("Calcolatore Ore - Turno Sera 🌙")

st.write("Niente più file Excel impazziti! Copia la colonna dei turni dal file originale e incollala qui sotto.")

# 3. Creiamo un grande box di testo dove incollare i turni
testo_incollato = st.text_area("Incolla qui la colonna dei turni:", height=300, placeholder="Incolla qui...\nEsempio:\nM1r\nP\nF\n...")

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
            # Puliamo la riga da spazi vuoti accidentali e trasformiamo in minuscolo
            # Così se tua moglie copia "M1r", "m1r" o " M1r ", il programma lo capisce lo stesso
            valore_pulito = riga.strip().lower()
            
            # Se la sigla incollata è nella nostra tabella, sommiamo le ore
            if valore_pulito in TABELLA_ORE:
                somma_totale += TABELLA_ORE[valore_pulito]
                turni_trovati += 1
                
        # Mostriamo il risultato
        st.success("✅ Calcolo completato!")
        st.metric(label="Totale Ore Calcolate", value=f"{somma_totale} ore")
        st.write(f"*(Ho riconosciuto e sommato {turni_trovati} turni validi dalla tua selezione)*")
