from main_agent import create_agent

agents_by_user = {}


def agent_for_user(user_token):
    chat_agent = agents_by_user.get(user_token)

    if chat_agent is None:
        chat_agent = create_agent()
        agents_by_user[user_token] = chat_agent

    return chat_agent
