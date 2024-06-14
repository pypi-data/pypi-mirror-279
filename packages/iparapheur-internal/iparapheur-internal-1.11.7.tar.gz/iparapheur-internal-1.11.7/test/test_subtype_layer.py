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

from iparapheur_internal.models.subtype_layer import SubtypeLayer

class TestSubtypeLayer(unittest.TestCase):
    """SubtypeLayer unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SubtypeLayer:
        """Test SubtypeLayer
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SubtypeLayer`
        """
        model = SubtypeLayer()
        if include_optional:
            return SubtypeLayer(
                id = iparapheur_internal.models.composite_id.CompositeId(
                    layer_id = '', ),
                association = 'ALL'
            )
        else:
            return SubtypeLayer(
        )
        """

    def testSubtypeLayer(self):
        """Test SubtypeLayer"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
