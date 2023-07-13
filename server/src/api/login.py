from .forms.user_form import UserCredentialLoginForm
from .decorators import is_authenticated
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import JSONResponse
from ..utils.auth import encode_jwt


class Login(HTTPMethodView):

    @is_authenticated()
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse(body={'token': request.token})

    @staticmethod
    async def post(request: Request) -> JSONResponse:
        user_form = UserCredentialLoginForm(request.json)
        is_valid = await user_form.is_valid()
        if not is_valid:
            body = {
                'errors': user_form.errors
            }
            return JSONResponse(body=body, status=400)
        token = encode_jwt(user_form.cleaned_instance.to_dict())
        if isinstance(token, dict):
            body = {
                'errors': token
            }
            return JSONResponse(body=body, status=500)
        return JSONResponse(body={
            'token': token
        })
