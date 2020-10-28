from bonds.models import Bond
from rest_framework import serializers



class BondSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']
