import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from graphene.test import Client
from mixer.backend.django import mixer
from socialidea.models import Idea
from socialuser.models import User

from z1socialideas.schema import schema

FAKE_USERNAME = "fakeusername"
FAKE_CONTENT = "Fake Content"
FAKE_PRIVACITY_OK = Idea.PUBLIC
FAKE_PRIVACITY_NOK = "ERROR PRIVACITY"

CREATE_IDEA_QUERY = """
    mutation
    {
      createIdea(content:"Fake Content", privacity:"PUB")
      {
        idea {
          content,
          privacity,
          user{
            username
          }
        }
      }
    }
"""


@pytest.mark.django_db
class TestCreateIdea(TestCase):
    def setUp(self):
        request_factory = RequestFactory()

        self.client = Client(schema)
        self.user = mixer.blend(User, username=FAKE_USERNAME)

        self.my_request = request_factory.get("/api/")
        self.my_request.user = self.user

    def test_create_idea_ok(self):
        response = self.client.execute(CREATE_IDEA_QUERY, context_value=self.my_request)

        response_create = response.get("data").get("createIdea").get("idea")
        response_errors = response.get("errors")

        assert not response_errors
        assert response_create["content"] == FAKE_CONTENT
        assert response_create["privacity"] == FAKE_PRIVACITY_OK
        assert response_create["user"]["username"] == FAKE_USERNAME

    def test_create_idea_nok(self):
        bad_query = CREATE_IDEA_QUERY.replace('"PUB"', '"ERROR"')

        response = self.client.execute(bad_query, context_value=self.my_request)

        response_errors = response.get("errors")

        assert response_errors
