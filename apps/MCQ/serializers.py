from rest_framework import serializers
from .models import Question, Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title', 'duration_minutes', 'is_active', 'created_at']

    def create(self, validated_data):
        return Test.objects.create(
            **validated_data,
            teacher=self.context['request'].user, 
            is_active=False
        )

class Questionerializers(serializers.ModelSerializer):
    test_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'option', 'correct_option', 'test_id']
    
    def validate_test_id(self, value):
        user = self.context['request'].user
        test = Test.objects.filter(id=value, teacher=user).first()
        if not test:
            raise serializers.ValidationError("Siz faqat o'zingiz yaratgan testga savol qo'sha olasiz")
        return value
    
    def create(self, validated_data):
        test_id = validated_data.pop('test_id')
        test = Test.objects.get(id=test_id)
        return Question.objects.create(test=test, **validated_data)

# test active
class TestActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['is_active']

    def update(self, instance, validated_data):
        if validated_data.get('is_active') and not instance.question_set.exists():
            raise serializers.ValidationError('test ni foal qilish uchun test bulishi kerak')
        return super().update(instance, validated_data)
    
class ActiveTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title', 'duration_minutes', 'created_at']
