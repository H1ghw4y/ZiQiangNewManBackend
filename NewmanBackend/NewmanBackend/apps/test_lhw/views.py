from django.shortcuts import render

# Create your views here.
# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    """
    发送短信验证码
    传入参数：

    """
    def get(self, request):
        return Response({"message": "OK"})
    pass