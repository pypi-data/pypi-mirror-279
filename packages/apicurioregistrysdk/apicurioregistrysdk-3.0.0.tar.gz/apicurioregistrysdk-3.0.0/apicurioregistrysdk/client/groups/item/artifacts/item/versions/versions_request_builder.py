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
    from ......models.create_version import CreateVersion
    from ......models.error import Error
    from ......models.sort_order import SortOrder
    from ......models.version_meta_data import VersionMetaData
    from ......models.version_search_results import VersionSearchResults
    from ......models.version_sort_by import VersionSortBy
    from .item.with_version_expression_item_request_builder import WithVersionExpressionItemRequestBuilder

class VersionsRequestBuilder(BaseRequestBuilder):
    """
    Manage all the versions of an artifact in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new VersionsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/groups/{groupId}/artifacts/{artifactId}/versions{?offset*,limit*,order*,orderby*,dryRun*}", path_parameters)
    
    def by_version_expression(self,version_expression: str) -> WithVersionExpressionItemRequestBuilder:
        """
        Manage a single version of a single artifact in the registry.
        param version_expression: An expression resolvable to a specific version ID within the given group and artifact. The following rules apply: - If the expression is in the form "branch={branchId}", and artifact branch {branchId} exists: The expression is resolved to a version that the branch points to. - Otherwise: The expression is resolved to a version with the same ID, which must follow the "[a-zA-Z0-9._//-+]{1,256}" pattern.
        Returns: WithVersionExpressionItemRequestBuilder
        """
        if not version_expression:
            raise TypeError("version_expression cannot be null.")
        from .item.with_version_expression_item_request_builder import WithVersionExpressionItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["versionExpression"] = version_expression
        return WithVersionExpressionItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[VersionsRequestBuilderGetRequestConfiguration] = None) -> Optional[VersionSearchResults]:
        """
        Returns a list of all versions of the artifact.  The result set is paged.This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VersionSearchResults]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.version_search_results import VersionSearchResults

        return await self.request_adapter.send_async(request_info, VersionSearchResults, error_mapping)
    
    async def post(self,body: Optional[CreateVersion] = None, request_configuration: Optional[VersionsRequestBuilderPostRequestConfiguration] = None) -> Optional[VersionMetaData]:
        """
        Creates a new version of the artifact by uploading new content.  The configured rules forthe artifact are applied, and if they all pass, the new content is added as the most recent version of the artifact.  If any of the rules fail, an error is returned.The body of the request can be the raw content of the new artifact version, or the raw content and a set of references pointing to other artifacts, and the typeof that content should match the artifact's type (for example if the artifact type is `AVRO`then the content of the request should be an Apache Avro document).This operation can fail for the following reasons:* Provided content (request body) was empty (HTTP error `400`)* No artifact with this `artifactId` exists (HTTP error `404`)* The new content violates one of the rules configured for the artifact (HTTP error `409`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[VersionMetaData]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ......models.error import Error

        error_mapping: Dict[str, ParsableFactory] = {
            "404": Error,
            "409": Error,
            "500": Error,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ......models.version_meta_data import VersionMetaData

        return await self.request_adapter.send_async(request_info, VersionMetaData, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[VersionsRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a list of all versions of the artifact.  The result set is paged.This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
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
    
    def to_post_request_information(self,body: Optional[CreateVersion] = None, request_configuration: Optional[VersionsRequestBuilderPostRequestConfiguration] = None) -> RequestInformation:
        """
        Creates a new version of the artifact by uploading new content.  The configured rules forthe artifact are applied, and if they all pass, the new content is added as the most recent version of the artifact.  If any of the rules fail, an error is returned.The body of the request can be the raw content of the new artifact version, or the raw content and a set of references pointing to other artifacts, and the typeof that content should match the artifact's type (for example if the artifact type is `AVRO`then the content of the request should be an Apache Avro document).This operation can fail for the following reasons:* Provided content (request body) was empty (HTTP error `400`)* No artifact with this `artifactId` exists (HTTP error `404`)* The new content violates one of the rules configured for the artifact (HTTP error `409`)* A server error occurred (HTTP error `500`)
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation()
        if request_configuration:
            request_info.headers.add_all(request_configuration.headers)
            request_info.set_query_string_parameters_from_raw_object(request_configuration.query_parameters)
            request_info.add_request_options(request_configuration.options)
        request_info.url_template = self.url_template
        request_info.path_parameters = self.path_parameters
        request_info.http_method = Method.POST
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
        Returns a list of all versions of the artifact.  The result set is paged.This operation can fail for the following reasons:* No artifact with this `artifactId` exists (HTTP error `404`)* A server error occurred (HTTP error `500`)
        """
        # The number of versions to return.  Defaults to 20.
        limit: Optional[int] = None

        # The number of versions to skip before starting to collect the result set.  Defaults to 0.
        offset: Optional[int] = None

        # Sort order, ascending (`asc`) or descending (`desc`).
        order: Optional[SortOrder] = None

        # The field to sort by.  Can be one of:* `name`* `version`* `createdOn`
        orderby: Optional[VersionSortBy] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class VersionsRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[VersionsRequestBuilder.VersionsRequestBuilderGetQueryParameters] = None

    
    @dataclass
    class VersionsRequestBuilderPostQueryParameters():
        """
        Creates a new version of the artifact by uploading new content.  The configured rules forthe artifact are applied, and if they all pass, the new content is added as the most recent version of the artifact.  If any of the rules fail, an error is returned.The body of the request can be the raw content of the new artifact version, or the raw content and a set of references pointing to other artifacts, and the typeof that content should match the artifact's type (for example if the artifact type is `AVRO`then the content of the request should be an Apache Avro document).This operation can fail for the following reasons:* Provided content (request body) was empty (HTTP error `400`)* No artifact with this `artifactId` exists (HTTP error `404`)* The new content violates one of the rules configured for the artifact (HTTP error `409`)* A server error occurred (HTTP error `500`)
        """
        def get_query_parameter(self,original_name: Optional[str] = None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "dry_run":
                return "dryRun"
            return original_name
        
        # When set to `true`, the operation will not result in any changes. Instead, itwill return a result based on whether the operation **would have succeeded**.
        dry_run: Optional[bool] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class VersionsRequestBuilderPostRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[VersionsRequestBuilder.VersionsRequestBuilderPostQueryParameters] = None

    

