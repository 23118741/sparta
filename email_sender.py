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

        
    #email voor u16 dus ouders worden aangesproken
    def send_wv_email(self, row):
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
        plaats = str(row.get("wachtlijst_plaats", "")).strip()

        # Bepaal voornaamwoorden en geslachtstekst
        if "m" in geslacht or geslacht == "man" or geslacht == "jongen":
            pr_onderwerp = "hij"
            pr_bezit = "zijn"
            geslacht_cat = "Mannen"
        elif "v" in geslacht or "f" in geslacht or geslacht == "vrouw" or geslacht == "meisje":
            pr_onderwerp = "zij"
            pr_bezit = "haar"
            geslacht_cat = "Vrouwen"
        else:
            pr_onderwerp = "hij/zij"
            pr_bezit = "zijn/haar"
            geslacht_cat = "Mannen/Vrouwen"

        # Formatteer de categorie string (bijv. "Meisjes U8")
        volledige_categorie = f"{geslacht_cat} {categorie}"

        # Bouw de mail op
        content = f"""Beste {voornaam} en/of ouder(s)/verzorgers van {voornaam},

Leuk dat je kennis wil maken met atletiek bij AV Sparta!
Je aanmelding voor de wachtlijst bij locatie Westvliet is goed doorgekomen.
Je valt in de categorie {volledige_categorie} en staat momenteel op plaats {plaats} op de wachtlijst. Wanneer er plek is voor je om mee te doen aan proeftrainingen ontvang je een e-mail.

De trainingen vinden plaats op:
Pupillen: maandag en woensdag van 18:00 tot 19:00 uur
Junioren: maandag en woensdag óf dinsdag en donderdag van 19:00 tot 20:15 uur
Meer uitleg over de trainingstijden zal volgen bij de proeftrainingen.

De trainingen worden gegeven op onze baan op sportpark Westvliet.
Adres: Groene Zoom 20, Den Haag

Meer informatie over de trainingen en het lidmaatschap staan op onze website: 
https://www.avsparta.nl/jeugdatletiek
https://www.avsparta.nl/lidmaatschap 
Mocht u nog vragen hebben over jeugdatletiek bij AV Sparta dan kunt u altijd contact met ons opnemen.

Met sportieve groet,

Jonatan Janssen
Administratie proeftrainingen AV Sparta
Website: www.avsparta.nl"""
        
        msg = EmailMessage()
        msg['Subject'] = "Proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content(content)
        
        self.send_email(msg)
    
    def send_zp_email(self, row):
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
        elif "v" in geslacht or "f" in geslacht or geslacht == "vrouw":
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
        
    def send_too_young_email(self, row):
        ontvanger = row.get("email")
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
            
        voornaam = str(row.get("voornaam", "Kandidaat")).strip()

        content = f"""Beste {voornaam} en/of ouder(s)/verzorgers van {voornaam},

Bedankt voor de aanmelding bij AV Sparta! 

We vinden het superleuk dat er al zo vroeg interesse is in atletiek. Naar aanleiding van de geboortedatum hebben we echter geconstateerd dat de kandidaat op dit moment helaas nog iets te jong is om deel te nemen aan onze trainingen. 

Zodra de minimale leeftijd voor onze pupillentrainingen is bereikt, zijn jullie natuurlijk van harte welkom om opnieuw een aanmelding te doen voor de proeftrainingen! Houd hiervoor onze website in de gaten.

Mochten hier nog vragen over zijn, neem dan gerust contact met ons op.

Met sportieve groet,

Jonatan Janssen
Administratie proeftrainingen AV Sparta
Website: www.avsparta.nl"""

        msg = EmailMessage()
        msg['Subject'] = "Aanmelding proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content(content)
        
        self.send_email(msg)
        print(f"Te jong-mail succesvol verstuurd naar {ontvanger}!")

    def send_too_old_email(self, row):
        ontvanger = row.get("email")
        if not ontvanger:
            print("geen ontvanger opgegeven, geen mail verzonden")
            return
            
        voornaam = str(row.get("voornaam", "Kandidaat")).strip()

        content = f"""Beste {voornaam},

Bedankt voor je aanmelding voor de proeftrainingen bij AV Sparta!

Naar aanleiding van je geboortedatum hebben we gezien dat je helaas te oud bent voor onze specifieke jeugd- en juniorencategorieën waar deze aanmeldprocedure voor bedoeld is. 

Mocht je toch interesse hebben in atletiek of hardlopen voor oudere jeugd/volwassenen, dan kijken we graag samen naar de mogelijkheden binnen onze loopgroepen of baanatletiek voor senioren. Neem hiervoor even contact op met onze ledenadministratie via de website.

Met vriendelijke groet,

Jonatan Janssen
Administratie proeftrainingen AV Sparta
Website: www.avsparta.nl"""

        msg = EmailMessage()
        msg['Subject'] = "Aanmelding proeftraining AV Sparta"
        msg['From'] = self.config.gmail_user
        msg['To'] = ontvanger
        msg.set_content(content)
        
        self.send_email(msg)
        print(f"Te oud-mail succesvol verstuurd naar {ontvanger}!")

