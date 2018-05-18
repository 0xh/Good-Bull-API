from goodbullapi.models import Section
from goodbullapi.serializers import SectionSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404


class SectionRetrieve(generics.RetrieveAPIView):
    """
    Given a term code and CRN, retrieves a specific section, its GPA distribution (if applicable), and 
    detailed information about the building it's in.
    """
    serializer_class = SectionSerializer
    queryset = Section.objects.all()

    def get_object(self):
        queryset = self.get_queryset()

        filter = {
            'term_code': self.kwargs['term_code'],
            'crn': self.kwargs['crn']
        }
        return get_object_or_404(queryset, **filter)
