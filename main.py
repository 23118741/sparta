import os
from dotenv import load_dotenv
from sheets_config import GoogleSheetsConfig
from sheet_updater import SheetUpdater
from email_sender import EmailSender
from mail_assingment import MailAssignment

load_dotenv()
config = GoogleSheetsConfig()

def main():
    updater = SheetUpdater(config)
    emailer = EmailSender(config)
    assignment = MailAssignment()
    
    # Initialiseer headers in wachtlijst als de sheet leeg is
    updater.init_wachtlijst_headers()
    huidige_wachtlijst_personen = updater.get_wachtlijst_keys()
    wachtlijst_counts = updater.get_wachtlijst_counts_per_categorie()

    # Haal de kolomindex op voor 'mail1_verstuurd' en 'wachtlijst'
    mail_verstuurd_col = updater.get_column_index("mail1_verstuurd")
    if not mail_verstuurd_col:
        print("Kan kolom 'mail1_verstuurd' niet vinden. Let op dat we wellicht geen mails kunnen markeren.")
        
    wachtlijst_col = updater.get_column_index("wachtlijst")
    if not wachtlijst_col:
        print("Kan kolom 'wachtlijst' niet vinden. We kunnen de status niet naar 'toegevoegd' updaten.")

    alle_rijen = updater.get_all_rows()
    if not alle_rijen:
        print("Geen data om te verwerken.")
        return
        
    # Doorloop alle rijen (index start op 2 in de Google Sheet)
    for index, rij in enumerate(alle_rijen):
        row_number = index + 2
        voornaam = str(rij.get("voornaam", "")).strip()
        achternaam = str(rij.get("achternaam", "")).strip()
        email = str(rij.get("email", "")).strip()
        leeftijdscategorie = str(rij.get("leeftijdscategorie", "")).strip().upper()  # Direct naar uppercase voor consistentie met counts
        geboortedatum = str(rij.get("geboortedatum", "")).strip()

        # --- Wachtlijst Logica ---
        wachtlijst_waarde = str(rij.get("wachtlijst", "")).strip().lower()
        is_wachtlijst = wachtlijst_waarde == "ja"
        sleutel = (voornaam.lower(), achternaam.lower(), geboortedatum.lower())
        mag_op_wachtlijst = leeftijdscategorie not in ["TE JONG", "TE OUD"]
        
        if is_wachtlijst and mag_op_wachtlijst and sleutel not in huidige_wachtlijst_personen and voornaam and achternaam:
            # Bereken de plek per leeftijdscategorie
            wachtlijst_counts[leeftijdscategorie] = wachtlijst_counts.get(leeftijdscategorie, 0) + 1
            wachtlijst_plek = wachtlijst_counts[leeftijdscategorie]
            
            wachtlijst_rij = [
                voornaam,
                achternaam,
                email,
                leeftijdscategorie,
                geboortedatum,
                wachtlijst_plek
            ]
            updater.append_to_wachtlijst(wachtlijst_rij)
            huidige_wachtlijst_personen.append(sleutel)
            
            # Update de huidige rij dictionary met de zojuist berekende plek voor de mailer
            rij["wachtlijst_plaats"] = wachtlijst_plek
            
            if wachtlijst_col:
                updater.update_cell(row=row_number, col=wachtlijst_col, value="toegevoegd")
                
            print(f"Rij {row_number} ({voornaam} {achternaam}) toegevoegd aan de wachtlijst ({leeftijdscategorie}) op plek {wachtlijst_plek}.")

        # --- Mail Logica ---
        # Probeer mail toe te wijzen en te versturen (heeft nu de geüpdatete wachtlijst_plaats bij de hand)
        mail_is_verstuurd = assignment.assign_and_send(emailer, rij)
        
        if mail_is_verstuurd and mail_verstuurd_col:
            print(f"Mail succesvol verstuurd voor rij {row_number}. Update spreadsheet...")
            # Update de "mail1_verstuurd" kolom in de sheet naar "Ja"
            updater.update_cell(row=row_number, col=mail_verstuurd_col, value="Ja")
        else:
            print(f"Rij {row_number} overgeslagen of mail is al verstuurd.")

if __name__ == "__main__":
    main()