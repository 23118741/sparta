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

        # Logica voor "TE JONG"
        if categorie == "TE JONG":
            emailer.send_to_young_email(ontvanger)
            return True

        # Logica voor "TE OUD"
        if categorie == "TE OUD":
            emailer.send_to_old_email(ontvanger)
            return True

        # Logica voor U16 (U8 t/m U16)
        u16_groepen = ["U8", "U10", "U11", "U12", "U14", "U16"]
        if categorie in u16_groepen:
            if "ZUIDERPARK" in locatie:
                emailer.send_u16_zp_email(row)
                return True
            elif "WESTVLIET" in locatie:
                emailer.send_u16_wv_email(ontvanger)
                return True
            else:
                print(f"Onbekende locatie '{locatie}' voor categorie {categorie}")
                return False

        # Logica voor U20 (U18 en U20)
        u20_groepen = ["U18", "U20"]
        if categorie in u20_groepen:
            if "ZUIDERPARK" in locatie:
                emailer.send_u20_zp_email(row)
                return True
            elif "WESTVLIET" in locatie:
                emailer.send_u20_wv_email(ontvanger)
                return True
            else:
                print(f"Onbekende locatie '{locatie}' voor categorie {categorie}")
                return False

        print(f"Geen match gevonden voor categorie '{categorie}'")
        return False

