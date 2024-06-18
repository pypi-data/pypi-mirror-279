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
    from ........models.add_version_to_branch import AddVersionToBranch
    from ........models.error import Error
    from ........models.replace_branch_versions import ReplaceBranchVersions
    from ........models.version_search_results import VersionSearchResults

class VersionsRequestBuilder(BaseRequestBuilder):
    """
    Manage the versions in a branch.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new VersionsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/branches/{branchId}/versions{?offset*,limit*}", path_parameters)
    
    async def get(self,request_configuration: Optional[VersionsRequestBuilderGetRequestConfiguration] = None) -> Optional[VersionSearchResults]:
        """
        Get a list of all versions in the branch.  Returns a list of version identifiers in the branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VersionSearchResults]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ........models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ........models.version_search_results import VersionSearchResults

        return await self.request_adapter.send_async(request_info, VersionSearchResults, error_mapping)
    
    async def post(self,body: Optional[AddVersionToBranch] = None, request_configuration: Optional[VersionsRequestBuilderPostRequestConfiguration] = None) -> None:
        """
        Add a new version to an artifact branch. Returns a list of version identifiers in the branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* Branch already contains the given version. Artifact branches are append-only, cycles and history rewrites, except by replacing the entire branch using the replaceBranchVersions operation,  are not supported. (HTTP error `409`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ........models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "409": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    async def put(self,body: Optional[ReplaceBranchVersions] = None, request_configuration: Optional[VersionsRequestBuilderPutRequestConfiguration] = None) -> None:
        """
        Add a new version to an artifact branch. Branch is created if it does not exist. Returns a list of version identifiers in the artifact branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_put_request_information(
            body, request_configuration
        )
        from ........models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[VersionsRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Get a list of all versions in the branch.  Returns a list of version identifiers in the branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_post_request_information(self,body: Optional[AddVersionToBranch] = None, request_configuration: Optional[VersionsRequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Add a new version to an artifact branch. Returns a list of version identifiers in the branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* Branch already contains the given version. Artifact branches are append-only, cycles and history rewrites, except by replacing the entire branch using the replaceBranchVersions operation,  are not supported. (HTTP error `409`)* A server error occurred (HTTP error `500`)
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
        request_info.http_method = Method.POST
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def to_put_request_information(self,body: Optional[ReplaceBranchVersions] = None, request_configuration: Optional[VersionsRequestBuilderPutRequestConfiguration] = None) -> RequestInformation:
        """
        Add a new version to an artifact branch. Branch is created if it does not exist. Returns a list of version identifiers in the artifact branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def with_url(self,raw_url: Optional[str] = None) -> VersionsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: VersionsRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return VersionsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class VersionsRequestBuilderGetQueryParameters():
        """
        Get a list of all versions in the branch.  Returns a list of version identifiers in the branch, ordered from the latest (tip of the branch) to the oldest.This operation can fail for the following reasons:* No artifact with this `groupId` and `artifactId` exists (HTTP error `404`)* No branch with this `branchId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        """
        # The number of versions to return.  Defaults to 20.
        limit: Optional[int] = None

        # The number of versions to skip before starting to collect the result set.  Defaults to 0.
        offset: Optional[int] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class VersionsRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[VersionsRequestBuilder.VersionsRequestBuilderGetQueryParameters] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class VersionsRequestBuilderPostRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class VersionsRequestBuilderPutRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
    

