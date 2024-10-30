from rest_framework.pagination import LimitOffsetPagination

class EmployeeLimitOffsetPagination(LimitOffsetPagination):
    page_size_query_param = 'limit'
    page_query_param = 'page'
    