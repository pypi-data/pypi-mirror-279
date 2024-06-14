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
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from iparapheur_internal.models.gdpr_cookie import GdprCookie
from iparapheur_internal.models.gdpr_data_element import GdprDataElement
from iparapheur_internal.models.gdpr_data_set import GdprDataSet
from iparapheur_internal.models.gdpr_entity import GdprEntity
from typing import Optional, Set
from typing_extensions import Self

class GdprApplication(BaseModel):
    """
    GdprApplication
    """ # noqa: E501
    name: Optional[StrictStr] = None
    cookie_session_duration: Optional[StrictStr] = Field(default=None, alias="cookieSessionDuration")
    mandatory_cookies: Optional[List[StrictStr]] = Field(default=None, alias="mandatoryCookies")
    preserved_data_after_deletion: Optional[List[StrictStr]] = Field(default=None, alias="preservedDataAfterDeletion")
    optional_cookies: Optional[List[GdprCookie]] = Field(default=None, alias="optionalCookies")
    no_cookies: Optional[StrictBool] = Field(default=None, alias="noCookies")
    editor: Optional[GdprEntity] = None
    no_data_processed: Optional[StrictBool] = Field(default=None, alias="noDataProcessed")
    no_data_collected: Optional[StrictBool] = Field(default=None, alias="noDataCollected")
    data_processes: Optional[List[GdprDataElement]] = Field(default=None, alias="dataProcesses")
    collected_data_set: Optional[List[GdprDataSet]] = Field(default=None, alias="collectedDataSet")
    __properties: ClassVar[List[str]] = ["name", "cookieSessionDuration", "mandatoryCookies", "preservedDataAfterDeletion", "optionalCookies", "noCookies", "editor", "noDataProcessed", "noDataCollected", "dataProcesses", "collectedDataSet"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GdprApplication from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in optional_cookies (list)
        _items = []
        if self.optional_cookies:
            for _item in self.optional_cookies:
                if _item:
                    _items.append(_item.to_dict())
            _dict['optionalCookies'] = _items
        # override the default output from pydantic by calling `to_dict()` of editor
        if self.editor:
            _dict['editor'] = self.editor.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in data_processes (list)
        _items = []
        if self.data_processes:
            for _item in self.data_processes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['dataProcesses'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in collected_data_set (list)
        _items = []
        if self.collected_data_set:
            for _item in self.collected_data_set:
                if _item:
                    _items.append(_item.to_dict())
            _dict['collectedDataSet'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GdprApplication from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "cookieSessionDuration": obj.get("cookieSessionDuration"),
            "mandatoryCookies": obj.get("mandatoryCookies"),
            "preservedDataAfterDeletion": obj.get("preservedDataAfterDeletion"),
            "optionalCookies": [GdprCookie.from_dict(_item) for _item in obj["optionalCookies"]] if obj.get("optionalCookies") is not None else None,
            "noCookies": obj.get("noCookies"),
            "editor": GdprEntity.from_dict(obj["editor"]) if obj.get("editor") is not None else None,
            "noDataProcessed": obj.get("noDataProcessed"),
            "noDataCollected": obj.get("noDataCollected"),
            "dataProcesses": [GdprDataElement.from_dict(_item) for _item in obj["dataProcesses"]] if obj.get("dataProcesses") is not None else None,
            "collectedDataSet": [GdprDataSet.from_dict(_item) for _item in obj["collectedDataSet"]] if obj.get("collectedDataSet") is not None else None
        })
        return _obj


