from django.db import models
from account.models import Account
from django.db.models.signals import post_save


class Invitation(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, )


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    participants = models.ManyToManyField(Account)
    invitation = models.ManyToManyField(Invitation,  blank=True)


class Lider(models.Model):
    id = models.AutoField(primary_key=True)
    lider = models.OneToOneField(Account, on_delete=models.CASCADE)
    team = models.OneToOneField(Team, on_delete=models.CASCADE, )


class Groups(models.Model):
    name = models.CharField(max_length=120)
    participants = models.ManyToManyField(Account)


class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    team = models.ManyToManyField(Team)
    participants = models.ManyToManyField(Account, blank=True)
    groups = models.ManyToManyField(Groups, blank=True)


class Thread(models.Model):
    name = models.CharField(max_length=120)
    channel = models.ManyToManyField(Channel)
    last_message = models.DateTimeField(null=True, blank=True, db_index=True)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


class ThreadIm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    participants = models.ManyToManyField(Account, blank=True)

    last_message = models.DateTimeField(null=True, blank=True, db_index=True)

    YEAR_IN_SCHOOL_CHOICES = (
        ('LS', 'Личное сообщение'),
        ('GR', 'Групповое сообщение'),
    )

    vid = models.CharField(max_length=2,
                           choices=YEAR_IN_SCHOOL_CHOICES,
                           default='LS')


class MessageIm(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    thread = models.ForeignKey(ThreadIm, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


def update_last_message_datetime(sender, instance, created, **kwargs):
    """
    Update Thread's last_message field when
    a new message is sent.
    """
    if not created:
        return

    Thread.objects.filter(id=instance.thread.id).update(
        last_message=instance.datetime
    )


def update_last_message_datetime2(sender, instance, created, **kwargs):
    """
    Update Thread's last_message field when
    a new message is sent.
    """
    if not created:
        return

    ThreadIm.objects.filter(id=instance.thread.id).update(
        last_message=instance.datetime
    )


post_save.connect(update_last_message_datetime2, sender=MessageIm)
post_save.connect(update_last_message_datetime, sender=Message)

# Create your models here.
