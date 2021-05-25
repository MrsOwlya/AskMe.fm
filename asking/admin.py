from django.contrib import admin

from .models import Account, Ask, Answer, Like

# Register your models here.

admin.site.register(Ask)
admin.site.register(Answer)
admin.site.register(Account)
admin.site.register(Like)