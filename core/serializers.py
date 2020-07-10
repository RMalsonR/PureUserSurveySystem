from rest_framework import serializers

from core.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow start_datetime to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('start_datetime').read_only = True

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'
        extra_kwargs = {'questions': {'required': False}}


class AnswerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow answer to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('answer').read_only = True

    user = UserSerializer(many=False, read_only=True)
    question = QuestionSerializer(many=False, read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
