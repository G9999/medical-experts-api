from datetime import datetime

import django_filters
from django.db.models import Count, Sum

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from .helpers import medical_expert_affiliations, medical_expert_connections
from .serializers import AffiliationSerializer, \
                         ClinicalTrialConditionTotalSerializer, \
                         ClinicalTrialSerializer, \
                         CompanyCooperationsSerializer, \
                         CooperationInstitutionTotalAmountSerializer, \
                         CountryTotalSerializer, EventSerializer, \
                         EventSubTypeTotalSerializer, \
                         FavoriteMedicalExpertSerializer, \
                         FavoriteMedicalExpertSerializerSuperUser, \
                         InstitutionTotalSerializer, \
                         InterventionTotalSerializer, \
                         InvestigatorSerializer, \
                         InvestigatorSerializerSuperUser, \
                         MedicalExpertAffiliationSerializer, \
                         MedicalExpertConnectionMedicalExpertSerializer, \
                         MedicalExpertConnectionSerializer, \
                         MedicalExpertEventPositionTotalSerializer, \
                         NatureOfPaymentTotalAmountSerializer, \
                         ProfessionTotalSerializer, \
                         PublicationSerializer, \
                         PublicationSubTypeTotalSerializer, \
                         PublicationYearTotalSerializer, RequestSerializer, \
                         SpeakerSerializer, SpeakerSerializerSuperUser, \
                         SpecialtyTotalSerializer, StudyPhaseTotalSerializer
from app.models import ClinicalTrial, Event, MedicalExpert, Publication
from app.models_relations import ClinicalTrialInstitution, \
                                 ClinicalTrialIntervention, \
                                 MedicalExpertClinicalTrial, \
                                 MedicalExpertEvent, \
                                 MedicalExpertInstitution, \
                                 MedicalExpertInstitutionCOI, \
                                 MedicalExpertPublication
from app_helpers.models import ClinicalTrialCondition, EventSubtype, \
                               PublicationSubtype
from client.models import Request


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class AliasedOrderingFilter(OrderingFilter):
    ''' this allows us to "alias" fields on our model to ensure consistency at
        the API level We do so by allowing the ordering_fields attribute to
        accept a list of tuples. You can mix and match, i.e.: ordering_fields
        = (('alias1', 'field1'), 'field2', ('alias2', 'field2')) '''

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if valid_fields is None or valid_fields == '__all__':
            return super(AliasedOrderingFilter, self).remove_invalid_fields(
                queryset, fields, view)

        aliased_fields = {}
        for field in valid_fields:
            if isinstance(field, basestring):
                aliased_fields[field] = field
            else:
                aliased_fields[field[0]] = field[1]

        ordering = []
        for raw_field in fields:
            invert = raw_field[0] == '-'
            field = raw_field.lstrip('-')
            if field in aliased_fields:
                if invert:
                    ordering.append('-{}'.format(aliased_fields[field]))
                else:
                    ordering.append(aliased_fields[field])
        return ordering


class InvestigatorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(name="first_name",
                                           lookup_expr='icontains')
    middle_name = django_filters.CharFilter(name="middle_name",
                                            lookup_expr='icontains')
    last_name = django_filters.CharFilter(name="last_name",
                                          lookup_expr='icontains')
    city = django_filters.CharFilter(name="city", lookup_expr='icontains')
    country = django_filters.CharFilter(name="country__name",
                                        lookup_expr='icontains')
    prop_therapeutic_areas = django_filters.CharFilter(
        name="therapeutic_areas__name", lookup_expr='icontains', distinct=True)
    prop_specialties = django_filters.CharFilter(
        name="specialties__name", lookup_expr='icontains', distinct=True)

    class Meta:
        model = MedicalExpert
        fields = (
            'first_name', 'middle_name', 'last_name', 'city',
            'country', 'number_linked_clinical_trials', 'number_linked_events',
            'number_linked_institutions', 'number_linked_publications',
            'number_linked_institutions_subtype_company',
            'number_linked_institutions_coi')


