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
from iparapheur_provisioning.models.metadata_dto import MetadataDto
from typing import Optional, Set
from typing_extensions import Self

class SubtypeMetadataDto(BaseModel):
    """
    SubtypeMetadataDto
    """ # noqa: E501
    metadata_id: Optional[StrictStr] = Field(default=None, alias="metadataId")
    metadata: Optional[MetadataDto] = None
    default_value: Optional[StrictStr] = Field(default=None, alias="defaultValue")
    mandatory: Optional[StrictBool] = None
    editable: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["metadataId", "metadata", "defaultValue", "mandatory", "editable"]

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
        """Create an instance of SubtypeMetadataDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        # set to None if default_value (nullable) is None
        # and model_fields_set contains the field
        if self.default_value is None and "default_value" in self.model_fields_set:
            _dict['defaultValue'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SubtypeMetadataDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "metadataId": obj.get("metadataId"),
            "metadata": MetadataDto.from_dict(obj["metadata"]) if obj.get("metadata") is not None else None,
            "defaultValue": obj.get("defaultValue"),
            "mandatory": obj.get("mandatory"),
            "editable": obj.get("editable")
        })
        return _obj


