#Django modules
from django.urls import path
#Rest framework 
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import CourseViewSet,LessonViewSet

course_list = CourseViewSet.as_view({'get': 'list', 'post': 'create'})
course_detail = CourseViewSet.as_view({'get': 'retrieve', 'put': 'update'})
course_activate = CourseViewSet.as_view({'post': 'activate'})
course_deactivate = CourseViewSet.as_view({'post': 'deactivate'})
course_lessons = CourseViewSet.as_view({'get': 'lessons'})

lesson_create = LessonViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('v1/education/courses/', course_list),
    path('v1/education/courses/<int:pk>/', course_detail),
    path('v1/education/courses/<int:pk>/activate/', course_activate),
    path('v1/education/courses/<int:pk>/deactivate/', course_deactivate),
    path('v1/education/courses/<int:pk>/lessons/', course_lessons),
    path('v1/education/lessons/',lesson_create),
]