from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import json
import asyncio
from service import get_chat_response


@view_config(route_name='ask', request_method='POST', renderer='json')
def ask_view(request):
    try:
        if not request.content_length:
            return Response(
                json.dumps({"error": "Empty request body"}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        data = request.json_body
        print(data)
        user_input = data.get("question")
        if not user_input:
            return Response(
                json.dumps({"error": "Missing 'question'"}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        reply = loop.run_until_complete(get_chat_response(user_input))
        loop.close()
        return {"answer": reply}
    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type='application/json; charset=utf-8'
        )


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('ask', '/ask')
    config.scan()
    return config.make_wsgi_app()
