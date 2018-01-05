import re

from django.contrib.auth import get_user_model, views
from django.core.files import File
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse


from rest_framework import status

from ..forms import AuthorsRequestForm, CompanyCooperationRequestForm, \
                    InvestigatorFeedbackForm, MarketAccessRequestForm, \
                    OtherRequestForm
from ..models import AuthorsRequest, CompanyCooperationRequest, \
                     FavoritesBaseDataRequest, FavoritesFullProfileRequest, \
                     FavoriteInvestigator, MarketAccessRequest, OtherRequest, \
                     Request, UnlockedInvestigator
from ..views import AuthorsView, CompanyCooperationView, InvestigatorView, \
                    InvestigatorsView, MarketAccessView, \
                    MyFavoriteInvestigatorsView, MyRequestsView, OtherView, \
                    SpeakersView
from app.models import Institution, MedicalExpert
from app.models_relations import MedicalExpertInstitution
from app_helpers.models import Country, MedicalExpertInstitutionPosition, \
                               PublicationSubtype

User = get_user_model()


def remove_csrf_tag(text):
    """Remove csrf tag from TEXT"""
    return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)


class LoginPageTest(TestCase):
    def setUp(self):
        # Add subscription user
        self.user = User.objects.create_user(
            username='user1234', password='demo1234', subscription=True)
        # Add non subscription user
        self.user_non_subscription = User.objects.create_user(
            username='user0000', password='demo0000')

    def test_login_url_resolves_to_login_view(self):
        found = resolve('/login/')
        self.assertEqual(found.func, views.login)

    def test_login_page_returns_correct_html(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')

    def test_sucessful_login_renders_landing_page(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'landing.html', context={
                'user': user, 'subscription': True,
                'action_url': reverse('investigators')}
        )
        self.assertEqual(response.render().content.decode(), expected_html)

    def test_sucessful_login_renders_landing_page_non_subscription_user(self):
        self.client.login(username='user0000', password='demo0000')
        response = self.client.get('/', follow=True)
        expected_html = render_to_string(
            'landing.html', context={
                'user': self.user_non_subscription, 'subscription': False,
                'action_url': reverse('my_favorite_investigators')}
        )
        self.assertEqual(response.render().content.decode(), expected_html)


class InvestigatorsPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add subscription user
        self.user = User.objects.create_user(
            username='user1234', password='demo1234', subscription=True)
        # Add non subscription user
        User.objects.create_user(username='user0000', password='demo0000')

    def test_investigators_page_url_resolves_to_investigators_view(self):
        found = resolve('/investigators/')
        self.assertEqual(found.func.__name__,
                         InvestigatorsView.as_view().__name__)

    def test_investigators_page_redirects_unauthenticated_user(self):
        response = self.client.get('/investigators/')
        self.assertRedirects(response, '/login/?next=/investigators/')

    def test_investigators_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/investigators/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'investigators.html', context={'user': user,
                                           'dummy_id': '000-000000'}
        )
        self.assertEqual(response.render().content.decode(), expected_html)

    def test_investigators_page_returns_403_logged_user_non_subscription(self):
        self.client.login(username='user0000', password='demo0000')
        response = self.client.get('/investigators/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InvestigatorPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(
            username='user1234', password='demo1234', subscription=True)
        # Add non subscription user
        User.objects.create_user(username='user0000', password='demo0000')

        # Add ME's
        self.investigator_1 = MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last', number_linked_clinical_trials=2)
        self.investigator_1_oid = self.investigator_1.oid.replace('think-me-',
                                                                  '')
        investigator_2 = MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last')
        self.investigator_2_oid = investigator_2.oid.replace('think-me-', '')
        self.investigator_3 = MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last', number_linked_clinical_trials=1)
        self.investigator_3_oid = self.investigator_3.oid.replace('think-me-',
                                                                  '')
        investigator_4 = MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_clinical_trials=2)
        self.investigator_4_oid = investigator_4.oid.replace('think-me-', '')

        UnlockedInvestigator.objects.create(user=self.user,
                                            investigator=self.investigator_1)
        UnlockedInvestigator.objects.create(user=self.user,
                                            investigator=self.investigator_3)

        # Add institutions and ME-I relations
        institution_1 = Institution.objects.create(
            hospital_university='Hospital 1',
            healthcare_network_trust='Healthcare 1',
            department='Department 1', division='Division 1',
            phone_country_code='000', phone_city_code=11,
            phone_number=222222, email='email1@domain.com')
        position_1 = MedicalExpertInstitutionPosition.objects.create(
            name='Position 1')

        MedicalExpertInstitution.objects.create(
            medical_expert=self.investigator_1, institution=institution_1,
            primary_affiliation=True, position=position_1)

    def test_investigators_url_resolves_to_investigators_view(self):
        investigator_1_oid = self.investigator_1.oid.replace('think-me-', '')
        found = resolve('/investigator/%s/' % investigator_1_oid)
        self.assertEqual(found.func.__name__,
                         InvestigatorView.as_view().__name__)

    def test_investigator_page_redirects_unauthenticated_user(self):
        response = self.client.get(
            '/investigator/%s/' % self.investigator_1_oid)
        self.assertRedirects(
            response,
            '/login/?next=/investigator/%s/' % self.investigator_1_oid)

    def test_investigator_page_returns_correct_html_authenticated_user_valid_1(
         self):
        # check investigator with existing affiliation
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get(
            '/investigator/%s/' % self.investigator_1_oid, follow=True)
        user = self.user
        expected_html = render_to_string(
            'investigator.html',
            context={
                'user': user,
                'object': self.investigator_1,
                'feedback_form': InvestigatorFeedbackForm(),
                'affiliation': {
                    'combined_name':
                    'Healthcare 1 - Hospital 1, Department 1 - Division 1',
                    'phone': '000 11 222222',
                    'position': 'Position 1',
                    'email': 'email1@domain.com',
                },
                'object_oid': self.investigator_1_oid,
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_investigator_page_returns_correct_html_authenticated_user_valid_2(
         self):
        # check investigator without existing affiliation
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get(
            '/investigator/%s/' % self.investigator_3_oid, follow=True)
        user = self.user
        request = HttpRequest()
        request.user = self.user
        request.method = 'GET'
        expected_html = render_to_string(
            'investigator.html',
            context={
                'user': user,
                'object': self.investigator_3,
                'feedback_form': InvestigatorFeedbackForm(),
                'affiliation': {
                    'combined_name': 'To be defined',
                    'phone': 'To be defined',
                    'position': 'To be defined',
                    'email': 'To be defined',
                },
                'object_oid': self.investigator_3_oid,
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_investigator_page_zero_clinical_trials_events(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get(
            '/investigator/%s/' % self.investigator_2_oid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_investigator_page_authenticated_user_locked(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get(
            '/investigator/%s/' % self.investigator_4_oid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_investigator_page_authenticated_user_unexisting(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/investigator/000-000000/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_submit_feedback_investigator_authenticated(self):
        # Authenticated user post an investigator feedback message
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('investigator_submit_feedback',
                    kwargs={'oid': self.investigator_1_oid}),
            data={'message': 'This is a test message'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_submit_feedback_investigator_unauthenticated(self):
        # Non authenticated user tries to post an investigator feedback message
        response = self.client.post(
            reverse('investigator_submit_feedback',
                    kwargs={'oid': self.investigator_1_oid}),
            data={'message': 'This is a test message'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FavoriteInvestigatorTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user_1 = User.objects.create_user(username='user1234',
                                               password='demo1234')
        self.user_2 = User.objects.create_user(username='user5678',
                                               password='demo5678')

        # Add ME's
        self.investigator_1 = MedicalExpert.objects.create(
            first_name='First_first', middle_name='First_middle',
            last_name='First_last', number_linked_clinical_trials=2)
        self.investigator_1_oid = self.investigator_1.oid.replace('think-me-',
                                                                  '')
        self.investigator_2 = MedicalExpert.objects.create(
            first_name='Second_first', middle_name='Second_middle',
            last_name='Second_last', number_linked_clinical_trials=1)
        self.investigator_2_oid = self.investigator_2.oid.replace('think-me-',
                                                                  '')
        self.investigator_3 = MedicalExpert.objects.create(
            first_name='Third_first', middle_name='Third_middle',
            last_name='Third_last')
        self.investigator_3_oid = self.investigator_3.oid.replace('think-me-',
                                                                  '')
        self.investigator_4 = MedicalExpert.objects.create(
            first_name='Fourth_first', middle_name='Fourth_middle',
            last_name='Fourth_last', number_linked_clinical_trials=3)
        self.investigator_4_oid = self.investigator_4.oid.replace('think-me-',
                                                                  '')
        FavoriteInvestigator.objects.create(user=self.user_1,
                                            investigator=self.investigator_2)
        FavoriteInvestigator.objects.create(user=self.user_2,
                                            investigator=self.investigator_3)

    def test_add_favorite_investigator_authenticated(self):
        # Authenticated user add a favorite investigator
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('investigator_add_favorite',
                    kwargs={'oid': self.investigator_1_oid}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorite = FavoriteInvestigator.objects. \
            filter(user=self.user_1, investigator=self.investigator_1).first()
        self.assertEqual(type(favorite), FavoriteInvestigator)

    def test_add_favorite_investigator_zero_clinical_trials_events(self):
        # Authenticated user add a favorite investigator
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('investigator_add_favorite',
                    kwargs={'oid': self.investigator_3_oid}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_favorite_investigator_unauthenticated(self):
        # Non authenticated user tries to add a favorite investigator
        response = self.client.post(
            reverse('investigator_add_favorite',
                    kwargs={'oid': self.investigator_1_oid}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_favorite_investigator_authenticated(self):
        # Authenticated user remove a favorite investigator
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('investigator_remove_favorite',
                    kwargs={'oid': self.investigator_2_oid}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorite = FavoriteInvestigator.objects. \
            filter(user=self.user_1, investigator=self.investigator_2).first()
        self.assertEqual(favorite, None)

    def test_add_favorite_investigators_authenticated(self):
        # Authenticated user add a favorite investigator
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('add_favorite_investigators'),
            data={'oids[]': [self.investigator_1_oid,
                             self.investigator_4_oid]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorite_count = FavoriteInvestigator.objects. \
            filter(user=self.user_1, investigator__in=[self.investigator_1,
                                                       self.investigator_4]). \
            count()
        self.assertEqual(favorite_count, 2)

    def test_remove_favorite_investigators_authenticated(self):
        # Authenticated user removes a favorite investigator
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('remove_favorite_investigators'),
            data={'oids[]': [self.investigator_1_oid, self.investigator_2_oid,
                             self.investigator_4_oid]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorite_count = FavoriteInvestigator.objects. \
            filter(user=self.user_1,
                   investigator__in=[self.investigator_1, self.investigator_2,
                                     self.investigator_4]).count()
        self.assertEqual(favorite_count, 0)

    def test_submit_favorites_base_data_request_authenticated(self):
        # Authenticated user post Favorites Base Data request
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('submit_favorites_base_data_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_BASE_DATA,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_favorites_base_data_request_unauthenticated(self):
        # Non authenticated user try to post Favorites Base Data request
        response = self.client.post(
            reverse('submit_favorites_base_data_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_BASE_DATA,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)

    def test_submit_favorites_base_data_request_zero_favorites(self):
        """
        User with no valid favorites tries to post Favorites Base Data request
        """
        self.client.login(username='user5678', password='demo5678')
        response = self.client.post(
            reverse('submit_favorites_base_data_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_BASE_DATA,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)

    def test_submit_favorites_full_profile_request_authenticated(self):
        # Authenticated user post Favorites Base Data request
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('submit_favorites_full_profile_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_FULL_PROFILE,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_favorites_full_profile_request_unauthenticated(self):
        # Non authenticated user try to post Favorites Base Data request
        response = self.client.post(
            reverse('submit_favorites_full_profile_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_FULL_PROFILE,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)

    def test_submit_favorites_full_profile_request_zero_favorites(self):
        """
        User with no valid favorites tries to post Favorites Base Data request
        """
        self.client.login(username='user5678', password='demo5678')
        response = self.client.post(
            reverse('submit_favorites_full_profile_request'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        request = Request.objects.filter(
            user=self.user_1,
            request_type=Request.REQUEST_TYPE_FAVORITES_FULL_PROFILE,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)

    def test_favorites_download_authenticated(self):
        # Authenticated user post Download favorites request
        self.client.login(username='user1234', password='demo1234')
        response = self.client.post(
            reverse('my_favorite_investigators'),
            data={'action': 'download'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("content-type"),
                         'application/vnd.openxmlformats-'
                         'officedocument.spreadsheetml.sheet')

    def test_favorites_download_unauthenticated(self):
        # Non authenticated user try to post Download favorites request
        response = self.client.post(
            reverse('my_favorite_investigators'),
            data={'action': 'download'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_favorites_download_zero_favorites(self):
        """
        User with no valid favorites tries to post Download favorites request
        """
        self.client.login(username='user5678', password='demo5678')
        response = self.client.post(
            reverse('my_favorite_investigators'),
            data={'action': 'download'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MyFavoriteInvestigatorsPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

    def test_my_favorites_page_url_resolves_to_investigators_view(self):
        found = resolve('/my-favorites/')
        self.assertEqual(found.func.__name__,
                         MyFavoriteInvestigatorsView.as_view().__name__)

    def test_my_favorites_page_redirects_unauthenticated_user(self):
        response = self.client.get('/my-favorites/')
        self.assertRedirects(response, '/login/?next=/my-favorites/')

    def test_my_favorites_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/my-favorites/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'my_favorite_investigators.html', context={
                'user': user, 'dummy_id': '000-000000'
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))


class AuthorsPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

        self.country_1 = Country.objects.create(name='United States')
        self.country_2 = Country.objects.create(name='Austria')
        self.publication_subtype_1 = PublicationSubtype.objects.create(
            name='Publication Type 1')
        self.publication_subtype_2 = PublicationSubtype.objects.create(
            name='Publication Type 2')

    def test_authors_page_url_resolves_to_investigators_view(self):
        found = resolve('/authors/')
        self.assertEqual(found.func.__name__,
                         AuthorsView.as_view().__name__)

    def test_authors_page_redirects_unauthenticated_user(self):
        response = self.client.get('/authors/')
        self.assertRedirects(response, '/login/?next=/authors/')

    def test_authors_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/authors/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'authors.html', context={
                'user': user,
                'form': AuthorsRequestForm(user=self.user),
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_submit_request_authenticated(self):
        # Authenticated user post a request
        self.client.login(username='user1234', password='demo1234')
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('authors'), data={
                'year_from': 2016,
                'year_to': 2017,
                'types_publication_interest': [self.publication_subtype_1.pk,
                                               self.publication_subtype_2.pk],
                'topic_interest': 'This is a test message',
                'countries_interest': [self.country_1.pk,
                                       self.country_2.pk],
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_AUTHORS,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_request_unauthenticated(self):
        # Non authenticated user tries to post a request
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('authors'), data={
                'year_from': 2016,
                'year_to': 2017,
                'types_publication_interest': [self.publication_subtype_1.pk,
                                               self.publication_subtype_2.pk],
                'topic_interest': 'This is a test message',
                'countries_interest': [self.country_1.pk,
                                       self.country_2.pk],
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_AUTHORS,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)


class MarketAccessPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

        self.country_1 = Country.objects.create(name='United States')
        self.country_2 = Country.objects.create(name='Austria')

    def test_market_access_page_url_resolves_to_investigators_view(self):
        found = resolve('/market-access/')
        self.assertEqual(found.func.__name__,
                         MarketAccessView.as_view().__name__)

    def test_market_access_page_redirects_unauthenticated_user(self):
        response = self.client.get('/market-access/')
        self.assertRedirects(response, '/login/?next=/market-access/')

    def test_market_access_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/market-access/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'market_access.html', context={
                'user': user,
                'form': MarketAccessRequestForm(user=self.user),
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_submit_request_authenticated(self):
        # Authenticated user post a request
        self.client.login(username='user1234', password='demo1234')
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('market_access'), data={
                'topic_interest': 'This is a test message',
                'countries_interest': [self.country_1.pk,
                                       self.country_2.pk],
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_MARKET_ACCESS,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_request_unauthenticated(self):
        # Non authenticated user tries to post a request
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('market_access'), data={
                'topic_interest': 'This is a test message',
                'countries_interest': [self.country_1.pk,
                                       self.country_2.pk],
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_MARKET_ACCESS,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)


class CompanyCooperationPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

    def test_company_cooperation_page_url_resolves_to_investigators_view(self):
        found = resolve('/company-cooperation/')
        self.assertEqual(found.func.__name__,
                         CompanyCooperationView.as_view().__name__)

    def test_company_cooperation_page_redirects_unauthenticated_user(self):
        response = self.client.get('/company-cooperation/')
        self.assertRedirects(response, '/login/?next=/company-cooperation/')

    def test_company_cooperation_page_returns_correct_html_authenticated_user(
            self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/company-cooperation/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'company_cooperation.html', context={
                'user': user,
                'form': CompanyCooperationRequestForm(user=self.user),
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_submit_request_authenticated(self):
        # Authenticated user post a request
        self.client.login(username='user1234', password='demo1234')
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('company_cooperation'), data={
                'companies_interest': 'This is a test companies message',
                'drugs_medical_devices_interest':
                'This is a test drugs message',
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_COMPANY_COOPERATION,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_request_unauthenticated(self):
        # Non authenticated user tries to post a request
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('company_cooperation'), data={
                'companies_interest': 'This is a test companies message',
                'drugs_medical_devices_interest':
                'This is a test drugs message',
                'other_comments': 'This is a test comment',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_COMPANY_COOPERATION,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)


class OtherPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')

    def test_other_page_url_resolves_to_investigators_view(self):
        found = resolve('/other/')
        self.assertEqual(found.func.__name__,
                         OtherView.as_view().__name__)

    def test_other_page_redirects_unauthenticated_user(self):
        response = self.client.get('/other/')
        self.assertRedirects(response, '/login/?next=/other/')

    def test_other_page_returns_correct_html_authenticated_user(
            self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/other/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'other.html', context={
                'user': user,
                'form': OtherRequestForm(user=self.user),
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_submit_request_authenticated(self):
        # Authenticated user post a request
        self.client.login(username='user1234', password='demo1234')
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('other'), data={
                'description': 'This is a test description message',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_OTHER,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(type(request), Request)

    def test_submit_request_unauthenticated(self):
        # Non authenticated user tries to post a request
        response = None
        with open('dummy_file.xlsx') as dummy_file:
            response = self.client.post(reverse('other'), data={
                'description': 'This is a test description message',
                'request_file': dummy_file,
                'favorites': False,
            })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        request = Request.objects.filter(
            user=self.user,
            request_type=Request.REQUEST_TYPE_OTHER,
            status=Request.REQUEST_STATUS_PENDING).first()
        self.assertEqual(request, None)


class MyRequestsPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(username='user1234',
                                             password='demo1234')
        # Add requests
        publication_subtype_1 = PublicationSubtype.objects.create(
            name='Publication Type 1')
        publication_subtype_2 = PublicationSubtype.objects.create(
            name='Publication Type 2')
        country_1 = Country.objects.create(name='United States')
        country_2 = Country.objects.create(name='Austria')
        request_file = open('dummy_file.xlsx')
        self.request_1 = FavoritesBaseDataRequest.objects.create(
            user=self.user)
        self.request_2 = FavoritesFullProfileRequest.objects.create(
            user=self.user)
        self.request_3 = AuthorsRequest.objects.create(
            user=self.user, year_from=2015, year_to=2016,
            topic_interest='This is a dummy topic message',
            other_comments='This is a dummy comments message', favorites=True)
        self.request_3.types_publication_interest.add(publication_subtype_1)
        self.request_3.types_publication_interest.add(publication_subtype_2)
        self.request_3.countries_interest.add(country_1)
        self.request_3.countries_interest.add(country_2)
        self.request_4 = MarketAccessRequest.objects.create(
            user=self.user, topic_interest='This is a dummy topic message',
            other_comments='This is a dummy comments message',
            favorites=False)
        self.request_4.request_file.save('dummy_file.xlsx', File(request_file))
        self.request_4.countries_interest.add(country_1)
        self.request_5 = CompanyCooperationRequest.objects.create(
            user=self.user, favorites=True)
        self.request_6 = OtherRequest.objects.create(user=self.user,
                                                     favorites=False)
        self.request_6.request_file.save('dummy_file.xlsx', File(request_file))

    def test_my_requests_page_url_resolves_to_investigators_view(self):
        found = resolve('/my-requests/')
        self.assertEqual(found.func.__name__,
                         MyRequestsView.as_view().__name__)

    def test_my_requests_page_redirects_unauthenticated_user(self):
        response = self.client.get('/my-requests/')
        self.assertRedirects(response, '/login/?next=/my-requests/')

    def test_my_requests_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/my-requests/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'my_requests.html', context={
                'user': user,
            }
        )
        self.assertMultiLineEqual(
            remove_csrf_tag(response.render().content.decode()),
            remove_csrf_tag(expected_html))

    def test_send_requests_authenticated(self):
        # Authenticated user sends requests
        self.client.login(username='user1234', password='demo1234')
        requests_ids = [self.request_1.pk, self.request_2.pk,
                        self.request_3.pk, self.request_4.pk,
                        self.request_5.pk, self.request_6.pk]
        response = self.client.post(
            reverse('send_requests'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sent_requests = Request.objects. \
            filter(user=self.user, pk__in=requests_ids,
                   status=Request.REQUEST_STATUS_SENT).count()
        self.assertEqual(sent_requests, 6)

    def test_send_requests_unauthenticated(self):
        # Non authenticated user tries to send requests
        requests_ids = [self.request_1.pk, self.request_2.pk,
                        self.request_3.pk, self.request_4.pk,
                        self.request_5.pk, self.request_6.pk]
        response = self.client.post(
            reverse('send_requests'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        sent_requests = Request.objects. \
            filter(user=self.user, pk__in=requests_ids,
                   status=Request.REQUEST_STATUS_SENT).count()
        self.assertEqual(sent_requests, 0)

    def test_delete_requests_authenticated(self):
        # Authenticated user deletes requests
        self.client.login(username='user1234', password='demo1234')
        requests_ids = [self.request_1.pk, self.request_2.pk,
                        self.request_3.pk, self.request_4.pk,
                        self.request_5.pk, self.request_6.pk]
        response = self.client.post(
            reverse('delete_requests'), data={'ids[]': requests_ids},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request_count = Request.objects. \
            filter(user=self.user, pk__in=requests_ids).count()
        self.assertEqual(request_count, 0)

    def test_delete_requests_unauthenticated(self):
        # Authenticated user deletes requests
        self.client.login(username='user1234', password='demo1234')
        requests_ids = [self.request_1.pk, self.request_2.pk,
                        self.request_3.pk, self.request_4.pk,
                        self.request_5.pk, self.request_6.pk]
        response = self.client.post(
            reverse('delete_requests'), data={'ids[]': requests_ids},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # simulate AJAX request

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request_count = Request.objects. \
            filter(user=self.user, pk__in=requests_ids).count()
        self.assertEqual(request_count, 0)


class SpeakersPageTest(TestCase):
    maxDiff = None

    def setUp(self):
        # Add user
        self.user = User.objects.create_user(
            username='user1234', password='demo1234', subscription=True)
        # Add non subscription user
        User.objects.create_user(username='user0000', password='demo0000')

    def test_speakers_page_url_resolves_to_speakers_view(self):
        found = resolve('/speakers/')
        self.assertEqual(found.func.__name__,
                         SpeakersView.as_view().__name__)

    def test_speakers_page_redirects_unauthenticated_user(self):
        response = self.client.get('/speakers/')
        self.assertRedirects(response, '/login/?next=/speakers/')

    def test_speakers_page_returns_correct_html_authenticated_user(self):
        self.client.login(username='user1234', password='demo1234')
        response = self.client.get('/speakers/', follow=True)
        user = self.user
        expected_html = render_to_string(
            'speakers.html', context={'user': user,
                                      'dummy_id': '000-000000'}
        )
        self.assertEqual(response.render().content.decode(), expected_html)

    def test_speakers_page_returns_403_logged_user_non_subscription(self):
        self.client.login(username='user0000', password='demo0000')
        response = self.client.get('/speakers/', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