class InvestigatorsListView(generics.ListAPIView):
    serializer_class = InvestigatorSerializer
    filter_class = InvestigatorFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = (
        'first_name', 'middle_name', 'last_name', 'city',
        ('country', 'country__name'), 'number_linked_clinical_trials',
        'number_linked_events', 'number_linked_institutions',
        'number_linked_publications',
        'number_linked_institutions_subtype_company',
        'number_linked_institutions_coi'
    )

    def get_serializer_class(self):
        """
        Return InvestigatorSerializerSuperUser for superuser
        """
        if self.request.user.is_superuser:
            return InvestigatorSerializerSuperUser
        return super(InvestigatorsListView, self).get_serializer_class()

    def get_queryset(self):
        queryset = MedicalExpert.objects.filter(
            number_linked_clinical_trials__gt=0).order_by('pk')
        return queryset


class InvestigatorsPerCountryListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_clinical_trials__gt=0). \
        exclude(country=None).values('country__name'). \
        annotate(total=Count('country__name')). \
        order_by('total', 'country__name')
    serializer_class = CountryTotalSerializer
    pagination_class = LargeResultsSetPagination


class InvestigatorsPerProfessionListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_clinical_trials__gt=0).exclude(profession=None). \
        values('profession__name').annotate(total=Count('profession__name')). \
        order_by('total', 'profession__name')
    serializer_class = ProfessionTotalSerializer
    pagination_class = LargeResultsSetPagination


class InvestigatorsPerSpecialtyListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_clinical_trials__gt=0). \
        exclude(specialties=None).values('specialties__name'). \
        annotate(total=Count('specialties__name')). \
        order_by('total', 'specialties__name')
    serializer_class = SpecialtyTotalSerializer
    pagination_class = LargeResultsSetPagination


class InvestigatorConnectionsListView(generics.ListAPIView):
    serializer_class = MedicalExpertConnectionSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = medical_expert_connections(self.kwargs['pk'])
        return queryset


class InvestigatorConnectionsMedicalExpertsFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(name="first_name",
                                           lookup_expr='icontains')
    middle_name = django_filters.CharFilter(name="middle_name",
                                            lookup_expr='icontains')
    last_name = django_filters.CharFilter(name="last_name",
                                          lookup_expr='icontains')
    city = django_filters.CharFilter(name="city", lookup_expr='icontains')
    country = django_filters.CharFilter(name="country__name",
                                        lookup_expr='icontains')

    class Meta:
        model = MedicalExpert
        fields = (
            'first_name', 'middle_name', 'last_name', 'city', 'country')


