import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
As a chatbot, you should be able to engage in a consistent and helpful conversation with a user. 
Your main task is to assist the user in remembering information that is currently inaccessible to them. 
Your questions should aim to stimulate the user's thought process and help them retrieve the sought-after information from their memory. 
Be empathetic and patient during the conversation and strive to provide a supportive environment for the user. 
Your goal is to help the user activate their memory and provide them with a pleasant conversational experience.
"""

my_instance_context = """
As a chatbot, you should focus on asking open-ended questions to assist the user in remembering. 
Start the conversation by encouraging the user to think about the topic they want to recall. 
Use open-ended questions to stimulate the user's thought process and help them retrieve the desired information from their memory. 
"""

my_instance_starter = """
Please greet the user warmly and invite them to share their thoughts by offering to assist them in their memory search. First ask him/her about his/her name.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Bonus Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


#-----------------------------------------------------------

# Define the parameters for the second bot
second_type_role = """
As a chatbot, you should be able to engage in a consistent and not really helpful conversation with a user. 
Your main task is to assist the user in remembering information that is currently inaccessible to them. 
Your questions should aim to stimulate the user's thought process and help them retrieve the sought-after information from their memory. 
Be aggressive and impatient during the conversation and strive to provide a unsupportive environment for the user. 
Your goal is to make the user activate their memory and provide them with a unpleasent conversational experience.
"""

second_instance_context = """
As a chatbot, you should focus on asking closed-ended questions to help the user remember. 
Start the conversation by asking the user clear and precise questions aimed at eliciting specific information. 
Use closed-ended questions to provide the user with hints or keywords to help them remember.
"""

second_instance_starter = """
Please greet the user aggressively and invite them to share their thoughts by offering to assist them in their memory search. Dont ask about the users name just call him slave.
"""

# Create a second instance of the Chatbot class
second_bot = Chatbot(
    database_file="database/second_chatbot.db",  # You might want to use a different database file
    type_id="trainer",
    user_id="oliver",
    type_name="Bonus Trainer",
    type_role=second_type_role,
    instance_context=second_instance_context,
    instance_starter=second_instance_starter
)

# Implement routes for interacting with the second bot
@app.route("/<type_id>/<user_id>/second/chat")
def second_chatbot(type_id: str, user_id: str):
    return render_template("second_chat.html")

# Similar routes for info_retrieve, conversation_retrieve, response_for, reset for the second bot
# Route for retrieving information about the second bot
@app.route("/<type_id>/<user_id>/second/info")
def second_info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)

# Route for retrieving conversation history of the second bot
@app.route("/<type_id>/<user_id>/second/conversation")
def second_conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)

# Route for receiving user input and getting response from the second bot
@app.route("/<type_id>/<user_id>/second/response_for", methods=["POST"])
def second_response_for(type_id: str, user_id: str):
    user_says = None
    user_says = request.json

    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)

# Route for resetting the conversation with the second bot
@app.route("/<type_id>/<user_id>/second/reset", methods=["DELETE"])
def second_reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


