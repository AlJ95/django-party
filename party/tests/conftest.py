import datetime

import pytest
from django.test import Client

from party.models import Party, Gift, Guest


@pytest.fixture(scope='function')
def create_user(django_user_model):
    return django_user_model.objects.create_user(username='testuser',password='123456')

@pytest.fixture(scope="session")
def authenticated_client():
    def _authenticated_client(test_user):
        client = Client()
        client.force_login(test_user)

        return client

    return _authenticated_client


@pytest.fixture(scope='session')
def create_party():
    def _create_party(organizer, **kwargs):
        party = Party.objects.create(
            organizer=organizer,
            party_date=kwargs.get('party_date', datetime.date.today()),
            party_time=kwargs.get('party_time', datetime.datetime.now()),
            venue=kwargs.get('venue', 'Amazing Castle'),
        )

        return party

    return _create_party


@pytest.fixture(scope='session')
def create_gift():
    def _create_gift(party, **kwargs):
        gift = Gift.objects.create(
            party=party,
            name=kwargs.get('name', 'Test gift'),
            price=kwargs.get('price', 12.5),
            link=kwargs.get('link', 'https://testlink.com'),
        )

        return gift

    return _create_gift


@pytest.fixture(scope='session')
def create_guest():
    def _create_guest(party, **kwargs):
        guest = Guest.objects.create(
            party=party,
            name=kwargs.get('name', 'Anna Boleyn'),
            attending=kwargs.get('attending', True),
        )

        return guest

    return _create_guest