class InvestigatorConnectionsMedicalExpertsListView(generics.ListAPIView):
    serializer_class = MedicalExpertConnectionMedicalExpertSerializer
    filter_class = InvestigatorConnectionsMedicalExpertsFilter
    filter_backends = (OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = (
        'first_name', 'middle_name', 'last_name', 'city',
        ('country', 'country__name')
    )


class InvestigatorConnectionsAuthorsListView(
      InvestigatorConnectionsMedicalExpertsListView):

    def get_queryset(self):
        medical_experts = MedicalExpertPublication.objects. \
            filter(publication__in=MedicalExpertPublication.objects.
                   filter(medical_expert=self.kwargs['pk']).
                   exclude(publication=None).values('publication')). \
            exclude(medical_expert=self.kwargs['pk']). \
            values('medical_expert').distinct()
        queryset = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        return queryset


class InvestigatorConnectionsCTCollaboratorListView(
      InvestigatorConnectionsMedicalExpertsListView):

    def get_queryset(self):
        medical_experts = MedicalExpertClinicalTrial.objects. \
            filter(clinical_trial__in=MedicalExpertClinicalTrial.objects.
                   filter(medical_expert=self.kwargs['pk']).
                   exclude(clinical_trial=None).values('clinical_trial')). \
            exclude(medical_expert=self.kwargs['pk']). \
            values('medical_expert').distinct()
        queryset = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        return queryset


class InvestigatorConnectionsEventParticipantListView(
      InvestigatorConnectionsMedicalExpertsListView):

    def get_queryset(self):
        medical_experts = MedicalExpertEvent.objects. \
            filter(event__in=MedicalExpertEvent.objects.
                   filter(medical_expert=self.kwargs['pk']).
                   exclude(event=None).values('event')). \
            exclude(medical_expert=self.kwargs['pk']). \
            values('medical_expert').distinct()
        queryset = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        return queryset


class InvestigatorConnectionsPhysiciansListView(
      InvestigatorConnectionsMedicalExpertsListView):

    def get_queryset(self):
        physicians_institutions_filter = {
            'institution__institution_subtype__name__in':
            ['Hospital', 'Hospital Department', 'Medical Practice'],
            'position__name__in': ['Role Physician', 'Head of'],
        }
        medical_experts = MedicalExpertInstitution.objects. \
            filter(institution__in=MedicalExpertInstitution.objects.
                   filter(medical_expert=self.kwargs['pk']).
                   exclude(institution=None).
                   filter(**physicians_institutions_filter).
                   values('institution')). \
            exclude(medical_expert=self.kwargs['pk']). \
            values('medical_expert').distinct()
        queryset = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        return queryset


class InvestigatorConnectionsResearchersListView(
      InvestigatorConnectionsMedicalExpertsListView):

    def get_queryset(self):
        researchers_institutions_exclude = {
            'institution__institution_subtype__name__in':
            ['Hospital', 'Hospital Department', 'Medical Practice'],
            'position__name__in': ['Role Physician', 'Head of'],
        }
        medical_experts = MedicalExpertInstitution.objects. \
            filter(institution__in=MedicalExpertInstitution.objects.
                   filter(medical_expert=self.kwargs['pk']).
                   exclude(institution=None).
                   exclude(**researchers_institutions_exclude).
                   values('institution')). \
            exclude(medical_expert=self.kwargs['pk']). \
            values('medical_expert').distinct()
        queryset = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        return queryset


class InvestigatorAffiliationsPerInstitutionTypeListView(generics.ListAPIView):
    serializer_class = MedicalExpertAffiliationSerializer

    def get_queryset(self):
        queryset = medical_expert_affiliations(self.kwargs['pk'])
        return queryset


class InvestigatorAffiliationsFilter(django_filters.FilterSet):
    position__name = django_filters.CharFilter(
        name="position__name", lookup_expr='icontains')
    institution__hospital_university = django_filters.CharFilter(
        name="institution__hospital_university", lookup_expr='icontains')
    institution__department = django_filters.CharFilter(
        name="institution__department", lookup_expr='icontains')
    institution__institution_subtype__name = django_filters.CharFilter(
        name="institution__institution_subtype__name", lookup_expr='icontains')
    past_position = django_filters.CharFilter(name="past_position",
                                              lookup_expr='icontains')
    year = django_filters.CharFilter(name="year", lookup_expr='iexact')
    institution__city = django_filters.CharFilter(name="institution__city",
                                                  lookup_expr='icontains')
    institution__country__name = django_filters.CharFilter(
        name="institution__country__name", lookup_expr='icontains')

    class Meta:
        model = MedicalExpertInstitution
        fields = ('position__name', 'institution__hospital_university',
                  'institution__institution_subtype__name',
                  'institution__city',
                  'institution__country__name')


class InvestigatorAffiliationsListView(generics.ListAPIView):
    serializer_class = AffiliationSerializer
    filter_class = InvestigatorAffiliationsFilter
    filter_backends = (OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ('position__name', 'institution__hospital_university',
                       'institution__department',
                       'institution__institution_subtype__name',
                       'past_position', 'year', 'institution__city',
                       'institution__country__name')


institution_categories = {
    'universities': ['University', 'University Department'],
    'hospitals': ['Hospital', 'Hospital Department', 'Medical Practice'],
}


class InvestigatorAffiliationsUniversitiesListView(
      InvestigatorAffiliationsListView):
    def get_queryset(self):
        affiliations_universities_filter = {
            'institution__institution_subtype__name__in':
            institution_categories['universities']
        }
        queryset = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(**affiliations_universities_filter). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        return queryset


class InvestigatorAffiliationsHospitalsListView(
      InvestigatorAffiliationsListView):
    def get_queryset(self):
        affiliations_hospitals_filter = {
            'institution__institution_subtype__name__in':
            institution_categories['hospitals']
        }
        queryset = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(**affiliations_hospitals_filter). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        return queryset


class InvestigatorAffiliationsAssociationsListView(
      InvestigatorAffiliationsListView):
    def get_queryset(self):
        affiliations_associations_exclude = {
            'institution__institution_subtype__name__in':
            institution_categories['universities'] +
            institution_categories['hospitals']
        }
        queryset = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            exclude(**affiliations_associations_exclude). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        return queryset


class InvestigatorCompanyCooperationsPerCompanyListView(generics.ListAPIView):
    serializer_class = CooperationInstitutionTotalAmountSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        current_year = datetime.now().year
        years = (str(current_year), str(current_year - 1),
                 str(current_year - 2), str(current_year - 3),
                 str(current_year - 4), str(current_year - 5))

        queryset = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.kwargs['pk'], year__in=years). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            exclude(amount=None). \
            values('institution__oid', 'institution__hospital_university',
                   'year').annotate(total_amount=Sum('amount')). \
            order_by('-year', 'institution__hospital_university',
                     'total_amount')
        return queryset


class InvestigatorCompanyCooperationsPerNatureOfPaymentListView(
      generics.ListAPIView):
    serializer_class = NatureOfPaymentTotalAmountSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            exclude(amount=None).exclude(nature_of_payment=None). \
            values('nature_of_payment__name'). \
            annotate(total_amount=Sum('amount')). \
            order_by('total_amount', 'nature_of_payment__name')
        return queryset


class InvestigatorCompanyCooperationsFilter(django_filters.FilterSet):
    nature_of_payment = django_filters.CharFilter(
        name="nature_of_payment__name", lookup_expr='icontains')
    institution = django_filters.CharFilter(
        name="institution__hospital_university", lookup_expr='icontains')
    currency = django_filters.CharFilter(
        name="currency__code", lookup_expr='iexact')

    class Meta:
        model = MedicalExpertInstitutionCOI
        fields = ('nature_of_payment', 'year', 'institution', 'amount',
                  'currency')


class InvestigatorCompanyCooperationsListView(generics.ListAPIView):
    serializer_class = CompanyCooperationsSerializer
    filter_class = InvestigatorCompanyCooperationsFilter
    filter_backends = (OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = (('nature_of_payment', 'nature_of_payment__name'),
                       'year',
                       ('institution', 'institution__hospital_university'),
                       'amount', ('currency', 'currency__code'))

    def get_queryset(self):
        queryset = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            order_by('year')
        return queryset


class InvestigatorClinicalTrialsPerConditionListView(generics.ListAPIView):
    serializer_class = ClinicalTrialConditionTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.kwargs['pk']
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        queryset = ClinicalTrialCondition.objects. \
            filter(clinicaltrial__in=clinical_trials).values('name'). \
            annotate(total=Count('name')).order_by('total', 'name')
        return queryset


class InvestigatorClinicalTrialsPerSponsorListView(generics.ListAPIView):
    serializer_class = InstitutionTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.kwargs['pk']
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        queryset = ClinicalTrialInstitution.objects. \
            filter(clinical_trial__in=clinical_trials). \
            exclude(relationship_type=None). \
            filter(relationship_type__name='Sponsor'). \
            exclude(institution=None). \
            values('institution__hospital_university'). \
            annotate(total=Count('institution__hospital_university')). \
            order_by('total', 'institution__hospital_university')
        return queryset


class InvestigatorClinicalTrialsPerStudyPhaseListView(generics.ListAPIView):
    serializer_class = StudyPhaseTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.kwargs['pk']
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).values('pk').distinct()
        queryset = ClinicalTrial.objects. \
            filter(pk__in=clinical_trials).exclude(study_phases=None). \
            values('study_phases__name'). \
            annotate(total=Count('study_phases__name')). \
            order_by('total', 'study_phases__name')
        return queryset


class InvestigatorClinicalTrialsPerInterventionListView(
      generics.ListAPIView):
    serializer_class = InterventionTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.kwargs['pk']
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        queryset = ClinicalTrialIntervention.objects. \
            filter(clinical_trial__in=clinical_trials). \
            exclude(intervention=None). \
            values('intervention__name'). \
            annotate(total=Count('intervention__name')). \
            order_by('total', 'intervention__name')
        return queryset


class InvestigatorClinicalTrialsFilter(django_filters.FilterSet):
    brief_public_title = django_filters.CharFilter(name="brief_public_title",
                                                   lookup_expr='icontains')
    recruitment_status = django_filters.CharFilter(
        name="recruitment_status__name", lookup_expr='icontains')
    study_type = django_filters.CharFilter(name="study_type__name",
                                           lookup_expr='icontains')
    enrollment = django_filters.CharFilter(name="enrollment__name",
                                           lookup_expr='icontains')
    intervention = django_filters.CharFilter(name="intervention",
                                             lookup_expr='icontains')

    class Meta:
        model = ClinicalTrial
        fields = ('brief_public_title', 'recruitment_status',
                  'start_date_year', 'end_date_year', 'study_type',
                  'enrollment', 'intervention')


class InvestigatorClinicalTrialsListView(generics.ListAPIView):
    serializer_class = ClinicalTrialSerializer
    filter_class = InvestigatorClinicalTrialsFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = (
        'brief_public_title',
        ('recruitment_status', 'recruitment_status__name'), 'start_date_year',
        'end_date_year', ('study_type', 'study_type__name'),
        ('enrollment', 'enrollment__name'), 'intervention'
    )

    def get_queryset(self):
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.kwargs['pk']
        }
        queryset = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).order_by('pk')
        return queryset


