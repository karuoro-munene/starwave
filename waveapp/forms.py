from django.forms import ModelForm
from .models import Loans


class LoansForm(ModelForm):
    class Meta:
        model = Loans
        fields = "__all__"
