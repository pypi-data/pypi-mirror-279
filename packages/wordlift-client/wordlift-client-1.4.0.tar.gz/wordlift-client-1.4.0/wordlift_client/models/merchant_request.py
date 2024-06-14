# coding: utf-8

"""
    Middleware

    Knowledge Graph data management.

    The version of the OpenAPI document: 1.0
    Contact: hello@wordlift.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class MerchantRequest(BaseModel):
    """
    The Merchant request
    """ # noqa: E501
    access_token: Optional[StrictStr] = Field(default=None, description="Google Merchant access token")
    dataset_domain: Optional[StrictStr] = Field(default=None, description="The custom domain (for example data.example.org)")
    dataset_name: Optional[StrictStr] = Field(default=None, description="The dataset path (for example \"data\")")
    deleted: Optional[StrictBool] = Field(default=False, description="True if the merchant has been deleted")
    google_merchant_id: StrictInt = Field(description="The Google Merchant id")
    ignore_brand: Optional[StrictBool] = Field(default=None, description="Whether to ignore the `brand` property during validation")
    ignore_image: Optional[StrictBool] = Field(default=None, description="Whether to ignore the `image` property during validation")
    publisher_name: StrictStr = Field(description="The publisher name (shows in schema publisher)")
    refresh_token: StrictStr = Field(description="Google Merchant refresh token")
    url: StrictStr = Field(description="The website URL")
    writer_service: Optional[StrictStr] = Field(default=None, description="How to write the merchant data to the graph, if unsure, do not set anything (by default `wordpressMerchantWriter`).")
    __properties: ClassVar[List[str]] = ["access_token", "dataset_domain", "dataset_name", "deleted", "google_merchant_id", "ignore_brand", "ignore_image", "publisher_name", "refresh_token", "url", "writer_service"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of MerchantRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MerchantRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "access_token": obj.get("access_token"),
            "dataset_domain": obj.get("dataset_domain"),
            "dataset_name": obj.get("dataset_name"),
            "deleted": obj.get("deleted") if obj.get("deleted") is not None else False,
            "google_merchant_id": obj.get("google_merchant_id"),
            "ignore_brand": obj.get("ignore_brand"),
            "ignore_image": obj.get("ignore_image"),
            "publisher_name": obj.get("publisher_name"),
            "refresh_token": obj.get("refresh_token"),
            "url": obj.get("url"),
            "writer_service": obj.get("writer_service")
        })
        return _obj


