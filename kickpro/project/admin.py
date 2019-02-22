from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Category)
admin.site.register(Project)
#admin.site.register(Tag)
admin.site.register(Project_Images)
admin.site.register(Comments)
admin.site.register(projectReport)
admin.site.register(commentReport)

