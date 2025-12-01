#Python modules
from typing import Any, Optional

#Django Modules
from  django.utils import timezone
from django.db.models import QuerySet, Count

#Django RestFramework
from rest_framework import viewsets,status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request



#Project modules
from .models import Courses, Lesson
from .serializers import CoursesSerializer, LessonSerializer
from .permission import isOwner

class CourseViewSet(ViewSet):
    """Course view"""
    permission_classes = [IsAuthenticated]

    def get_course(self, pk: int) -> Courses | None:
        return Courses.objects.filter(id=pk, deleted_at__isnull = True).first()


    def list(self, request):
        """
        List all non-deleted with courses optional filtering by 'is_active'.

        Parameters:
            is_active (bool): Filter inly active/inactive courses.

        Returns:
            Response: Serialized list of courses /       
        """
        queryset: QuerySet = Courses.objects.filter(deleted_at__isnull = True).annotate(
            lessons_count = Count("lessons")
        )
        is_active = request.query_params.get('is_active', None)
        # courses = Courses.objects.filter(deleted_at__isnull = True)
        if is_active is not None:
            courses = courses.filter(is_active = is_active.lower() == 'true')
        serializer = CoursesSerializer(courses, many = True)
        return Response(serializer.data)
    
    def create(self, request: Request ) -> Response:
        """
        Create a new course.

        Owner is automatically set from request.user.

        Returns:
            Response: Serialized created course.
        """
        serializer = CoursesSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(owner = request.user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    def retrieve(self, request: Request, pk: int | None = None) -> Response:
        """
        Retrieve a specific course by ID.

        Args:
            pk(int): Course ID.

        Returns:
            Response: Course data or 404 if not found.
        """
        
        course =self.get_course(pk)
        if not course:
            return Response({"detail": "Course not found"}, status = 404)
        serializer = CoursesSerializer(course)
        return Response(serializer.data)
    
    def update(self, request: Request, pk: int | None = None) -> Response:
        """
        Fully update a course.

        Only the owner of the course can update it.

        Args:
            pk(int): Course ID.

        Returns:
            Response: Updated course data
        """
        course = self.get_course(pk)
        if not course:
            return Response({"detail": "Course not found"}, status = 404)
        self.check_object_permissions(request, course)
        serializer = CoursesSerializer(course, data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail = True,methods = ("POST",),)
    def activate(self, request: Request, pk:int | None = None)-> Response:
        """
        Activate a course.

        Only owner can activate.

        Returns:
            Response:Updated course object.
        """
        course = self.get_course(pk)
        if not course:
            return Response({"detail": "Course not found"}, status = 404)
        
        if course.is_active: 
            return Response({"detail": "Already active"}, status = 400)
        course.is_active = True
        course.save()

        return Response(CoursesSerializer(course).data)

    def deactivate(self, request: Request, pk:int | None = None)-> Response:
        """
        Deactivate a course.

        Only owner can deactivate.

        Returns:
            Response:Updated course object.
        """
        course = self.get_course(pk)
        if not course:
            return Response({"detail": "Course not found"}, status = 404)
        
        if course.is_active: 
            return Response({"detail": "Already inactive"}, status = 400)
        course.is_active = False
        course.save()

        return Response(CoursesSerializer(course).data)
    
    @action(detail = True, method = ("GET",),)
    def lessons(self,request: Request, pk:int | None = None) -> Response:
        """
        List all lessons of a course(not deleted).

        Returns:
            Response: Serialized list of lessons.

        """
        course = self.get_course(pk)
        if not course:
            return Response({"detail": "Course not found"}, status = 404)
        lessons = course.lessons.filter(deleted_at__isnull = True)
        serializer = LessonSerializer(lessons, many = True)

        return Response(serializer.data)
    

class LessonViewSet(ViewSet):
    """
    View Set for managing lessons
    """
    queryset =Lesson.objects.select_related("course").all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer: LessonSerializer) -> None:
        """
        Override creation logic.
        Currently it just saves the lesson,
        but this is a place for additional rules.
        """
        serializer.save()

    def get_queryset(self) -> Any:
        """Optimized queryset with optional filtering by course"""
        qs = super().get_queryset()
        course_id = self.query_params.get("course_id")
        if course_id:
            qs = qs.filter(course_id = course_id)
        return qs
        
    
