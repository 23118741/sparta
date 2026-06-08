import smtplib
from email.message import EmailMessage
from sheets_config import GoogleSheetsConfig

class EmailSender:
    """Verantwoordelijk voor het versturen van e-mails via Gmail."""
    def __init__(self, config: GoogleSheetsConfig):
        self.config = config
        
    def send_email(self, msg):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.config.gmail_user, self.config.gmail_password)
            smtp.send_message(msg)
        

    def send_test_email(self, ontvanger):
        if not ontvanger:
            print("Geen ontvanger opgegeven, mail niet verzonden.")
            return

        msg = EmailMessage()
        msg['Subject'] = "Veilige Test van Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content("baap")
        
        self.send_email(msg)
        
        print(f"Testmail succesvol verstuurd naar {ontvanger}!")
    
    #email voor te jong of te oud in de sheet
    def send_to_young_email(self, ontvanger):
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content("hier komt de mail voor als iemand te jong is")
        
        self.send_email(msg)
        
    #email voor te jong of te oud in de sheet
    def send_to_old_email(self, ontvanger):
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content("hier komt de mail voor als iemand te oud is")
        
        self.send_email(msg)
    
    #email voor u16 dus ouders worden aangesproken
    def send_u16_wv_email(self, ontvanger):
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content("hier komt de mail voor u16 wv")
        
        self.send_email(msg)
    
    #mail voor u20 dus de persoon zelf wordt aangesproken
    def send_u20_wv_email(self, ontvanger):
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content("hier komt de mail voor u20 wv")
        
        self.send_email(msg)
        
    #email voor u16 dus ouders worden aangesproken
    def send_u16_zp_email(self, row):
        ontvanger = row.get("email")
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
            
        voornaam = str(row.get("voornaam", "Kandidaat")).strip()
        geslacht = str(row.get("geslacht", "")).strip().lower()
        categorie = str(row.get("leeftijdscategorie", "")).strip().upper()
        startdatum = str(row.get("startdatum", "[startdatum]")).strip()
        trainingsdagen = str(row.get("trainingsdagen", "[trainingsdagen]")).strip()
        trainingstijden = str(row.get("trainingstijden", "[trainingstijden]")).strip()

        # Bepaal voornaamwoorden en geslachtstekst
        if "m" in geslacht or geslacht == "man" or geslacht == "jongen":
            pr_onderwerp = "hij"
            pr_bezit = "zijn"
            geslacht_cat = "Jongens"
        elif "v" in geslacht or "f" in geslacht or geslacht == "vrouw" or geslacht == "meisje":
            pr_onderwerp = "zij"
            pr_bezit = "haar"
            geslacht_cat = "Meisjes"
        else:
            pr_onderwerp = "hij/zij"
            pr_bezit = "zijn/haar"
            geslacht_cat = "Jongens/Meisjes"

        # Formatteer de categorie string (bijv. "Meisjes U8")
        volledige_categorie = f"{geslacht_cat} {categorie}"

        # Bouw de mail op
        content = f"""Beste ouder(s) van {voornaam},

Leuk dat {voornaam} kennis wil maken met atletiek bij AV Sparta!  
{pr_onderwerp.capitalize()} mag vanaf {startdatum} een maand lang gratis aan proeftrainingen meedoen. {pr_onderwerp.capitalize()} valt in de categorie {volledige_categorie}. De training wordt gegeven op maandag, woensdag en zaterdag. De trainingstijden zijn: van 18.30 tot 19.30 op maandag en woensdag en van 9.30 tot 10.30 op zaterdag. Aan- of afmelden voor de training is niet nodig.

De trainingen worden gegeven op onze baan in het Zuiderpark, ingang Melis Stokelaan. Wilt u ervoor zorgen dat {voornaam} tien minuten voor aanvang van de training aanwezig is en sportieve kleding en schoenen passend bij de weersomstandigheden draagt? En als u voor het eerst komt, vraagt u dan bij een van onze vrijwilligers in de kantine naar de trainers van {pr_bezit} categorie ({volledige_categorie}).

Meer informatie over het lidmaatschap van AV Sparta staat op onze website: http://www.avsparta.nl/Lidmaatschap. Daar vindt u ook het aanmeldformulier om in te schrijven als lid. 

Mocht u nog vragen hebben over jeugdatletiek bij AV Sparta dan kunt u altijd contact met ons opnemen.

Wij wensen {voornaam} veel plezier met de proeftrainingen.

Met vriendelijke groet,

Dick Holstein,
bestuurslid jeugd AV Sparta."""
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content(content)
        
        self.send_email(msg)
    
    #mail voor u20 dus de persoon zelf wordt aangesproken
    def send_u20_zp_email(self, row):
        ontvanger = row.get("email")
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
            
        voornaam = str(row.get("voornaam", "Kandidaat")).strip()
        geslacht = str(row.get("geslacht", "")).strip().lower()
        categorie = str(row.get("leeftijdscategorie", "")).strip().upper()
        startdatum = str(row.get("startdatum", "[startdatum]")).strip()
        trainingsdagen = str(row.get("trainingsdagen", "[trainingsdagen]")).strip()
        trainingstijden = str(row.get("trainingstijden", "[trainingstijden]")).strip()

        # Bepaal geslachtstekst (Mannen/Vrouwen voor U18/U20)
        if "m" in geslacht or geslacht == "man" or geslacht == "jongen":
            geslacht_cat = "Mannen"
        elif "v" in geslacht or "f" in geslacht or geslacht == "vrouw" or geslacht == "meisje":
            geslacht_cat = "Vrouwen"
        else:
            geslacht_cat = "Mannen/Vrouwen"

        volledige_categorie = f"{geslacht_cat} {categorie}"

        content = f"""Beste {voornaam},

Leuk dat je kennis wil maken met atletiek bij AV Sparta!
Je mag vanaf {startdatum} de hele maand kostenloos aan proeftrainingen meedoen. Je valt in de categorie {volledige_categorie}. De training wordt gegeven op maandag en woensdag van 19.00 tot 20.30 uur. Aan- en afmelden voor de trainingen is niet nodig.

De training wordt gehouden op onze baan in het Zuiderpark, ingang Melis Stokelaan. Je kunt je tien minuten voor aanvang van de training melden. En als je voor het eerst komt, vraag dan aan de medewerkers in de kantine naar de trainer van je groep. Doorgaans is dit Hans de Vries of Roald Bakker.

Meer informatie over het lidmaatschap van AV Sparta staat op onze website: http://www.avsparta.nl/Lidmaatschap. Daar vind je ook het aanmeldformulier om in te schrijven als lid. 

Mocht je nog vragen hebben over atletiek bij AV Sparta dan kun je altijd contact met ons opnemen.

Wij wensen je veel plezier met de proeftrainingen.

Met vriendelijke groet,

Dick Holstein,
voorzitter AV Sparta."""

        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content(content)
        
        self.send_email(msg)

