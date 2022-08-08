from django.db import models


# Create your models here.
class User(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True, default='email@example.com')
    password = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=20, null=True)
    age = models.IntegerField(default=20)
    current_film = models.ForeignKey("film.Film", on_delete=models.CASCADE,
                                     db_column='current_film', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'


