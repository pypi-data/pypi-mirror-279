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

from pydantic import BaseModel, Field, StrictBytes, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from iparapheur_provisioning.models.seal_certificate_dto import SealCertificateDto
from typing import Optional, Set
from typing_extensions import Self

class UpdateSealCertificateRequest(BaseModel):
    """
    UpdateSealCertificateRequest
    """ # noqa: E501
    seal_certificate: SealCertificateDto = Field(alias="sealCertificate")
    certificate_file: Optional[Union[StrictBytes, StrictStr]] = Field(default=None, description="Certificate file", alias="certificateFile")
    image_file: Optional[Union[StrictBytes, StrictStr]] = Field(default=None, description="Image file", alias="imageFile")
    __properties: ClassVar[List[str]] = ["sealCertificate", "certificateFile", "imageFile"]

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
        """Create an instance of UpdateSealCertificateRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of seal_certificate
        if self.seal_certificate:
            _dict['sealCertificate'] = self.seal_certificate.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateSealCertificateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "sealCertificate": SealCertificateDto.from_dict(obj["sealCertificate"]) if obj.get("sealCertificate") is not None else None,
            "certificateFile": obj.get("certificateFile"),
            "imageFile": obj.get("imageFile")
        })
        return _obj


