#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
"""
对所有请求进行预处理，加入头信息以实现跨站资源共享
"""
class MyMiddle(MiddlewareMixin):

    def __init__(self,  get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "content-type, x-requested-with, X-CSRFToken, X-XSRF-TOKEN, HTTP_X_XSRF_TOKEN, *"

        if request.method == 'OPTIONS':
            return response
        print(request.body)
        return None

    def process_response(self, request, response):
        http_origin = request.META.get("HTTP_ORIGIN")
        response["Access-Control-Allow-Origin"] = http_origin if http_origin else "http://www.cloudjyk.me:9090"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "content-type, x-requested-with, X-CSRFToken, X-XSRF-TOKEN, HTTP_X_XSRF_TOKEN, *"
        return response