class InvestigatorEventsPerTypeListView(generics.ListAPIView):
    serializer_class = EventSubTypeTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        events_filter = {
            'medicalexpertevent__medical_expert': self.kwargs['pk']
        }
        events = Event.objects. \
            filter(**events_filter).distinct()
        queryset = EventSubtype.objects.filter(event__in=events). \
            values('name').annotate(total=Count('name')). \
            order_by('total', 'name')
        return queryset


class InvestigatorEventsPerPositionListView(generics.ListAPIView):
    serializer_class = MedicalExpertEventPositionTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = MedicalExpertEvent.objects. \
            filter(medical_expert=self.kwargs['pk']). \
            exclude(position=None).values('position__name'). \
            annotate(total=Count('position__name')). \
            order_by('total', 'position__name')
        return queryset


class InvestigatorEventsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr='icontains')
    event_subtype = django_filters.CharFilter(name="event_subtype__name",
                                              lookup_expr='icontains')
    city = django_filters.CharFilter(name="city", lookup_expr='icontains')
    country = django_filters.CharFilter(name="country__name",
                                        lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ('name', 'event_subtype', 'start_date_year', 'city',
                  'country')


class InvestigatorEventsListView(generics.ListAPIView):
    serializer_class = EventSerializer
    filter_class = InvestigatorEventsFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = (
        'name',
        ('event_subtype', 'event_subtype__name'), 'start_date_year',
        'city', ('country', 'country__name')
    )

    def get_queryset(self):
        events_filter = {
            'medicalexpertevent__medical_expert': self.kwargs['pk']
        }
        queryset = Event.objects.filter(**events_filter).order_by('pk')
        return queryset


class InvestigatorPublicationsPerTypeListView(generics.ListAPIView):
    serializer_class = PublicationSubTypeTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        publications_filter = {
            'medicalexpertpublication__medical_expert': self.kwargs['pk']
        }
        publications = Publication.objects. \
            filter(**publications_filter).distinct()
        queryset = PublicationSubtype.objects. \
            filter(publication__in=publications). \
            values('name').annotate(total=Count('name')). \
            order_by('total', 'name')
        return queryset


class InvestigatorPublicationsPerYearListView(generics.ListAPIView):
    serializer_class = PublicationYearTotalSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        publications_filter = {
            'medicalexpertpublication__medical_expert': self.kwargs['pk']
        }
        publications = Publication.objects. \
            filter(**publications_filter).values('pk').distinct()
        queryset = Publication.objects. \
            filter(pk__in=publications).exclude(publication_year=None). \
            values('publication_year'). \
            annotate(total=Count('publication_year')). \
            order_by('publication_year')
        return queryset


class InvestigatorPublicationsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr='icontains')
    publication_subtype = django_filters.CharFilter(
        name="publication_subtype__name", lookup_expr='icontains')

    class Meta:
        model = Publication
        fields = ('name', 'publication_year')


