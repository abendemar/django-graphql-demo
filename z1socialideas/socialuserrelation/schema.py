import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialuser.models import User
from socialuser.schema import UserType
from socialuserrelation.models import UserRelation


class UserRelationType(DjangoObjectType):
    class Meta:
        model = UserRelation


class Query(object):
    get_follow_requests = graphene.List(UserRelationType,)
    get_followers = graphene.List(UserRelationType,)
    get_following = graphene.List(UserRelationType,)

    # Resolving Ideas
    @login_required
    def resolve_get_follow_requests(self, info):
        return UserRelation.objects.filter(user_followed=info.context.user).filter(
            follow_status=UserRelation.PENDING
        )

    @login_required
    def resolve_get_followers(self, info, **kwargs):
        return UserRelation.objects.filter(user_followed=info.context.user).filter(
            follow_status=UserRelation.ACCEPTED
        )

    @login_required
    def resolve_get_following(self, info, **kwargs):
        return UserRelation.objects.filter(user_follower=info.context.user).filter(
            follow_status=UserRelation.ACCEPTED
        )


class FollowRequest(graphene.Mutation):
    follow_request = graphene.Field(UserRelationType)

    class Arguments:
        user_to_follow = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_to_follow):
        try:
            user_followed = User.objects.get(pk=user_to_follow)
        except ObjectDoesNotExist:
            raise GraphQLError(f"The user id {user_to_follow} to follow not exists!")
        follow_request = UserRelation(
            user_follower=info.context.user,
            user_followed=user_followed,
            follow_status=UserRelation.PENDING,
        )
        try:
            follow_request.save()
        except IntegrityError:
            raise GraphQLError(
                f"The user {info.context.user.id} have already a petition to follow user {user_followed.id}."
            )
        return FollowRequest(follow_request=follow_request)


class UnfollowUser(graphene.Mutation):
    current_user = graphene.Field(UserType)

    class Arguments:
        user_to_unfollow = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_to_unfollow):
        try:
            unfollow_request = UserRelation.objects.filter(
                user_follower=info.context.user
            ).get(user_followed_id=user_to_unfollow)
        except ObjectDoesNotExist:
            raise GraphQLError(
                f"The user {user_to_unfollow} not exists or not following!"
            )
        unfollow_request.delete()
        return UnfollowUser(current_user=info.context.user)


class RemoveFollower(graphene.Mutation):
    current_user = graphene.Field(UserType)

    class Arguments:
        follower_to_remove = graphene.Int(required=True)

    @login_required
    def mutate(self, info, follower_to_remove):
        try:
            remove_follower = UserRelation.objects.filter(
                user_followed=info.context.user
            ).get(user_follower_id=follower_to_remove)
        except ObjectDoesNotExist:
            raise GraphQLError(
                f"The user {follower_to_remove} is not following you or not exists!"
            )
        remove_follower.delete()
        return RemoveFollower(current_user=info.context.user)


class ApproveFollower(graphene.Mutation):
    followers = graphene.Field(UserRelationType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_id):
        try:
            followers = UserRelation.objects.filter(user_id=info.context.user.id).get(
                pk=user_id
            )
        except ObjectDoesNotExist:
            raise GraphQLError("The follow request does not exists!")
        followers.status = UserRelation.ACCEPTED
        followers.save()
        return ApproveFollower(followers=followers)


class DenyFollower(graphene.Mutation):
    followers = graphene.Field(UserRelationType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_id):
        try:
            followers = UserRelation.objects.filter(user_id=info.context.user.id).get(
                pk=user_id
            )
        except ObjectDoesNotExist:
            raise GraphQLError("The follow request does not exists!")
        followers.follow_status = UserRelation.DENIED
        followers.save()
        return DenyFollower(followers=followers)


class Mutation(graphene.ObjectType):
    follow_request = FollowRequest.Field()
    unfollow_user = UnfollowUser.Field()
    remove_follower = RemoveFollower.Field()
    approve_follower = ApproveFollower.Field()
    deny_follower = DenyFollower.Field()
