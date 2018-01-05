from collections import OrderedDict
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.files import File
from django.db.models import Count, Sum
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status

from app.models import ActiveIngredient, ClinicalTrial, Event, \
                       Institution, Intervention, MedicalExpert, Publication
from app.models_relations import ClinicalTrialActiveIngredient, \
                                 ClinicalTrialInstitution, \
                                 ClinicalTrialIntervention, \
                                 MedicalExpertClinicalTrial, \
                                 MedicalExpertEvent, \
                                 MedicalExpertInstitution, \
                                 MedicalExpertInstitutionCOI, \
                                 MedicalExpertPublication
from app_helpers.models import ClinicalTrialCondition, \
                               ClinicalTrialInstitutionRelationshipType, \
                               ClinicalTrialStudyPhase, Country, \
                               EventSubtype, InstitutionSubtype, \
                               MedicalExpertise, MedicalExpertEventPosition, \
                               MedicalExpertInstitutionNatureOfPayment, \
                               MedicalExpertInstitutionPosition, \
                               PersonGender, PublicationSubtype, Profession, \
                               TherapeuticArea
from client.models import AuthorsRequest, CompanyCooperationRequest, \
                          FavoritesBaseDataRequest, \
                          FavoritesFullProfileRequest, FavoriteInvestigator, \
                          MarketAccessRequest, OtherRequest, Request


from ..helpers import medical_expert_affiliations, medical_expert_connections
from ..serializers import AffiliationSerializer, \
                          ClinicalTrialConditionTotalSerializer, \
                          ClinicalTrialSerializer, \
                          CompanyCooperationsSerializer, \
                          CooperationInstitutionTotalAmountSerializer, \
                          CountryTotalSerializer, EventSerializer, \
                          EventSubTypeTotalSerializer, \
                          FavoriteMedicalExpertSerializer, \
                          InstitutionTotalSerializer, \
                          InterventionTotalSerializer, \
                          InvestigatorSerializer, \
                          MedicalExpertAffiliationSerializer, \
                          MedicalExpertConnectionMedicalExpertSerializer, \
                          MedicalExpertConnectionSerializer, \
                          MedicalExpertEventPositionTotalSerializer, \
                          NatureOfPaymentTotalAmountSerializer, \
                          ProfessionTotalSerializer, \
                          PublicationSerializer, \
                          PublicationSubTypeTotalSerializer, \
                          PublicationYearTotalSerializer, RequestSerializer, \
                          SpeakerSerializer, SpecialtyTotalSerializer, \
                          StudyPhaseTotalSerializer

User = get_user_model()

# initialize the APIClient app
client = Client()


