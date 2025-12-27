from django.db import models
from apps.users.models import UserProfile
from apps.MCQ.models import Test, Question

class Submission(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  
    status = models.CharField(
        max_length=150,
        choices=[('in_progress', 'in_progress'), ('submitted', 'submitted')],
        default='in_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.score
    
class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    answer_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.selected_option
    