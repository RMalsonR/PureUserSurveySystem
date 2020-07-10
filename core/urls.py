from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import *

app_name = 'api_core'

router = DefaultRouter()
router.register('question', QuestionViewSet, 'questions')
router.register('poll', PollViewSet, 'polls')
router.register('answer', AnswerViewSet, 'answers')

urlpatterns = [
    # JWT Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]