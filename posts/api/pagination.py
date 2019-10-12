from rest_framework import pagination


class PostPagination(pagination.PageNumberPagination):
    page_size = 10


class LikePagination(pagination.PageNumberPagination):
    page_size = 50
