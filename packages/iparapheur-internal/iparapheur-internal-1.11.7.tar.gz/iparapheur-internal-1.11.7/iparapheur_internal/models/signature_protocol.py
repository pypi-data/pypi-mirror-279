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


class SignatureProtocol(str, Enum):
    """
    SignatureProtocol
    """

    """
    allowed enum values
    """
    HELIOS = 'HELIOS'
    ACTES = 'ACTES'
    NONE = 'NONE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SignatureProtocol from a JSON string"""
        return cls(json.loads(json_str))


