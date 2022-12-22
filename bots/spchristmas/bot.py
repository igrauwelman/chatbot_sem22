import random
import time
import re

class BooleanAttribute():
    value = None

class StringAttribute():
    value = None

class Student():
    name = StringAttribute()
    religious = BooleanAttribute()
    got_gifts = BooleanAttribute()
    gifts = StringAttribute()
    tree = BooleanAttribute()
    food = StringAttribute()
    weather = BooleanAttribute()

student = Student()
attributes = ['name', 'religious', 'gifts', 'tree', 'food', 'weather']
name_keywords = ['llamo', 'nombre']
response_keywords = ['sí', 'no']
food_keywords = ['come', 'como', 'comemos']
# negation_keywords = ['no', 'nada', 'tampoco', 'nunca', 'ni']
bot_should_prompt_question = True
current_attribute = None

class Bot:
    name = random.choice(['José', 'Alma'])
    if name == 'José':
        country = 'México'
    elif name == 'Alma':
        country = 'España'
    avatar = 'avatar/perroquet.png'
    defaultResponse = "Lo siento, no entiendo lo que me quieres decir... ¿Lo podrías repetir, por favor?"
    endMessage = "It was so nice learning about how you spent the holidays!"
    age = 15

    def process_user_name(self, keyword, index, splitMessage):
        if keyword == 'llamo':
            # "Me llamo NAME"
            return splitMessage[index + 1]
        elif keyword == 'nombre':
            # "Mi nombre es NAME"
            return splitMessage[index + 2]
        else:
            return None

    # remove finished attribute and randomly choose the next one
    # if there is no attribute left, end the conversation
    def update_attribute_todo_and_choose_next(self, current_attribute):
        attributes.remove(current_attribute)
        if len(attributes) == 0:
            return self.endMessage
        else:
            current_attribute = attributes[random.randint(0, len(attributes) - 1)]
            # TODO: add questions the bot could ask to get info about the attribute, so that one 
            # of the questions can be returned here as a string to be able to concatenate it to
            # the bot's response to the student's answer regarding the previous attribute
            return current_attribute

    # TODO: differentiate between Spanish and Mexican bot in responses
    def chat(self, last_user_message, session):
        global current_attribute

        # TODO: incorporate in conversational flow
        # if bot_should_prompt_question == False:
        #     time.sleep(random.randint(10,20))

        # response delay for authenticity
        time.sleep(random.randint(1,5))
        
        # remove punctuation
        last_user_message = re.sub(r'[^\w\s]', '', last_user_message)

        # split message into word chunks
        splitMessage = last_user_message.split()

        # NAME
        for keyword in name_keywords:
            for index, string in enumerate(splitMessage):
                if string == keyword:
                    # if student.name.status == str('finished'):
                    if student.name.value != None:
                        # TODO: check whether student changed their name ?
                        # alternatively, just say "Okay, NAME" and prompt the next question
                        return "¡Lo sé, " + student.name.value + "! "
                    else:
                        current_attribute = 'name'
                        student.name.value = self.process_user_name(keyword, index, splitMessage)
                        if student.name.value != None:
                            attributes.remove(current_attribute)
                            current_attribute = 'religious'
                            return "¡Hola " + student.name.value + "! Hablemos de la vacaciones. ¿Es la Navidad una fiesta religiosa para ti?"
                        else:
                            return self.defaultResponse
            
        # RESPONSE KEYWORDS
        for keyword in response_keywords:
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if keyword == str('sí'):
                        if current_attribute == str('religious'):
                            student.religious.value = True
                            # student.religious.status = 'finished'
                            current_attribute = self.update_attribute_todo_and_choose_next('religious')
                            return "Oh, I am curious how you celebrate christmas in your culture! + question about " + current_attribute
                        elif current_attribute == str('gifts'):
                            student.got_gifts.value = True
                            student.gifts.value = 'GIFTS THE STUDENT MENTIONED'
                            # student.got_gifts.status = 'finished'
                            current_attribute = self.update_attribute_todo_and_choose_next('gifts')
                            return "¡Qué padre! Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños. + question about " + current_attribute
                        elif current_attribute == str('tree'):
                            student.tree.value = True
                            current_attribute = self.update_attribute_todo_and_choose_next('tree')
                            return "Eso suena genial. Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús + question about " + current_attribute
                        elif current_attribute == str('weather'):
                            student.weather.value = True
                            current_attribute = self.update_attribute_todo_and_choose_next('weather')
                            return "¡Wow, me encantaría ver eso! Mucha gente pasó las Navidades en la playa porque hacía mucho calor. Entonces, ¡el árbol de Navidad está hecho con una palmera! + question about " + current_attribute
                    elif keyword == str('no'):
                        if current_attribute == str('religious'):
                            student.religious.value = False
                            # student.religious.status = 'finished'
                            current_attribute = self.update_attribute_todo_and_choose_next('religious')
                            return "Oh, what do you normally do during the holiday season?"
                            # TODO: how to handle user that does not celebrate christmas?
                        elif current_attribute == str('gifts'):
                            student.got_gifts.value = False
                            student.gifts.value = 'none'
                            # student.gifts.status = 'finished'
                            current_attribute = self.update_attribute_todo_and_choose_next('gifts')
                            return "Some response about how gifts are not important + question about " + current_attribute
                        elif current_attribute == str('tree'):
                            student.tree.value = False
                            current_attribute = self.update_attribute_todo_and_choose_next('tree')
                            return "No importa, no todas las familias tienen árbol de Navidad! Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús + question about " + current_attribute
                        elif current_attribute == str('weather'):
                            student.weather.value = False
                            current_attribute = self.update_attribute_todo_and_choose_next('weather')
                            return "¡Tampoco con nosotros! En nuestro país, mucha gente pasó las Navidades en la playa, ¡porque hacía mucho calor! Entonces, ¡el árbol de Navidad está hecho con una palmera! + question about " + current_attribute
                    else:
                        return "??"

        # TODO: do the same for negation keywords --> check current attribute to find out what the student "negates"

        for keyword in food_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # save what student mentioned about what they ate
                    current_attribute = self.update_attribute_todo_and_choose_next('food')
                    return "¡Suena delicioso! En México, la mayoría de las familias come pavo con ensalada de manzana y pescado en salsa de tomate en Nochebuena, pero muchas otras familias también comen su propia comida tradicional, como tacos, enchiladas, quesadillas y burritos con guacamole. Y siempre hay salsa picante. + question about " + current_attribute


        return "..."

    def welcome(self):
        return "¡Hola! Me llamo " + self.name + " y soy de " + self.country + " ¿Cómo te llamas?"
