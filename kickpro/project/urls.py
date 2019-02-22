from . views import *

from django.urls import path,include


urlpatterns = [
    path('new/',newProject,name='new_project'),
    path('view/<int:project_id>/', singleProject, name='view_project'),
    # path('comments/<int:project_id>/', comments, name='view_comments'),
    path('reportcomment/<int:id>/', report_comment, name='reportcomment'),
    path('reportproject/<int:id>/', report_project, name='reportproject'),
]
