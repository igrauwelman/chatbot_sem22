class Bot:

    name = 'Perroquet'
    avatar = 'avatar/perroquet.png'

    def welcome(self):
        return "Bonjour! Je vais répéter tout ce que tu dis."

    def chat(self, last_user_message, session):
        return last_user_message
