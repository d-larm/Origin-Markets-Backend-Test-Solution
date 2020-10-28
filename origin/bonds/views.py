from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core import serializers
from bonds.serializers import BondSerializer
from bonds.models import Bond
import requests
import json



class HelloWorld( APIView ):
    def get( self, request ):
        return Response( "Hello World!" )


class Bonds( APIView ):
    permission_classes = ( IsAuthenticated, )

    @staticmethod
    def getLegalName( lei ): # Retrieves the legal name from the GLEIF API
        URL = "https://leilookup.gleif.org/api/v2/leirecords?lei="+lei
        legalNameRequest = requests.get( URL )
        legalNameData = legalNameRequest.json()
        return legalNameData[0]['Entity']['LegalName']['$'].replace( " ", "" ) 

    def get( self, request ):
        result = Bond.objects.all().filter( user=request.user )
        for key, value in request.GET.items(): # Filters by any URL parameters
            result = result.filter( **{ key: value } )
        return Response( BondSerializer( result, many=True ).data )
    
    def post( self, request ):
        bondData = request.data
        bondData['legal_name'] = self.getLegalName( bondData['lei'] )
        bondData['user'] = request.user # Add user object to make bond exclusive to current user 
        instance = Bond.objects.create( **bondData )
        return Response( BondSerializer( instance=instance ).data )