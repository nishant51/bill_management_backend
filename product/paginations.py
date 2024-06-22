from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


class TenPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        request = self.request
        protocol = "https://" if request.is_secure() else "https://"
        base_url = protocol + request.get_host() + request.path

        return Response(
            {
                "total_pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "next": self.get_next_link(base_url),
                "previous": self.get_previous_link(base_url),
                "results": data,
                "current_page": self.page.number,
            }
        )

    def get_next_link(self, base_url):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param(base_url, self.page_query_param, page_number)

    def get_previous_link(self, base_url):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(base_url, self.page_query_param)
        return replace_query_param(base_url, self.page_query_param, page_number)
    

class FivePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        request = self.request
        protocol = "https://" if request.is_secure() else "https://"
        base_url = protocol + request.get_host() + request.path

        return Response(
            {
                "total_pages": self.page.paginator.num_pages,
                "count": self.page.paginator.count,
                "next": self.get_next_link(base_url),
                "previous": self.get_previous_link(base_url),
                "results": data,
                "current_page": self.page.number,
            }
        )

    def get_next_link(self, base_url):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param(base_url, self.page_query_param, page_number)

    def get_previous_link(self, base_url):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(base_url, self.page_query_param)
        return replace_query_param(base_url, self.page_query_param, page_number)