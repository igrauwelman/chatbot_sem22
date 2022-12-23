import random
import time
import re

class Attribute():
    def __init__(self, n, v, q):
        self.name = n
        self.value = v
        self.questions = q

class Student():
    name = Attribute('name', None, None)
    religious = Attribute('religious', None, None)
    got_gifts = Attribute('got gifts', None, None)
    gifts = Attribute('gifts', None, ['¿Qué te regalaron?', '¿Recibiste algún regalo?', '¿Recibiste regalos por navidad?'])
    tree = Attribute('tree', None, ['¿Tuviste un árbol de navidad?', 'Escuché que la gente en Alemania tiene un árbol de Navidad. ¿Tú también tenías un árbol?', '¿Tuviste un árbol de navidad? ¡Escuché que la gente en Alemania tradicionalmente decora un árbol para Navidad!'])
    food = Attribute('food', None, ['¿Qué comistéis en Navidad?', '¿Qué sueles comer en Navidad?', '¿Qué cenaste en Navidad?'])
    weather = Attribute('weather', None, ['¿Hacía frío en Navidad en tu ciudad?', '¿Cómo estuvo el tiempo en navidad?'])

student = Student()
attributes = [student.name, student.religious, student.gifts, student.tree, student.food, student.weather]
name_keywords = ['llamo', 'nombre']
response_keywords = ['sí', 'no']
food_keywords = ['come', 'como', 'comemos']
weather_keywords = ['nieve', 'sol', 'fría', 'frio', 'cálida', 'cálido', 'lluvia', 'lloviendo', 'lluvioso']
# negation_keywords = ['no', 'nada', 'tampoco', 'nunca', 'ni']
bot_should_prompt_question = True
current_attribute = None
next_question = None

# TODO: different responses to choose from for a given attribute? (similar to questions)
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
    # returns a question regarding the attribute or the end message
    def update_attribute_todo_and_choose_next(self, attribute_to_be_removed):
        global current_attribute
        global attributes

        attributes.remove(attribute_to_be_removed)

        if attributes:
            current_attribute = attributes[random.randint(0, len(attributes) - 1)]
            return current_attribute.questions[random.randint(0, len(current_attribute.questions) - 1)]
        else:
            return self.endMessage

    # TODO: differentiate between Spanish and Mexican bot in responses
    def chat(self, last_user_message, session):
        global current_attribute
        global next_question

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
                        current_attribute = student.name
                        student.name.value = self.process_user_name(keyword, index, splitMessage)
                        if student.name.value != None:
                            attributes.remove(student.name)
                            current_attribute = student.religious
                            return "¡Hola " + student.name.value + "! Hablemos de la vacaciones. ¿Es la Navidad una fiesta religiosa para ti?"
                        else:
                            return self.defaultResponse
            
        # RESPONSE KEYWORDS
        for keyword in response_keywords:
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if keyword == str('sí'):
                        if current_attribute == student.religious:
                            student.religious.value = True
                            next_question = self.update_attribute_todo_and_choose_next(student.religious)
                            return "Oh, I am curious how you celebrate christmas in your culture! En México, las familias preparan una gran celebración para toda la familia para Nochebuena. Y hay muchos juegos para niños, como golpear piñatas rellenas con frutas, dulces y regalos pequeños. " + next_question
                        elif current_attribute == student.gifts:
                            student.got_gifts.value = True
                            student.gifts.value = 'GIFTS THE STUDENT MENTIONED'
                            next_question = self.update_attribute_todo_and_choose_next(student.gifts)
                            return "¡Qué padre! Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños. " + next_question
                        elif current_attribute == student.tree:
                            student.tree.value = True
                            next_question = self.update_attribute_todo_and_choose_next(student.tree)
                            return "Eso suena genial. Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús " + next_question
                        elif current_attribute == student.weather:
                            student.weather.value = True
                            next_question = self.update_attribute_todo_and_choose_next(student.weather)
                            return "¡Wow, me encantaría ver eso! Mucha gente pasó las Navidades en la playa porque hacía mucho calor. Entonces, ¡el árbol de Navidad está hecho con una palmera! " + next_question
                    elif keyword == str('no'):
                        if current_attribute == student.religious:
                            student.religious.value = False
                            next_question = self.update_attribute_todo_and_choose_next(student.religious)
                            return "Oh, what do you normally do during the holiday season?"
                            # TODO: how to handle user that does not celebrate christmas?
                        elif current_attribute == student.gifts:
                            student.got_gifts.value = False
                            student.gifts.value = 'none'
                            next_question = self.update_attribute_todo_and_choose_next(student.gifts)
                            return "Some response about how gifts are not important. Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños. " + next_question
                        elif current_attribute == student.tree:
                            student.tree.value = False
                            next_question = self.update_attribute_todo_and_choose_next(student.tree)
                            return "No importa, no todas las familias tienen árbol de Navidad! Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús " + next_question
                        elif current_attribute == student.weather:
                            student.weather.value = False
                            next_question = self.update_attribute_todo_and_choose_next(student.weather)
                            return "¡Tampoco con nosotros! En nuestro país, mucha gente pasó las Navidades en la playa, ¡porque hacía mucho calor! Entonces, ¡el árbol de Navidad está hecho con una palmera! " + next_question
                    else:
                        return "??"

        # TODO: do the same for negation keywords --> check current attribute to find out what the student "negates"

        for keyword in food_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: save what student mentioned about what they ate
                    next_question = self.update_attribute_todo_and_choose_next(student.food)
                    return "¡Suena delicioso! En México, la mayoría de las familias come pavo con ensalada de manzana y pescado en salsa de tomate en Nochebuena, pero muchas otras familias también comen su propia comida tradicional, como tacos, enchiladas, quesadillas y burritos con guacamole. Y siempre hay salsa picante. " + next_question

        for keyword in weather_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about the weather
                    # differentiate between cold and warm weather in the bot's response
                    next_question = self.update_attribute_todo_and_choose_next(student.weather)
                    return 'aha... ' + next_question  


        return "..."

    def welcome(self):
        return "¡Hola! Me llamo " + self.name + " y soy de " + self.country + " ¿Cómo te llamas?"
