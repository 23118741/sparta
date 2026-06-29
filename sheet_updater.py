from sheets_config import GoogleSheetsConfig

class SheetUpdater:
    """Verantwoordelijk voor acties/updates binnen Google Sheets."""
    def __init__(self, config: GoogleSheetsConfig):
        self.config = config

    def get_all_rows(self):
        return self.config.sheet.get_all_records()

    def get_first_row(self):
        all_data = self.config.sheet.get_all_records()
        if all_data:
            print("First row of data:", all_data[0])
            return all_data[0]
        print("Geen data gevonden in de sheet.")
        return None

    def get_column_index(self, header_name):
        """Zoekt de 1-gebaseerde kolomindex op basis van de kolomnaam in de eerste rij."""
        headers = self.config.sheet.row_values(1)
        try:
            return headers.index(header_name) + 1
        except ValueError:
            print(f"Kolom '{header_name}' niet gevonden in de sheet.")
            return None

    def update_cell(self, row, col, value):
        self.config.sheet.update_cell(row, col, value)
        print(f"Cell ({row}, {col}) updated successfully to '{value}'!")

    def update_gender_cell(self, row=2, col=5, value="man"):
        self.update_cell(row, col, value)

    def init_wachtlijst_headers(self):
        if not self.config.wachtlijst_sheet:
            return
        vals = self.config.wachtlijst_sheet.get_all_values()
        if not vals:
            # GECORRIGEERD: "email" toegevoegd zodat dit matcht met 'wachtlijst_rij'
            headers = ["voornaam", "achternaam", "email", "leeftijdscategorie", "geboortedatum", "wachtlijst_plek"]
            self.config.wachtlijst_sheet.append_row(headers)
            print("Wachtlijst headers aangemaakt.")

    def get_wachtlijst_counts_per_categorie(self):
        if not self.config.wachtlijst_sheet:
            return {}
        try:
            records = self.config.wachtlijst_sheet.get_all_records()
            counts = {}
            for r in records:
                cat = str(r.get("leeftijdscategorie", "")).strip().upper()
                if cat:
                    counts[cat] = counts.get(cat, 0) + 1
            return counts
        except Exception:
            return {}

    def get_wachtlijst_keys(self):
        """Geeft een lijst van (voornaam, achternaam, geboortedatum) tuples terug om te checken wie er al in staan."""
        if not self.config.wachtlijst_sheet:
            return []
        try:
            records = self.config.wachtlijst_sheet.get_all_records()
            return [
                (
                    str(r.get("voornaam", "")).strip().lower(),
                    str(r.get("achternaam", "")).strip().lower(),
                    str(r.get("geboortedatum", "")).strip().lower()
                )
                for r in records
            ]
        except Exception:
            return []

    def append_to_wachtlijst(self, row_data):
        if self.config.wachtlijst_sheet:
            self.config.wachtlijst_sheet.append_row(row_data)
            print(f"Toegevoegd aan wachtlijst: {row_data}")