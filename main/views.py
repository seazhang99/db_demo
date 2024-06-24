from flask import Blueprint, render_template, request, get_template_attribute
import json

from .controllers import do_chat

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/conversation', methods=['POST'])
def conversation():
    question = request.form.get('question')
    #print(request.files)
    res = do_chat(question, request.files)
    print(res)
    bot_message = get_template_attribute('_bot_message.html', 'bot_message')
    html = bot_message(res)
    return html
