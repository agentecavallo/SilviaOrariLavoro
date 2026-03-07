import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

# 1. Definiamo la tabella dei valori e le ore corrispondenti
TABELLA_ORE = {
    "M1r": 5.5,
    "M2r": 4.5,
    "Pr": 4.5,
    "Pdlr": 3.0,
    "P": 5.0,
    "F": 5.0
}

def calcola_ore_sera(file_path):
    try:
        # Leggiamo l'Excel. header=None ci assicura di contare le righe esattamente come le vedi su Excel.
        df = pd.read_excel(file_path, header=None)
        
        # In Python si conta da 0. Quindi la riga 5 di Excel è l'indice 4 per Python.
        riga_5 = df.iloc[4] 
        
        colonna_sera = None
        # Cerchiamo la colonna che contiene la parola "sera"
        for col_indice, valore in riga_5.items():
            # Trasformiamo in testo, togliamo spazi vuoti e mettiamo in minuscolo per evitare errori di battitura
            if str(valore).strip().lower() == "sera":
                colonna_sera = col_indice
                break
        
        # Se non troviamo la parola "sera" ci fermiamo
        if colonna_sera is None:
            return "Errore: Non ho trovato la parola 'sera' nella riga 5."

        # Prendiamo i dati di quella colonna, dalla riga 6 in poi (indice 5 in Python)
        dati_sotto_sera = df.iloc[5:, colonna_sera]
        
        # Iniziamo la somma
        somma_totale = 0.0
        
        for valore in dati_sotto_sera:
            # Puliamo il testo da eventuali spazi vuoti accidentali
            valore_pulito = str(valore).strip()
            # Se la sigla è nella nostra tabella, aggiungiamo le ore
            if valore_pulito in TABELLA_ORE:
                somma_totale += TABELLA_ORE[valore_pulito]
                
        return f"Calcolo completato con successo!\n\nTotale ore calcolate: {somma_totale}"
        
    except Exception as e:
        return f"C'è stato un problema nella lettura del file:\n{str(e)}"


# 2. Creiamo l'interfaccia grafica (La finestra Drag & Drop)
class FinestraDragAndDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcolatore Ore - Turno Sera")
        self.resize(450, 300)
        
        # Abilitiamo il drag and drop sulla finestra
        self.setAcceptDrops(True)
        
        layout = QVBoxLayout()
        self.testo = QLabel("Trascina e rilascia qui\nil tuo file Excel (.xlsx)\n\n🔽", self)
        self.testo.setAlignment(Qt.AlignCenter)
        self.testo.setStyleSheet("""
            QLabel {
                font-size: 18px; 
                border: 3px dashed #888; 
                border-radius: 10px;
                background-color: #f0f0f0;
                color: #333;
            }
        """)
        layout.addWidget(self.testo)
        self.setLayout(layout)

    # Evento che si attiva quando entri col mouse tenendo il file
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # Evento che si attiva quando "lasci" il file nella finestra
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            percorso_file = url.toLocalFile()
            
            # Controlliamo che sia davvero un file Excel
            if percorso_file.endswith(('.xlsx', '.xls')):
                self.testo.setText("Sto calcolando le ore...")
                # Avviamo il calcolo
                risultato = calcola_ore_sera(percorso_file)
                nome_file = percorso_file.split('/')[-1]
                
                self.testo.setText(f"File elaborato: {nome_file}\n\n{risultato}\n\n(Trascina un altro file se vuoi riprovare)")
                break
            else:
                self.testo.setText("Formato non valido.\nPer favore, rilascia un file Excel (.xlsx o .xls)")

# 3. Avvio del programma
if __name__ == '__main__':
    app = QApplication(sys.argv)
    finestra = FinestraDragAndDrop()
    finestra.show()
    sys.exit(app.exec_())
