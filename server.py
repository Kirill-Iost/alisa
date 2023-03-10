# from flask import Flask, url_for
# from data import db_session, news_api
# from flask import make_response, jsonify
# from flask_restful import Api
# import news_resources
# import users_resource
#
# app = Flask(__name__)
# api = Api(app)
#
#
# api.add_resource(news_resources.NewsListResource, '/api/v2/news/')
# api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
#
# api.add_resource(users_resource.UsersListResource, '/api/v2/users/')
# api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
#
# # @app.errorhandler(404)
# # def not_found(error):
# #     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# def main():
#     db_session.global_init("db/blogs.db")
#     app.register_blueprint(news_api.blueprint)
#     app.run()
#
# if __name__ == '__main__':
#     main()

import json
import logging

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests

@app.route("/")
def index():
    return "<h1>Привет, мир!</h1>"


if __name__ == '__main__':
    app.run(port=5000)