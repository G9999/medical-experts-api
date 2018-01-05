from rest_framework import serializers
from rest_framework_constant.fields import ConstantField

from app.models import ClinicalTrial, Event, MedicalExpert, Publication
from app.models_relations import MedicalExpertInstitutionCOI
from client.models import Request


class InvestigatorSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    is_unlocked_investigator = serializers.SerializerMethodField(
        '_is_unlocked_investigator')
    is_favorite_investigator = serializers.SerializerMethodField(
        '_is_favorite_investigator')

    def _is_unlocked_investigator(self, obj):
        user = self.context['request'].user
        return obj.is_unlocked_investigator(user)

    def _is_favorite_investigator(self, obj):
        user = self.context['request'].user
        return obj.is_favorite_investigator(user)

    class Meta:
        model = MedicalExpert
        fields = ('oid', 'first_name', 'middle_name', 'last_name',
                  'prop_therapeutic_areas', 'prop_specialties', 'city',
                  'country', 'number_linked_clinical_trials',
                  'number_linked_events', 'number_linked_institutions',
                  'number_linked_publications',
                  'number_linked_institutions_subtype_company',
                  'number_linked_institutions_coi', 'is_unlocked_investigator',
                  'is_favorite_investigator')


class InvestigatorSerializerSuperUser(InvestigatorSerializer):
    """
    Overwrite the 'is_unlocked_investigator' with True when the user is
    superuser
    """
    is_unlocked_investigator = ConstantField(value=True)


class CountryTotalSerializer(serializers.Serializer):
    country__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('country__name', 'total')


class ProfessionTotalSerializer(serializers.Serializer):
    profession__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('profession__name', 'total')


class SpecialtyTotalSerializer(serializers.Serializer):
    specialties__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('specialties__name', 'total')


class MedicalExpertConnectionSerializer(serializers.Serializer):
    connection_type = serializers.CharField()
    label = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('connection_type', 'label', 'total')


