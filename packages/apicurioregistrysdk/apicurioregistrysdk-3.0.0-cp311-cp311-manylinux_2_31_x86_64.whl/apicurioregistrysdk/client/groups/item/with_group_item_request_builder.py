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
    from ...models.editable_group_meta_data import EditableGroupMetaData
    from ...models.error import Error
    from ...models.group_meta_data import GroupMetaData
    from .artifacts.artifacts_request_builder import ArtifactsRequestBuilder

class WithGroupItemRequestBuilder(BaseRequestBuilder):
    """
    Collection to manage a single group in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithGroupItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithGroupItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a group by identifier.  This operation also deletes all artifacts withinthe group, so should be used very carefully.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)* The group does not exist (HTTP error `404`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithGroupItemRequestBuilderGetRequestConfiguration] = None) -> Optional[GroupMetaData]:
        """
        Returns a group using the specified id.This operation can fail for the following reasons:* No group exists with the specified ID (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[GroupMetaData]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.group_meta_data import GroupMetaData

        return await self.request_adapter.send_async(request_info, GroupMetaData, error_mapping)
    
    async def put(self,body: Optional[EditableGroupMetaData] = None, request_configuration: Optional[WithGroupItemRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Updates the metadata of a group using the specified id.This operation can fail for the following reasons:* No group exists with the specified ID (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithGroupItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a group by identifier.  This operation also deletes all artifacts withinthe group, so should be used very carefully.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)* The group does not exist (HTTP error `404`)
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
    
    def to_get_request_information(self,request_configuration: Optional[WithGroupItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a group using the specified id.This operation can fail for the following reasons:* No group exists with the specified ID (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_put_request_information(self,body: Optional[EditableGroupMetaData] = None, request_configuration: Optional[WithGroupItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the metadata of a group using the specified id.This operation can fail for the following reasons:* No group exists with the specified ID (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def with_url(self,raw_url: Optional[str] = None) -> WithGroupItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithGroupItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return WithGroupItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def artifacts(self) -> ArtifactsRequestBuilder:
        """
        Manage the collection of artifacts within a single group in the registry.
        """
        from .artifacts.artifacts_request_builder import ArtifactsRequestBuilder

        return ArtifactsRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithGroupItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithGroupItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithGroupItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

