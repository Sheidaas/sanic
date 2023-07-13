from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import JSONResponse
from .forms.user_form import UserRegisterForm
from .decorators import is_authenticated
from ..utils.auth import encode_jwt


class User(HTTPMethodView):

    @is_authenticated()
    async def get(self, request: Request):
        return JSONResponse(body=request.ctx['USER'].to_dict())

    @staticmethod
    async def post(request: Request) -> JSONResponse:
        user_form = UserRegisterForm(request.json)
        is_valid = await user_form.is_valid()
        if not is_valid:
            body = {
                'errors': user_form.errors
            }
            return JSONResponse(body=body, status=400)
        await user_form.save()
        user_data = encode_jwt(user_form.cleaned_instance.to_dict())
        if isinstance(user_data, dict):
            body = {
                'errors': user_data
            }
            return JSONResponse(body=body, status=500)

        return JSONResponse(body={
            'token': user_data
        }, status=201)

    @is_authenticated()
    async def put(self, request: Request):
        pass

    @is_authenticated()
    async def delete(self, request: Request):
        pass
