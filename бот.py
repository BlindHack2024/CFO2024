import vkapi
from flask import Flask, request, jsonify
import requests
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def send_text_message(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message
    )

def send_url(user_id, url):
    vk.messages.send(
        user_id=user_id,
        attachment=url
    )

def send_pdf(user_id, pdf_file):
    upload_server = vk.docs.getMessagesUploadServer(type='doc', peer_id=user_id)['upload_url']
    response = requests.post(upload_server, files={'file': open(pdf_file, 'rb')}).json()
    doc = vk.docs.save(file=response['file'])
    attachment = 'doc{}_{}'.format(doc['doc']['owner_id'], doc['doc']['id'])

    vk.messages.send(
        user_id=user_id,
        attachment=attachment
    )





app = Flask(__name__)


token = '225725134'
group_id = '225725134'


vk_session = vkapi (token=token)
vk = vk_session.get_api()


longpoll = VkBotLongPoll(vk_session, group_id=group_id)


keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Отправка пдф', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('ссылка на вакансию', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Отправка текста', color=VkKeyboardColor.NEGATIVE)


@app.route('/bot', methods=['POST'])
def bot():
    data = request.get_json()
    if data['type'] == 'message_new':
        user_id = data['object']['from_id']
        vk.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            peer_id=user_id,
            keyboard=keyboard.get_keyboard(),
            message='Hello! Please choose a button.'
        )
    return jsonify({'response': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

