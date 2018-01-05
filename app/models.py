from __future__ import unicode_literals
from django.db import models
from app_helpers import models as helper_models
from datetime import datetime


months_list = ['January', 'February', 'March',
               'April', 'May', 'June',
               'July', 'August', 'September',
               'October', 'November', 'December']
MONTHS = zip(months_list, months_list)

years_list = range(1920, datetime.now().year + 1)
YEARS = zip(years_list, years_list)


class ActiveIngredientAbstract(helper_models.OIDModel):
    name = models.CharField(max_length=1024)
    description = models.TextField(max_length=1024, null=True, blank=True)
    category = models.ForeignKey(helper_models.ActiveIngredientCategory,
                                 models.SET_NULL, null=True)
    weblink = models.CharField(max_length=512)
    comment = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True

    main_fields = ('name',)


class ActiveIngredient(ActiveIngredientAbstract):
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class InterventionAbstract(helper_models.OIDModel):
    intervention_subtype = models.ForeignKey(
        helper_models.InterventionSubtype, models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    weblink = models.CharField(max_length=512, null=True, blank=True)
    # drug fields
    inn_common_name = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='Internat. non-proprietary (INN)/common name')
    active_substance = models.TextField(max_length=200, null=True, blank=True)
    therapeutic_area = models.ManyToManyField(helper_models.TherapeuticArea,
                                              blank=True)
    drug_class = models.ManyToManyField(helper_models.DrugClass, blank=True)
    agency_product_number = models.CharField(max_length=512, null=True,
                                             blank=True)
    status = models.ForeignKey(helper_models.DrugStatus, models.SET_NULL,
                               blank=True, null=True)
    marketing_status = models.ForeignKey(helper_models.MarketingStatus,
                                         models.SET_NULL, blank=True,
                                         null=True)
    application_number = models.CharField(max_length=10, null=True,
                                          blank=True)
    administration_route = models.ForeignKey(
        helper_models.AdministrationRoute, models.SET_NULL,
        verbose_name='Route of administration', blank=True, null=True)
    dosage_form = models.ForeignKey(helper_models.DosageForm, models.SET_NULL,
                                    blank=True, null=True)
    strength = models.CharField(max_length=200, null=True, blank=True)
    atc_number = models.CharField(max_length=10, verbose_name='ATC Code',
                                  blank=True, null=True)
    ndc_code = models.CharField(max_length=12, verbose_name='NDC Code',
                                blank=True, null=True)
    te_code = models.CharField(max_length=20, null=True, blank=True,
                               verbose_name='TE code')
    anda_number = models.CharField(max_length=10, null=True, blank=True,
                                   verbose_name='ANDA number')
    patent_number = models.CharField(max_length=20, null=True, blank=True)
    additional_monitoring = models.ForeignKey(
        helper_models.AdditionalMonitoring, models.SET_NULL, blank=True,
        null=True)
    rld = models.ForeignKey(helper_models.RLD, models.SET_NULL, blank=True,
                            null=True, verbose_name='RLD')
    biosimilar = models.ForeignKey(helper_models.Biosimilar, models.SET_NULL,
                                   blank=True, null=True)
    is_orphan = models.BooleanField(default=False)
    is_generic = models.BooleanField(default=False)
    pharmaceutical_equivalent = models.ForeignKey(
        'self', related_name='%(app_label)s_%(class)s_related_ph_eq',
        blank=True, null=True)
    pharmaceutical_alternative = models.ForeignKey(
        'self', related_name='%(app_label)s_%(class)s_related_ph_alt',
        blank=True, null=True)
    therapeutic_alternative = models.ForeignKey(
        'self', related_name='%(app_label)s_%(class)s_related_th_alt',
        blank=True, null=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    # active ingredient fields
    description = models.TextField(max_length=512, null=True, blank=True)
    category = models.ForeignKey(helper_models.ActiveIngredientCategory,
                                 models.SET_NULL, null=True, blank=True)
    # medical device fields
    product_code = models.CharField(max_length=200, null=True, blank=True)
    gmdn_preferred_term_name = models.CharField(
        max_length=200, verbose_name='GMDN Preferred Term Name', null=True,
        blank=True)
    regulation_number = models.CharField(max_length=200, null=True, blank=True)
    issuing_agency = models.CharField(max_length=200, null=True, blank=True)
    device_regulatory_class = models.ForeignKey(
        helper_models.MedicalDeviceRegulatoryClass, models.SET_NULL, null=True,
        blank=True)
    life_sustain_support_device = models.BooleanField(
        default=False, verbose_name='Life-Sustain/Support Device')
    prescription_use_rx = models.BooleanField(
        default=False, verbose_name='Prescription Use (Rx)')
    for_single_use = models.BooleanField(default=False)
    implantable_device = models.BooleanField(default=False)
    over_the_counter_otc = models.BooleanField(
        default=False, verbose_name='Over the Counter (OTC)')

    class Meta:
        abstract = True

    main_fields = ('name', 'active_substance', 'administration_route',
                   'dosage_form')


class Intervention(InterventionAbstract):
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialAbstract(helper_models.OIDModel):
    brief_public_title = models.CharField(max_length=1024,
                                          verbose_name='Brief (Public) Title',
                                          null=True)
    official_scientific_title = models.CharField(
        max_length=1024, verbose_name='Official (Scientific) Title', null=True,
        blank=True)
    therapeutic_area = models.ManyToManyField(helper_models.TherapeuticArea,
                                              blank=True)
    condition = models.ManyToManyField(helper_models.ClinicalTrialCondition,
                                       blank=True)
    start_date_day = models.IntegerField(blank=True, null=True)
    start_date_month = models.CharField(max_length=20, blank=True, null=True)
    start_date_year = models.IntegerField(blank=True, null=True)
    end_date_day = models.IntegerField(blank=True, null=True)
    end_date_month = models.CharField(max_length=20, blank=True, null=True)
    end_date_year = models.IntegerField(blank=True, null=True)
    ct_id_in_main_source = models.CharField(
        max_length=1024, null=True, blank=True,
        verbose_name='CT ID in Main Source')
    other_study_id_numbers = models.CharField(max_length=1024, null=True,
                                              blank=True)
    study_type = models.ForeignKey(helper_models.ClinicalTrialStudyType,
                                   models.SET_NULL, null=True, blank=True)
    intervention = models.TextField(max_length=512, null=True, blank=True)
    conditions_diseases = models.TextField(max_length=1024, null=True,
                                           blank=True,
                                           verbose_name='Conditions/Diseases')
    primary_purpose = models.ForeignKey(
        helper_models.ClinicalTrialPrimaryPurpose, models.SET_NULL, null=True,
        blank=True)
    endpoint_classification = models.ForeignKey(
        helper_models.ClinicalTrialEndpointClassification, models.SET_NULL,
        null=True, blank=True)
    intervention_model = models.ForeignKey(
        helper_models.ClinicalTrialInterventionModel, models.SET_NULL,
        null=True, blank=True)
    masking = models.ForeignKey(helper_models.ClinicalTrialMasking,
                                models.SET_NULL, null=True, blank=True)
    allocation = models.ForeignKey(helper_models.ClinicalTrialAllocation,
                                   models.SET_NULL, null=True, blank=True)
    enrollment = models.ForeignKey(helper_models.ClinicalTrialEnrollment,
                                   models.SET_NULL, null=True, blank=True)
    observational_study_model_1 = models.ForeignKey(
        helper_models.ClinicalTrialObservationalStudyModel, models.SET_NULL,
        verbose_name='Observational Study Model(1)', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_related_1')
    time_perspective_1 = models.ForeignKey(
        helper_models.ClinicalTrialTimePerspective, models.SET_NULL,
        verbose_name='Time Perspective(1)', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_related_1')
    observational_study_model_2 = models.ForeignKey(
        helper_models.ClinicalTrialObservationalStudyModel, models.SET_NULL,
        verbose_name='Observational Study Model(2)', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_related_2')
    time_perspective_2 = models.ForeignKey(
        helper_models.ClinicalTrialTimePerspective, models.SET_NULL,
        verbose_name='Time Perspective(2)', null=True, blank=True,
        related_name='%(app_label)s_%(class)s_related_2')
    target_follow_up_duration = models.CharField(
        max_length=512, null=True, blank=True,
        verbose_name='Target Follow-Up Duration')
    biospecimen_retention = models.ForeignKey(
        helper_models.ClinicalTrialBiospecimenRetention, models.SET_NULL,
        null=True, blank=True)
    number_groups_cohorts = models.CharField(
        max_length=512, null=True, blank=True,
        verbose_name='Number of Groups/Cohorts')
    study_arm_1 = models.ForeignKey(
        helper_models.ClinicalTrialStudyArmType, models.SET_NULL, null=True,
        blank=True, related_name='%(app_label)s_%(class)s_related_1')
    comment_study_arm_1 = models.CharField(max_length=512, null=True,
                                           blank=True)
    study_arm_2 = models.ForeignKey(
        helper_models.ClinicalTrialStudyArmType, models.SET_NULL, null=True,
        blank=True, related_name='%(app_label)s_%(class)s_related_2')
    comment_study_arm_2 = models.CharField(max_length=512, null=True,
                                           blank=True)
    study_phases = models.ManyToManyField(
        helper_models.ClinicalTrialStudyPhase, blank=True)
    brief_summary = models.TextField(max_length=1024, null=True, blank=True)
    recruitment_status = models.ForeignKey(
        helper_models.ClinicalTrialRecruitmentStatus, models.SET_NULL,
        null=True, blank=True)
    estimated_enrollment = models.CharField(max_length=1024, null=True,
                                            blank=True)
    gender = models.ForeignKey(helper_models.ClinicalTrialGender,
                               models.SET_NULL, null=True, blank=True)
    age = models.ForeignKey(helper_models.ClinicalTrialAge, models.SET_NULL,
                            null=True, blank=True)
    maximum_age = models.CharField(max_length=200, null=True, blank=True)
    minimum_age = models.CharField(max_length=200, null=True, blank=True)
    accepts_healthy_volunteers = models.BooleanField(default=False, blank=True)
    has_data_monitoring_commitee = models.BooleanField(default=False,
                                                       blank=True)
    acronym = models.CharField(max_length=1024, blank=True, null=True)
    main_source_database = models.CharField(max_length=1024, blank=True,
                                            null=True)
    comment = models.TextField(max_length=512, null=True, blank=True)
    comment_2 = models.TextField(max_length=512, null=True, blank=True)
    weblink = models.CharField(max_length=512, null=True, blank=True)

    number_linked_medical_experts = models.PositiveIntegerField(
        default=0, verbose_name='ME')
    number_linked_interventions = models.PositiveIntegerField(
        default=0, verbose_name='Interv')
    number_linked_institutions = models.PositiveIntegerField(
        default=0, verbose_name='Inst')

    class Meta:
        abstract = True

    main_fields = ('brief_public_title', 'ct_id_in_main_source',
                   'other_study_id_numbers', 'condition')


class ClinicalTrial(ClinicalTrialAbstract):
    class Meta:
        ordering = ('brief_public_title',)

    @property
    def prop_conditions(self):
        return ", ".join(
            [condition.name for condition in self.condition.all()])

    @property
    def prop_study_phases(self):
        return ", ".join(
            [study_phase.name for study_phase in self.study_phases.all()])

    def __unicode__(self):
        clinical_trial_unicode = u'%s' % self.brief_public_title
        if len(clinical_trial_unicode) > 50:
            clinical_trial_unicode = u'%s...' % clinical_trial_unicode[:50]
        return clinical_trial_unicode

    def update_number_linked_medical_experts(self):
        number_linked_medical_experts = \
            self.medicalexpertclinicaltrial_set.count()
        if self.number_linked_medical_experts != number_linked_medical_experts:
            self.number_linked_medical_experts = number_linked_medical_experts
            self.save(update_fields=['number_linked_medical_experts'])

    def update_number_linked_interventions(self):
        number_linked_interventions = \
            self.clinicaltrialintervention_set.count()
        if self.number_linked_interventions != number_linked_interventions:
            self.number_linked_interventions = number_linked_interventions
            self.save(update_fields=['number_linked_interventions'])

    def update_number_linked_institutions(self):
        number_linked_institutions = \
            self.clinicaltrialinstitution_set.count()
        if self.number_linked_institutions != number_linked_institutions:
            self.number_linked_institutions = number_linked_institutions
            self.save(update_fields=['number_linked_institutions'])


class InstitutionAbstract(helper_models.OIDModel):
    hospital_university = models.CharField(
        max_length=512, null=True, blank=True,
        verbose_name='Hospital/University/Etc')
    abbreviation = models.CharField(max_length=100, blank=True, null=True)
    original_other_name = models.CharField(max_length=512, null=True,
                                           blank=True,
                                           verbose_name='Orig./Other Name')
    healthcare_network_trust = models.CharField(
        max_length=512, null=True, blank=True,
        verbose_name='Healthcare Network/Trust')
    campus_location = models.CharField(max_length=512, null=True, blank=True,
                                       verbose_name='Campus/Location')
    school = models.CharField(max_length=512, null=True, blank=True)
    department = models.CharField(max_length=512, null=True, blank=True)
    division = models.CharField(max_length=512, null=True, blank=True)
    institution_subtype = models.ForeignKey(
        helper_models.InstitutionSubtype, models.SET_NULL, null=True)
    locality = models.ForeignKey(helper_models.Locality, models.SET_NULL,
                                 null=True)
    therapeutic_area = models.ManyToManyField(helper_models.TherapeuticArea)
    board_member_team_list = models.TextField(
        max_length=1024, null=True, blank=True,
        verbose_name='Board Member/Team List')
    street_and_number = models.CharField(max_length=1024, null=True,
                                         blank=True)
    postal_code = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.ForeignKey(
        helper_models.CountryState, models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(helper_models.Country, models.SET_NULL,
                                null=True, blank=True)
    phone_country_code = models.CharField(
        max_length=100, null=True, verbose_name='Phone Country Code')
    phone_city_code = models.IntegerField(
        null=True, verbose_name='Phone City Code')
    phone_number = models.BigIntegerField(null=True,
                                          verbose_name='Phone Number')
    email = models.CharField(max_length=512, null=True, blank=True)
    weblink = models.CharField(max_length=1024)
    weblink_bm_team_list = models.CharField(
        max_length=512, null=True, blank=True,
        verbose_name='Weblink (BM/Team List)')
    comment = models.CharField(max_length=512, null=True, blank=True)
    comment_2 = models.CharField(max_length=512, null=True, blank=True)
    comment_3 = models.CharField(max_length=512, null=True, blank=True)

    number_linked_medical_experts = models.PositiveIntegerField(
        default=0, verbose_name='ME')
    number_linked_medical_experts_coi = models.PositiveIntegerField(
        default=0, verbose_name='CoI')
    number_linked_institutions = models.PositiveIntegerField(
        default=0, verbose_name='Inst')

    class Meta:
        abstract = True

    main_fields = ('hospital_university', 'department', 'division',
                   'institution_subtype', 'city', 'country')


class Institution(InstitutionAbstract):
    def phone(self):
        if self.phone_country_code or self.phone_city_code \
           or self.phone_number:
            return '%s %s %s' % (self.phone_country_code or '',
                                 self.phone_city_code or '',
                                 self.phone_number or '')
        return None

    class Meta:
        ordering = ('hospital_university',)

    def combined_name(self):
        combined_name = u''
        if self.healthcare_network_trust and self.hospital_university:
            combined_name += u'%s - %s' % (self.healthcare_network_trust,
                                           self.hospital_university)
        elif self.healthcare_network_trust:
            combined_name += u'%s' % self.healthcare_network_trust
        elif self.hospital_university:
            combined_name += u'%s' % self.hospital_university

        if self.department or self.division:
            combined_name += u', '
            if self.department and self.division:
                combined_name += u'%s - %s' % (self.department, self.division)
            elif self.department:
                combined_name += u'%s' % self.department
            else:
                combined_name += u'%s' % self.division
        return combined_name

    def __unicode__(self):
        institution_unicode = u'%s' % (self.combined_name()) or str(self.pk)
        if len(institution_unicode) > 50:
            institution_unicode = u'%s...' % institution_unicode[:50]
        return institution_unicode

    def update_number_linked_medical_experts(self):
        number_linked_medical_experts = \
            self.medicalexpertinstitution_set.count()
        if self.number_linked_medical_experts != number_linked_medical_experts:
            self.number_linked_medical_experts = number_linked_medical_experts
            self.save(update_fields=['number_linked_medical_experts'])

    def update_number_linked_medical_experts_coi(self):
        number_linked_medical_experts_coi = \
            self.medicalexpertinstitutioncoi_set.count()
        if self.number_linked_medical_experts_coi != \
           number_linked_medical_experts_coi:
            self.number_linked_medical_experts_coi = \
                number_linked_medical_experts_coi
            self.save(update_fields=['number_linked_medical_experts_coi'])

    def update_number_linked_institutions(self):
        number_linked_institutions = \
            self.institutions_related.count()
        if self.number_linked_institutions != number_linked_institutions:
            self.number_linked_institutions = number_linked_institutions
            self.save(update_fields=['number_linked_institutions'])


class MedicalExpertAbstract(helper_models.OIDModel):
    degree = models.ForeignKey(helper_models.Degree, models.SET_NULL,
                               null=True)
    first_name = models.CharField(max_length=1024)
    middle_name = models.CharField(max_length=1024,
                                   null=True, blank=True)
    last_name = models.CharField(max_length=1024)
    original_name = models.CharField(max_length=1024, null=True, blank=True)
    specialties = models.ManyToManyField(
        helper_models.MedicalExpertise,
        related_name='%(app_label)s_%(class)s_related', blank=True)
    therapeutic_areas = models.ManyToManyField(
        helper_models.TherapeuticArea,
        related_name='%(app_label)s_%(class)s_related', blank=True)
    focus_areas_reasearch_interests = models.CharField(
        max_length=1024, null=True, blank=True,
        verbose_name='Focus Area/Research Interests')
    profession = models.ForeignKey(helper_models.Profession, models.SET_NULL,
                                   null=True)
    career_stage = models.ForeignKey(helper_models.CareerStage,
                                     models.SET_NULL, null=True, blank=True)
    gender = models.ForeignKey(helper_models.PersonGender, models.SET_NULL,
                               null=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    cv = models.CharField(max_length=1024, null=True, blank=True)
    email = models.CharField(max_length=512, null=True, blank=True)
    photo_url = models.URLField(max_length=512, null=True, blank=True)
    npi_number = models.CharField(max_length=300, null=True, blank=True,
                                  verbose_name='NPI Number')
    other_id_register_number = models.CharField(
        max_length=300, null=True, blank=True,
        verbose_name='Other ID/Register Number')
    comment = models.CharField(max_length=512, null=True, blank=True)
    comment_2 = models.CharField(max_length=512, null=True, blank=True)
    comment_3 = models.CharField(max_length=512, null=True, blank=True)
    comment_4 = models.CharField(max_length=512, null=True, blank=True)

    source_id = models.CharField(max_length=200, null=True, blank=True,
                                 verbose_name='Source ID')
    source = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(helper_models.Country, models.SET_NULL,
                                null=True, blank=True)
    justification_1 = models.CharField(max_length=512, null=True, blank=True)
    justification_2 = models.CharField(max_length=512, null=True, blank=True)
    justification_3 = models.CharField(max_length=512, null=True, blank=True)

    number_linked_clinical_trials = models.PositiveIntegerField(
        default=0, verbose_name='CT')
    number_linked_institutions = models.PositiveIntegerField(
        default=0, verbose_name='Inst')
    number_linked_institutions_primary_affiliation = \
        models.PositiveIntegerField(default=0, verbose_name='Inst*')
    number_linked_institutions_subtype_company = \
        models.PositiveIntegerField(default=0, verbose_name='C')
    number_linked_institutions_coi = \
        models.PositiveIntegerField(default=0, verbose_name='CoI')
    number_linked_events = models.PositiveIntegerField(
        default=0, verbose_name='E')
    number_linked_publications = models.PositiveIntegerField(
        default=0, verbose_name='P')

    class Meta:
        abstract = True

    main_fields = ('first_name', 'middle_name', 'last_name', 'original name',
                   'specialties', 'city', 'country')


class MedicalExpert(MedicalExpertAbstract):
    class Meta:
        ordering = ('first_name', 'last_name')

    def __unicode__(self):
        if self.middle_name:
            return u'%s %s %s' % (self.first_name, self.middle_name,
                                  self.last_name)
        else:
            return u'%s %s' % (self.first_name, self.last_name)

    def combined_name(self):
        if self.middle_name:
            return u'%s %s %s' % (self.first_name, self.middle_name,
                                  self.last_name)
        else:
            return u'%s %s' % (self.first_name, self.last_name)

    @property
    def prop_combined_name(self):
        return self.combined_name()

    @property
    def prop_therapeutic_areas(self):
        return ", ".join([area.name for area in self.therapeutic_areas.all()])

    @property
    def prop_specialties(self):
        return ', '.join(
            [specialty.name for specialty in self.specialties.all()])

    @property
    def country_name(self):
        return self.country.name if self.country else ''

    def update_number_linked_clinical_trials(self):
        number_linked_clinical_trials = \
            self.medicalexpertclinicaltrial_set.count()
        if self.number_linked_clinical_trials != number_linked_clinical_trials:
            self.number_linked_clinical_trials = number_linked_clinical_trials
            self.save(update_fields=['number_linked_clinical_trials'])

    def update_number_linked_institutions(self):
        # all linked institutions
        number_linked_institutions = \
            self.medicalexpertinstitution_set.count()
        if self.number_linked_institutions != number_linked_institutions:
            self.number_linked_institutions = number_linked_institutions
            self.save(update_fields=['number_linked_institutions'])
        # linked institutions with primary_affiliation = True
        number_linked_institutions_primary_affiliation = \
            self.medicalexpertinstitution_set.filter(
                primary_affiliation=True).count()
        if self.number_linked_institutions_primary_affiliation != \
                number_linked_institutions_primary_affiliation:
            self.number_linked_institutions_primary_affiliation = \
                number_linked_institutions_primary_affiliation
            self.save(update_fields=[
                'number_linked_institutions_primary_affiliation'])
        # linked institutions with institution_subtype = 'Company'
        number_linked_institutions_subtype_company = \
            self.medicalexpertinstitution_set.filter(
                institution__institution_subtype__name='Company').count()
        if self.number_linked_institutions_subtype_company != \
                number_linked_institutions_subtype_company:
            self.number_linked_institutions_subtype_company = \
                number_linked_institutions_subtype_company
            self.save(update_fields=[
                'number_linked_institutions_subtype_company'])

    def update_number_linked_institutions_coi(self):
        number_linked_institutions_coi = \
            self.medicalexpertinstitutioncoi_set.count()
        if self.number_linked_institutions_coi != \
                number_linked_institutions_coi:
            self.number_linked_institutions_coi = \
                number_linked_institutions_coi
            self.save(update_fields=[
                'number_linked_institutions_coi'])

    def update_number_linked_events(self):
        number_linked_events = \
            self.medicalexpertevent_set.count()
        if self.number_linked_events != number_linked_events:
            self.number_linked_events = number_linked_events
            self.save(update_fields=['number_linked_events'])

    def update_number_linked_publications(self):
        number_linked_publications = \
            self.medicalexpertpublication_set.count()
        if self.number_linked_publications != number_linked_publications:
            self.number_linked_publications = number_linked_publications
            self.save(update_fields=['number_linked_publications'])

    def affiliation_name(self):
        affiliation = self.medicalexpertinstitution_set.filter(
            primary_affiliation=True).exclude(institution=None). \
            order_by('pk').first()
        if affiliation:
            return affiliation.institution.combined_name()
        return ''

    def is_unlocked_investigator(self, user):
        if user:
            try:
                if user.unlockedinvestigator_set.filter(investigator=self). \
                   count():
                    return True
            except:
                pass
        return False

    def is_favorite_investigator(self, user):
        if user:
            try:
                if user.favoriteinvestigator_set.filter(investigator=self). \
                   count():
                    return True
            except:
                pass
        return False


class PublicationAbstract(helper_models.OIDModel):
    name = models.CharField(max_length=1024)
    original_name = models.CharField(max_length=1024, null=True, blank=True)
    publication_subtype = models.ForeignKey(helper_models.PublicationSubtype,
                                            models.SET_NULL, null=True)
    therapeutic_area = models.ManyToManyField(helper_models.TherapeuticArea)
    primary_source_id = models.CharField(max_length=1024, blank=True,
                                         null=True,
                                         verbose_name='Primary Source ID')
    publication_month = models.CharField(max_length=20, choices=MONTHS,
                                         null=True, blank=True)
    publication_year = models.IntegerField(choices=YEARS, null=True,
                                           blank=True)
    journal = models.CharField(max_length=512, null=True, blank=True)
    weblink = models.CharField(max_length=512)
    comment = models.CharField(max_length=512, null=True, blank=True)
    authors_list = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True

    main_fields = ('name', 'primary_source_id', 'publication_subtype',
                   'publication_year')


class Publication(PublicationAbstract):
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        publication_unicode = u'%s' % self.name
        if len(publication_unicode) > 50:
            publication_unicode = u'%s...' % publication_unicode[:50]
        return publication_unicode


class EventAbstract(helper_models.OIDModel):
    name = models.CharField(max_length=1024)
    original_name = models.CharField(max_length=1024, null=True, blank=True)
    event_subtype = models.ForeignKey(helper_models.EventSubtype,
                                      models.SET_NULL, null=True)
    therapeutic_area = models.ManyToManyField(helper_models.TherapeuticArea)
    city = models.CharField(max_length=1024, null=True)
    state = models.ForeignKey(
        helper_models.CountryState, models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(helper_models.Country, models.SET_NULL,
                                null=True)
    start_date_day = models.IntegerField(blank=True, null=True)
    start_date_month = models.CharField(max_length=20, blank=True, null=True)
    start_date_year = models.IntegerField(blank=True, null=True)
    end_date_day = models.IntegerField(blank=True, null=True)
    end_date_month = models.CharField(max_length=20, blank=True, null=True)
    end_date_year = models.IntegerField(blank=True, null=True)
    weblink = models.CharField(max_length=512)
    comment = models.CharField(max_length=512, null=True, blank=True)
    program = models.TextField(max_length=1024, null=True, blank=True)
    program_weblink = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True

    main_fields = ('name', 'event_subtype', 'start_date_year')


class Event(EventAbstract):
    class Meta:
        ordering = ('start_date_year', 'start_date_month', 'start_date_day')

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalDeviceAbstract(helper_models.OIDModel):
    product_code = models.CharField(max_length=200)
    device_name = models.CharField(max_length=200)
    gmdn_preferred_term_name = models.CharField(
        max_length=200, verbose_name='GMDN Preferred Term Name')
    regulation_number = models.CharField(max_length=200)
    issuing_agency = models.CharField(max_length=200)
    device_regulatory_class = models.ForeignKey(
        helper_models.MedicalDeviceRegulatoryClass, models.SET_NULL, null=True)
    life_sustain_support_device = models.BooleanField(
        default=False, verbose_name='Life-Sustain/Support Device')
    prescription_use_rx = models.BooleanField(
        default=False, verbose_name='Prescription Use (Rx)')
    for_single_use = models.BooleanField(default=False)
    implantable_device = models.BooleanField(default=False)
    over_the_counter_otc = models.BooleanField(
        default=False, verbose_name='Over the Counter (OTC)')
    weblink = models.CharField(max_length=512, null=True, blank=True)
    comment = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True


class MedicalDevice(MedicalDeviceAbstract):
    class Meta:
        ordering = ('product_code', 'device_name')

    def __unicode__(self):
        return u'%s' % (self.device_name)
