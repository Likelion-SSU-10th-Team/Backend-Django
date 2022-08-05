from django.db import models


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE,
                              db_column='Album_owner', null=True, blank=True)

    def __str__(self):
        name = str(self.owner.__str__()) + "의 앨범 : " + self.name
        return name

    class Meta:
        db_table = 'album'
