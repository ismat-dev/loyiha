from rest_framework import serializers
from .models import Submission, Answer
from django.utils import timezone
from datetime import timedelta

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'student', 'test', 'status', 'score', 'started_at', 'finished_at']
        read_only_fields = ['student', 'status', 'score', 'started_at', 'finished_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)
    
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'submission', 'question', 'selected_option']
        read_only_fields = ['answer_at']

        def validate(self, attrs):
            submission = attrs['submission']

            if submission.student != self.context['request'].user:
                raise serializers.ValidationError("Siz bu submission uchun javob bera olmaysiz.")

            if submission.status != 'in_progress':
                raise serializers.ValidationError("Submission allaqachon topshirilgan.")

            end_time = submission.started_at + submission.test.duration_minutes
            if timezone.now() > end_time:
                raise serializers.ValidationError("Test vaqti tugagan.")
            
            return attrs
    
# submit
class SubmissionSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = []  

    def update(self, instance, validated_data):
        if instance.status == 'submitted':
            raise serializers.ValidationError("Bu tests allaqachon topshirilgan.")
        
        deadline = instance.started_at + instance.test.duration_minutes
        if timezone.now() > deadline:
            raise serializers.ValidationError("Tests vaqti tugagan.")
        
        correct = 0
        answers = instance.answers.all()
        for ans in answers:
            if ans.selected_option == ans.question.correct_option:
                correct += 1

        instance.score = correct
        instance.status = 'submitted'
        instance.finished_at = timezone.now()
        instance.save()


        return instance


class SubmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'test', 'score', 'status', 'started_at', 'finished_at']
