import datetime

from django import forms
from django.urls import reverse_lazy

from .models import Party


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ["party_date", "party_time", "venue", "invitation"]
        widgets = {
            "party_date": forms.DateInput(
                attrs={
                    "type": "date",
                    # NEW
                    "hx-get": reverse_lazy("partial_check_party_date"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_party_date",
                }
            ),
            "party_time": forms.TimeInput(attrs={"type": "time"}),
            "invitation": forms.Textarea(
                attrs={
                    "rows": 10,
                    "cols": 30,
                    # NEW
                    "hx-get": reverse_lazy("partial_check_invitation"),
                    "hx-trigger": "blur",
                    "hx-swap": "outerHTML",
                    "hx-target": "#div_id_invitation",
                }
            ),
        }

    def clean_invitation(self):
        invitation = self.cleaned_data["invitation"]

        if len(invitation) < 10:
            raise forms.ValidationError("Invitation must be at least 10 characters long.")

        return invitation


    def clean_party_date(self):
        party_date = self.cleaned_data["party_date"]

        if party_date < datetime.date.today():
            raise forms.ValidationError("Party date must be in the future.")

        return party_date