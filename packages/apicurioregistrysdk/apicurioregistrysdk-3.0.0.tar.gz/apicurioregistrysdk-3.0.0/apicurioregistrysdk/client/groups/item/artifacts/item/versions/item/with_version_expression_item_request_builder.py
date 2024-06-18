from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .......models.editable_version_meta_data import EditableVersionMetaData
    from .......models.error import Error
    from .......models.version_meta_data import VersionMetaData
    from .comments.comments_request_builder import CommentsRequestBuilder
    from .content.content_request_builder import ContentRequestBuilder
    from .references.references_request_builder import ReferencesRequestBuilder

class WithVersionExpressionItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single version of a single artifact in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithVersionExpressionItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/versions/{versionExpression}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithVersionExpressionItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Error,
            "404": Error,
            "405": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithVersionExpressionItemRequestBuilderGetRequestConfiguration] = None) -> Optional[VersionMetaData]:
        """
        Retrieves the metadata for a single version of the artifact.  The version metadata is a subset of the artifact metadata and only includes the metadata that is specific tothe version (for example, this doesn't include `modifiedOn`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VersionMetaData]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Error,
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .......models.version_meta_data import VersionMetaData

        return await self.request_adapter.send_async(request_info, VersionMetaData, error_mapping)
    
    async def put(self,body: Optional[EditableVersionMetaData] = None, request_configuration: Optional[WithVersionExpressionItemRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Updates the user-editable portion of the artifact version's metadata.  Only some of the metadata fields are editable by the user.  For example, `description` is editable, but `createdOn` is not.This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "400": Error,
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithVersionExpressionItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a single version of the artifact. Parameters `groupId`, `artifactId` and the unique `version`are needed. If this is the only version of the artifact, this operation is the same as deleting the entire artifact.This feature is disabled by default and it's discouraged for normal usage. To enable it, set the `registry.rest.artifact.deletion.enabled` property to true. This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`) * Feature is disabled (HTTP error `405`) * A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.DELETE
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_get_request_information(self,request_configuration: Optional[WithVersionExpressionItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Retrieves the metadata for a single version of the artifact.  The version metadata is a subset of the artifact metadata and only includes the metadata that is specific tothe version (for example, this doesn't include `modifiedOn`).This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_put_request_information(self,body: Optional[EditableVersionMetaData] = None, request_configuration: Optional[WithVersionExpressionItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the user-editable portion of the artifact version's metadata.  Only some of the metadata fields are editable by the user.  For example, `description` is editable, but `createdOn` is not.This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* No version with this `version` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.PUT
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> WithVersionExpressionItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithVersionExpressionItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return WithVersionExpressionItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def comments(self) -> CommentsRequestBuilder:
        """
        Manage a collection of comments for an artifact version
        """
        from .comments.comments_request_builder import CommentsRequestBuilder

        return CommentsRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def content(self) -> ContentRequestBuilder:
        """
        Manage a single version of a single artifact in the registry.
        """
        from .content.content_request_builder import ContentRequestBuilder

        return ContentRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def references(self) -> ReferencesRequestBuilder:
        """
        Manage the references for a single version of an artifact in the registry.
        """
        from .references.references_request_builder import ReferencesRequestBuilder

        return ReferencesRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithVersionExpressionItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithVersionExpressionItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithVersionExpressionItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

