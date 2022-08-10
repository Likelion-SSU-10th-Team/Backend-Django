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


class Composition(models.Model):
    album = models.ForeignKey('album.Album', on_delete=models.CASCADE, db_column='album',
                              null=True, blank=True)
    diary = models.ForeignKey('diary.Diary', on_delete=models.CASCADE, db_column='diary',
                              null=True, blank=True)

    def __str__(self):
        name = str(self.album)+" 에 속해있는 "+str(self.diary)
        return name

    class Meta:
        db_table = 'composition'
