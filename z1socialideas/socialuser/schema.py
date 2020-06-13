import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialuser.models import User

MIN_CHAR_QUERY_LENGTH = 3


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    get_users_by_username = graphene.List(
        UserType,
        username=graphene.String(required=True),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @login_required
    def resolve_get_users_by_username(self, info, username, **kwargs):
        skip = kwargs.get("skip", None)
        first = kwargs.get("first", None)

        if len(username) < MIN_CHAR_QUERY_LENGTH:
            raise GraphQLError(
                f"You must enter at least {MIN_CHAR_QUERY_LENGTH} characters to search"
            )

        users_found = User.objects.filter(username__contains=username)
        if skip:
            users_found = users_found[skip:]
        if first:
            users_found = users_found[:first]
        return users_found
