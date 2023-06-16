from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import JSONResponse
from .forms.user_form import UserRegisterForm
from .decorators import is_authenticated, is_game_session_owner


class GameSession(HTTPMethodView):

    decorators = [is_authenticated]

    @is_game_session_owner
    async def get(self, request: Request, game_session_uuid: str):
        return JSONResponse(body=request.ctx['GAME_SESSION'].to_dict())

    async def post(self, request: Request) -> JSONResponse:
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

    @is_game_session_owner
    async def put(self):
        pass
