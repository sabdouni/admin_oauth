import json

from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model, login
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.urls import reverse, path
from rauth import OAuth2Service


class OauthAdminSite(AdminSite):
    okta: OAuth2Service = OAuth2Service(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        name='okta',
        authorize_url=settings.AUTH_URL,
        access_token_url=settings.TOKEN_URL,
        base_url='https://dev-356260.okta.com/oauth2/default/v1/')



    def callback(self, request):
        redirect_uri = request.build_absolute_uri(reverse("admin:callback"))

        # create a dictionary for the data we'll post on the get_access_token request
        data = dict(code=request.GET.get("code"), redirect_uri=redirect_uri,grant_type="authorization_code")


        # retrieve the authenticated session
        # the decoder is needed, to specify the encoding to use when decoding the bytes
        # N.B : in order to get  the email from okta you should request the scope 'email'
        oauth_session = self.okta.get_auth_session(data=data, decoder=lambda x: json.loads(x.decode('utf-8')))

        # Call /userinfo to fetch informations about the connected user
        user_info = oauth_session.get('userinfo').json()

        email = user_info["email"]
        user =  get_user_model().objects.filter(email__iexact=email).first()

        login(request, user)

        return redirect(reverse("admin:index"))



    def login(self, request):
        redirect_uri = request.build_absolute_uri(reverse("admin:callback"))
        params = {'redirect_uri': redirect_uri,
                  'response_type': 'code', "scope":settings.SCOPE, "state":"dummy"}
        authorization_url = self.okta.get_authorize_url(**params)


        return redirect(authorization_url)

    def logout_redirect(self, request):
        pass

    def logout(self, request):
        pass

    def get_urls(self):
        """Overrided to add oauth custom urls"""
        urls = super(OauthAdminSite, self).get_urls()
        custom_urls = [
            path('callback/', self.callback, name='callback'),
            path('logout_redirect/', self.logout_redirect, name="logout_redirect"),
        ]
        return urls + custom_urls


#create a Admin_site object to register views
admin_site = OauthAdminSite()
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
