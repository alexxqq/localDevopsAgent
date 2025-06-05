from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import asyncio

import json

from .service import get_chat_response


@view_config(route_name='ask', request_method='POST', renderer='json')
def ask_view(request):
    try:
        if not request.content_length:
            return _json_error("Empty request body", 400)

        data = request.json_body
        question = data.get("question")

        if not question:
            return _json_error("Missing 'question'", 400)

        answer = asyncio.run(get_chat_response(question))
        return {"answer": answer}

    except Exception as e:
        return _json_error(str(e), 500)


def _json_error(message, status):
    """Helper to return JSON error responses."""
    return Response(
        json.dumps({"error": message}),
        status=status,
        content_type='application/json; charset=utf-8'
    )


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('ask', '/ask')
    config.scan()
    return config.make_wsgi_app()
