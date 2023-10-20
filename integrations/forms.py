from django import forms

from integrations.importers import GoodreadsImporter, SimklImporter


class ImportTrackingDataForm(forms.Form):
    import_format = forms.ChoiceField(
        choices=(
            (GoodreadsImporter.IMPORTER_NAME, "Goodreads (.csv)"),
            (SimklImporter.IMPORTER_NAME, "Simkl (.csv)"),
        )
    )
    import_file = forms.FileField()
