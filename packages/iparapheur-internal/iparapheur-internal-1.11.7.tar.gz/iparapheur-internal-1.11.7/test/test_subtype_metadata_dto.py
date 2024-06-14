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

from iparapheur_internal.models.subtype_metadata_dto import SubtypeMetadataDto

class TestSubtypeMetadataDto(unittest.TestCase):
    """SubtypeMetadataDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SubtypeMetadataDto:
        """Test SubtypeMetadataDto
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SubtypeMetadataDto`
        """
        model = SubtypeMetadataDto()
        if include_optional:
            return SubtypeMetadataDto(
                metadata_id = '',
                metadata = iparapheur_internal.models.metadata_dto.MetadataDto(
                    id = '', 
                    name = 'Example metadata', 
                    key = 'example_metadata', 
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
            return SubtypeMetadataDto(
        )
        """

    def testSubtypeMetadataDto(self):
        """Test SubtypeMetadataDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
