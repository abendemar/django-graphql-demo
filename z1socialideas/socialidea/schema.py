import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from socialidea.models import Idea


def check_valid_privacity(privacity):
    privacy_values = [accepted_value[0] for accepted_value in Idea.SHARE_IDEA_CHOICES]
    return privacity in privacy_values


class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea


class Query(object):
    get_ideas = graphene.List(IdeaType)

    @login_required
    def resolve_get_ideas(self, info, **kwargs):
        return Idea.objects.filter(user_id=info.context.user.id).order_by("-created")


# Mutate Notes


class CreateNote(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        idea = graphene.String(required=True)
        privacity = graphene.String(required=False)

    @login_required
    def mutate(self, info, idea, **kwargs):
        privacity = kwargs.get("privacity", Idea.PUBLIC)

        if not check_valid_privacity(privacity):
            raise GraphQLError(f"Error. Wrong Privacy Value {privacity}")

        idea = Idea(content=idea, privacity=privacity, user=info.context.user)
        idea.save()
        return CreateNote(idea=idea)


class RemoveIdea(graphene.Mutation):
    idea_id = graphene.Int()

    class Arguments:
        idea_id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, idea_id):
        try:
            idea = Idea.objects.get(pk=idea_id)
        except ObjectDoesNotExist:
            raise GraphQLError(f"The idea {idea_id} not exists!")
        if idea.user.id != info.context.user.id:
            raise GraphQLError(
                f"User ID {info.context.user.id} cant remove idea ID {idea_id}"
            )
        idea.delete()
        return RemoveIdea(idea_id=idea_id)


class SetIdeaPrivacity(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        idea_id = graphene.Int(required=True)
        privacity = graphene.String(required=True)

    @login_required
    def mutate(self, info, idea_id, privacity):

        if not check_valid_privacity(privacity):
            raise GraphQLError(f"Error. Wrong Privacy Value {privacity}")

        try:
            idea = Idea.objects.get(pk=idea_id)
        except ObjectDoesNotExist:
            raise GraphQLError("The idea not exists!")

        if idea.user_id != info.context.user.id:
            raise GraphQLError("You are not the owner!")
        idea.privacity = privacity
        idea.save()

        return SetIdeaPrivacity(idea=idea)


class Mutation(graphene.ObjectType):
    create_idea = CreateNote.Field()
    remove_idea = RemoveIdea.Field()
    set_idea_privacity = SetIdeaPrivacity.Field()
