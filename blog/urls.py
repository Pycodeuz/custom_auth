from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import NewsCreateApiView, PortfolioRetrieveUpdateDestroyAPIView, PortfolioCreateApiView, \
    PortfolioListApiView, CommentCreateApiView, CommentListApiView, NewsListApiView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('portfolio/create', PortfolioCreateApiView.as_view()),
    path('portfolio/<int:pk>', PortfolioRetrieveUpdateDestroyAPIView.as_view()),
    path('portfolio/list', PortfolioListApiView.as_view()),
    path('comment/create', CommentCreateApiView.as_view()),
    path('comment/list', CommentListApiView.as_view()),
    path('news/create', NewsCreateApiView.as_view()),
    path('news/list', NewsListApiView.as_view())
]
