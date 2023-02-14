# admin_oauth

## Okta Requirements
- An Okta dev server was created : https://dev-356260.okta.com/
- A **john.doe@oups.com** user was created on this server
- An application was created on okta : https://dev-356260-admin.okta.com/admin/app/oidc_client/instance/0oaeo3wk1cVctIq1U4x6
- The **Authorization Code Flow** was enabled on this application
- http://localhost:8000/admin/callback was configured as redirect uri for the application
- **john.doe@oups.com** user was added to this application

## Local Requirements
- Install requirements (pip install -r requirements.txt)
- Ask for .env file

### Testing
- Add an super user to your local application (the super user email must be **john.doe@oups.com** )
```
python manage.py createsuperuser
```
- Run the local server
```
python manage.py runserver
```
- Open uri http://localhost:8000/admin/ (you should be redirected to Okta)
- Login into Okta as **john.doe@oups.com** (you should ask for **john.doe@oups.com** Okta password)
- Tada you're connected to Django Admin

## Resources 
- https://github.com/RealGeeks/django-admin-oauth2