class GetInvestigatorsTest(TestCase):
    """ Test module for GET investigators API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Fifth_first', middle_name='Fifth_middle',
            last_name='Fifth_last')
        MedicalExpert.objects.create(
            first_name='Sixth_first', middle_name='Sixth_middle',
            last_name='Sixth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Seventh_first', middle_name='Seventh_middle',
            last_name='Seventh_last')
        MedicalExpert.objects.create(
            first_name='Eighth_first', middle_name='Eighth_middle',
            last_name='Eighth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Ninth_first', middle_name='Ninth_middle',
            last_name='Ninth_last')
        MedicalExpert.objects.create(
            first_name='Tenth_first', middle_name='Tenth_middle',
            last_name='Tenth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Eleventh_first', middle_name='Eleventh_middle',
            last_name='Eleventh_last')
        MedicalExpert.objects.create(
            first_name='Twelfth_first', middle_name='Twelfth_middle',
            last_name='Twelfth_last', number_linked_clinical_trials=2)
        client.login(username='user1234', password='demo1234')

    def test_get_investigators(self):
        # get API response
        response = client.get(reverse('get_investigators'))
        # get data from db
        investigators = MedicalExpert.objects.filter(
            number_linked_clinical_trials__gt=0).order_by('pk')[:5]
        request = HttpRequest()
        request.user = self.user
        serializer = InvestigatorSerializer(
            investigators, many=True, context={'request': request})
        serializer_data = OrderedDict([
            (u"count", 6),
            (u"next",
                "http://testserver/api/investigators/?limit=5&offset=5"),
            (u"previous", None),
            (u"results", serializer.data)
        ])
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetInvestigatorsStatisticsTest(TestCase):
    """ Test module for GET investigators statistics API """

    def setUp(self):
        User.objects.create_user(username='user1234', password='demo1234')

        # Add specialties
        specialty_1 = MedicalExpertise.objects.create(name='specialty_1')
        specialty_2 = MedicalExpertise.objects.create(name='specialty_2')
        specialty_3 = MedicalExpertise.objects.create(name='specialty_3')

        # Add genders
        male_gender = PersonGender.objects.create(name='male')
        female_gender = PersonGender.objects.create(name='female')

        # Add professions
        profession_1 = Profession.objects.create(name='profession_1')
        profession_2 = Profession.objects.create(name='profession_2')
        profession_3 = Profession.objects.create(name='profession_3')

        # Add countries
        country_1 = Country.objects.create(name='USA')
        country_2 = Country.objects.create(name='Austria')

        # Add initial MEs
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=2,
            gender=male_gender, profession=profession_1, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_clinical_trials=2,
            gender=male_gender, profession=profession_1, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Fifth_first', middle_name='Fifth_middle',
            last_name='Fifth_last')
        MedicalExpert.objects.create(
            first_name='Sixth_first', middle_name='Sixth_middle',
            last_name='Sixth_last', number_linked_clinical_trials=2,
            gender=male_gender, profession=profession_2, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Seventh_first', middle_name='Seventh_middle',
            last_name='Seventh_last')
        MedicalExpert.objects.create(
            first_name='Eighth_first', middle_name='Eighth_middle',
            last_name='Eighth_last', number_linked_clinical_trials=2,
            gender=male_gender, profession=profession_2, country=country_1). \
            specialties.add(specialty_2)
        MedicalExpert.objects.create(
            first_name='Ninth_first', middle_name='Ninth_middle',
            last_name='Ninth_last')
        MedicalExpert.objects.create(
            first_name='Tenth_first', middle_name='Tenth_middle',
            last_name='Tenth_last', number_linked_clinical_trials=2,
            gender=female_gender, profession=profession_3,
            country=country_2).specialties.add(specialty_2)
        MedicalExpert.objects.create(
            first_name='Eleventh_first', middle_name='Eleventh_middle',
            last_name='Eleventh_last')
        MedicalExpert.objects.create(
            first_name='Twelfth_first', middle_name='Twelfth_middle',
            last_name='Twelfth_last', number_linked_clinical_trials=2,
            gender=female_gender, profession=profession_3,
            country=country_2).specialties.add(specialty_3)

        client.login(username='user1234', password='demo1234')

    def test_get_investigators_per_country(self):
        # get API response
        response = client.get(reverse('get_investigators_per_country'))
        # get data from db
        countries = MedicalExpert.objects. \
            filter(number_linked_clinical_trials__gt=0). \
            exclude(country=None).values('country__name'). \
            annotate(total=Count('country__name')). \
            order_by('total', 'country__name')
        serializer = CountryTotalSerializer(countries, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigators_per_profession(self):
        # get API response
        response = client.get(reverse('get_investigators_per_profession'))
        # get data from db
        professions = MedicalExpert.objects. \
            filter(number_linked_clinical_trials__gt=0). \
            exclude(profession=None).values('profession__name'). \
            annotate(total=Count('profession__name')). \
            order_by('total', 'profession__name')
        serializer = ProfessionTotalSerializer(professions, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigators_per_specialty(self):
        # get API response
        response = client.get(reverse('get_investigators_per_specialty'))
        # get data from db
        specialties = MedicalExpert.objects. \
            filter(number_linked_clinical_trials__gt=0). \
            exclude(specialties=None).values('specialties__name'). \
            annotate(total=Count('specialties__name')). \
            order_by('total', 'specialties__name')
        serializer = SpecialtyTotalSerializer(specialties, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

institution_categories = {
    'universities': ['University', 'University Department'],
    'hospitals': ['Hospital', 'Hospital Department', 'Medical Practice'],
}


class GetSingleInvestigatorStatisticsTest(TestCase):
    """ Test module for GET single investigator API """
    current_year = datetime.now().year
    current_year_minus_1 = current_year - 1
    current_year_minus_2 = current_year - 2
    current_year_minus_3 = current_year - 3
    current_year_minus_4 = current_year - 4
    current_year_minus_5 = current_year - 5
    current_year_minus_6 = current_year - 6

    def setUp(self):
        User.objects.create_user(username='user1234', password='demo1234')

        self.investigator_1 = MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last', number_linked_clinical_trials=2)
        investigator_2 = MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=2)

        # Create institutions and link them to investigator
        institution_subtype_1 = InstitutionSubtype.objects.create(
            name='Company')
        institution_subtype_2 = InstitutionSubtype.objects.create(
            name='Hospital')
        institution_subtype_3 = InstitutionSubtype.objects.create(
            name='University')
        institution_1 = Institution.objects.create(
            hospital_university='Institution 1',
            institution_subtype=institution_subtype_1)
        institution_2 = Institution.objects.create(
            hospital_university='Institution 2',
            institution_subtype=institution_subtype_1)
        institution_3 = Institution.objects.create(
            hospital_university='Institution 3',
            institution_subtype=institution_subtype_2)
        institution_4 = Institution.objects.create(
            hospital_university='Institution 4',
            institution_subtype=institution_subtype_3)

        therapeutic_area_1 = TherapeuticArea.objects.create(
            name='Therapeutic Area 1')
        therapeutic_area_2 = TherapeuticArea.objects.create(
            name='Therapeutic Area 2')
        institution_1.therapeutic_area.add(therapeutic_area_1)
        institution_2.therapeutic_area.add(therapeutic_area_1)
        institution_3.therapeutic_area.add(therapeutic_area_2)

        position_1 = MedicalExpertInstitutionPosition.objects.create(
            name='Position 1')
        position_2 = MedicalExpertInstitutionPosition.objects.create(
            name='Role Physician')
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_1,
            primary_affiliation=True, position=position_1)
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_1,
            primary_affiliation=True, position=position_1, year=2015)
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_2,
            primary_affiliation=True, position=position_1, year=2016)
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_2,
            primary_affiliation=True, position=position_1, year=2017)
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_3,
            primary_affiliation=False, position=position_2)
        MedicalExpertInstitution.objects.create(
            medical_expert=investigator_2, institution=institution_3,
            primary_affiliation=False, position=position_2)
        for i in range(0, 2):
            MedicalExpertInstitution.objects.create(
                medical_expert=self.investigator_1, institution=institution_4,
                primary_affiliation=False, position=position_2)
        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_4,
            primary_affiliation=False, position=position_1)
        MedicalExpertInstitution.objects.create(
            medical_expert=investigator_2, institution=institution_4,
            primary_affiliation=False, position=position_1)

        nature_of_payment_1 = MedicalExpertInstitutionNatureOfPayment. \
            objects.create(name='Nature of Payment 1')
        nature_of_payment_2 = MedicalExpertInstitutionNatureOfPayment. \
            objects.create(name='Nature of Payment 2')
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=self.investigator_1, institution=institution_1,
            nature_of_payment=nature_of_payment_1, year=str(self.current_year),
            amount=100)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=self.investigator_1, institution=institution_1,
            nature_of_payment=nature_of_payment_1, year=str(self.current_year),
            amount=200)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=self.investigator_1, institution=institution_2,
            nature_of_payment=nature_of_payment_1,
            year=str(self.current_year_minus_1), amount=300)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=self.investigator_1, institution=institution_2,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_1), amount=400)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=self.investigator_1, institution=institution_3,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_2), amount=500)
        for i in range(0, 2):
            MedicalExpertInstitutionCOI.objects.create(
                medical_expert=self.investigator_1, institution=institution_4,
                nature_of_payment=nature_of_payment_2,
                year=str(self.current_year_minus_2), amount=600)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=investigator_2, institution=institution_3,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_3), amount=700)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=investigator_2, institution=institution_3,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_4), amount=700)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=investigator_2, institution=institution_3,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_5), amount=700)
        MedicalExpertInstitutionCOI.objects.create(
            medical_expert=investigator_2, institution=institution_3,
            nature_of_payment=nature_of_payment_2,
            year=str(self.current_year_minus_6), amount=700)

        # Create CTs and link them to investigator
        condition_1 = ClinicalTrialCondition.objects.create(name='Condition 1')
        condition_2 = ClinicalTrialCondition.objects.create(name='Condition 2')
        study_phase_1 = ClinicalTrialStudyPhase.objects.create(
            name='Study Phase 1')
        study_phase_2 = ClinicalTrialStudyPhase.objects.create(
            name='Study Phase 2')

        clinical_trial_1 = ClinicalTrial.objects.create()
        clinical_trial_1.condition.add(condition_1)
        clinical_trial_1.condition.add(condition_2)
        clinical_trial_1.study_phases.add(study_phase_1)
        clinical_trial_1.study_phases.add(study_phase_2)

        clinical_trial_2 = ClinicalTrial.objects.create()
        clinical_trial_2.condition.add(condition_1)
        clinical_trial_2.study_phases.add(study_phase_2)

        MedicalExpertClinicalTrial.objects.create(
            medical_expert=self.investigator_1,
            clinical_trial=clinical_trial_1)
        MedicalExpertClinicalTrial.objects.create(
            medical_expert=self.investigator_1,
            clinical_trial=clinical_trial_2)
        MedicalExpertClinicalTrial.objects.create(
            medical_expert=investigator_2, clinical_trial=clinical_trial_2)

        relationship_type_1 = ClinicalTrialInstitutionRelationshipType. \
            objects.create(name='Sponsor')
        ClinicalTrialInstitution.objects.create(
            institution=institution_1,
            clinical_trial=clinical_trial_1,
            relationship_type=relationship_type_1)
        ClinicalTrialInstitution.objects.create(
            institution=institution_2,
            clinical_trial=clinical_trial_1,
            relationship_type=relationship_type_1)
        ClinicalTrialInstitution.objects.create(
            institution=institution_3,
            clinical_trial=clinical_trial_2)

        intervention_1 = Intervention.objects.create(name='Intervention 1')
        intervention_2 = Intervention.objects.create(name='Intervention 2')
        ClinicalTrialIntervention.objects.create(
            clinical_trial=clinical_trial_1, intervention=intervention_1)
        ClinicalTrialIntervention.objects.create(
            clinical_trial=clinical_trial_1, intervention=intervention_2)
        ClinicalTrialIntervention.objects.create(
            clinical_trial=clinical_trial_2, intervention=intervention_2)

        active_ingredient_1 = ActiveIngredient.objects.create(
            name='Active Ingredient 1')
        active_ingredient_2 = ActiveIngredient.objects.create(
            name='Active Ingredient 2')
        ClinicalTrialActiveIngredient.objects.create(
            clinical_trial=clinical_trial_1,
            active_ingredient=active_ingredient_1)
        ClinicalTrialActiveIngredient.objects.create(
            clinical_trial=clinical_trial_1,
            active_ingredient=active_ingredient_2)
        ClinicalTrialActiveIngredient.objects.create(
            clinical_trial=clinical_trial_2,
            active_ingredient=active_ingredient_2)

        event_subtype_1 = EventSubtype.objects.create(name='Subtype 1')
        event_subtype_2 = EventSubtype.objects.create(name='Subtype 2')
        event_1 = Event.objects.create(name='Event 1',
                                       event_subtype=event_subtype_1)
        event_2 = Event.objects.create(name='Event 2',
                                       event_subtype=event_subtype_1)
        event_3 = Event.objects.create(name='Event 3',
                                       event_subtype=event_subtype_2)
        position_1 = MedicalExpertEventPosition.objects.create(
            name='Position 1')
        position_2 = MedicalExpertEventPosition.objects.create(
            name='Position 2')
        MedicalExpertEvent.objects.create(medical_expert=self.investigator_1,
                                          event=event_1, position=position_1)
        MedicalExpertEvent.objects.create(medical_expert=self.investigator_1,
                                          event=event_2, position=position_2)
        MedicalExpertEvent.objects.create(medical_expert=self.investigator_1,
                                          event=event_3, position=position_2)
        MedicalExpertEvent.objects.create(medical_expert=investigator_2,
                                          event=event_3, position=position_2)
        event_1.therapeutic_area.add(therapeutic_area_1)
        event_1.therapeutic_area.add(therapeutic_area_2)
        event_2.therapeutic_area.add(therapeutic_area_2)

        publication_subtype_1 = PublicationSubtype.objects.create(
            name='Publication Type 1')
        publication_subtype_2 = PublicationSubtype.objects.create(
            name='Publication Type 2')
        publication_1 = Publication.objects.create(
            name='Publication 1', publication_subtype=publication_subtype_1,
            publication_year=2015)
        publication_2 = Publication.objects.create(
            name='Publication 2', publication_subtype=publication_subtype_1,
            publication_year=2015)
        publication_3 = Publication.objects.create(
            name='Publication 3', publication_subtype=publication_subtype_2,
            publication_year=2016)
        MedicalExpertPublication.objects.create(
            medical_expert=self.investigator_1, publication=publication_1)
        MedicalExpertPublication.objects.create(
            medical_expert=self.investigator_1, publication=publication_2)
        MedicalExpertPublication.objects.create(
            medical_expert=self.investigator_1, publication=publication_3)
        MedicalExpertPublication.objects.create(
            medical_expert=investigator_2, publication=publication_3)

        client.login(username='user1234', password='demo1234')

    def test_get_investigator_connections(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        connections = medical_expert_connections(self.investigator_1)
        serializer = MedicalExpertConnectionSerializer(connections, many=True)

        serializer_data = OrderedDict([
            (u"count", 5),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_connections_authors(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections_authors',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        medical_experts = MedicalExpertPublication.objects. \
            filter(publication__in=MedicalExpertPublication.objects.
                   filter(medical_expert=self.investigator_1).
                   exclude(publication=None).values('publication')). \
            exclude(medical_expert=self.investigator_1). \
            values('medical_expert').distinct()
        connections = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        serializer = MedicalExpertConnectionMedicalExpertSerializer(
            connections, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_connections_clinical_trial_collaborators(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections_clinical_trial_collaborators',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        medical_experts = MedicalExpertClinicalTrial.objects. \
            filter(clinical_trial__in=MedicalExpertClinicalTrial.objects.
                   filter(medical_expert=self.investigator_1).
                   exclude(clinical_trial=None).values('clinical_trial')). \
            exclude(medical_expert=self.investigator_1). \
            values('medical_expert').distinct()
        connections = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        serializer = MedicalExpertConnectionMedicalExpertSerializer(
            connections, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_connections_event_participants(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections_event_participants',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        medical_experts = MedicalExpertEvent.objects. \
            filter(event__in=MedicalExpertEvent.objects.
                   filter(medical_expert=self.investigator_1).
                   exclude(event=None).values('event')). \
            exclude(medical_expert=self.investigator_1). \
            values('medical_expert').distinct()
        connections = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        serializer = MedicalExpertConnectionMedicalExpertSerializer(
            connections, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_connections_physicians(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections_physicians',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        physicians_institutions_filter = {
            'institution__institution_subtype__name__in':
            ['Hospital', 'Hospital Department', 'Medical Practice'],
            'position__name__in': ['Role Physician', 'Head of'],
        }
        medical_experts = MedicalExpertInstitution.objects. \
            filter(institution__in=MedicalExpertInstitution.objects.
                   filter(medical_expert=self.investigator_1).
                   exclude(institution=None).
                   filter(**physicians_institutions_filter).
                   values('institution')). \
            exclude(medical_expert=self.investigator_1). \
            values('medical_expert').distinct()
        connections = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        serializer = MedicalExpertConnectionMedicalExpertSerializer(
            connections, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_connections_researchers(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_connections_researchers',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        researchers_institutions_exclude = {
            'institution__institution_subtype__name__in':
            ['Hospital', 'Hospital Department', 'Medical Practice'],
            'position__name__in': ['Role Physician', 'Head of'],
        }
        medical_experts = MedicalExpertInstitution.objects. \
            filter(institution__in=MedicalExpertInstitution.objects.
                   filter(medical_expert=self.investigator_1).
                   exclude(institution=None).
                   exclude(**researchers_institutions_exclude).
                   values('institution')). \
            exclude(medical_expert=self.investigator_1). \
            values('medical_expert').distinct()
        connections = MedicalExpert.objects.filter(pk__in=medical_experts). \
            order_by('pk')
        serializer = MedicalExpertConnectionMedicalExpertSerializer(
            connections, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_investigator_affiliations_per_institution_type(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_affiliations_per_institution_type',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        affiliations = medical_expert_affiliations(self.investigator_1)
        serializer = MedicalExpertAffiliationSerializer(affiliations,
                                                        many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_affiliations_universities(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_affiliations_universities',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        affiliations_universities_filter = {
            'institution__institution_subtype__name__in':
            institution_categories['universities']
        }
        affiliations = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(**affiliations_universities_filter). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        serializer = AffiliationSerializer(affiliations, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_affiliations_hospitals(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_affiliations_hospitals',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        affiliations_hospitals_filter = {
            'institution__institution_subtype__name__in':
            institution_categories['hospitals']
        }
        affiliations = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(**affiliations_hospitals_filter). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        serializer = AffiliationSerializer(affiliations, many=True)
        serializer_data = OrderedDict([
            (u"count", 1),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_affiliations_associations(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_affiliations_associations',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        affiliations_associations_exclude = {
            'institution__institution_subtype__name__in':
            institution_categories['universities'] +
            institution_categories['hospitals']
        }
        affiliations = MedicalExpertInstitution.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            exclude(**affiliations_associations_exclude). \
            values('position__name', 'institution__hospital_university',
                   'institution__department',
                   'institution__institution_subtype__name', 'past_position',
                   'year', 'institution__city',
                   'institution__country__name'). \
            order_by('pk')
        serializer = AffiliationSerializer(affiliations, many=True)
        serializer_data = OrderedDict([
            (u"count", 4),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_cooperations_per_company(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_cooperations_per_company',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        years = (str(self.current_year), str(self.current_year_minus_1),
                 str(self.current_year_minus_2),
                 str(self.current_year_minus_3),
                 str(self.current_year_minus_4),
                 str(self.current_year_minus_5))
        cooperations = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.investigator_1, year__in=years). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            exclude(amount=None). \
            values('institution__oid', 'institution__hospital_university',
                   'year').annotate(total_amount=Sum('amount')). \
            order_by('-year', 'institution__hospital_university',
                     'total_amount')
        serializer = CooperationInstitutionTotalAmountSerializer(cooperations,
                                                                 many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_cooperations_per_nature_of_payment(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_company_cooperations_per_nature_of_payment',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        cooperations = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            exclude(amount=None).exclude(nature_of_payment=None). \
            values('nature_of_payment__name'). \
            annotate(total_amount=Sum('amount')). \
            order_by('total_amount', 'nature_of_payment__name')
        serializer = NatureOfPaymentTotalAmountSerializer(cooperations,
                                                          many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_company_cooperations(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_company_cooperations',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        cooperations = MedicalExpertInstitutionCOI.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(institution=None). \
            exclude(institution__institution_subtype=None). \
            filter(institution__institution_subtype__name='Company'). \
            order_by('year')
        serializer = CompanyCooperationsSerializer(cooperations, many=True)
        serializer_data = OrderedDict([
            (u"count", 4),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_clinical_trials_per_condition(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_clinical_trials_per_condition',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.investigator_1
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        conditions = ClinicalTrialCondition.objects. \
            filter(clinicaltrial__in=clinical_trials).values('name'). \
            annotate(total=Count('name')).order_by('total', 'name')
        serializer = ClinicalTrialConditionTotalSerializer(conditions,
                                                           many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_clinical_trials_per_sponsor(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_clinical_trials_per_sponsor',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.investigator_1
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        companies = ClinicalTrialInstitution.objects. \
            filter(clinical_trial__in=clinical_trials). \
            exclude(relationship_type=None). \
            filter(relationship_type__name='Sponsor'). \
            exclude(institution=None). \
            values('institution__hospital_university'). \
            annotate(total=Count('institution__hospital_university')). \
            order_by('total', 'institution__hospital_university')
        serializer = InstitutionTotalSerializer(companies, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_clinical_trials_per_study_phase(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_clinical_trials_per_study_phase',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.investigator_1
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).values('pk').distinct()
        study_phases = ClinicalTrial.objects. \
            filter(pk__in=clinical_trials).exclude(study_phases=None). \
            values('study_phases__name'). \
            annotate(total=Count('study_phases__name')). \
            order_by('total', 'study_phases__name')
        serializer = StudyPhaseTotalSerializer(study_phases, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_clinical_trials_per_intervention(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_clinical_trials_per_intervention',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.investigator_1
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).distinct()
        interventions = ClinicalTrialIntervention.objects. \
            filter(clinical_trial__in=clinical_trials). \
            exclude(intervention=None). \
            values('intervention__name'). \
            annotate(total=Count('intervention__name')). \
            order_by('total', 'intervention__name')
        serializer = InterventionTotalSerializer(interventions,
                                                 many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_clinical_trials(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_clinical_trials',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        clinical_trials_filter = {
            'medicalexpertclinicaltrial__medical_expert': self.investigator_1
        }
        clinical_trials = ClinicalTrial.objects. \
            filter(**clinical_trials_filter).order_by('pk')
        serializer = ClinicalTrialSerializer(clinical_trials, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_events_per_type(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_events_per_type',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        events_filter = {
            'medicalexpertevent__medical_expert': self.investigator_1
        }
        events = Event.objects. \
            filter(**events_filter).distinct()
        event_subtypes = EventSubtype.objects.filter(event__in=events). \
            values('name').annotate(total=Count('name')). \
            order_by('total', 'name')
        serializer = EventSubTypeTotalSerializer(event_subtypes, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_events_per_position(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_events_per_position',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        positions = MedicalExpertEvent.objects. \
            filter(medical_expert=self.investigator_1). \
            exclude(position=None).values('position__name'). \
            annotate(total=Count('position__name')). \
            order_by('total', 'position__name')
        serializer = MedicalExpertEventPositionTotalSerializer(positions,
                                                               many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_events(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_events',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        events_filter = {
            'medicalexpertevent__medical_expert': self.investigator_1
        }
        events = Event.objects.filter(**events_filter).order_by('pk')
        serializer = EventSerializer(events, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_publications_per_type(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_publications_per_type',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        publications_filter = {
            'medicalexpertpublication__medical_expert': self.investigator_1
        }
        publications = Publication.objects. \
            filter(**publications_filter).distinct()
        publication_subtypes = PublicationSubtype.objects. \
            filter(publication__in=publications). values('name'). \
            annotate(total=Count('name')). \
            order_by('total', 'name')
        serializer = PublicationSubTypeTotalSerializer(publication_subtypes,
                                                       many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_publications_per_year(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_publications_per_year',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        publications_filter = {
            'medicalexpertpublication__medical_expert': self.investigator_1
        }
        publications = Publication.objects. \
            filter(**publications_filter).values('pk').distinct()
        publication_years = Publication.objects. \
            filter(pk__in=publications).exclude(publication_year=None). \
            values('publication_year'). \
            annotate(total=Count('publication_year')). \
            order_by('publication_year')
        serializer = PublicationYearTotalSerializer(publication_years,
                                                    many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_investigator_publications(self):
        # get API response
        response = client.get(reverse(
            'get_investigator_publications',
            kwargs={'pk': self.investigator_1.pk}))
        # get data from db
        events_filter = {
            'medicalexpertpublication__medical_expert': self.investigator_1
        }
        publications = Publication.objects.filter(**events_filter). \
            order_by('pk')
        serializer = PublicationSerializer(publications, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFavoriteInvestigatorsTest(TestCase):
    """ Test module for GET investigators API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        investigator_2 = MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        investigator_4 = MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Fifth_first', middle_name='Fifth_middle',
            last_name='Fifth_last')
        investigator_6 = MedicalExpert.objects.create(
            first_name='Sixth_first', middle_name='Sixth_middle',
            last_name='Sixth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Seventh_first', middle_name='Seventh_middle',
            last_name='Seventh_last')
        investigator_8 = MedicalExpert.objects.create(
            first_name='Eighth_first', middle_name='Eighth_middle',
            last_name='Eighth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Ninth_first', middle_name='Ninth_middle',
            last_name='Ninth_last')
        investigator_10 = MedicalExpert.objects.create(
            first_name='Tenth_first', middle_name='Tenth_middle',
            last_name='Tenth_last', number_linked_clinical_trials=2)
        MedicalExpert.objects.create(
            first_name='Eleventh_first', middle_name='Eleventh_middle',
            last_name='Eleventh_last')
        investigator_12 = MedicalExpert.objects.create(
            first_name='Twelfth_first', middle_name='Twelfth_middle',
            last_name='Twelfth_last', number_linked_clinical_trials=2)

        # Add favorite investigators
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_2)
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_4)
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_6)
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_8)
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_10)
        FavoriteInvestigator.objects.create(user=self.user,
                                            investigator=investigator_12)

        client.login(username='user1234', password='demo1234')

    def test_get_favorite_investigators(self):
        # get API response
        response = client.get(reverse('get_favorite_investigators'))
        # get data from db
        investigators = MedicalExpert.objects. \
            filter(number_linked_clinical_trials__gt=0,
                   favoriteinvestigator__user=self.user).order_by('pk')[:5]
        request = HttpRequest()
        request.user = self.user
        serializer = FavoriteMedicalExpertSerializer(
            investigators, many=True, context={'request': request})
        serializer_data = OrderedDict([
            (u"count", 6),
            (u"next",
                "http://testserver/api/favorite-investigators/"
                "?limit=5&offset=5"),
            (u"previous", None),
            (u"results", serializer.data)
        ])
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetRequestsTest(TestCase):
    """ Test module for GET investigators API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

        country_1 = Country.objects.create(name='United States')
        country_2 = Country.objects.create(name='Austria')
        publication_subtype_1 = PublicationSubtype.objects.create(
            name='Publication Type 1')
        publication_subtype_2 = PublicationSubtype.objects.create(
            name='Publication Type 2')
        request_file = open('dummy_file.xlsx')

        FavoritesBaseDataRequest.objects.create(user=self.user)
        FavoritesFullProfileRequest.objects.create(user=self.user)
        request_3 = AuthorsRequest.objects.create(
            user=self.user, year_from=2015, year_to=2016,
            topic_interest='This is a dummy topic message',
            other_comments='This is a dummy comments message', favorites=True)
        request_3.types_publication_interest.add(publication_subtype_1)
        request_3.types_publication_interest.add(publication_subtype_2)
        request_3.countries_interest.add(country_1)
        request_3.countries_interest.add(country_2)
        request_4 = MarketAccessRequest.objects.create(
            user=self.user, topic_interest='This is a dummy topic message',
            other_comments='This is a dummy comments message',
            favorites=False)
        request_4.request_file.save('dummy_file.xlsx', File(request_file))
        request_4.countries_interest.add(country_1)
        CompanyCooperationRequest.objects.create(user=self.user,
                                                 favorites=True)
        request_6 = OtherRequest.objects.create(user=self.user,
                                                favorites=False)
        request_6.request_file.save('dummy_file.xlsx', File(request_file))

        client.login(username='user1234', password='demo1234')

    def test_get_requests(self):
        # get API response
        response = client.get(reverse('get_requests'))
        # get data from db
        requests = Request.objects.filter(user=self.user).order_by('pk')[:5]
        request = HttpRequest()
        request.user = self.user
        serializer = RequestSerializer(requests, many=True)
        serializer_data = serializer.data
        for result in serializer_data:
            request_file = result['request_file']
            if request_file:
                result['request_file'] = \
                    'http://testserver%s' % request_file
        serializer_data = OrderedDict([
            (u"count", 6),
            (u"next",
                "http://testserver/api/requests/"
                "?limit=5&offset=5"),
            (u"previous", None),
            (u"results", serializer_data)
        ])
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSpeakersTest(TestCase):
    """ Test module for GET speakers API """

    def setUp(self):
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_events=2)
        MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_events=2)
        MedicalExpert.objects.create(
            first_name='Fifth_first', middle_name='Fifth_middle',
            last_name='Fifth_last')
        MedicalExpert.objects.create(
            first_name='Sixth_first', middle_name='Sixth_middle',
            last_name='Sixth_last', number_linked_events=2)
        MedicalExpert.objects.create(
            first_name='Seventh_first', middle_name='Seventh_middle',
            last_name='Seventh_last')
        MedicalExpert.objects.create(
            first_name='Eighth_first', middle_name='Eighth_middle',
            last_name='Eighth_last', number_linked_events=2)
        MedicalExpert.objects.create(
            first_name='Ninth_first', middle_name='Ninth_middle',
            last_name='Ninth_last')
        MedicalExpert.objects.create(
            first_name='Tenth_first', middle_name='Tenth_middle',
            last_name='Tenth_last', number_linked_events=2)
        MedicalExpert.objects.create(
            first_name='Eleventh_first', middle_name='Eleventh_middle',
            last_name='Eleventh_last')
        MedicalExpert.objects.create(
            first_name='Twelfth_first', middle_name='Twelfth_middle',
            last_name='Twelfth_last', number_linked_events=2)
        client.login(username='user1234', password='demo1234')

    def test_get_speakers(self):
        # get API response
        response = client.get(reverse('get_speakers'))
        # get data from db
        speakers = MedicalExpert.objects.filter(
            number_linked_events__gt=0).order_by('pk')[:5]
        request = HttpRequest()
        request.user = self.user
        serializer = SpeakerSerializer(
            speakers, many=True, context={'request': request})
        serializer_data = OrderedDict([
            (u"count", 6),
            (u"next",
                "http://testserver/api/speakers/?limit=5&offset=5"),
            (u"previous", None),
            (u"results", serializer.data)
        ])
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSpeakersStatisticsTest(TestCase):
    """ Test module for GET speakers statistics API """

    def setUp(self):
        User.objects.create_user(username='user1234', password='demo1234')

        # Add specialties
        specialty_1 = MedicalExpertise.objects.create(name='specialty_1')
        specialty_2 = MedicalExpertise.objects.create(name='specialty_2')
        specialty_3 = MedicalExpertise.objects.create(name='specialty_3')

        # Add genders
        male_gender = PersonGender.objects.create(name='male')
        female_gender = PersonGender.objects.create(name='female')

        # Add professions
        profession_1 = Profession.objects.create(name='profession_1')
        profession_2 = Profession.objects.create(name='profession_2')
        profession_3 = Profession.objects.create(name='profession_3')

        # Add countries
        country_1 = Country.objects.create(name='USA')
        country_2 = Country.objects.create(name='Austria')

        # Add initial MEs
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_events=2,
            gender=male_gender, profession=profession_1, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_events=2,
            gender=male_gender, profession=profession_1, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Fifth_first', middle_name='Fifth_middle',
            last_name='Fifth_last')
        MedicalExpert.objects.create(
            first_name='Sixth_first', middle_name='Sixth_middle',
            last_name='Sixth_last', number_linked_events=2,
            gender=male_gender, profession=profession_2, country=country_1). \
            specialties.add(specialty_1)
        MedicalExpert.objects.create(
            first_name='Seventh_first', middle_name='Seventh_middle',
            last_name='Seventh_last')
        MedicalExpert.objects.create(
            first_name='Eighth_first', middle_name='Eighth_middle',
            last_name='Eighth_last', number_linked_events=2,
            gender=male_gender, profession=profession_2, country=country_1). \
            specialties.add(specialty_2)
        MedicalExpert.objects.create(
            first_name='Ninth_first', middle_name='Ninth_middle',
            last_name='Ninth_last')
        MedicalExpert.objects.create(
            first_name='Tenth_first', middle_name='Tenth_middle',
            last_name='Tenth_last', number_linked_events=2,
            gender=female_gender, profession=profession_3,
            country=country_2).specialties.add(specialty_2)
        MedicalExpert.objects.create(
            first_name='Eleventh_first', middle_name='Eleventh_middle',
            last_name='Eleventh_last')
        MedicalExpert.objects.create(
            first_name='Twelfth_first', middle_name='Twelfth_middle',
            last_name='Twelfth_last', number_linked_events=2,
            gender=female_gender, profession=profession_3,
            country=country_2).specialties.add(specialty_3)

        client.login(username='user1234', password='demo1234')

    def test_get_speakers_per_country(self):
        # get API response
        response = client.get(reverse('get_speakers_per_country'))
        # get data from db
        countries = MedicalExpert.objects. \
            filter(number_linked_events__gt=0). \
            exclude(country=None).values('country__name'). \
            annotate(total=Count('country__name')). \
            order_by('total', 'country__name')
        serializer = CountryTotalSerializer(countries, many=True)
        serializer_data = OrderedDict([
            (u"count", 2),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_speakers_per_profession(self):
        # get API response
        response = client.get(reverse('get_speakers_per_profession'))
        # get data from db
        professions = MedicalExpert.objects. \
            filter(number_linked_events__gt=0). \
            exclude(profession=None).values('profession__name'). \
            annotate(total=Count('profession__name')). \
            order_by('total', 'profession__name')
        serializer = ProfessionTotalSerializer(professions, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_speakers_per_specialty(self):
        # get API response
        response = client.get(reverse('get_speakers_per_specialty'))
        # get data from db
        specialties = MedicalExpert.objects. \
            filter(number_linked_events__gt=0). \
            exclude(specialties=None).values('specialties__name'). \
            annotate(total=Count('specialties__name')). \
            order_by('total', 'specialties__name')
        serializer = SpecialtyTotalSerializer(specialties, many=True)
        serializer_data = OrderedDict([
            (u"count", 3),
            (u"next", None),
            (u"previous", None),
            (u"results", serializer.data)
        ])

        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
