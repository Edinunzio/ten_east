import pytest, json
from django.urls import reverse
from django.test import Client
from portal.models import Offering, RequestAllocation, InvestorType, OfferingTag, User, Referral


@pytest.mark.django_db
class TestViews:

    def setup_method(self):
        self.client = Client()
        self.investor_type = InvestorType.objects.create(name='Accredited Investor')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            country_of_residence='USA',
            phone_number='1234567890',

        )
        self.user.investor_types.add(self.investor_type)

    def test_signup_get(self):
        response = self.client.get(reverse('signup'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_signup_post_valid(self, mocker):
        """
        Tests that valid signups redirects to home page. A 200 status code
        implies errors in the form.
        """
        mocker.patch('django.contrib.auth.login')
        form_data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'newuser@example.com',
            'country_of_residence': 'USA',
            'phone_number':'1234567890',
            'investor_types': 2,
        }
        response = self.client.post(reverse('signup'), data=form_data)
        assert response.status_code == 302
        assert response.url == reverse('home')

    def test_signup_post_invalid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
            'email': 'newuser@example.com',
            'country_of_residence': 'USA'
        }
        response = self.client.post(reverse('signup'), data=form_data)
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_landing(self):
        response = self.client.get(reverse('landing'))
        assert response.status_code == 200

    def test_home_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        offering_tag = OfferingTag.objects.create(name='Technology')
        offering = Offering.objects.create(
            title='Test Offering',
            start_date='2024-01-01',
            end_date='2024-12-31',
            irr=12.5,
            moic=1.5,
            summary='Test summary',
            minimum=10000,
            is_active=True
        )
        offering.investor_types.add(self.investor_type)
        offering.tags.add(offering_tag)
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        assert 'offerings' in response.context
        assert 'req_allocations' in response.context
        assert 'username' in response.context

    def test_home_not_logged_in(self):
        response = self.client.get(reverse('home'))
        expected_url = f"{reverse('login')}?next={reverse('home')}"
        assert response.status_code == 302
        assert response.url == expected_url

    def test_offerings_list_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        offering_tag = OfferingTag.objects.create(name='Healthcare')
        offering = Offering.objects.create(
            title='Another Test Offering',
            start_date='2024-01-01',
            end_date='2024-12-31',
            irr=15.0,
            moic=2.0,
            summary='Another test summary',
            minimum=5000,
            is_active=True
        )
        offering.investor_types.add(self.investor_type)
        offering.tags.add(offering_tag)
        response = self.client.get(reverse('offerings_list'))
        assert response.status_code == 200
        assert 'offerings' in response.context
        assert 'past_offerings' in response.context

    def test_offerings_list_not_logged_in(self):
        response = self.client.get(reverse('offerings_list'))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_offerings_detail_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        offering_tag = OfferingTag.objects.create(name='Real Estate')
        offering = Offering.objects.create(
            title='Detailed Test Offering',
            start_date='2024-01-01',
            end_date='2024-12-31',
            irr=18.0,
            moic=2.5,
            summary='Detailed test summary',
            minimum=20000,
            is_active=True
        )
        offering.investor_types.add(self.investor_type)
        offering.tags.add(offering_tag)
        response = self.client.get(reverse('offerings_detail', args=[offering.slug]))
        assert response.status_code == 200
        assert 'offering' in response.context

    def test_offerings_detail_not_logged_in(self):
        offering = Offering.objects.create(
            title='Non-Logged In Test Offering',
            start_date='2024-01-01',
            end_date='2024-12-31',
            irr=12.0,
            moic=1.8,
            summary='Non-logged in test summary',
            minimum=15000,
            is_active=True
        )
        offering.investor_types.add(self.investor_type)
        offering.tags.add(OfferingTag.objects.create(name='Finance'))
        response = self.client.get(reverse('offerings_detail', args=[offering.slug]))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))

    def test_create_request_allocation_view_success(self, mocker):
        self.client.login(username='testuser', password='testpassword')
        offering = Offering.objects.create(
            title='Allocation Test Offering',
            start_date='2024-01-01',
            end_date='2024-12-31',
            irr=20.0,
            moic=3.0,
            summary='Allocation test summary',
            minimum=25000,
            is_active=True
        )
        offering.investor_types.add(self.investor_type)
        offering.tags.add(OfferingTag.objects.create(name='Energy'))
        payload = {
            'user': self.user.id,
            'offering': offering.id,
            'amount': '5000.00'
        }
        response = self.client.post(reverse('create_request_allocation'), data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == 'success'

    def test_create_request_allocation_view_error(self, mocker):
        self.client.login(username='testuser', password='testpassword')
        payload = {
            'user': self.user.id,
            'offering': 999,  # Non-existent offering
            'amount': '5000.00'
        }
        response = self.client.post(reverse('create_request_allocation'), data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == 'error'

@pytest.mark.django_db
class TestCreateReferralView:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )

    def test_create_referral_success(self):
        payload = {
            'user': self.user.id,
            'invite_name': 'John Doe',
            'invite_email': 'johndoe@example.com',
        }
        response = self.client.post(reverse('create_referral'), data=json.dumps(payload), content_type='application/json')
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['status'] == 'success'
        assert 'id' in response_data['data']
        
        # Verify that the referral was actually created in the database
        referral = Referral.objects.get(id=response_data['data']['id'])
        assert referral.user == self.user
        assert referral.invite_name == 'John Doe'
        assert referral.invite_email == 'johndoe@example.com'

    def test_create_referral_user_does_not_exist(self):
        # Test creating a referral with a non-existent user
        payload = {
            'user': 999,
            'invite_name': 'Jane Doe',
            'invite_email': 'janedoe@example.com',
        }
        response = self.client.post(reverse('create_referral'), data=json.dumps(payload), content_type='application/json')
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['status'] == 'error'
        assert 'message' in response_data
