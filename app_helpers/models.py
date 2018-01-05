from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from project.settings import APP_OID_PREFIX

User = settings.AUTH_USER_MODEL


class OIDModel(models.Model):
    oid = models.CharField(max_length=30, blank=True, null=True,
                           verbose_name='Object ID', default='')
    last_changed_on = models.DateTimeField(auto_now=True, null=True)
    last_changed_by = models.ForeignKey(User, models.SET_NULL, blank=True,
                                        null=True)
    check_status = models.BooleanField(default=False, blank=True)

    @classmethod
    def get_model_prefix(cls):
        upper_letters = ''.join([c for c in cls.__name__ if c.isupper()])
        return upper_letters.lower()

    @staticmethod
    def format_oid(instance_id, model_prefix):
        formatted_oid = str(instance_id).zfill(9)
        formatted_oid = formatted_oid[:3] + '-' + formatted_oid[3:]
        formatted_oid = '{}-{}-{}'.format(APP_OID_PREFIX, model_prefix,
                                          formatted_oid)
        return formatted_oid

    def save(self, *args, **kwargs):
        save_oid = False
        if not self.oid and not self.id:
            save_oid = True

        super(OIDModel, self).save(*args, **kwargs)

        if save_oid:
            model_prefix = self.__class__.get_model_prefix()
            self.oid = self.__class__.format_oid(self.id, model_prefix)
            # remove force_insert kwarg in case the objet was already created
            if kwargs.get('force_insert', False):
                kwargs.pop('force_insert')
            super(OIDModel, self).save(*args, **kwargs)

    class Meta():
        abstract = True


class ActiveIngredientCategory(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Active Ingredient categories'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class TherapeuticArea(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class InterventionSubtype(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class DrugStatus(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Drug statuses'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class DrugClass(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Drug classes'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MarketingStatus(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Marketing statuses'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class DosageForm(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class AdministrationRoute(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class AdditionalMonitoring(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Currency(OIDModel):
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=100)

    class Meta:
        ordering = ('code',)
        verbose_name_plural = "Currencies"

    def __unicode__(self):
        return u'%s' % (self.code)


class Country(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return u'%s' % (self.name)


class CountryState(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class InstitutionSubtype(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Locality(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Localities'

    def __unicode__(self):
        return u'%s' % (self.name)


class RelationshipType(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertise(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class FocusAreaResearchInterest(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Focus Area / Research Interest'
        verbose_name_plural = 'Focus Areas / Research Interests'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Profession(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class CareerStage(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialCondition(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialStudyType(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialStudyPhase(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialAllocation(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialEnrollment(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialObservationalStudyModel(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialEndpointClassification(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialInterventionModel(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialTimePerspective(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialBiospecimenRetention(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialMasking(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialPrimaryPurpose(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialStudyArmType(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialRecruitmentStatus(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Clinical trial recruitment statuses'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialAge(OIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Degree(OIDModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class RLD(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'RLD'
        verbose_name_plural = 'RLDs'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class Biosimilar(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class PublicationSubtype(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class EventSubtype(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class PersonGender(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialGender(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertInstitutionPosition(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertInstitutionNatureOfPayment(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertInstitutionFormOfPayment(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertClinicalTrialPosition(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertPublicationPosition(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class MedicalExpertEventPosition(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % (self.name)


class ClinicalTrialInstitutionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class ClinicalTrialInterventionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class ClinicalTrialActiveIngredientRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class EventInstitutionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class InterventionInstitutionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class PublicationClinicalTrialRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class MedicalDeviceRegulatoryClass(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)
        verbose_name_plural = 'Medical device regulatory classes'

    def __unicode__(self):
        return u'%s' % self.name


class InstitutionInstitutionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name


class InterventionInterventionRelationshipType(OIDModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('id', 'name',)

    def __unicode__(self):
        return u'%s' % self.name
