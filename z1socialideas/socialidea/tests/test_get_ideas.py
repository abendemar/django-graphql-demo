import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from graphene.test import Client
from mixer.backend.django import mixer
from socialidea.models import Idea
from socialuser.models import User

from z1socialideas.schema import schema

GET_IDEAS_QUERY = """
    query
    {
       getIdeas {
        content
        privacity
        user {
          username
        }
      }
    }
"""

FAKE_USERNAME = "fakeusername"
FAKE_CONTENT = "fake content"


@pytest.mark.django_db
class TestSocialIdeaSchema(TestCase):
    def setUp(self):
        request_factory = RequestFactory()

        self.client = Client(schema)
        self.user = mixer.blend(User, username=FAKE_USERNAME)
        self.idea = mixer.blend(Idea, user=self.user, content=FAKE_CONTENT)

        self.my_request = request_factory.get("/api/")
        self.my_request.user = self.user

    def test_get_ideas(self):
        response = self.client.execute(GET_IDEAS_QUERY, context_value=self.my_request)

        response_users = response.get("data").get("getIdeas")

        assert response_users[0]["content"] == FAKE_CONTENT
        assert response_users[0]["user"]["username"] == FAKE_USERNAME
