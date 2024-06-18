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
    from ...models.error import Error
    from ...models.role_mapping import RoleMapping
    from ...models.role_mapping_search_results import RoleMappingSearchResults
    from .item.with_principal_item_request_builder import WithPrincipalItemRequestBuilder

class RoleMappingsRequestBuilder(BaseRequestBuilder):
    """
    Collection to manage role mappings for authenticated principals
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new RoleMappingsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/admin/roleMappings{?limit*,offset*}", path_parameters)
    
    def by_principal_id(self,principal_id: str) -> WithPrincipalItemRequestBuilder:
        """
        Manage the configuration of a single role mapping.
        param principal_id: Unique id of a principal (typically either a user or service account).
        Returns: WithPrincipalItemRequestBuilder
        """
        if not principal_id:
            raise TypeError("principal_id cannot be null.")
        from .item.with_principal_item_request_builder import WithPrincipalItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["principalId"] = principal_id
        return WithPrincipalItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RoleMappingsRequestBuilderGetRequestConfiguration] = None) -> Optional[RoleMappingSearchResults]:
        """
        Gets a list of all role mappings configured in the registry (if any).This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[RoleMappingSearchResults]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.role_mapping_search_results import RoleMappingSearchResults

        return await self.request_adapter.send_async(request_info, RoleMappingSearchResults, error_mapping)
    
    async def post(self,body: Optional[RoleMapping] = None, request_configuration: Optional[RoleMappingsRequestBuilderPostRequestConfiguration] = None) -> None:
        """
        Creates a new mapping between a user/principal and a role.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param body: The mapping between a user/principal and their role.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ...models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RoleMappingsRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Gets a list of all role mappings configured in the registry (if any).This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.GET
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: Optional[RoleMapping] = None, request_configuration: Optional[RoleMappingsRequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Creates a new mapping between a user/principal and a role.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param body: The mapping between a user/principal and their role.
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
        request_info.http_method = Method.POST
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> RoleMappingsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: RoleMappingsRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return RoleMappingsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class RoleMappingsRequestBuilderGetQueryParameters():
        """
        Gets a list of all role mappings configured in the registry (if any).This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        """
        # The number of role mappings to return.  Defaults to 20.
        limit: Optional[int] = None

        # The number of role mappings to skip before starting the result set.  Defaults to 0.
        offset: Optional[int] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class RoleMappingsRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[RoleMappingsRequestBuilder.RoleMappingsRequestBuilderGetQueryParameters] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class RoleMappingsRequestBuilderPostRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

