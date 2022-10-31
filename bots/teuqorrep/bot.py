class Bot:

    name = 'Teuqorrep'
    avatar = 'avatar/teuqorrep.png'

    def welcome(self):
        return "Bonjour! Je vais répéter tout ce que tu dis à l'envers."

    def chat(self, last_user_message, session):
        return last_user_message[::-1]
