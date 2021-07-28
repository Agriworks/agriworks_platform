from functools import wraps

from flask import Flask, jsonify, make_response, request

from Response import Response
from Services.AuthenticationService import AuthenticationService

AuthenticationService = AuthenticationService()


# TODO: remove view endpoints from non protected endpoints after figuring out the session ID bug
NON_PROTECTED_ENDPOINTS = [
    "index",
    "sendStaticComponent",
    "static",
    "api.specs",
    "api.doc",
    "api.root",
    "restplus_doc.static",
    "api.admin_index",
    "api.admin_account",
    "api.auth_login",
    "api.auth_signup",
    "api.auth_confirm_user",
    "api.auth_forgot_password",
    "api.auth_reset_password",
    "api.auth_verify_session",
    "api.auth_resend_confirmation_email",
    "api.auth_authorize",
    "api.view_create_new_view",
    "api.view_fetch_views",
]


def authRequired(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "SID" not in request.cookies:
            return Response(status=403)

        cookie = request.cookies["SID"]

        try:
            user = AuthenticationService.verifySessionAndReturnUser(cookie)
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return Response("Invalid session ID", status=403)

    return decorator
