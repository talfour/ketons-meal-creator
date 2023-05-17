from django.contrib import admin
from .models import Question, VoteSystem, Category, Answer

# Register your models here.

admin.site.register(Question)
admin.site.register(VoteSystem)
admin.site.register(Category)
admin.site.register(Answer)