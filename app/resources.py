from django.contrib.auth.models import User

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from app_helpers import models as helper_models
from .models import MedicalExpert


class MedicalExpertResource(resources.ModelResource):
    degree = fields.Field(column_name='degree', attribute='degree',
                          widget=ForeignKeyWidget(helper_models.Degree,
                                                  field='name'))
    last_changed_by = fields.Field(column_name='last_changed_by',
                                   attribute='last_changed_by',
                                   widget=ForeignKeyWidget(User,
                                                           field='username'))
    profession = fields.Field(column_name='profession', attribute='profession',
                              widget=ForeignKeyWidget(helper_models.Profession,
                                                      field='name'))
    career_stage = fields.Field(column_name='career_stage',
                                attribute='career_stage',
                                widget=ForeignKeyWidget(
                                    helper_models.CareerStage, field='name'))
    gender = fields.Field(column_name='gender', attribute='gender',
                          widget=ForeignKeyWidget(helper_models.PersonGender,
                                                  field='name'))
    specialties = fields.Field(column_name='specialties',
                               attribute='specialties',
                               widget=ManyToManyWidget(
                                helper_models.MedicalExpertise, separator='|',
                                field='name'))
    therapeutic_areas = fields.Field(column_name='therapeutic_areas',
                                     attribute='therapeutic_areas',
                                     widget=ManyToManyWidget(
                                        helper_models.TherapeuticArea,
                                        separator='|', field='name'))
    country = fields.Field(column_name='country', attribute='country',
                           widget=ForeignKeyWidget(helper_models.Country,
                                                   field='name'))
    combined_name = fields.Field(column_name='combined_name',
                                 attribute='combined_name')

    similar_matches_rules = [
        (['first_name'], 0.7),
        (['last_name'], 0.7),
    ]

    similar_matches_rules_full_match_search = [
        (['last_name'], 0.7),
    ]

    class Meta:
        model = MedicalExpert
        exclude = ('id',)
        import_id_fields = ('oid',)


class MedicalExpertExportResource(MedicalExpertResource):
    combined_name = fields.Field(column_name='combined_name',
                                 attribute='combined_name')

    class Meta:
        export_order = ('oid', 'combined_name', 'degree', 'first_name',
                        'middle_name', 'last_name', 'original_name',
                        'therapeutic_areas', 'specialties',
                        'focus_areas_reasearch_interests', 'profession',
                        'career_stage', 'gender', 'year_of_birth', 'cv',
                        'email', 'photo_url', 'npi_number',
                        'other_id_register_number', 'city', 'country',
                        'justification_1', 'justification_2',
                        'justification_3', 'comment', 'comment_2',
                        'comment_3', 'comment_4', 'last_changed_on',
                        'last_changed_by')
