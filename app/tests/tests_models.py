from django.test import TestCase
from ..models import Institution, MedicalExpert


class MedicalExpertTest(TestCase):
    def setUp(self):
        MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last')
        MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=2)

    def test_medical_expert_number_linked_clinical_trials(self):
        medical_expert_1 = MedicalExpert.objects.get(first_name='First_first')
        medical_expert_2 = MedicalExpert.objects.get(first_name='Second_first')
        self.assertEqual(
            medical_expert_1.number_linked_clinical_trials, 0)
        self.assertEqual(
            medical_expert_2.number_linked_clinical_trials, 2)


class InstitutionTest(TestCase):
    def setUp(self):
        Institution.objects.create(
            hospital_university='Hospital 1',
            healthcare_network_trust='Healthcare 1',
            department='Department 1', division='Division 1',
            phone_country_code='000', phone_city_code=11,
            phone_number=222222)
        Institution.objects.create(
            hospital_university='Hospital 2', department='Department 2')

    def test_institution_data(self):
        institution_1 = Institution.objects.get(
            hospital_university='Hospital 1')
        institution_2 = Institution.objects.get(
            hospital_university='Hospital 2')
        self.assertEqual(
            institution_1.combined_name(),
            'Healthcare 1 - Hospital 1, Department 1 - Division 1')
        self.assertEqual(
            institution_1.phone(), '000 11 222222')
        self.assertEqual(
            institution_2.combined_name(), 'Hospital 2, Department 2')
        self.assertEqual(
            institution_2.phone(), None)
