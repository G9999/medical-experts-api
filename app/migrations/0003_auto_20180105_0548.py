# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-05 05:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_helpers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_publicationclinicaltrial_relationship_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.PublicationSubtype'),
        ),
        migrations.AddField(
            model_name='publication',
            name='therapeutic_area',
            field=models.ManyToManyField(to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='medicalexpertpublication',
            name='medical_expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MedicalExpert'),
        ),
        migrations.AddField(
            model_name='medicalexpertpublication',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertPublicationPosition'),
        ),
        migrations.AddField(
            model_name='medicalexpertpublication',
            name='publication',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Publication'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitutioncoi',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Currency'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitutioncoi',
            name='form_of_payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertInstitutionFormOfPayment'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitutioncoi',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitutioncoi',
            name='medical_expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MedicalExpert'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitutioncoi',
            name='nature_of_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertInstitutionNatureOfPayment'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitution',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitution',
            name='medical_expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MedicalExpert'),
        ),
        migrations.AddField(
            model_name='medicalexpertinstitution',
            name='position',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertInstitutionPosition'),
        ),
        migrations.AddField(
            model_name='medicalexpertevent',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Event'),
        ),
        migrations.AddField(
            model_name='medicalexpertevent',
            name='medical_expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MedicalExpert'),
        ),
        migrations.AddField(
            model_name='medicalexpertevent',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertEventPosition'),
        ),
        migrations.AddField(
            model_name='medicalexpertclinicaltrial',
            name='clinical_trial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ClinicalTrial'),
        ),
        migrations.AddField(
            model_name='medicalexpertclinicaltrial',
            name='medical_expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MedicalExpert'),
        ),
        migrations.AddField(
            model_name='medicalexpertclinicaltrial',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalExpertClinicalTrialPosition'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='career_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.CareerStage'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Country'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='degree',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Degree'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.PersonGender'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='profession',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Profession'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='specialties',
            field=models.ManyToManyField(blank=True, related_name='app_medicalexpert_related', to='app_helpers.MedicalExpertise'),
        ),
        migrations.AddField(
            model_name='medicalexpert',
            name='therapeutic_areas',
            field=models.ManyToManyField(blank=True, related_name='app_medicalexpert_related', to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='medicaldevice',
            name='device_regulatory_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalDeviceRegulatoryClass'),
        ),
        migrations.AddField(
            model_name='medicaldevice',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interventionintervention',
            name='intervention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interventions_related', to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionintervention',
            name='intervention_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interventions_related_to', to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionintervention',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.InterventionInterventionRelationshipType'),
        ),
        migrations.AddField(
            model_name='interventioninstitution',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AddField(
            model_name='interventioninstitution',
            name='intervention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='interventioninstitution',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.InterventionInstitutionRelationshipType'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='additional_monitoring',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.AdditionalMonitoring'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='administration_route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.AdministrationRoute', verbose_name='Route of administration'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='biosimilar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Biosimilar'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ActiveIngredientCategory'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='device_regulatory_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MedicalDeviceRegulatoryClass'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='dosage_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.DosageForm'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='drug_class',
            field=models.ManyToManyField(blank=True, to='app_helpers.DrugClass'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='intervention_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.InterventionSubtype'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='intervention',
            name='marketing_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.MarketingStatus'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pharmaceutical_alternative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_intervention_related_ph_alt', to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='pharmaceutical_equivalent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_intervention_related_ph_eq', to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='rld',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.RLD', verbose_name='RLD'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.DrugStatus'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='therapeutic_alternative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_intervention_related_th_alt', to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='therapeutic_area',
            field=models.ManyToManyField(blank=True, to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='institutioninstitution',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institutions_related', to='app.Institution'),
        ),
        migrations.AddField(
            model_name='institutioninstitution',
            name='institution_related',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institutions_related_to', to='app.Institution'),
        ),
        migrations.AddField(
            model_name='institutioninstitution',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.InstitutionInstitutionRelationshipType'),
        ),
        migrations.AddField(
            model_name='institution',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Country'),
        ),
        migrations.AddField(
            model_name='institution',
            name='institution_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.InstitutionSubtype'),
        ),
        migrations.AddField(
            model_name='institution',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institution',
            name='locality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Locality'),
        ),
        migrations.AddField(
            model_name='institution',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.CountryState'),
        ),
        migrations.AddField(
            model_name='institution',
            name='therapeutic_area',
            field=models.ManyToManyField(to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='eventinstitution',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Event'),
        ),
        migrations.AddField(
            model_name='eventinstitution',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AddField(
            model_name='eventinstitution',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.EventInstitutionRelationshipType'),
        ),
        migrations.AddField(
            model_name='event',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.Country'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.EventSubtype'),
        ),
        migrations.AddField(
            model_name='event',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.CountryState'),
        ),
        migrations.AddField(
            model_name='event',
            name='therapeutic_area',
            field=models.ManyToManyField(to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='clinicaltrialintervention',
            name='clinical_trial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ClinicalTrial'),
        ),
        migrations.AddField(
            model_name='clinicaltrialintervention',
            name='intervention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Intervention'),
        ),
        migrations.AddField(
            model_name='clinicaltrialintervention',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialInterventionRelationshipType'),
        ),
        migrations.AddField(
            model_name='clinicaltrialinstitution',
            name='clinical_trial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ClinicalTrial'),
        ),
        migrations.AddField(
            model_name='clinicaltrialinstitution',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AddField(
            model_name='clinicaltrialinstitution',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialInstitutionRelationshipType'),
        ),
        migrations.AddField(
            model_name='clinicaltrialactiveingredient',
            name='active_ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ActiveIngredient'),
        ),
        migrations.AddField(
            model_name='clinicaltrialactiveingredient',
            name='clinical_trial',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ClinicalTrial'),
        ),
        migrations.AddField(
            model_name='clinicaltrialactiveingredient',
            name='relationship_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialActiveIngredientRelationshipType'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='age',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialAge'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='allocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialAllocation'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='biospecimen_retention',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialBiospecimenRetention'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='condition',
            field=models.ManyToManyField(blank=True, to='app_helpers.ClinicalTrialCondition'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='endpoint_classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialEndpointClassification'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='enrollment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialEnrollment'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialGender'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='intervention_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialInterventionModel'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='masking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialMasking'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='observational_study_model_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_1', to='app_helpers.ClinicalTrialObservationalStudyModel', verbose_name='Observational Study Model(1)'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='observational_study_model_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_2', to='app_helpers.ClinicalTrialObservationalStudyModel', verbose_name='Observational Study Model(2)'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='primary_purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialPrimaryPurpose'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='recruitment_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialRecruitmentStatus'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='study_arm_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_1', to='app_helpers.ClinicalTrialStudyArmType'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='study_arm_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_2', to='app_helpers.ClinicalTrialStudyArmType'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='study_phases',
            field=models.ManyToManyField(blank=True, to='app_helpers.ClinicalTrialStudyPhase'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='study_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ClinicalTrialStudyType'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='therapeutic_area',
            field=models.ManyToManyField(blank=True, to='app_helpers.TherapeuticArea'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='time_perspective_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_1', to='app_helpers.ClinicalTrialTimePerspective', verbose_name='Time Perspective(1)'),
        ),
        migrations.AddField(
            model_name='clinicaltrial',
            name='time_perspective_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='app_clinicaltrial_related_2', to='app_helpers.ClinicalTrialTimePerspective', verbose_name='Time Perspective(2)'),
        ),
        migrations.AddField(
            model_name='activeingredient',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_helpers.ActiveIngredientCategory'),
        ),
        migrations.AddField(
            model_name='activeingredient',
            name='last_changed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
