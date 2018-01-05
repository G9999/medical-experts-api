from app.models_relations import MedicalExpertClinicalTrial, \
                                 MedicalExpertEvent, \
                                 MedicalExpertInstitution, \
                                 MedicalExpertPublication


def medical_expert_connections(medical_expert):
    connections = []

    connections_authors = MedicalExpertPublication.objects. \
        filter(publication__in=MedicalExpertPublication.objects.
               filter(medical_expert=medical_expert).exclude(publication=None).
               values('publication')). \
        exclude(medical_expert=medical_expert).values('medical_expert'). \
        distinct().count()
    if connections_authors > 0:
        connections.append({'connection_type': 'authors',
                            'label': 'Authors',
                            'total': connections_authors})

    connections_event_participants = MedicalExpertEvent.objects. \
        filter(event__in=MedicalExpertEvent.objects.
               filter(medical_expert=medical_expert).exclude(event=None).
               values('event')). \
        exclude(medical_expert=medical_expert).values('medical_expert'). \
        distinct().count()
    if connections_event_participants > 0:
        connections.append({'connection_type': 'event_participants',
                            'label': 'Event Participants',
                            'total': connections_event_participants})

    physicians_institutions_filter = {
        'institution__institution_subtype__name__in':
        ['Hospital', 'Hospital Department', 'Medical Practice'],
        'position__name__in': ['Role Physician', 'Head of'],
    }
    connections_physicians = MedicalExpertInstitution.objects. \
        filter(institution__in=MedicalExpertInstitution.objects.
               filter(medical_expert=medical_expert).exclude(institution=None).
               exclude(institution__institution_subtype=None).
               exclude(position=None).
               filter(**physicians_institutions_filter).
               values('institution')). \
        exclude(medical_expert=medical_expert).count()
    if connections_physicians > 0:
        connections.append({'connection_type': 'physicians',
                            'label': 'Physicians',
                            'total': connections_physicians})

    esearchers_institutions_exclude = {
            'institution__institution_subtype__name__in':
            ['Hospital', 'Hospital Department', 'Medical Practice'],
            'position__name__in': ['Role Physician', 'Head of'],
        }
    connections_researchers = MedicalExpertInstitution.objects. \
        filter(institution__in=MedicalExpertInstitution.objects.
               filter(medical_expert=medical_expert).exclude(institution=None).
               exclude(institution__institution_subtype=None).
               exclude(position=None).
               exclude(**esearchers_institutions_exclude).
               values('institution')). \
        exclude(medical_expert=medical_expert).values('medical_expert'). \
        distinct().count()
    if connections_researchers > 0:
        connections.append({'connection_type': 'researchers',
                            'label': 'Researchers & Co',
                            'total': connections_researchers})

    connections_clinical_trial_collaborators = \
        MedicalExpertClinicalTrial.objects. \
        filter(clinical_trial__in=MedicalExpertClinicalTrial.objects.
               filter(medical_expert=medical_expert).
               exclude(clinical_trial=None).values('clinical_trial').
               distinct()). \
        exclude(medical_expert=medical_expert).values('medical_expert'). \
        distinct().count()
    if connections_clinical_trial_collaborators > 0:
        connections.append({'connection_type': 'clinical_trial_collaborators',
                            'label': 'Investigators',
                            'total': connections_clinical_trial_collaborators})

    return connections


def medical_expert_affiliations(medical_expert):
    institution_categories = {
        'universities': ['University', 'University Department'],
        'hospitals': ['Hospital', 'Hospital Department', 'Medical Practice'],
    }
    affiliations = []

    affiliations_universities_filter = {
        'institution__institution_subtype__name__in':
        institution_categories['universities']
    }
    affiliations_universities = \
        MedicalExpertInstitution.objects. \
        filter(medical_expert=medical_expert).exclude(institution=None). \
        exclude(institution__institution_subtype=None). \
        filter(**affiliations_universities_filter).count()
    affiliations.append({'affiliation_type': 'universities',
                         'total': affiliations_universities})

    affiliations_hospitals_filter = {
        'institution__institution_subtype__name__in':
        institution_categories['hospitals']
    }
    affiliations_hospitals = \
        MedicalExpertInstitution.objects. \
        filter(medical_expert=medical_expert).exclude(institution=None). \
        exclude(institution__institution_subtype=None). \
        filter(**affiliations_hospitals_filter).count()
    affiliations.append({'affiliation_type': 'hospitals',
                         'total': affiliations_hospitals})

    affiliations_associations_exclude = {
        'institution__institution_subtype__name__in':
        institution_categories['universities'] +
        institution_categories['hospitals']
    }
    affiliations_associations = \
        MedicalExpertInstitution.objects. \
        filter(medical_expert=medical_expert).exclude(institution=None). \
        exclude(institution__institution_subtype=None). \
        exclude(**affiliations_associations_exclude).count()
    affiliations.append({'affiliation_type': 'associations',
                         'total': affiliations_associations})

    return affiliations
