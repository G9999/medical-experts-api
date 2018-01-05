from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from app.models import MedicalExpert
from app_helpers import models as helper_models

User = settings.AUTH_USER_MODEL


class FavoriteInvestigator(models.Model):
    user = models.ForeignKey(User)
    investigator = models.ForeignKey(MedicalExpert)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'investigator'),)


class UnlockedInvestigator(models.Model):
    user = models.ForeignKey(User)
    investigator = models.ForeignKey(MedicalExpert)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'investigator'),)


class Request(models.Model):
    REQUEST_TYPE_FAVORITES_BASE_DATA = 'favorites_base_data'
    REQUEST_TYPE_FAVORITES_FULL_PROFILE = 'favorites_full_profile'
    REQUEST_TYPE_AUTHORS = 'authors'
    REQUEST_TYPE_MARKET_ACCESS = 'market_access'
    REQUEST_TYPE_COMPANY_COOPERATION = 'company_cooperation'
    REQUEST_TYPE_OTHER = 'other'

    REQUEST_TYPE_CHOICES = (
        (REQUEST_TYPE_FAVORITES_BASE_DATA, 'My favorites (Base Data)'),
        (REQUEST_TYPE_FAVORITES_FULL_PROFILE, 'My favorites (Full Profile)'),
        (REQUEST_TYPE_AUTHORS, 'Authors'),
        (REQUEST_TYPE_MARKET_ACCESS, 'Market Access'),
        (REQUEST_TYPE_COMPANY_COOPERATION, 'Company Cooperation'),
        (REQUEST_TYPE_OTHER, 'Other'),
    )

    REQUEST_STATUS_PENDING = 'pending'
    REQUEST_STATUS_SENT = 'sent'
    REQUEST_STATUS_COMPLETED = 'completed'
    REQUEST_STATUS_DELETED = 'deleted'

    REQUEST_STATUS_CHOICES = (
        (REQUEST_STATUS_PENDING, 'Pending'),
        (REQUEST_STATUS_SENT, 'Sent'),
        (REQUEST_STATUS_COMPLETED, 'Completed'),
        (REQUEST_STATUS_DELETED, 'Deleted'),
    )

    user = models.ForeignKey(User)
    request_type = models.CharField(max_length=25,
                                    choices=REQUEST_TYPE_CHOICES)
    request_file = models.FileField(upload_to='requests', null=True,
                                    blank=True)
    favorites = models.BooleanField()
    added = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES,
                              default=REQUEST_STATUS_PENDING)

    @property
    def added_date(self):
        return self.added.date()

    @property
    def sent_date(self):
        if self.sent:
            return self.sent.date()
        return 'Pending'

    @property
    def details(self):
        details_text = ''
        if self.request_type == self.REQUEST_TYPE_FAVORITES_BASE_DATA:
            details_text = 'Base Data'
        elif self.request_type == self.REQUEST_TYPE_FAVORITES_FULL_PROFILE:
            details_text = 'Full Profile'
        elif self.request_type == self.REQUEST_TYPE_AUTHORS:
            request = AuthorsRequest.objects.get(pk=self.pk)
            details_text = 'From: %s To: %s<br />' \
                           'Type of Publication of Interest: %s<br />' \
                           'Topic of Interest: %s<br />' \
                           'Countries of Interest: %s<br />' \
                           'Other Comments: %s' % \
                           (request.year_from, request.year_to,
                            ', '.join(type_publication_interest.name for
                                      type_publication_interest in
                                      request.types_publication_interest.
                                      all()),
                            request.topic_interest,
                            ', '.join(country_interest.name for
                                      country_interest in
                                      request.countries_interest.all()),
                            request.other_comments)
        elif self.request_type == self.REQUEST_TYPE_MARKET_ACCESS:
            request = MarketAccessRequest.objects.get(pk=self.pk)
            details_text = 'Topic of Interest: %s<br />' \
                           'Countries of Interest: %s<br />' \
                           'Other Comments: %s' % \
                           (request.topic_interest,
                            ', '.join(country_interest.name for
                                      country_interest in
                                      request.countries_interest.all()),
                            request.other_comments)
        elif self.request_type == self.REQUEST_TYPE_COMPANY_COOPERATION:
            request = CompanyCooperationRequest.objects.get(pk=self.pk)
            details_text = 'Companies of Interest: %s<br />' \
                           'Drugs / Medical Devices of Interest: %s<br />' \
                           'Other Comments: %s' % \
                           (request.companies_interest,
                            request.drugs_medical_devices_interest,
                            request.other_comments)
        elif self.request_type == self.REQUEST_TYPE_OTHER:
            request = OtherRequest.objects.get(pk=self.pk)
            details_text = 'Description: %s' % \
                           (request.description)
        return [
            {"details_text": details_text}
        ]


class FavoritesBaseDataRequest(Request):
    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_FAVORITES_BASE_DATA
        self.request_file = None
        self.favorites = True
        super(FavoritesBaseDataRequest, self).save(*args, **kwargs)


class FavoritesFullProfileRequest(Request):
    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_FAVORITES_FULL_PROFILE
        self.request_file = None
        self.favorites = True
        super(FavoritesFullProfileRequest, self).save(*args, **kwargs)


class AuthorsRequest(Request):
    year_from = models.PositiveSmallIntegerField()
    year_to = models.PositiveSmallIntegerField()
    types_publication_interest = models.ManyToManyField(
        helper_models.PublicationSubtype)
    topic_interest = models.TextField()
    countries_interest = models.ManyToManyField(
        helper_models.Country)
    other_comments = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_AUTHORS
        super(AuthorsRequest, self).save(*args, **kwargs)


class MarketAccessRequest(Request):
    topic_interest = models.TextField()
    countries_interest = models.ManyToManyField(
        helper_models.Country)
    other_comments = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_MARKET_ACCESS
        super(MarketAccessRequest, self).save(*args, **kwargs)


class CompanyCooperationRequest(Request):
    companies_interest = models.TextField()
    drugs_medical_devices_interest = models.TextField()
    other_comments = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_COMPANY_COOPERATION
        super(CompanyCooperationRequest, self).save(*args, **kwargs)


class OtherRequest(Request):
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.request_type = self.REQUEST_TYPE_OTHER
        super(OtherRequest, self).save(*args, **kwargs)
