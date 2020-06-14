import graphene
import graphql_jwt
import socialidea.schema
import socialuser.schema
import socialuserrelation.schema
import socialuserrelationideas.schema
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(
    UserQuery,
    MeQuery,
    socialuser.schema.Query,
    socialidea.schema.Query,
    socialuserrelation.schema.Query,
    socialuserrelationideas.schema.Query,
    graphene.ObjectType,
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(
    AuthMutation,
    socialidea.schema.Mutation,
    socialuserrelation.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()


class Subscription(socialuserrelationideas.schema.Subscription):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
