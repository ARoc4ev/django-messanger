from django.contrib import admin
from .models import Thread, Message, Team,Channel, Lider, MessageIm, ThreadIm
# Register your models here.
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(Team)
admin.site.register(Lider)
admin.site.register(Channel)
admin.site.register(MessageIm)
admin.site.register(ThreadIm)



