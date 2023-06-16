from .forms.user_form import UserTokenLoginForm, UserCredentialLoginForm
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import JSONResponse


class Login(HTTPMethodView):

    @staticmethod
    async def get(request: Request) -> JSONResponse:
        user_form = UserTokenLoginForm({'token': request.token})
        is_valid = await user_form.is_valid()
        if not is_valid:
            body = {
                'errors': user_form.errors
            }
            return JSONResponse(body=body, status=400)
        return JSONResponse(body={
            'token': request.token
        })

    @staticmethod
    async def post(request: Request) -> JSONResponse:
        user_form = UserCredentialLoginForm(request.json)
        is_valid = await user_form.is_valid()
        if not is_valid:
            body = {
                'errors': user_form.errors
            }
            return JSONResponse(body=body, status=400)
        return JSONResponse(body={
            'token': user_form.cleaned_instance.get_token()
        })