class InvestigatorPublicationsListView(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_class = InvestigatorPublicationsFilter
    filter_backends = (OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend)
    ordering_fields = ('name', 'publication_year',
                       ('publication_subtype', 'publication_subtype__name'))

    def get_queryset(self):
        events_filter = {
            'medicalexpertpublication__medical_expert': self.kwargs['pk']
        }
        queryset = Publication.objects.filter(**events_filter).order_by('pk')
        return queryset


class FavoriteInvestigatorsListView(generics.ListAPIView):
    serializer_class = FavoriteMedicalExpertSerializer
    filter_class = InvestigatorFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = (
        'first_name', 'middle_name', 'last_name', 'city',
        ('country', 'country__name'), 'number_linked_clinical_trials',
        'number_linked_events', 'number_linked_institutions',
        'number_linked_publications',
        'number_linked_institutions_subtype_company',
        'number_linked_institutions_coi'
    )

    def get_serializer_class(self):
        """
        Return FavoriteMedicalExpertSerializerSuperUser for superuser
        """
        if self.request.user.is_superuser:
            return FavoriteMedicalExpertSerializerSuperUser
        return super(FavoriteInvestigatorsListView, self). \
            get_serializer_class()

    def get_queryset(self):
        queryset = MedicalExpert.objects. \
            filter(number_linked_clinical_trials__gt=0,
                   favoriteinvestigator__user=self.request.user).order_by('pk')
        return queryset


class RequestFilter(django_filters.FilterSet):
    get_request_type_display = django_filters.CharFilter(
        name="request_type", lookup_expr='icontains')
    added_date = django_filters.DateFilter(name="added",
                                           lookup_expr='contains')
    sent_date = django_filters.DateFilter(name="sent",
                                          lookup_expr='contains')
    get_status_display = django_filters.CharFilter(
        name="status", lookup_expr='icontains')

    class Meta:
        model = Request
        fields = ('get_request_type_display', 'added_date', 'sent_date',
                  'get_status_display')


class RequestsListView(generics.ListAPIView):
    serializer_class = RequestSerializer
    filter_class = RequestFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = (
        ('get_request_type_display', 'request_type'), ('added_date', 'added'),
        ('sent_date', 'sent'), ('get_status_display', 'status')
    )

    def get_queryset(self):
        queryset = Request.objects.filter(user=self.request.user). \
            order_by('pk')
        return queryset


class SpeakerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(name="first_name",
                                           lookup_expr='icontains')
    middle_name = django_filters.CharFilter(name="middle_name",
                                            lookup_expr='icontains')
    last_name = django_filters.CharFilter(name="last_name",
                                          lookup_expr='icontains')
    city = django_filters.CharFilter(name="city", lookup_expr='icontains')
    country = django_filters.CharFilter(name="country__name",
                                        lookup_expr='icontains')
    prop_therapeutic_areas = django_filters.CharFilter(
        name="therapeutic_areas__name", lookup_expr='icontains', distinct=True)
    prop_specialties = django_filters.CharFilter(
        name="specialties__name", lookup_expr='icontains', distinct=True)

    class Meta:
        model = MedicalExpert
        fields = (
            'first_name', 'middle_name', 'last_name', 'city',
            'country', 'number_linked_clinical_trials', 'number_linked_events',
            'number_linked_institutions', 'number_linked_publications',
            'number_linked_institutions_subtype_company',
            'number_linked_institutions_coi')


class SpeakersListView(generics.ListAPIView):
    serializer_class = SpeakerSerializer
    filter_class = SpeakerFilter
    filter_backends = (AliasedOrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = (
        'first_name', 'middle_name', 'last_name', 'city',
        ('country', 'country__name'), 'number_linked_clinical_trials',
        'number_linked_events', 'number_linked_institutions',
        'number_linked_publications',
        'number_linked_institutions_subtype_company',
        'number_linked_institutions_coi'
    )

    def get_serializer_class(self):
        """
        Return SpeakerSerializerSuperUser for superuser
        """
        if self.request.user.is_superuser:
            return SpeakerSerializerSuperUser
        return super(SpeakersListView, self).get_serializer_class()

    def get_queryset(self):
        queryset = MedicalExpert.objects.filter(
            number_linked_events__gt=0).order_by('pk')
        return queryset


class SpeakersPerCountryListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_events__gt=0). \
        exclude(country=None).values('country__name'). \
        annotate(total=Count('country__name')). \
        order_by('total', 'country__name')
    serializer_class = CountryTotalSerializer
    pagination_class = LargeResultsSetPagination


class SpeakersPerProfessionListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_events__gt=0).exclude(profession=None). \
        values('profession__name').annotate(total=Count('profession__name')). \
        order_by('total', 'profession__name')
    serializer_class = ProfessionTotalSerializer
    pagination_class = LargeResultsSetPagination


class SpeakersPerSpecialtyListView(generics.ListAPIView):
    queryset = MedicalExpert.objects. \
        filter(number_linked_events__gt=0). \
        exclude(specialties=None).values('specialties__name'). \
        annotate(total=Count('specialties__name')). \
        order_by('total', 'specialties__name')
    serializer_class = SpecialtyTotalSerializer
    pagination_class = LargeResultsSetPagination
