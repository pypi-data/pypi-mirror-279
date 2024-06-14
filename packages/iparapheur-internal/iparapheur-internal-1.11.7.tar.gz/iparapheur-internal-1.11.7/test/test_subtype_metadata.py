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

from iparapheur_internal.models.subtype_metadata import SubtypeMetadata

class TestSubtypeMetadata(unittest.TestCase):
    """SubtypeMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SubtypeMetadata:
        """Test SubtypeMetadata
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SubtypeMetadata`
        """
        model = SubtypeMetadata()
        if include_optional:
            return SubtypeMetadata(
                id = iparapheur_internal.models.composite_id.CompositeId(
                    layer_id = '', ),
                metadata = iparapheur_internal.models.metadata.Metadata(
                    id = '', 
                    key = '', 
                    name = '', 
                    index = 56, 
                    type = 'TEXT', 
                    restricted_values = [
                        ''
                        ], ),
                default_value = '',
                mandatory = True,
                editable = True
            )
        else:
            return SubtypeMetadata(
        )
        """

    def testSubtypeMetadata(self):
        """Test SubtypeMetadata"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
