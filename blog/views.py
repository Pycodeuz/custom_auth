from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import News, Portfolio, Comment, CommonAuthMixin
from blog.serializers import NewsModelSerializer, PortfolioModelSerializer, CommentModelSerializer


class PortfolioCreateApiView(generics.CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioModelSerializer
    parser_classes = FormParser, MultiPartParser


class CommentCreateApiView(CommonAuthMixin, APIView):

    @swagger_auto_schema(request_body=CommentModelSerializer)
    def post(self, request):
        serializer = CommentModelSerializer(data=request.data)
        user = self.authenticate_user(request)

        if serializer.is_valid():
            Comment.objects.create(name=serializer.validated_data.get('name'), owner=user)
            return Response('Comment created successfully', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# News Api
class NewsCreateApiView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer
    parser_classes = FormParser, MultiPartParser


class NewsListApiView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer
    parser_classes = FormParser, MultiPartParser


# Portfolio Apis


class PortfolioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioModelSerializer


class PortfolioListApiView(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioModelSerializer


# Comment Apis


class CommentListApiView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = PortfolioModelSerializer
