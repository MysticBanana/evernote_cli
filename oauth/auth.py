# https://github.com/Jaymon/enno/blob/master/enno/__main__.py

import exceptions
import subprocess

import enum
import server

from evernote.api.client import EvernoteClient

# test
import webbrowser

class Auth:
    CONSUMER_KEY = None
    CONSUMER_SECRET = None
    SANDBOX = True

    class AuthError(exceptions.Exception):
        class ErrorReason(enum.Enum):
            DEFAULT = 1

    def __init__(self, controller, *args, **kwargs):
        self.CONSUMER_KEY = kwargs.get("CONSUMER_KEY", None)
        self.CONSUMER_SECRET = kwargs.get("CONSUMER_SECRET", None)
        self.SANDBOX = kwargs.get("SANDBOX", True)
        self.logger = kwargs.get("logger", None)
        self.controller = controller

        self.access_token = None

        if self.logger is None:
            raise self.AuthError(self.AuthError.ErrorReason.DEFAULT, "no logger defined")

        request_token = dict()
        def callback(request):
            access_token = client.get_access_token(
                request_token['oauth_token'],
                request_token['oauth_token_secret'],
                request.query.get('oauth_verifier', '')
            )

            # todo
            self.access_token = access_token
            return access_token

        self.logger.info("")
        self.server = server.BasicServer(callback, logger=self.controller.create_logger("HTTPServer"))
        self.server.start()

        client = EvernoteClient(
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            sandbox=self.SANDBOX
        )

        request_token = client.get_request_token(self.server.url)
        auth_url = client.get_authorize_url(request_token)

        # windows error
        # subprocess.call(["open", auth_url])
        try:
            webbrowser.open(auth_url)
            self.server.handle_request()
        except Exception as e:
            print e

        self.server.stop()
