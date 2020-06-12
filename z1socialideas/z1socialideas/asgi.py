"""
ASGI config for z1socialideas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import channels.auth
from django.urls import path
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "z1socialideas.settings")

application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter([path("graphql/", GraphqlSubscriptionConsumer)])
        )
    }
)
