# https://github.com/Jaymon/enno/blob/master/enno/__main__.py

from helper import exception
from time import sleep
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

    class AuthError(exception.EvernoteException):
        class ErrorReason(enum.Enum):
            DEFAULT = 1

    def __init__(self, controller, *args, **kwargs):
        self.CONSUMER_KEY = kwargs.get("CONSUMER_KEY", None)
        self.CONSUMER_SECRET = kwargs.get("CONSUMER_SECRET", None)
        self.SANDBOX = kwargs.get("SANDBOX", True)
        self.logger = kwargs.get("logger", None)
        self.controller = controller

        # access token user needs for oauth
        self.access_token = None

        if self.logger is None:
            raise self.AuthError(self.AuthError.ErrorReason.DEFAULT, "no logger defined")

        request_token = dict()
        # callback from the evernote server
        def callback(request):
            self.logger.info("successfully got the user access token")
            access_token = client.get_access_token(
                request_token['oauth_token'],
                request_token['oauth_token_secret'],
                request.query.get('oauth_verifier', '')
            )

            self.access_token = access_token
            return access_token

        self.logger.info("trying to start webserver...")
        self.server = server.BasicServer(callback, logger=self.controller.create_logger("HTTPServer"))
        self.server.start()
        self.logger.info("webserver successfully started")

        self.logger.info("getting the request token from evernote server")

        # evernote client for to authorize for oauth
        client = EvernoteClient(
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            sandbox=self.SANDBOX
        )
        request_token = client.get_request_token(self.server.url)
        auth_url = client.get_authorize_url(request_token)

        self.logger.info("calling browser for authentication")

        # windows error, linux works
        # subprocess.call(["open", auth_url])

        # call webbrowser to open url for oauth authentication
        try:
            test = webbrowser.open(auth_url)
            self.server.handle_request()
        except Exception as e:
            raise self.AuthError(None, "can not open the browser for access token")

        sleep(1)
        self.logger.info("stopping webserver")
        self.server.stop()
