import pytest

from django.urls import reverse

from party.models import Party

@pytest.mark.django_db
def test_create_party(authenticated_client, create_user):

    url = reverse("page_new_party")

    data = {
        "party_date": "2025-12-12",
        "party_time": "12:00",
        "venue": "Test Venue",
        "invitation": "Test Invitation, Come to my Party!",
    }

    response = authenticated_client(create_user).post(url, data)

    assert response.status_code == 302
    assert Party.objects.count() == 1


def test_create_party_invitation_too_short(authenticated_client, create_user):

    url = reverse("page_new_party")

    data = {
        "party_date": "2025-12-12",
        "party_time": "12:00",
        "venue": "Test Venue",
        "invitation": "Test",
    }

    responses = authenticated_client(create_user).post(url, data)

    assert not responses.context["form"].is_valid()
    assert  Party.objects.count() == 0

def test_create_party_past_date_returns_error(authenticated_client, create_user):

    url = reverse("page_new_party")

    data = {
        "party_date": "2020-12-12",
        "party_time": "12:00",
        "venue": "Test Venue",
        "invitation": "Test Invitation, Come to my Party!",
    }

    responses = authenticated_client(create_user).post(url, data)

    assert not responses.context["form"].is_valid()
    assert Party.objects.count() == 0

def test_partial_check_party_date(authenticated_client, create_user):
    url = reverse("partial_check_party_date")
    data = {
        "party_date": "2020-06-06",
    }

    response = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_party_date"' in response.content.decode()


def test_partial_check_invitation(authenticated_client, create_user):
    url = reverse("partial_check_invitation")
    data = {
        "invitation": "Too short",
    }

    response = authenticated_client(create_user).get(url, data)

    assert response.status_code == 200
    assert 'id="id_invitation"' in response.content.decode()
