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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wordlift_client.models.website_search import WebsiteSearch
from typing import Optional, Set
from typing_extensions import Self

class PageWebsiteSearch(BaseModel):
    """
    A page object with links to move to other pages and the list of objects.
    """ # noqa: E501
    first: Optional[StrictStr] = Field(description="The link to the first page.")
    items: List[WebsiteSearch] = Field(description="An array of objects.")
    last: Optional[StrictStr] = Field(description="The link to the last page.")
    next: Optional[StrictStr] = Field(description="The link to the next page or `null` if there's no page.")
    prev: Optional[StrictStr] = Field(description="The link to the previous page or `null` if there's no page.")
    var_self: Optional[StrictStr] = Field(description="The link to the current page.", alias="self")
    __properties: ClassVar[List[str]] = ["first", "items", "last", "next", "prev", "self"]

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
        """Create an instance of PageWebsiteSearch from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item in self.items:
                if _item:
                    _items.append(_item.to_dict())
            _dict['items'] = _items
        # set to None if first (nullable) is None
        # and model_fields_set contains the field
        if self.first is None and "first" in self.model_fields_set:
            _dict['first'] = None

        # set to None if last (nullable) is None
        # and model_fields_set contains the field
        if self.last is None and "last" in self.model_fields_set:
            _dict['last'] = None

        # set to None if next (nullable) is None
        # and model_fields_set contains the field
        if self.next is None and "next" in self.model_fields_set:
            _dict['next'] = None

        # set to None if prev (nullable) is None
        # and model_fields_set contains the field
        if self.prev is None and "prev" in self.model_fields_set:
            _dict['prev'] = None

        # set to None if var_self (nullable) is None
        # and model_fields_set contains the field
        if self.var_self is None and "var_self" in self.model_fields_set:
            _dict['self'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PageWebsiteSearch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "first": obj.get("first"),
            "items": [WebsiteSearch.from_dict(_item) for _item in obj["items"]] if obj.get("items") is not None else None,
            "last": obj.get("last"),
            "next": obj.get("next"),
            "prev": obj.get("prev"),
            "self": obj.get("self")
        })
        return _obj


