from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Poll, Question, Answer
from core.permissions import IsAdmin, IsSurveyParticipant
from core.serializers import PollSerializer, QuestionSerializer, AnswerSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class PollViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | permissions.IsAdminUser, IsSurveyParticipant)
    serializer_class = PollSerializer

    def qs_as_survey(self, qs):
        return qs.filter(start_datetime__lte=datetime.now(),
                         end_datetime__gte=datetime.now())

    def get_queryset(self):
        qs = Poll.objects.all()
        if self.request.user.is_survey():
            return self.qs_as_survey(qs)
        return qs


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | permissions.IsAdminUser, )
    serializer_class = QuestionSerializer
    queryset = Question.objects.get_queryset()


class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSurveyParticipant, )
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)
