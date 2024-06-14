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

from wordlift_client.models.analyses_response import AnalysesResponse

class TestAnalysesResponse(unittest.TestCase):
    """AnalysesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AnalysesResponse:
        """Test AnalysesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AnalysesResponse`
        """
        model = AnalysesResponse()
        if include_optional:
            return AnalysesResponse(
                items = [
                    wordlift_client.models.analyses_response_item.AnalysesResponseItem(
                        text = '', 
                        confidence = 0, 
                        occurrences = 56, 
                        serp_position = 56, 
                        entity_id = '', 
                        entity_label = '', 
                        entity_type = '', 
                        entity_description = '', )
                    ]
            )
        else:
            return AnalysesResponse(
        )
        """

    def testAnalysesResponse(self):
        """Test AnalysesResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