class MedicalExpertConnectionMedicalExpertSerializer(
      serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = MedicalExpert
        fields = ('first_name', 'middle_name', 'last_name', 'city', 'country')


class MedicalExpertAffiliationSerializer(serializers.Serializer):
    affiliation_type = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('affiliation_type', 'total')


class AffiliationSerializer(serializers.Serializer):
    position__name = serializers.CharField()
    institution__hospital_university = serializers.CharField()
    institution__department = serializers.CharField()
    institution__institution_subtype__name = serializers.CharField()
    past_position = serializers.CharField()
    year = serializers.CharField()
    institution__city = serializers.CharField()
    institution__country__name = serializers.CharField()

    class Meta:
        fields = ('position__name', 'institution__hospital_university',
                  'institution__department',
                  'institution__institution_subtype__name', 'past_position',
                  'year', 'institution__city', 'institution__country__name')


class CooperationInstitutionTotalAmountSerializer(serializers.Serializer):
    institution__oid = serializers.CharField()
    institution__hospital_university = serializers.CharField()
    year = serializers.IntegerField()
    total_amount = serializers.FloatField()

    class Meta:
        fields = ('institution__oid', 'institution__hospital_university',
                  'year', 'total_amount')


class NatureOfPaymentTotalAmountSerializer(serializers.Serializer):
    nature_of_payment__name = serializers.CharField()
    total_amount = serializers.FloatField()

    class Meta:
        fields = ('nature_of_payment__name', 'total_amount')


class CompanyCooperationsSerializer(serializers.ModelSerializer):
    nature_of_payment = serializers.StringRelatedField()
    institution = serializers.StringRelatedField()
    currency = serializers.StringRelatedField()

    class Meta:
        model = MedicalExpertInstitutionCOI
        fields = ('nature_of_payment', 'year', 'institution', 'amount',
                  'currency')


class ClinicalTrialConditionTotalSerializer(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('name', 'total')


class InstitutionTotalSerializer(serializers.Serializer):
    institution__hospital_university = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('institution__hospital_university', 'total')


class StudyPhaseTotalSerializer(serializers.Serializer):
    study_phases__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('study_phases__name', 'total')


class InterventionTotalSerializer(serializers.Serializer):
    intervention__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('intervention__name', 'total')


class ClinicalTrialSerializer(serializers.ModelSerializer):
    recruitment_status = serializers.StringRelatedField()
    study_type = serializers.StringRelatedField()
    enrollment = serializers.StringRelatedField()

    class Meta:
        model = ClinicalTrial
        fields = ('brief_public_title', 'prop_conditions',
                  'recruitment_status', 'start_date_year', 'end_date_year',
                  'prop_study_phases', 'study_type', 'enrollment',
                  'intervention')


class EventSubTypeTotalSerializer(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('name', 'total')


class MedicalExpertEventPositionTotalSerializer(serializers.Serializer):
    position__name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('position__name', 'total')


class EventSerializer(serializers.ModelSerializer):
    event_subtype = serializers.StringRelatedField()
    country = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = ('name', 'event_subtype', 'start_date_year', 'city',
                  'country')


class PublicationSubTypeTotalSerializer(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('name', 'total')


class PublicationYearTotalSerializer(serializers.Serializer):
    publication_year = serializers.CharField()
    total = serializers.IntegerField()

    class Meta:
        fields = ('publication_year', 'total')


class PublicationSerializer(serializers.ModelSerializer):
    publication_subtype = serializers.StringRelatedField()

    class Meta:
        model = Publication
        fields = ('name', 'publication_year', 'publication_subtype')


class FavoriteMedicalExpertSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    is_unlocked_investigator = serializers.SerializerMethodField(
        '_is_unlocked_investigator')

    def _is_unlocked_investigator(self, obj):
        user = self.context['request'].user
        return obj.is_unlocked_investigator(user)

    class Meta:
        model = MedicalExpert
        fields = ('oid', 'first_name', 'middle_name', 'last_name',
                  'prop_therapeutic_areas', 'prop_specialties', 'city',
                  'country', 'number_linked_clinical_trials',
                  'number_linked_events', 'number_linked_institutions',
                  'number_linked_publications',
                  'number_linked_institutions_subtype_company',
                  'number_linked_institutions_coi',
                  'is_unlocked_investigator')


class FavoriteMedicalExpertSerializerSuperUser(
      FavoriteMedicalExpertSerializer):
    """
    Overwrite the 'is_unlocked_investigator' with True when the user is
    superuser
    """
    is_unlocked_investigator = ConstantField(value=True)


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('pk', 'get_request_type_display', 'request_file',
                  'favorites', 'added_date', 'sent_date', 'get_status_display',
                  'details')


class SpeakerSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    is_unlocked_investigator = serializers.SerializerMethodField(
        '_is_unlocked_investigator')
    is_favorite_investigator = serializers.SerializerMethodField(
        '_is_favorite_investigator')

    def _is_unlocked_investigator(self, obj):
        user = self.context['request'].user
        return obj.is_unlocked_investigator(user)

    def _is_favorite_investigator(self, obj):
        user = self.context['request'].user
        return obj.is_favorite_investigator(user)

    class Meta:
        model = MedicalExpert
        fields = ('oid', 'first_name', 'middle_name', 'last_name',
                  'prop_therapeutic_areas', 'prop_specialties', 'city',
                  'country', 'number_linked_clinical_trials',
                  'number_linked_events', 'number_linked_institutions',
                  'number_linked_publications',
                  'number_linked_institutions_subtype_company',
                  'number_linked_institutions_coi', 'is_unlocked_investigator',
                  'is_unlocked_investigator', 'is_favorite_investigator')


class SpeakerSerializerSuperUser(SpeakerSerializer):
    """
    Overwrite the 'is_unlocked_investigator' with True when the user is
    superuser
    """
    is_unlocked_investigator = ConstantField(value=True)
