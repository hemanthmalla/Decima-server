import uuid
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
    phone = models.CharField(max_length=13)
    gcm_id = models.CharField(max_length=200)
    fb_id = models.CharField(max_length=100)

    def __str__(self):
        return '("%s","%s")' % (self.full_name, self.phone)


class Question(models.Model):
    statement = models.CharField(max_length=200)
    options = models.ManyToManyField(Option)
    is_active = models.BooleanField(default=True)
    date_time_asked = models.DateTimeField(auto_now_add=True)
    date_time_answered = models.DateTimeField(null=True)
    asked_by = models.ForeignKey(User, related_name='asked')
    answers_by = models.ManyToManyField(User, related_name='answered', through='Vote')

    def __str__(self):
        return self.statement

    def get_absolute_url(self):
        return "/decimo/%d/"%self.id

    def get_add_option_url(self):
        return "/decimo/question/%d/"%self.id

    def get_add_invite_url(self):
        return "/decimo/invite/%d/"%self.id



class Vote(models.Model):
    user_id = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    voted = models.BooleanField(default=False)
    option = models.ForeignKey(Option, null=True)


class DecimaQuestions(models.Model):
    key = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.key)

    def get_absolute_url(self):
        return "/decima/%s/"%self.key


    def send_mail(self):
        from post_office import mail
        mail.send(
                recipients=[self.user.email],
                template='decima_question', # Could be an EmailTemplate instance or name
                context={'decima':self},
                priority='now',
            )
        # print "Send mail implementation"
        return

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4()
            self.send_mail()
        return super(DecimaQuestions, self).save(*args, **kwargs)
