from django.db import models

# Create your models here.



class User(models.Model):
    user_tg_id = models.IntegerField(unique=True, null=False)
    tg_username = models.CharField(max_length=250, null=False)
    tg_full_name = models.CharField(max_length=250, null=True)

    def as_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ev_datetime = models.DateTimeField()
    ev_title = models.CharField(max_length=100)
    ev_tags = models.TextField()
    ev_text = models.TextField()

    def as_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }
    

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.TextField()
    note_text = models.TextField()
    note_tags = models.TextField()

    def as_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_timezone = models.CharField(max_length=20)  # Europe/Berlin etc...
    ai_platform = models.CharField(max_length=50)
    ai_api_key = models.CharField(max_length=50)


class Screenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=100)
    hashtags = models.TextField()
    caption = models.TextField()
    ocr_text = models.TextField()
    created = models.DateTimeField()

    def as_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self._meta.fields
        }

