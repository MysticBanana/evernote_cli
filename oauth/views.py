from evernote.api.client import EvernoteClient

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
# rename config.py.template to config.py and paste your credentials.
from config import EN_CONSUMER_KEY, EN_CONSUMER_SECRET
from django.views.generic import View


def get_evernote_client(token=None, controller=None):
    sandbox = True if not controller else controller.sandbox

    if token:
        return EvernoteClient(token=token, sandbox=sandbox)
    else:
        return EvernoteClient(
            consumer_key=EN_CONSUMER_KEY,
            consumer_secret=EN_CONSUMER_SECRET,
            sandbox=sandbox
        )


def index(request):
    return render_to_response('oauth/index.html')


class Auth(View):
    controller = None

    def get(self, request):
        client = get_evernote_client(controller=self.controller)
        callbackUrl = 'http://%s%s' % (
            request.get_host(), reverse('evernote_callback'))
        request_token = client.get_request_token(callbackUrl)

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token['oauth_token_secret']

        # Redirect the user to the Evernote authorization URL
        print(client.get_authorize_url(request_token))
        return redirect(client.get_authorize_url(request_token))


def callback(request):
    controller = Auth.controller

    try:
        client = get_evernote_client()
        token = client.get_access_token(
            request.session['oauth_token'],
            request.session['oauth_token_secret'],
            request.GET.get('oauth_verifier', '')

        )
    except KeyError:
        return redirect('/')

    controller.user.user_token = token
    print(token)
    controller.user.dump_config()
    controller.user.user_config.dump()
    controller.logger.info("setting user key for user: {}".format(controller.user.user_name))

    return render_to_response('oauth/callback.html')

def reset(request):
    return redirect('/')
