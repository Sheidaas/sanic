from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import JSONResponse
from .forms.user_form import UserRegisterForm
from .decorators import is_authenticated


class User(HTTPMethodView):

    @is_authenticated
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
        return JSONResponse(body={
            'token': user_form.cleaned_instance.get_token()
        }, status=201)

    @is_authenticated
    async def put(self, request: Request):
        pass

    @is_authenticated
    async def delete(self, request: Request):
        pass
