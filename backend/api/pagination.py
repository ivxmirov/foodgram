from rest_framework.pagination import PageNumberPagination

from foodgram import constants


class CustomLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = constants.PAGE_SIZE
