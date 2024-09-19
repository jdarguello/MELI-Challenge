from src.tests.testconfig import TestConfig
from src.application.usecases.identity_provider_service import IdentityProviderService
from sqlalchemy.orm.exc import NoResultFound

class TestIdentityProviderService(TestConfig):
    def setUp(self):
        super().setUp()
        self.identityProviderService = IdentityProviderService()

        # idps
        self.google = {"clientId": "10394", "name": "Google", "clientSecret": "1j3n", "baseUrl": "https://www.google.com", "tokenUrl": "https://www.google.com/oauth/token", "authorizationUrl": "https://www.google.com/oauth/authorize", "redirectUrl": "https://www.google.com/oauth/redirect"}
        self.facebook = {"clientId": "10395", "name": "Facebook", "clientSecret": "1j3n", "baseUrl": "https://www.facebook.com", "tokenUrl": "https://www.facebook.com/oauth/token", "authorizationUrl": "https://www.facebook.com/oauth/authorize", "redirectUrl": "https://www.facebook.com/oauth/redirect"}
        self.twitter = {"clientId": "10396", "name": "Twitter", "clientSecret": "1j3n", "baseUrl": "https://www.twitter.com", "tokenUrl": "https://www.twitter.com/oauth/token", "authorizationUrl": "https://www.twitter.com/oauth/authorize", "redirectUrl": "https://www.twitter.com/oauth/redirect"}

    def test_create_and_get_idps(self):
        for idp_info in [self.google, self.facebook, self.twitter]:
            idp = self.identityProviderService.create(**idp_info)
            self.assertIsNotNone(idp.identityProviderId)
            self.assertEqual(idp.name, idp_info["name"])
            self.assertEqual(idp.clientId, self.identityProviderService.get(idp.name).clientId)
    
    def test_get_idp_that_not_exists(self):
        self.assertIsNone(self.identityProviderService.get("NotExists"))
    
    def test_update_idp(self):
        google = self.identityProviderService.create(**self.google)

        new_google = self.identityProviderService.update(google.name, clientSecret="2j3n")
        self.assertEqual(google.identityProviderId, new_google.identityProviderId)
        self.assertEqual("2j3n", self.identityProviderService.get(self.google["name"]).clientSecret)
    
    def test_update_idp_that_not_exists(self):
        amazon_ad = "Amazon Active Directory"
        with self.assertRaises(NoResultFound) as error:
            self.identityProviderService.update(amazon_ad, clientSecret="2j3n")
        self.assertEqual(str(error.exception), "Identity Provider with name '" + amazon_ad + "' not found")

    def test_update_idp_with_non_existant_attribute(self):
        google = self.identityProviderService.create(**self.google)
        with self.assertRaises(AttributeError) as error:
            self.identityProviderService.update(self.google["name"], non_existant_attribute="2j3n")
        self.assertEqual(str(error.exception), "Identity Provider object has no attribute of Type:'non_existant_attribute'")

    def test_delete_idp_that_exists(self):
        facebook = self.identityProviderService.create(**self.facebook)
        self.assertIsNotNone(self.identityProviderService.get(facebook.name))
        self.identityProviderService.delete(facebook.name)
        self.assertIsNone(self.identityProviderService.get(facebook.name))

    def test_delete_permission_that_not_exists(self):
        amazon_ad = "Amazon Active Directory"
        with self.assertRaises(NoResultFound) as error:
            self.identityProviderService.delete(amazon_ad)
        self.assertEqual(str(error.exception), "Identity Provider with name '" + amazon_ad + "' not found")