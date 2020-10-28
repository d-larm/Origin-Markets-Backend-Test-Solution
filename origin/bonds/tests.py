from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from bonds.views import Bonds
from bonds.models import Bond


class HelloWorld( APITestCase ):
    bondData = {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    }

    apiData = bondData.copy()

    def setUp( self ): # Initialise users
        User = get_user_model()
        user1 = User.objects.create_user('test', 'test@test.com', 'test')
        user2 = User.objects.create_user('test2', 'test2@test.com', 'test2')
        self.bondData['user'] = user1
    
    def test_root( self ):
        resp = self.client.get( "/" )
        assert resp.status_code == 200
    
    def test_no_auth( self ): # Test failed authentication
        resp = self.client.get( "/bonds/" )
        assert resp.status_code == 403
    
    def test_create_user( self ): # Test creation of users
        userData = {
            'username': 'test_user',
            'password': 'test',
            'email': 'test_user@test.com',
        }
        resp = self.client.post( "/create-user/", userData, format="json" )
        assert resp.status_code == 200
        assert len( resp.data ) > 0
        assert resp.data['token'] != None
    
    def test_legal_name( self ): # Test retrieval of legal name given the lei
        result = Bonds.getLegalName( "R0MUWSFPU8MPRO8K5P83" )
        assert result == "BNPPARIBAS"

    def test_bonds_get_user( self ): # Test if users only have access to their own data
        Bond.objects.create( **self.bondData )
        self.client.login( username='test', password='test' )
        resp1 = self.client.get( "/bonds/" )
        self.client.logout()
        self.client.login( username='test2', password='test2' )
        resp2 = self.client.get( "/bonds/" )

        assert resp1.status_code == 200 
        assert resp2.status_code == 200

        assert len( resp1.data ) == 1
        assert len( resp2.data ) == 0

        assert resp1.data[0] == self.apiData

    def test_bonds_get_all_api( self ): # Test getting all bonds for a user
        Bond.objects.create( **self.bondData )
        Bond.objects.create( **self.bondData )
        Bond.objects.create( **{ **self.bondData, 'user' : get_user_model().objects.get(username='test2') } )

        self.client.login( username='test', password='test' )
        resp = self.client.get( "/bonds/")
        assert ( resp.status_code == 200 )
        assert( len( resp.data ) == 2 )
        assert resp.data[0] == self.apiData

    def test_bonds_get_single_api( self ): # Test getting a single bond for a user
        Bond.objects.create( **self.bondData )
        Bond.objects.create( **{ **self.bondData, 'legal_name': 'BNPPPPPPPPP'} )
        self.client.login( username='test', password='test' )
        resp = self.client.get( "/bonds/?legal_name=BNPPARIBAS")
        assert ( resp.status_code == 200 )
        assert len( resp.data ) == 1
        assert( resp.data[0] == self.apiData )

    def test_bonds_post_api( self ): # Test adding bond data for a user
        originalSize = len(list(Bond.objects.all())) 
        requestData = {
            "isin": "FR0000131104",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83",
        } 

        self.client.login(username='test', password='test')
        resp = self.client.post( "/bonds/", requestData, format='json' )
        assert resp.status_code == 200
        assert resp.data == self.apiData
        assert len( list( Bond.objects.all().values() ) ) == originalSize + 1