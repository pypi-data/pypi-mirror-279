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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from wordlift_client.models.filter import Filter
from typing import Optional, Set
from typing_extensions import Self

class VectorSearchQueryRequest(BaseModel):
    """
    A query request.
    """ # noqa: E501
    fields: Optional[List[StrictStr]] = Field(default=None, description="List of extra fields to be retrieved.")
    filters: Optional[List[Filter]] = Field(default=None, description="A list of prefilters.")
    query_embedding: Optional[List[Union[StrictFloat, StrictInt]]] = Field(default=None, description="The list of embeddings, not required if `query_string` is provided.")
    query_string: Optional[StrictStr] = Field(default=None, description="The query string, not required if the `query_embeddings` are provided. Please note that the `query_string` is ignored if the `query_embeddings` are provided.")
    query_uri: Optional[StrictStr] = Field(default=None, description="Perform a Vector Search based on similarities with an entity with the specified URI.")
    query_url: Optional[StrictStr] = Field(default=None, description="Perform a Vector Search based on similarities with an entity with the specified URL (schema:url).")
    similarity_top_k: Optional[Annotated[int, Field(strict=True, ge=1)]] = Field(default=2, description="The similarity top K.")
    __properties: ClassVar[List[str]] = ["fields", "filters", "query_embedding", "query_string", "query_uri", "query_url", "similarity_top_k"]

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
        """Create an instance of VectorSearchQueryRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in filters (list)
        _items = []
        if self.filters:
            for _item in self.filters:
                if _item:
                    _items.append(_item.to_dict())
            _dict['filters'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of VectorSearchQueryRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "fields": obj.get("fields"),
            "filters": [Filter.from_dict(_item) for _item in obj["filters"]] if obj.get("filters") is not None else None,
            "query_embedding": obj.get("query_embedding"),
            "query_string": obj.get("query_string"),
            "query_uri": obj.get("query_uri"),
            "query_url": obj.get("query_url"),
            "similarity_top_k": obj.get("similarity_top_k") if obj.get("similarity_top_k") is not None else 2
        })
        return _obj


