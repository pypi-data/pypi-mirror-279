# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 1.1.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.conflict_detection_interval import ConflictDetectionInterval
from typing import Optional, Set
from typing_extensions import Self

class TenantSettings(BaseModel):
    """
    TenantSettings
    """ # noqa: E501
    uid: Optional[StrictStr] = Field(default=None, description="The unique identifier of the tenant in CDO.")
    change_request_support: Optional[StrictBool] = Field(default=None, description="Indicates if the tenant supports change requests.", alias="changeRequestSupport")
    auto_accept_device_changes: Optional[StrictBool] = Field(default=None, description="Indicates if changes made out-of-band on devices on the tenant are automatically accepted without manual approval.", alias="autoAcceptDeviceChanges")
    web_analytics: Optional[StrictBool] = Field(default=None, description="Indicates if web analytics are enabled for the tenant.", alias="webAnalytics")
    scheduled_deployments: Optional[StrictBool] = Field(default=None, description="Indicates if the tenant has scheduled deployments enabled.", alias="scheduledDeployments")
    deny_cisco_support_access_to_tenant: Optional[StrictBool] = Field(default=None, description="Indicates if Cisco support is denied access to the tenant.", alias="denyCiscoSupportAccessToTenant")
    multicloud_defense: Optional[StrictBool] = Field(default=None, description="Indicates if the tenant has the multicloud defense enabled.", alias="multicloudDefense")
    ai_assistant: Optional[StrictBool] = Field(default=None, description="Indicates if the tenant has the AI assistant enabled.", alias="aiAssistant")
    auto_discover_on_prem_fmcs: Optional[StrictBool] = Field(default=None, description="Indicates if the system automatically discovers on-premise FMCs.", alias="autoDiscoverOnPremFmcs")
    conflict_detection_interval: Optional[ConflictDetectionInterval] = Field(default=None, alias="conflictDetectionInterval")
    __properties: ClassVar[List[str]] = ["uid", "changeRequestSupport", "autoAcceptDeviceChanges", "webAnalytics", "scheduledDeployments", "denyCiscoSupportAccessToTenant", "multicloudDefense", "aiAssistant", "autoDiscoverOnPremFmcs", "conflictDetectionInterval"]

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
        """Create an instance of TenantSettings from a JSON string"""
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
        """Create an instance of TenantSettings from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "uid": obj.get("uid"),
            "changeRequestSupport": obj.get("changeRequestSupport"),
            "autoAcceptDeviceChanges": obj.get("autoAcceptDeviceChanges"),
            "webAnalytics": obj.get("webAnalytics"),
            "scheduledDeployments": obj.get("scheduledDeployments"),
            "denyCiscoSupportAccessToTenant": obj.get("denyCiscoSupportAccessToTenant"),
            "multicloudDefense": obj.get("multicloudDefense"),
            "aiAssistant": obj.get("aiAssistant"),
            "autoDiscoverOnPremFmcs": obj.get("autoDiscoverOnPremFmcs"),
            "conflictDetectionInterval": obj.get("conflictDetectionInterval")
        })
        return _obj


