from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Message(models.Model):
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=500)
    author = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=30, blank=False, default="ToGod")

    def __str__(self):
        return self.text


class UserGroup(models.Model):
    groupname = models.CharField(max_length=100, blank=False, null=True)
    privilege_level = models.IntegerField(default=0)
    def __str__(self):
        return self.groupname


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False, default="none")
    second_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=False, default="none")
    telegram_id = models.CharField(max_length=30, blank=True)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Order(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, default="none")
    worker = models.CharField(max_length=30, blank=True)
    about = models.TextField(max_length=500, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=False, default="sent")
    created_time = models.DateTimeField(blank=False, default=timezone.now)

    def __str__(self):
        return self.name


class UrlsOrders(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    url_isCloud = models.BooleanField(default=False)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.url


class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    sk_prempro = models.BooleanField(blank=False, default=False)
    sk_aftereffects = models.BooleanField(blank=False, default=False)
    sk_illustrator = models.BooleanField(blank=False, default=False)
    sk_photoshop = models.BooleanField(blank=False, default=False)
    sk_audition = models.BooleanField(blank=False, default=False)
    sk_vegaspro = models.BooleanField(blank=False, default=False)

    sk_cut = models.BooleanField(blank=False, default=False)
    sk_subtitles = models.BooleanField(blank=False, default=False)
    sk_transitions = models.BooleanField(blank=False, default=False)
    sk_memes = models.BooleanField(blank=False, default=False)
    sk_infograf = models.BooleanField(blank=False, default=False)
    sk_effects = models.BooleanField(blank=False, default=False)

    def setAll(self, array):
        self.sk_prempro = array[0]
        self.sk_aftereffects = array[1]
        self.sk_illustrator = array[2]
        self.sk_photoshop = array[3]
        self.sk_audition = array[4]
        self.sk_vegaspro = array[5]

        self.sk_cut = array[6]
        self.sk_subtitles = array[7]
        self.sk_transitions = array[8]
        self.sk_memes = array[9]
        self.sk_infograf = array[10]
        self.sk_effects = array[11]

    def getAll(self):
        return [self.sk_prempro, self.sk_aftereffects, self.sk_illustrator, self.sk_photoshop,
                self.sk_audition, self.sk_vegaspro, self.sk_cut, self.sk_subtitles, self.sk_transitions,
                self.sk_memes, self.sk_infograf, self.sk_effects]

class Help(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=70, blank=False)
    description = models.CharField(max_length=700, blank=False)
    callback = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.topic
class Telegram_Code(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    code = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    maybe_tg_id = models.CharField(max_length=40, blank=True)

