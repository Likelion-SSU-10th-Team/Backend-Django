from django.db import models


# Create your models here.
class Film(models.Model):

    class ChoiceSize(models.IntegerChoices):
        small = 7
        medium = 15
        big = 31

    size = models.IntegerField(choices=ChoiceSize.choices, default=ChoiceSize.medium)
    count = models.SmallIntegerField(default=0)
    isFull = models.BooleanField(default=False)
    # 날짜 -> ??월 ??일 형식으로 바꿔야함
    startDate = models.DateTimeField(auto_now_add=True) 
    endDate = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, db_column='owner', null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'film'
