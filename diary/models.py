from django.db import models

# Create your models here.


class Diary(models.Model):
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='writer')
    belong_to_film = models.ForeignKey('film.Film', on_delete=models.CASCADE, db_column='belong_to_film',
                                       null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        name = str(self.writer.__str__()) + "의 일기 : " + str(self.pk)
        return name

    class Meta:
        db_table = 'Diary'


class Comment(models.Model):
    belong_to_diary = models.ForeignKey(Diary, on_delete=models.CASCADE, db_column='belong_to_diary')
    comment = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        name = self.belong_to_diary.__str__() + " 댓글 [" + self.comment + "]"
        return name

    class Meta:
        db_table = 'comment'
