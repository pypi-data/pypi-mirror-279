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


class TemplateType(str, Enum):
    """
    TemplateType
    """

    """
    allowed enum values
    """
    MAIL_NOTIFICATION_SINGLE = 'MAIL_NOTIFICATION_SINGLE'
    MAIL_NOTIFICATION_DIGEST = 'MAIL_NOTIFICATION_DIGEST'
    MAIL_ACTION_SEND = 'MAIL_ACTION_SEND'
    SIGNATURE_SMALL = 'SIGNATURE_SMALL'
    SIGNATURE_MEDIUM = 'SIGNATURE_MEDIUM'
    SIGNATURE_LARGE = 'SIGNATURE_LARGE'
    SIGNATURE_ALTERNATE_1 = 'SIGNATURE_ALTERNATE_1'
    SIGNATURE_ALTERNATE_2 = 'SIGNATURE_ALTERNATE_2'
    SEAL_AUTOMATIC = 'SEAL_AUTOMATIC'
    SEAL_MEDIUM = 'SEAL_MEDIUM'
    SEAL_LARGE = 'SEAL_LARGE'
    SEAL_ALTERNATE = 'SEAL_ALTERNATE'
    DOCKET = 'DOCKET'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TemplateType from a JSON string"""
        return cls(json.loads(json_str))


