# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from iparapheur_internal.models.mail_template_test_request import MailTemplateTestRequest

class TestMailTemplateTestRequest(unittest.TestCase):
    """MailTemplateTestRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MailTemplateTestRequest:
        """Test MailTemplateTestRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MailTemplateTestRequest`
        """
        model = MailTemplateTestRequest()
        if include_optional:
            return MailTemplateTestRequest(
                template = '',
                mail = ''
            )
        else:
            return MailTemplateTestRequest(
        )
        """

    def testMailTemplateTestRequest(self):
        """Test MailTemplateTestRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
