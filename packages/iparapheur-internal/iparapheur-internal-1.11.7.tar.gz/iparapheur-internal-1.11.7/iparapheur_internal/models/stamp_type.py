# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class StampType(str, Enum):
    """
    StampType
    """

    """
    allowed enum values
    """
    SIGNATURE = 'SIGNATURE'
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    METADATA = 'METADATA'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of StampType from a JSON string"""
        return cls(json.loads(json_str))


