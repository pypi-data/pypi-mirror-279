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
    from ...models.group_search_results import GroupSearchResults
    from ...models.group_sort_by import GroupSortBy
    from ...models.sort_order import SortOrder

class GroupsRequestBuilder(BaseRequestBuilder):
    """
    Search for groups in the registry.
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Optional[Union[Dict[str, Any], str]] = None) -> None:
        """
        Instantiates a new GroupsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the Url template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/search/groups{?offset*,limit*,order*,orderby*,labels*,description*,groupId*}", path_parameters)
    
    async def get(self,request_configuration: Optional[GroupsRequestBuilderGetRequestConfiguration] = None) -> Optional[GroupSearchResults]:
        """
        Returns a paginated list of all groups that match the provided filter criteria.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[GroupSearchResults]
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
        from ...models.group_search_results import GroupSearchResults

        return await self.request_adapter.send_async(request_info, GroupSearchResults, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[GroupsRequestBuilderGetRequestConfiguration] = None) -> RequestInformation:
        """
        Returns a paginated list of all groups that match the provided filter criteria.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
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
    
    def with_url(self,raw_url: Optional[str] = None) -> GroupsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: GroupsRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return GroupsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class GroupsRequestBuilderGetQueryParameters():
        """
        Returns a paginated list of all groups that match the provided filter criteria.This operation can fail for the following reasons:* A server error occurred (HTTP error `500`)
        """
        def get_query_parameter(self,original_name: Optional[str] = None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "group_id":
                return "groupId"
            if original_name == "description":
                return "description"
            if original_name == "labels":
                return "labels"
            if original_name == "limit":
                return "limit"
            if original_name == "offset":
                return "offset"
            if original_name == "order":
                return "order"
            if original_name == "orderby":
                return "orderby"
            return original_name
        
        # Filter by description.
        description: Optional[str] = None

        # Filter by group name.
        group_id: Optional[str] = None

        # Filter by one or more name/value label.  Separate each name/value pair using a colon.  Forexample `labels=foo:bar` will return only artifacts with a label named `foo`and value `bar`.
        labels: Optional[List[str]] = None

        # The number of artifacts to return.  Defaults to 20.
        limit: Optional[int] = None

        # The number of artifacts to skip before starting to collect the result set.  Defaults to 0.
        offset: Optional[int] = None

        # Sort order, ascending (`asc`) or descending (`desc`).
        order: Optional[SortOrder] = None

        # The field to sort by.  Can be one of:* `name`* `createdOn`
        orderby: Optional[GroupSortBy] = None

    
    from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

    @dataclass
    class GroupsRequestBuilderGetRequestConfiguration(BaseRequestConfiguration):
        from kiota_abstractions.base_request_configuration import BaseRequestConfiguration

        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        # Request query parameters
        query_parameters: Optional[GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters] = None

    

