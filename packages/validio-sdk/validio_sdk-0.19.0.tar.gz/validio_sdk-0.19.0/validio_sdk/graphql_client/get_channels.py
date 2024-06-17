from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from .base_model import BaseModel


class GetChannels(BaseModel):
    channels: List[
        Annotated[
            Union[
                "GetChannelsChannelsChannel",
                "GetChannelsChannelsMsTeamsChannel",
                "GetChannelsChannelsSlackChannel",
                "GetChannelsChannelsWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetChannelsChannelsChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List["GetChannelsChannelsChannelNotificationRules"] = Field(
        alias="notificationRules"
    )


class GetChannelsChannelsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelsChannelsMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List["GetChannelsChannelsMsTeamsChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "GetChannelsChannelsMsTeamsChannelConfig"


class GetChannelsChannelsMsTeamsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelsChannelsMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class GetChannelsChannelsSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List["GetChannelsChannelsSlackChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "GetChannelsChannelsSlackChannelConfig"


class GetChannelsChannelsSlackChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelsChannelsSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class GetChannelsChannelsWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: str = Field(alias="namespaceId")
    resource_namespace: str = Field(alias="resourceNamespace")
    notification_rules: List["GetChannelsChannelsWebhookChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "GetChannelsChannelsWebhookChannelConfig"


class GetChannelsChannelsWebhookChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class GetChannelsChannelsWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


GetChannels.model_rebuild()
GetChannelsChannelsChannel.model_rebuild()
GetChannelsChannelsMsTeamsChannel.model_rebuild()
GetChannelsChannelsSlackChannel.model_rebuild()
GetChannelsChannelsWebhookChannel.model_rebuild()
