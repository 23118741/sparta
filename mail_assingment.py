from email_sender import EmailSender

class MailAssignment:
    """Verantwoordelijk voor het toewijzen van de juiste mail op basis van categorie en locatie."""
    
    def assign_and_send(self, emailer: EmailSender, row):
        """
        Bepaalt welke mail gestuurd moet worden op basis van de rij-gegevens.
        Retourneert True als een mail succesvol is verstuurd of toegewezen, anders False.
        """
        mail_verstuurd = str(row.get("mail1_verstuurd", "")).strip().lower()
        if mail_verstuurd == "ja":
            return False

        ontvanger = row.get("email")
        categorie = str(row.get("leeftijdscategorie", "")).upper()
        locatie = str(row.get("locatie", "")).upper()
        
        if not ontvanger:
            print("Geen e-mailadres gevonden in deze rij.")
            return False
        
        # --- Check op Te Jong / Te Oud (Ongeacht locatie) ---
        if categorie == "TE JONG":
            emailer.send_too_young_email(row)
            return True
        elif categorie == "TE OUD":
            emailer.send_too_old_email(row)
            return True

        if "ZUIDERPARK" in locatie:
            emailer.send_zp_email(row)
            return True
        elif "WESTVLIET" in locatie:
            emailer.send_wv_email(row)
            return True
        else:
            print(f"Onbekende locatie '{locatie}' voor categorie {categorie}")
            return False

        print(f"Geen match gevonden voor categorie '{categorie}'")
        return False

