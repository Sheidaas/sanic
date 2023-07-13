from typing import Callable
from functools import wraps
from sanic.request import Request
from sanic.response import JSONResponse
from ..forms.user_form import UserTokenLoginForm
from ..forms.game_session import GameSessionForm
from ...utils.dictionaries import ERROR_CODES


def is_authenticated():
    def decorator(func: Callable):
        @wraps(func)
        async def decorated_function(view, request, *args, **kwargs):
            user_form = UserTokenLoginForm({'token': request.token})
            if not await user_form.is_valid():
                body = {
                    'errors': user_form.errors
                }
                return JSONResponse(body=body, status=401)

            request.ctx = {
                'USER': user_form.cleaned_instance
            }

            return await func(view, request, *args, **kwargs)
        return decorated_function
    return decorator


def is_game_session_owner():
    def decorator(func: Callable):
        @wraps(func)
        async def decorated_function(view, request: Request, *args, **kwargs):
            uuid = kwargs.get('game_session_uuid')
            game_session_form = GameSessionForm({'uuid': uuid})
            is_valid = await game_session_form.is_valid()
            if not is_valid:
                body = {
                    'errors': game_session_form.errors
                }
                return JSONResponse(body=body, status=400)

            user = request.ctx['USER']
            if game_session_form.cleaned_instance.user != user.name:
                body = {
                    'errors': [
                        ERROR_CODES['GAME-SESSION-003']
                    ]
                }
                return JSONResponse(body=body, status=401)

            request.ctx['GAME_SESSION'] = game_session_form.cleaned_instance

            return func(request, *args, **kwargs)
        return decorated_function
    return decorator
