# coding: utf-8

"""
    Analysis

    Analyse content using Linked Data and Knowledge Graphs.

    The version of the OpenAPI document: 1.0
    Contact: hello@wordlift.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from wordlift_client.models.create_seo_score200_response import CreateSEOScore200Response

class TestCreateSEOScore200Response(unittest.TestCase):
    """CreateSEOScore200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateSEOScore200Response:
        """Test CreateSEOScore200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateSEOScore200Response`
        """
        model = CreateSEOScore200Response()
        if include_optional:
            return CreateSEOScore200Response(
                analyze = '[{"M": 2, "T": 2, "O": 2}]'
            )
        else:
            return CreateSEOScore200Response(
        )
        """

    def testCreateSEOScore200Response(self):
        """Test CreateSEOScore200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
