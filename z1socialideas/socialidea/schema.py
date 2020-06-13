import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialidea.models import Idea


class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea


class Query(object):
    get_social_ideas = graphene.List(IdeaType)

    # Resolving Ideas
    @login_required
    def resolve_get_social_ideas(self, info, **kwargs):
        return Idea.objects.filter(user_id=info.context.user.id).order_by("-created")
