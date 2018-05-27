from rest_framework import viewsets, generics
from goodbullapi.serializers import CourseSerializer
from goodbullapi.models import Course


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DepartmentList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        dept = self.kwargs['dept']
        return Course.objects.filter(dept=dept)

class CourseRetrieve(generics.RetrieveAPIView):
    serializer_class = CourseSerializer

    def get_object(self):
        dept = self.kwargs['dept']
        course_num = self.kwargs['course_num']
        print(type(course_num))
        return Course.objects.get(dept=dept, course_num=course_num)