from django.db import models
from models import ActiveIngredient, ClinicalTrial, Event, Institution, \
                   Intervention, MedicalExpert, Publication
from app_helpers import models as helper_models


class MedicalExpertInstitutionAbstract(models.Model):
    institution = models.ForeignKey(Institution, null=True)
    medical_expert = models.ForeignKey(MedicalExpert, null=True)
    position = models.ForeignKey(
        helper_models.MedicalExpertInstitutionPosition, models.SET_NULL,
        default=1, null=True)
    primary_affiliation = models.BooleanField()
    past_position = models.BooleanField(default=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    weblink = models.TextField()
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

    unique_together_reference = (('institution', 'medical_expert'),)


class MedicalExpertInstitutionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        medical_experts = []
        institutions = []
        for obj in self:
            medical_expert = obj.medical_expert
            institution = obj.institution
            if medical_expert and medical_expert not in medical_experts:
                medical_experts.append(medical_expert)
            if institution and institution not in institutions:
                institutions.append(institution)
        super(MedicalExpertInstitutionQuerySet, self).delete(*args, **kwargs)
        for medical_expert in medical_experts:
            medical_expert.update_number_linked_institutions()
        for institution in institutions:
            institution.update_number_linked_medical_experts()


class MedicalExpertInstitution(MedicalExpertInstitutionAbstract):
    objects = MedicalExpertInstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = 'Medical Expert - Institution'
        verbose_name_plural = 'Medical Experts - Institutions'

    def prop_institution_oid(self):
        return self.institution.oid
    prop_institution_oid.short_description = 'Institution OID'

    def prop_institution_subtype(self):
        return self.institution.institution_subtype
    prop_institution_subtype.short_description = 'Institution Subtype'

    def prop_institution_country(self):
        return self.institution.country
    prop_institution_country.short_description = 'Institution Country'

    def prop_institution_hospital_university(self):
        return self.institution.hospital_university
    prop_institution_hospital_university.short_description = \
        'Institution Hospital/University/Etc'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(MedicalExpertInstitution, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.medical_expert:
                self.medical_expert.update_number_linked_institutions()
            if self.institution:
                self.institution.update_number_linked_medical_experts()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        medical_expert = self.medical_expert
        institution = self.institution
        super(MedicalExpertInstitution, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if medical_expert:
                medical_expert.update_number_linked_institutions()
            if institution:
                institution.update_number_linked_medical_experts()


class MedicalExpertInstitutionCOIAbstract(models.Model):
    institution = models.ForeignKey(Institution, null=True)
    medical_expert = models.ForeignKey(MedicalExpert, null=True)
    nature_of_payment = models.ForeignKey(
        helper_models.MedicalExpertInstitutionNatureOfPayment, models.SET_NULL,
        null=True)
    year = models.CharField(max_length=20)
    weblink = models.URLField()
    ct_id = models.CharField(max_length=255, null=True, blank=True)
    form_of_payment = models.ForeignKey(
        helper_models.MedicalExpertInstitutionFormOfPayment, models.SET_NULL,
        null=True, blank=True)
    name_d_b_md_ms = models.CharField(max_length=255, null=True, blank=True,
                                      verbose_name='Name of D/B/MD/MS')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    currency = models.ForeignKey(helper_models.Currency, models.SET_NULL,
                                 null=True, blank=True)

    class Meta:
        abstract = True

    unique_together_reference = (('institution', 'medical_expert'),)


class MedicalExpertInstitutionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        medical_experts = []
        institutions = []
        for obj in self:
            medical_expert = obj.medical_expert
            institution = obj.institution
            if medical_expert and medical_expert not in medical_experts:
                medical_experts.append(medical_expert)
            if institution and institution not in institutions:
                institutions.append(institution)
        super(MedicalExpertInstitutionQuerySet, self).delete(*args, **kwargs)
        for medical_expert in medical_experts:
            medical_expert.update_number_linked_institutions()
        for institution in institutions:
            institution.update_number_linked_medical_experts()


class MedicalExpertInstitutionCOI(MedicalExpertInstitutionCOIAbstract):
    objects = MedicalExpertInstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = 'Medical Expert - Institution (COI)'
        verbose_name_plural = 'Medical Experts - Institutions (COI)'

    def prop_institution_oid(self):
        return self.institution.oid
    prop_institution_oid.short_description = 'Institution OID'

    def prop_institution_subtype(self):
        return self.institution.institution_subtype
    prop_institution_subtype.short_description = 'Institution Subtype'

    def prop_institution_country(self):
        return self.institution.country
    prop_institution_country.short_description = 'Institution Country'

    def prop_institution_hospital_university(self):
        return self.institution.hospital_university
    prop_institution_hospital_university.short_description = \
        'Institution Hospital/University/Etc'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(MedicalExpertInstitutionCOI, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.medical_expert:
                self.medical_expert.update_number_linked_institutions_coi()
            if self.institution:
                self.institution.update_number_linked_medical_experts_coi()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        medical_expert = self.medical_expert
        institution = self.institution
        super(MedicalExpertInstitutionCOI, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if medical_expert:
                medical_expert.update_number_linked_institutions_coi()
            if institution:
                institution.update_number_linked_medical_experts_coi()


class MedicalExpertClinicalTrialAbstract(models.Model):
    clinical_trial = models.ForeignKey(ClinicalTrial, null=True)
    medical_expert = models.ForeignKey(MedicalExpert, null=True)
    position = models.ForeignKey(
        helper_models.MedicalExpertClinicalTrialPosition,
        models.SET_NULL, null=True)
    weblink = models.TextField()
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

    unique_together_reference = (('clinical_trial', 'medical_expert'),)


class MedicalExpertClinicalTrialQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        medical_experts = []
        clinical_trials = []
        for obj in self:
            medical_expert = obj.medical_expert
            clinical_trial = obj.clinical_trial
            if medical_expert and medical_expert not in medical_experts:
                medical_experts.append(medical_expert)
            if clinical_trial and clinical_trial not in clinical_trials:
                clinical_trials.append(clinical_trial)
        super(MedicalExpertClinicalTrialQuerySet, self).delete(*args, **kwargs)
        for medical_expert in medical_experts:
            medical_expert.update_number_linked_clinical_trials()
        for clinical_trial in clinical_trials:
            clinical_trial.update_number_linked_medical_experts()


class MedicalExpertClinicalTrial(MedicalExpertClinicalTrialAbstract):
    objects = MedicalExpertClinicalTrialQuerySet.as_manager()

    class Meta:
        verbose_name = 'Medical Expert - Clinical Trial'
        verbose_name_plural = 'Medical Experts - Clinical Trials'

    def prop_clinical_trial_oid(self):
        return self.clinical_trial.oid
    prop_clinical_trial_oid.short_description = 'CT OID'

    def prop_clinical_trial_ct_id_in_main_source(self):
        return self.clinical_trial.ct_id_in_main_source
    prop_clinical_trial_ct_id_in_main_source.short_description \
        = 'CT ID in Main Source'

    def prop_clinical_trial_condition(self):
        return ', '.join([condition.name for condition in
                          self.clinical_trial.condition.all()])
    prop_clinical_trial_condition.short_description = 'CT Condition'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(MedicalExpertClinicalTrial, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.medical_expert:
                self.medical_expert.update_number_linked_clinical_trials()
            if self.clinical_trial:
                self.clinical_trial.update_number_linked_medical_experts()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        medical_expert = self.medical_expert
        clinical_trial = self.clinical_trial
        super(MedicalExpertClinicalTrial, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if medical_expert:
                medical_expert.update_number_linked_clinical_trials()
            if clinical_trial:
                clinical_trial.update_number_linked_medical_experts()


class MedicalExpertPublicationAbstract(models.Model):
    publication = models.ForeignKey(Publication, null=True)
    medical_expert = models.ForeignKey(MedicalExpert, null=True)
    position = models.ForeignKey(
        helper_models.MedicalExpertPublicationPosition, models.SET_NULL,
        null=True)
    weblink = models.TextField()
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

    unique_together_reference = (('publication', 'medical_expert'),)


class MedicalExpertPublicationQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        medical_experts = []
        for obj in self:
            medical_expert = obj.medical_expert
            if medical_expert and medical_expert not in medical_experts:
                medical_experts.append(medical_expert)
        super(MedicalExpertPublicationQuerySet, self).delete(*args, **kwargs)
        for medical_expert in medical_experts:
            medical_expert.update_number_linked_publications()


class MedicalExpertPublication(MedicalExpertPublicationAbstract):
    objects = MedicalExpertPublicationQuerySet.as_manager()

    class Meta:
        verbose_name = 'Medical Expert - Publication'
        verbose_name_plural = 'Medical Experts - Publications'

    def prop_publication_oid(self):
        return self.publication.oid
    prop_publication_oid.short_description = 'Publication OID'

    def prop_publication_name(self):
        return self.publication.name
    prop_publication_name.short_description = 'Publication Name'

    def prop_publication_subtype(self):
        return self.publication.publication_subtype
    prop_publication_subtype.short_description = 'Publication Subtype'

    def prop_publication_year(self):
        return self.publication.publication_year
    prop_publication_year.short_description = 'Publication Year'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(MedicalExpertPublication, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.medical_expert:
                self.medical_expert.update_number_linked_publications()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        medical_expert = self.medical_expert
        super(MedicalExpertPublication, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if medical_expert:
                medical_expert.update_number_linked_publications()


class MedicalExpertEventAbstract(models.Model):
    event = models.ForeignKey(Event, null=True)
    medical_expert = models.ForeignKey(MedicalExpert, null=True)
    position = models.ForeignKey(helper_models.MedicalExpertEventPosition,
                                 models.SET_NULL, null=True)
    talks = models.TextField(null=True, blank=True)
    sessions = models.TextField(null=True, blank=True)
    posters = models.TextField(null=True, blank=True)
    weblink = models.TextField()
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        abstract = True

    unique_together_reference = (('event', 'medical_expert'),)


class MedicalExpertEventQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        medical_experts = []
        for obj in self:
            medical_expert = obj.medical_expert
            if medical_expert and medical_expert not in medical_experts:
                medical_experts.append(medical_expert)
        super(MedicalExpertEventQuerySet, self).delete(*args, **kwargs)
        for medical_expert in medical_experts:
            medical_expert.update_number_linked_events()


class MedicalExpertEvent(MedicalExpertEventAbstract):
    objects = MedicalExpertEventQuerySet.as_manager()

    class Meta:
        verbose_name = 'Medical Expert - Event'
        verbose_name_plural = 'Medical Experts - Events'

    def prop_event_oid(self):
        return self.event.oid
    prop_event_oid.short_description = 'Event OID'

    def prop_event_name(self):
        return self.event.name
    prop_event_name.short_description = 'Event Name'

    def prop_event_subtype(self):
        return self.event.event_subtype
    prop_event_subtype.short_description = 'Event Subtype'

    def prop_event_country(self):
        return self.event.country
    prop_event_country.short_description = 'Event Country'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(MedicalExpertEvent, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.medical_expert:
                self.medical_expert.update_number_linked_events()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        medical_expert = self.medical_expert
        super(MedicalExpertEvent, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if medical_expert:
                medical_expert.update_number_linked_events()


class ClinicalTrialInstitutionAbstract(models.Model):
    clinical_trial = models.ForeignKey(ClinicalTrial, null=True)
    institution = models.ForeignKey(Institution, null=True)
    relationship_type = models.ForeignKey(
        helper_models.ClinicalTrialInstitutionRelationshipType,
        models.SET_NULL, null=True)

    class Meta:
        abstract = True

    unique_together_reference = (('clinical_trial', 'institution'),)


class ClinicalTrialInstitutionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        clinical_trials = []
        for obj in self:
            clinical_trial = obj.clinical_trial
            if clinical_trial and clinical_trial not in clinical_trials:
                clinical_trials.append(clinical_trial)
        super(ClinicalTrialInstitutionQuerySet, self).delete(*args, **kwargs)
        for clinical_trial in clinical_trials:
            clinical_trial.update_number_linked_institutions()


class ClinicalTrialInstitution(ClinicalTrialInstitutionAbstract):
    objects = ClinicalTrialInstitutionQuerySet.as_manager()

    class Meta:
        verbose_name = 'Clinical Trial - Institution'
        verbose_name_plural = 'Clinical Trials - Institutions'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(ClinicalTrialInstitution, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.clinical_trial:
                self.clinical_trial.update_number_linked_institutions()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        clinical_trial = self.clinical_trial
        super(ClinicalTrialInstitution, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if clinical_trial:
                clinical_trial.update_number_linked_institutions()


class ClinicalTrialInterventionAbstract(models.Model):
    clinical_trial = models.ForeignKey(ClinicalTrial, null=True)
    intervention = models.ForeignKey(Intervention, null=True)
    relationship_type = models.ForeignKey(
        helper_models.ClinicalTrialInterventionRelationshipType,
        models.SET_NULL,
        null=True)

    class Meta:
        abstract = True

    unique_together_reference = (('clinical_trial', 'intervention'),)


class ClinicalTrialInterventionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        clinical_trials = []
        for obj in self:
            clinical_trial = obj.clinical_trial
            if clinical_trial and clinical_trial not in clinical_trials:
                clinical_trials.append(clinical_trial)
        super(ClinicalTrialInterventionQuerySet, self).delete(*args, **kwargs)
        for clinical_trial in clinical_trials:
            clinical_trial.update_number_linked_interventions()


class ClinicalTrialIntervention(ClinicalTrialInterventionAbstract):
    objects = ClinicalTrialInterventionQuerySet.as_manager()

    class Meta:
        verbose_name = 'Clinical Trial - Intervention'
        verbose_name_plural = 'Clinical Trials - Interventions'

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(ClinicalTrialIntervention, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.clinical_trial:
                self.clinical_trial.update_number_linked_interventions()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        clinical_trial = self.clinical_trial
        super(ClinicalTrialIntervention, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if clinical_trial:
                clinical_trial.update_number_linked_interventions()


class ClinicalTrialActiveIngredient(models.Model):
    clinical_trial = models.ForeignKey(ClinicalTrial, null=True)
    active_ingredient = models.ForeignKey(ActiveIngredient, null=True)
    relationship_type = models.ForeignKey(
        helper_models.ClinicalTrialActiveIngredientRelationshipType,
        models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Clinical Trial - Active Ingredient'
        verbose_name_plural = 'Clinical Trials - Active Ingredients'

    unique_together_reference = (('clinical_trial', 'active_ingredient'),)

    def save(self, *args, **kwargs):
        # prevent error if "ignore_update_related" kwarg is sent
        kwargs.pop('ignore_update_related', False)
        super(ClinicalTrialActiveIngredient, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # prevent error if "ignore_update_related" kwarg is sent
        kwargs.pop('ignore_update_related', False)
        super(ClinicalTrialActiveIngredient, self).delete(*args, **kwargs)


class EventInstitution(models.Model):
    event = models.ForeignKey(Event, null=True)
    institution = models.ForeignKey(Institution, null=True)
    relationship_type = models.ForeignKey(
        helper_models.EventInstitutionRelationshipType, models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = 'Event - Institution'
        verbose_name_plural = 'Events - Institutions'

    unique_together_reference = (('event', 'institution'),)


class InterventionInstitutionAbstract(models.Model):
    intervention = models.ForeignKey(Intervention, null=True)
    institution = models.ForeignKey(Institution, null=True)
    relationship_type = models.ForeignKey(
        helper_models.InterventionInstitutionRelationshipType, models.SET_NULL,
        null=True)

    class Meta:
        abstract = True

    unique_together_reference = (('intervention', 'institution'),)


class InterventionInstitution(InterventionInstitutionAbstract):
    class Meta:
        verbose_name = 'Intervention - Institution'
        verbose_name_plural = 'Interventions - Institutions'


class InterventionIntervention(models.Model):
    intervention = models.ForeignKey(Intervention, null=True,
                                     related_name='interventions_related')
    intervention_related = models.ForeignKey(
        Intervention, null=True, related_name='interventions_related_to')
    relationship_type = models.ForeignKey(
        helper_models.InterventionInterventionRelationshipType,
        models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Intervention - Intervention'
        verbose_name_plural = 'Interventions - Interventions'

    unique_together_reference = (('intervention', 'intervention_related'),)


class PublicationClinicalTrial(models.Model):
    publication = models.ForeignKey(Publication, null=True)
    clinical_trial = models.ForeignKey(ClinicalTrial, null=True)
    relationship_type = models.ForeignKey(
        helper_models.PublicationClinicalTrialRelationshipType,
        models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Publication - Clinical Trial'
        verbose_name_plural = 'Publications - Clinical Trials'

    unique_together_reference = (('publication', 'clinical_trial'),)

    def save(self, *args, **kwargs):
        # prevent error if "ignore_update_related" kwarg is sent
        kwargs.pop('ignore_update_related', False)
        super(PublicationClinicalTrial, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # prevent error if "ignore_update_related" kwarg is sent
        kwargs.pop('ignore_update_related', False)
        super(PublicationClinicalTrial, self).delete(*args, **kwargs)


class InstitutionInstitutionQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        institutions = []
        for obj in self:
            institution = obj.institution
            if institution and institution not in institutions:
                institutions.append(institution)
        super(InstitutionInstitutionQuerySet, self).delete(*args, **kwargs)
        for institution in institutions:
            institution.update_number_linked_institutions()


class InstitutionInstitution(models.Model):
    objects = InstitutionInstitutionQuerySet.as_manager()

    institution = models.ForeignKey(Institution, null=True,
                                    related_name='institutions_related')
    institution_related = models.ForeignKey(
        Institution, null=True, related_name='institutions_related_to')
    relationship_type = models.ForeignKey(
        helper_models.InstitutionInstitutionRelationshipType, models.SET_NULL,
        null=True)

    class Meta:
        verbose_name = 'Institution - Institution'
        verbose_name_plural = 'Institutions - Institutions'

    unique_together_reference = (('institution', 'institution_related'),)

    def save(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        super(InstitutionInstitution, self).save(*args, **kwargs)
        if not ignore_update_related:
            if self.institution:
                self.institution.update_number_linked_institutions()

    def delete(self, *args, **kwargs):
        ignore_update_related = kwargs.pop('ignore_update_related', False)
        institution = self.institution
        super(InstitutionInstitution, self).delete(*args, **kwargs)
        if not ignore_update_related:
            if institution:
                institution.update_number_linked_institutions()
