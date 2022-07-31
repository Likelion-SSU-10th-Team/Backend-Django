from django.db import models

# Create your models here.
class Diary(models.Model):
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='writer')
    date_of_written_diary = models.DateTimeField()
    content = models.TextField()

    class Meta:
        db_table = 'diary'

