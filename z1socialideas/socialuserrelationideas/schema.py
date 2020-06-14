import graphene
from graphene_subscriptions.events import CREATED
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialidea.models import Idea
from socialidea.schema import IdeaType
from socialuserrelation.models import UserRelation


class Query(object):
    get_user_timeline = graphene.List(IdeaType, user=graphene.Int(required=True))
    get_global_timeline = graphene.List(IdeaType)

    @login_required
    def resolve_get_user_timeline(self, info, user):

        if info.context.user.id == user:
            raise GraphQLError("You cant process this query for logged user")

        public_notes = Idea.objects.filter(user__id=user, privacity=Idea.PUBLIC)

        is_follower = UserRelation.objects.filter(
            user_follower__id=info.context.user.id,
            user_followed__id=user,
            follow_status=UserRelation.ACCEPTED,
        )

        if is_follower:
            protected_noted = Idea.objects.filter(
                user__id=user, privacity=Idea.PROTECTED
            )
            return public_notes.union(protected_noted).order_by("-created")

        return public_notes.order_by("-created")

    @login_required
    def resolve_get_global_timeline(self, info):
        own_notes = Idea.objects.filter(user__id=info.context.user.id)

        following_user_ids = UserRelation.objects.filter(
            user_follower__id=info.context.user.id, follow_status=UserRelation.ACCEPTED
        ).values_list("user_followed_id", flat=True)

        accessible_notes = [Idea.PUBLIC, Idea.PROTECTED]

        following_notes = Idea.objects.filter(
            user_id__in=following_user_ids, privacity__in=accessible_notes
        )

        if following_notes:
            return own_notes.union(following_notes).order_by("-created")

        return own_notes.order_by("-created")


class Subscription(graphene.ObjectType):
    note_created = graphene.Field(IdeaType)

    def resolve_note_created(root, info):

        following_user_ids = UserRelation.objects.filter(
            user_follower=info.context.user, follow_status=UserRelation.ACCEPTED
        ).values_list("user_followed__id", flat=True)

        return root.filter(
            lambda event: event.operation == CREATED
            and isinstance(event.instance, Idea)
            and event.instance.user.pk in following_user_ids
            and event.instance.privacity in [Idea.PUBLIC, Idea.PROTECTED]
        ).map(lambda event: event.instance)
