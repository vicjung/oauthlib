# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from oauthlib.oauth1.rfc5849.signature import *
from oauthlib.common import unicode_type
from ...unittest import TestCase


class SignatureTests(TestCase):

    uri_query = "b5=%3D%253D&a3=a&c%40=&a2=r%20b&c2=&a3=2+q"
    authorization_header = """OAuth realm="Example",
    oauth_consumer_key="9djdj82h48djs9d2",
    oauth_token="kkk9d7dh3k39sjv7",
    oauth_signature_method="HMAC-SHA1",
    oauth_timestamp="137131201",
    oauth_nonce="7d8f3e4a",
    oauth_signature="djosJKDKJSD8743243%2Fjdk33klY%3D" """.strip()
    body = "content=This+is+being+the+body+of+things"
    http_method = b"post"
    base_string_url = quote("http://example.com/request?b5=%3D%253D&a3=a&c%40=&a2=r%20b").encode('utf-8')
    normalized_encoded_request_parameters = quote("""OAuth realm="Example",oauth_consumer_key="9djdj82h48djs9d2",oauth_token="kkk9d7dh3k39sjv7",oauth_signature_method="HMAC-SHA1",oauth_timestamp="137131201",oauth_nonce="7d8f3e4a",oauth_signature="bYT5CMsGcbgUdFHObYMEfcx6bsw%3D" """.strip()).encode('utf-8')
    client_secret = b"ECrDNoq1VYzzzzzzzzzyAK7TwZNtPnkqatqZZZZ"
    resource_owner_secret = b"just-a-string    asdasd"
    control_base_string = "POST&http%253A%2F%2Fexample.com%2Frequest%253Fb5%253D%25253D%2525253D%2526a3%253Da%2526c%252540%253D%2526a2%253Dr%252520b&OAuth%2520realm%253D%2522Example%2522%252Coauth_consumer_key%253D%25229djdj82h48djs9d2%2522%252Coauth_token%253D%2522kkk9d7dh3k39sjv7%2522%252Coauth_signature_method%253D%2522HMAC-SHA1%2522%252Coauth_timestamp%253D%2522137131201%2522%252Coauth_nonce%253D%25227d8f3e4a%2522%252Coauth_signature%253D%2522bYT5CMsGcbgUdFHObYMEfcx6bsw%25253D%2522"

    def test_construct_base_string(self):
        """
        Example text to be turned into a base string::

            POST /request?b5=%3D%253D&a3=a&c%40=&a2=r%20b HTTP/1.1
            Host: example.com
            Content-Type: application/x-www-form-urlencoded
            Authorization: OAuth realm="Example",
                           oauth_consumer_key="9djdj82h48djs9d2",
                           oauth_token="kkk9d7dh3k39sjv7",
                           oauth_signature_method="HMAC-SHA1",
                           oauth_timestamp="137131201",
                           oauth_nonce="7d8f3e4a",
                           oauth_signature="bYT5CMsGcbgUdFHObYMEfcx6bsw%3D"

        Sample Base string generated and tested against::

            POST&http%253A%2F%2Fexample.com%2Frequest%253Fb5%253D%25253D%2525253D
            %2526a3%253Da%2526c%252540%253D%2526a2%253Dr%252520b&OAuth%2520realm%
            253D%2522Example%2522%252Coauth_consumer_key%253D%25229djdj82h48djs9d
            2%2522%252Coauth_token%253D%2522kkk9d7dh3k39sjv7%2522%252Coauth_signa
            ture_method%253D%2522HMAC-SHA1%2522%252Coauth_timestamp%253D%25221371
            31201%2522%252Coauth_nonce%253D%25227d8f3e4a%2522%252Coauth_signature
            %253D%2522bYT5CMsGcbgUdFHObYMEfcx6bsw%25253D%2522
        """

        # Create test variables
        # Create test variables
        # Create test variables

        self.assertRaises(ValueError, construct_base_string, self.http_method, self.base_string_url, self.normalized_encoded_request_parameters)
        self.assertRaises(ValueError, construct_base_string, self.http_method.decode('utf-8'), self.base_string_url, self.normalized_encoded_request_parameters)
        self.assertRaises(ValueError, construct_base_string, self.http_method.decode('utf-8'), self.base_string_url.decode('utf-8'), self.normalized_encoded_request_parameters)

        base_string = construct_base_string(self.http_method.decode('utf-8'), self.base_string_url.decode('utf-8'), self.normalized_encoded_request_parameters.decode('utf-8'))

        self.assertEqual(self.control_base_string, base_string)

    def test_normalize_base_string_uri(self):
        """
        Example text to be turned into a normalized base string uri::

            GET /?q=1 HTTP/1.1
            Host: www.example.net:8080

        Sample string generated::

            https://www.example.net:8080/
        """

        # test for unicode failure
        uri = b"www.example.com:8080"
        self.assertRaises(ValueError, normalize_base_string_uri, uri)

        uri = "http://www.example.com:80"
        self.assertEquals(normalize_base_string_uri(uri), "http://www.example.com")

    def test_collect_parameters(self):
        """ We check against parameters multiple times in case things change after more
                parameters are added.
        """
        # check against empty parameters
        # check against empty parameters
        # check against empty parameters
        self.assertEquals(collect_parameters(), [])

        # Check against uri_query
        # Check against uri_query
        # Check against uri_query

        parameters = collect_parameters(uri_query=self.uri_query)
        correct_parameters = [('b5', '=%3D'),
                              ('a3', 'a'),
                              ('c@', ''),
                              ('a2', 'r b'),
                              ('c2', ''),
                              ('a3', '2 q')]
        self.assertEqual(sorted(parameters), sorted(correct_parameters))

        # check against authorization header as well
        # check against authorization header as well
        # check against authorization header as well

        parameters = collect_parameters(uri_query=self.uri_query, headers={
            'Authorization': self.authorization_header,
        })
        parameters_with_realm = collect_parameters(uri_query=self.uri_query, headers={
            'Authorization': self.authorization_header,
        }, with_realm=True)
        # Redo the checks against all the parameters. Duplicated code but better safety
        correct_parameters += [
            ('oauth_nonce', '7d8f3e4a'),
            ('oauth_timestamp', '137131201'),
            ('oauth_consumer_key', '9djdj82h48djs9d2'),
            ('oauth_signature_method', 'HMAC-SHA1'),
            ('oauth_token', 'kkk9d7dh3k39sjv7')]
        correct_parameters_with_realm = correct_parameters + [('realm', 'Example')]
        self.assertEqual(sorted(parameters), sorted(correct_parameters))
        self.assertEqual(sorted(parameters_with_realm), sorted(correct_parameters_with_realm))

        # Add in the body.
        # TODO - add more valid content for the body. Daniel Greenfeld 2012/03/12
        # Redo again the checks against all the parameters. Duplicated code but better safety
        parameters = collect_parameters(uri_query=self.uri_query,
            body=self.body, headers={
                'Authorization': self.authorization_header,
            })
        correct_parameters += [
            ('content', 'This is being the body of things')]
        self.assertEqual(sorted(parameters), sorted(correct_parameters))

    def test_normalize_parameters(self):
        """ We copy some of the variables from the test method above."""

        # Create the parameters
        parameters = collect_parameters(uri_query=self.uri_query,
            body=self.body, headers={
                'Authorization': self.authorization_header,
            })
        normalized = normalize_parameters(parameters)

        # check the parameters type
        self.assertIsInstance(normalized, unicode_type)

        # Lets see if things are in order
        # check to see that querystring keys come in alphanumeric order:
        querystring_keys = ['a2', 'a3', 'b5', 'content', 'oauth_consumer_key', 'oauth_nonce', 'oauth_signature_method', 'oauth_timestamp', 'oauth_token']
        index = -1  # start at -1 because the 'a2' key starts at index 0
        for key in querystring_keys:
            self.assertGreater(normalized.index(key), index)
            index = normalized.index(key)

    def test_sign_hmac_sha1(self):
        """ Verifying correct HMAC-SHA1 signature against one created by openssl."""

        # self.control_base_string saved in <message>, hmac_key in <key>.
        # hmac_key = "ECrDNoq1VYzzzzzzzzzyAK7TwZNtPnkqatqZZZZ&just-a-string%20%20%20%20asdasd"
        # Control signature created using openssl:
        # $ echo -n $(cat <message>) | openssl dgst -binary -hmac <key> | base64
        control_signature = "Uau4O9Kpd2k6rvh7UZN/RN+RG7Y="

        # check for Unicode
        self.assertRaises(ValueError, sign_hmac_sha1, self.control_base_string, self.client_secret, self.resource_owner_secret)

        # Do the actual test
        sign = sign_hmac_sha1(self.control_base_string, self.client_secret.decode('utf-8'), self.resource_owner_secret.decode('utf-8'))
        self.assertEquals(len(sign), 28)
        self.assertEquals(sign, control_signature)

    def test_sign_rsa_sha1(self):
        """ Verify correct RSA-SHA1 signature against one created by openssl."""

        base_string = b"POST&http%253A%2F%2Fexample.com%2Frequest%253Fb5%253D%25253D%2525253D%2526a3%253Da%2526c%252540%253D%2526a2%253Dr%252520b&OAuth%2520realm%253D%2522Example%2522%252Coauth_consumer_key%253D%25229djdj82h48djs9d2%2522%252Coauth_token%253D%2522kkk9d7dh3k39sjv7%2522%252Coauth_signature_method%253D%2522HMAC-SHA1%2522%252Coauth_timestamp%253D%2522137131201%2522%252Coauth_nonce%253D%25227d8f3e4a%2522%252Coauth_signature%253D%2522bYT5CMsGcbgUdFHObYMEfcx6bsw%25253D%2522"

        # Generated using: $ openssl genrsa -out <key>.pem 1024
        # PyCrypto / python-rsa requires the key to be concatenated with linebreaks.
        private_key = b"-----BEGIN RSA PRIVATE KEY-----\nMIICXgIBAAKBgQDk1/bxyS8Q8jiheHeYYp/4rEKJopeQRRKKpZI4s5i+UPwVpupG\nAlwXWfzXwSMaKPAoKJNdu7tqKRniqst5uoHXw98gj0x7zamu0Ck1LtQ4c7pFMVah\n5IYGhBi2E9ycNS329W27nJPWNCbESTu7snVlG8V8mfvGGg3xNjTMO7IdrwIDAQAB\nAoGBAOQ2KuH8S5+OrsL4K+wfjoCi6MfxCUyqVU9GxocdM1m30WyWRFMEz2nKJ8fR\np3vTD4w8yplTOhcoXdQZl0kRoaDzrcYkm2VvJtQRrX7dKFT8dR8D/Tr7dNQLOXfC\nDY6xveQczE7qt7Vk7lp4FqmxBsaaEuokt78pOOjywZoInjZhAkEA9wz3zoZNT0/i\nrf6qv2qTIeieUB035N3dyw6f1BGSWYaXSuerDCD/J1qZbAPKKhyHZbVawFt3UMhe\n542UftBaxQJBAO0iJy1I8GQjGnS7B3yvyH3CcLYGy296+XO/2xKp/d/ty1OIeovx\nC60pLNwuFNF3z9d2GVQAdoQ89hUkOtjZLeMCQQD0JO6oPHUeUjYT+T7ImAv7UKVT\nSuy30sKjLzqoGw1kR+wv7C5PeDRvscs4wa4CW9s6mjSrMDkDrmCLuJDtmf55AkEA\nkmaMg2PNrjUR51F0zOEFycaaqXbGcFwe1/xx9zLmHzMDXd4bsnwt9kk+fe0hQzVS\nJzatanQit3+feev1PN3QewJAWv4RZeavEUhKv+kLe95Yd0su7lTLVduVgh4v5yLT\nGa6FHdjGPcfajt+nrpB1n8UQBEH9ZxniokR/IPvdMlxqXA==\n-----END RSA PRIVATE KEY-----"

        # Base string saved in "<message>". Signature obtained using:
        # $ echo -n $(cat <message>) | openssl dgst -sign <key>.pem | base64
        # where echo -n suppresses the last linebreak.
        control_signature = "zV5g8ArdMuJuOXlH8XOqfLHS11XdthfIn4HReDm7jz8JmgLabHGmVBqCkCfZoFJPHdka7tLvCplK/jsV4FUOnftrJOQhbXguuBdi87/hmxOFKLmQYqqlEW7BdXmwKLZckiqq3qE5XziBgKSAFRkxJ4gmJAymvJBtrJYN9728rK8="

        sign = sign_rsa_sha1(base_string, private_key)
        self.assertEquals(sign, control_signature)

    def test_sign_plaintext(self):
        """ """

        self.assertRaises(ValueError, sign_plaintext, self.client_secret, self.resource_owner_secret)
        sign = sign_plaintext(self.client_secret.decode('utf-8'), self.resource_owner_secret.decode('utf-8'))
        self.assertEquals(sign, "ECrDNoq1VYzzzzzzzzzyAK7TwZNtPnkqatqZZZZ&just-a-string%20%20%20%20asdasd")
