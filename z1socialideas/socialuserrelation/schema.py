import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialuserrelation.models import UserRelation


class UserRelationType(DjangoObjectType):
    class Meta:
        model = UserRelation


class Query(object):
    get_follow_requests = graphene.List(
        UserRelationType, first=graphene.Int(), skip=graphene.Int(),
    )
    get_followers = graphene.List(
        UserRelationType, first=graphene.Int(), skip=graphene.Int(),
    )
    get_following = graphene.List(
        UserRelationType, first=graphene.Int(), skip=graphene.Int(),
    )

    # Resolving Ideas
    @login_required
    def resolve_get_follow_requests(self, info):
        return UserRelation.objects.filter(
            following_user_id=info.context.user.id
        ).filter(status=UserRelation.Followstatus.PEN)

    @login_required
    def resolve_get_followers(self, info, **kwargs):
        return UserRelation.objects.filter(
            following_user_id=info.context.user.id
        ).filter(status=UserRelation.Followstatus.APP)

    @login_required
    def resolve_get_following(self, info, **kwargs):
        return UserRelation.objects.filter(user_id=info.context.user.id).filter(
            status=UserRelation.Followstatus.APP
        )
