import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from graphene.test import Client
from mixer.backend.django import mixer
from socialuser.models import User

from z1socialideas.schema import schema

get_users_by_username_query = """
    query
    {
        getUsersByUsername(username:"testname")
        {
        username,firstName, id
        }
    }
"""


@pytest.mark.django_db
class TestSocialUserSchema(TestCase):
    def setUp(self):
        request_factory = RequestFactory()

        self.client = Client(schema)
        self.user = mixer.blend(User, username="testname")

        self.my_request = request_factory.get("/api/")
        self.my_request.user = self.user

    def test_get_users_by_username_query(self):
        response = self.client.execute(
            get_users_by_username_query, context_value=self.my_request
        )
        response_users = response.get("data").get("getUsersByUsername")

        assert response_users[0]["username"] == "testname"
