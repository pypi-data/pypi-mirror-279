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
    from .......models.branch_meta_data import BranchMetaData
    from .......models.editable_branch_meta_data import EditableBranchMetaData
    from .......models.error import Error
    from .versions.versions_request_builder import VersionsRequestBuilder

class WithBranchItemRequestBuilder(BaseRequestBuilder):
    """
    Manage a single branch.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new WithBranchItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/branches/{branchId}", path_parameters)
    
    async def delete(self,request_configuration: Optional[WithBranchItemRequestBuilderDeleteRequestConfiguration] = None) -> None:
        """
        Deletes a single branch in the artifact.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "409": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def get(self,request_configuration: Optional[WithBranchItemRequestBuilderGetRequestConfiguration] = None) -> Optional[BranchMetaData]:
        """
        Returns the metaData of a branch.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[BranchMetaData]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from .......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .......models.branch_meta_data import BranchMetaData

        return await self.request_adapter.send_async(request_info, BranchMetaData, error_mapping)
    
    async def put(self,body: Optional[EditableBranchMetaData] = None, request_configuration: Optional[WithBranchItemRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Updates the metadata of a branch.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_delete_request_information(self,request_configuration: Optional[WithBranchItemRequestBuilderDeleteRequestConfiguration] = None) -> RequestInformation:
        """
        Deletes a single branch in the artifact.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_get_request_information(self,request_configuration: Optional[WithBranchItemRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns the metaData of a branch.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_put_request_information(self,body: Optional[EditableBranchMetaData] = None, request_configuration: Optional[WithBranchItemRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Updates the metadata of a branch.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def with_url(self,raw_url: Optional[str] = None) -> WithBranchItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithBranchItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return WithBranchItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def versions(self) -> VersionsRequestBuilder:
        """
        Manage the versions in a branch.
        """
        from .versions.versions_request_builder import VersionsRequestBuilder

        return VersionsRequestBuilder(self.request_adapter, self.path_parameters)
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithBranchItemRequestBuilderDeleteRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithBranchItemRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class WithBranchItemRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

