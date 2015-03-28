from django.db import models


# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=128)
    quest_id = models.IntegerField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    gcm_id = models.CharField(max_length=200)
    fb_id = models.CharField(max_length=100)

    def __str__(self):
        return '("%s","%s")' % (self.full_name, self.phone)


class Question(models.Model):
    statement = models.CharField(max_length=200)
    options = models.ManyToManyField(Option)
    is_active = models.BooleanField(default=True)
    date_time_asked = models.DateTimeField()
    date_time_answered = models.DateTimeField(null=True)
    asked_by = models.ForeignKey(User, related_name='asked')
    answers_by = models.ManyToManyField(User, related_name='answered', through='Vote')

    def __str__(self):
        return self.statement


class Vote(models.Model):
    user_id = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    voted = models.BooleanField(default=False)
    option = models.ForeignKey(Option, null=True)
