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

from wordlift_client.models.rule_request import RuleRequest

class TestRuleRequest(unittest.TestCase):
    """RuleRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RuleRequest:
        """Test RuleRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RuleRequest`
        """
        model = RuleRequest()
        if include_optional:
            return RuleRequest(
                description = '',
                fixes = [
                    wordlift_client.models.validation_fix.ValidationFix(
                        type = 'FIND_AND_REPLACE', 
                        what = '', 
                        with = '', )
                    ],
                is_enabled = True,
                level = 'RECOMMENDED',
                name = '',
                project_id = 56,
                project_type = 'SMART_CONTENT',
                scope = 'USER',
                type = '',
                what_operand_lhs = 'EVERYWHERE',
                what_operand_rhs = '',
                what_operator = 'CONTAINS',
                when_operand_lhs = '',
                when_operand_rhs = '',
                when_operator = 'ALWAYS'
            )
        else:
            return RuleRequest(
                level = 'RECOMMENDED',
                name = '',
                scope = 'USER',
                type = '',
                what_operand_lhs = 'EVERYWHERE',
                what_operand_rhs = '',
                what_operator = 'CONTAINS',
                when_operand_lhs = '',
                when_operand_rhs = '',
                when_operator = 'ALWAYS',
        )
        """

    def testRuleRequest(self):
        """Test RuleRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
