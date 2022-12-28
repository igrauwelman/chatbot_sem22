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

# instantiate student, attribute todo list and bot info todo list
student = Student()
attributes = [student.name, student.religious, student.gifts, student.tree, student.food, student.weather]
bot_infos = ['gifts', 'tree', 'food', 'weather']

# keywords
# TODO: also add words like 'arbol' for 'árbol' etc?
name_keywords = ['llamo', 'nombre', 'soy']
response_keywords = ['sí', 'si', 'no']
food_keywords = ['come', 'como', 'comemos', 'comiste', 'comistéis', 'comer', 'comisteis', 'comimos']
weather_keywords = ['nieve', 'sol', 'fría', 'fria', 'frio', 'frío', 'cálida', 'calida', 'cálido', 'calido', 'lluvia', 'lloviendo', 'lluvioso', 'tiempo']
gift_keywords = ['regalos', 'regalo', 'regalaron', 'tengo', 'recibí', 'recibi']
tree_keywords = ['árbol', 'arbol', 'decoras', 'decora', 'adornos', 'decoración', 'decoracion']
# TODO: negation_keywords = ['no', 'nada', 'tampoco', 'nunca', 'ni', 'ningún', 'ninguna', 'ninguno']

# variables
# indicates if bot should ask a next question or if it should wait for the user to ask a question
bot_should_prompt_question = True
# current attribute the bot is asking about
current_attribute = None
# next question the bot should ask
next_question = None
# final message
bot_response = None
# reaction to user message (without potential next question)
reaction = None

# dictionary with responses
response_dict = {
    "introduction": ["""! Hablemos de las vacaciones. ¿Celebras Navidad?""",
                    """! ¿Qué tal las vacaciones? ¿Celebras la Nacidad?"""],

    "religious": ["""También celebré la Navidad. 
                    En la Noche Buena, el 24 de diciembre, toda la familia se reúne para cenar, 
                    pero la Navidad en España comienza el 22 de diciembre con el sorteo de la lotería, 
                    lo llamamos "El Gordo" de Navidad porque el premio principal es muy grande. 
                    Todo el mundo participa y muchos ganan algo, por eso nos reunimos en las calles 
                    para celebrar juntos las ganancias.""",
                 """Yo tambíen. En España, la Navidad comienza el 22 de diciembre con el sorteo de la lotería 
                    conocido como "El Gordo". Este sorteo es muy popular porque el premio principal 
                    es muy grande. Muchas personas participan y muchas de ellas ganan algo, 
                    lo que nos lleva a reunirnos en las calles para celebrar juntos las ganancias. 
                    La Noche Buena, el 24 de diciembre, es cuando toda la familia se reúne para cenar."""],

    "food": ["""Como entrante comemos tapas de jamón o queso, por ejemplo. 
                Luego tomamos una sopa, seguida de pescado frito o carne, que me gusta muchísimo. 
                Pero lo que más espero es el postre, por ejemplo galletas como polvorones o mantecados, 
                pero mi dulce favorito es el turrón. Es una especialidad navideña española y lo comemos 
                entre o después de la comida festiva. Se compone de almendras tostadas, azúcar, clara de 
                huevo y miel. A veces se añade fruta confitada, chocolate o mazapán.""",
            """Como entrante en la cena navideña en España, a menudo se sirven tapas de jamón o queso. 
                Después se toma una sopa, seguida de pescado frito o carne. Pero lo que muchos esperan 
                con más ansias es el postre, que puede incluir galletas como polvorones o mantecados. 
                Uno de los dulces navideños más populares en España es el turrón, que se compone de 
                almendras tostadas, azúcar, clara de huevo y miel. A veces también se añade fruta confitada, 
                chocolate o mazapán. El turrón es una especialidad navideña española y se suele comer entre 
                o después de la comida festiva."""],

    "gifts": ["""¡Cómo mola! La entrega de regalos se celebra en España el 6 de enero. Es el día de los Reyes Magos. 
                Traen regalos a los niños. Tradicionalmente hay un "Resoco de Reyes". Es un pastel en forma de anillo 
                con una figura en su interior. Quien tenga la figura en su pieza puede llamarse rey durante todo el día.""",
            """ ¡Cómo mola! En España, el día de los Reyes Magos, el 6 de enero, es cuando se celebra la entrega de regalos. 
                Los Reyes Magos traen regalos a los niños. También se celebra el "Resoco de Reyes", que es un pastel 
                en forma de anillo con una figura escondida en su interior. Quien tenga la figura en su porción puede 
                considerarse rey durante todo el día."""],

    "tree": ["""No tenemos árbol de Navidad, pero ponemos un belén con la familia y lo decoramos. 
                Pero sé que algunos de mis amigos también tienen ya un árbol de Navidad.""",
            """En lugar de tener un árbol de Navidad, en nuestra familia ponemos un belén y lo decoramos. Sin embargo, 
                sé que algunos de mis amigos sí tienen un árbol de Navidad."""],

    "weather": ["""Vivo en Málaga, que está en el mar Mediterráneo. En diciembre tenemos 
                    unos 16 grados, por eso aquí no nieva. Pero a dos horas estamos en Sierra Nevada, hay nieve en invierno 
                    y podemos esquiar, eso me encanta.""",
                """Me encantaría ver eso. Actualmente vivo en Málaga, que se encuentra en la costa del mar Mediterráneo. 
                    En diciembre, las temperaturas aquí suelen estar alrededor de los 16 grados, por lo que no nevamos. 
                    Sin embargo, a solo dos horas de distancia está Sierra Nevada, donde sí hay nieve en invierno y 
                    es posible esquiar. ¡Eso me encanta!"""]

}

# TODO: different responses to choose from for a given attribute? (similar to questions)
# TODO: let the bot wait if the student asks a question --> what if the student does not send a message? (chat function will only be called if user sends a message)
class Bot:
    name = 'Alma'
    country = 'España'
    avatar = 'avatar/perroquet.png'
    defaultResponse = "Lo siento, no entiendo. ¿Puede repetir eso de nuevo?"
    endMessage = "It was so nice learning about how you spent the holidays!"
    age = 15

    # return the user name or None in case of failure
    def process_user_name(self, keyword, index, splitMessage):
        for index, string in enumerate(splitMessage):
            string = string.lower()
            if keyword == 'llamo' or keyword == 'soy':
                # "Me llamo NAME"
                # 'Yo soy NAME'
                return splitMessage[index + 1]
            elif keyword == 'nombre':
                # "Mi nombre es NAME"
                return splitMessage[index + 2]
            else:
                return None

    # remove finished attribute
    def update_attribute_todo_list(self, attribute_to_be_removed):
        global attributes

        for attribute in attributes:
            if attribute == attribute_to_be_removed:
                attributes.remove(attribute_to_be_removed)
                break

    # randomly choose the next attribute
    # if there is no attribute left, end the conversation
    # returns a random question regarding the attribute or the end message
    def choose_next_attribute_and_question(self):
        global current_attribute
        global attributes

        if attributes:
            current_attribute = attributes[random.randint(0, len(attributes) - 1)]
            return current_attribute.questions[random.randint(0, len(current_attribute.questions) - 1)]
        else:
            return self.endMessage
    
    # generate response based on bot_should_prompt_question
    def generate_response(self, response, current_attr):
        global next_question
        global attributes
        global bot_should_prompt_question 

        if bot_should_prompt_question:
            if current_attr:
                self.update_attribute_todo_list(current_attr)
            next_question = self.choose_next_attribute_and_question()
            return response + ' ' + next_question
        else:
            if current_attr:
                self.update_attribute_todo_list(current_attr)
            return '(student should write a message) ' + response
        
    # generate direct response to a user question (bot should ask back)
    def generate_response_to_user_question(self, response, current_attr):
        global next_question

        next_question = random.choice(["¿Y tú?", current_attr.questions[random.randint(0, len(current_attribute.questions) - 1)]])
        return response + ' ' + next_question

    # if info is still in bot_infos, the info was not given to the user yet
    def check_whether_info_already_given(self, info):
        global bot_infos

        for i in bot_infos:
            if i == info:
                return False
        return True

    def chat(self, last_user_message, session):
        global current_attribute
        global next_question
        global bot_response
        global bot_should_prompt_question
        global bot_infos
        global reaction
        global response_dict

        # randomly select whether bot should prompt a question after reacting to user message
        bot_should_prompt_question = random.choice([True, False])

        # response delay for authenticity
        # check how many characters are in the response and multiply with millisecond for delay
        time.sleep(random.randint(3,5))
        
        # remove punctuation
        last_user_message_cleaned = re.sub(r'[^\w\s]', '', last_user_message)

        # split message into word chunks
        splitMessage = last_user_message_cleaned.split()

        # check whether user asked back
        if last_user_message.__contains__('tú?') or last_user_message.__contains__('tu?'):
            for keyword in response_keywords:
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        if keyword == str('sí') or keyword == str('si'):
                            if current_attribute == student.religious:
                                student.religious.value = True
                                bot_response = self.generate_response(random.choice(response_dict['religious']), student.religious)
                                return bot_response
                            elif current_attribute == student.gifts:
                                student.got_gifts.value = True
                                student.gifts.value = 'GIFTS THE STUDENT MENTIONED'
                                if self.check_whether_info_already_given('gifts'):
                                    reaction = '¡Cómo mola! I already told you about my gifts blabla'
                                else:
                                    reaction = '¡Cómo mola! También recibí regalos.' + random.choice(response_dict['gifts'])
                                    bot_infos.remove('gifts')
                                bot_response = self.generate_response(reaction, student.gifts)
                                return bot_response
                            elif current_attribute == student.tree:
                                student.tree.value = True
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'Eso suena genial. I already told you that I did not have a christmas tree blabla'
                                else:
                                    reaction = 'Eso suena genial.' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                return bot_response
                            elif current_attribute == student.weather:
                                student.weather.value = True
                                if self.check_whether_info_already_given('weather'):
                                    reaction = '¡Wow, me encantaría ver eso! I already told you that it was warm blabla'
                                else:
                                    reaction = '¡Wow, me encantaría ver eso!' + random.choice(response_dict['weather'])
                                    bot_infos.remove('weather')
                                bot_response = self.generate_response(reaction, student.weather)
                        elif keyword == str('no'):
                            if current_attribute == student.religious:
                                student.religious.value = False
                                bot_response = self.generate_response('I do celebrate christmas! What do you normally do during the holiday season?', student.religious)
                                return bot_response
                                # next_question = self.update_attribute_todo_and_choose_next(student.religious)
                                # return "Oh, what do you normally do during the holiday season?"
                                # TODO: how to handle user that does not celebrate christmas?
                            elif current_attribute == student.gifts:
                                student.got_gifts.value = False
                                student.gifts.value = 'none'
                                if self.check_whether_info_already_given('gifts'):
                                    reaction = 'Some response about how gifts are not important. I already told you that I got gifts, but the most important thing is enjoying the time with family blabla'
                                else:
                                    reaction = 'Some response about how gifts are not important.' + random.choice(response_dict["gifts"])
                                    bot_infos.remove('gifts')
                                bot_response = self.generate_response(reaction, student.gifts)
                                return bot_response
                            elif current_attribute == student.tree:
                                student.tree.value = False
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'No importa, no todas las familias tienen árbol de Navidad! I already told you that we did not have a tree as well'
                                else:
                                    reaction = 'No importa, no todas las familias tienen árbol de Navidad!' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                return bot_response
                            elif current_attribute == student.weather:
                                student.weather.value = False
                                if self.check_whether_info_already_given('weather'):
                                    reaction = 'some reaction to not cold weather without repeating that it was not cold for bot either... I already told you that it was warm blabla'
                                else:
                                    reaction = '¡Tampoco con nosotros!' + random.choice(response_dict['weather'])
                                    bot_infos.remove('weather')
                                bot_response = self.generate_response(reaction, student.weather)
                                return bot_response
                        # fallback response
                        else:
                            return "??"

            if current_attribute == student.food:
                if self.check_whether_info_already_given('food'):
                    reaction = '¡Suena delicioso! I already told you that we eat blabla'
                else:
                    reaction = '¡Suena delicioso!' + random.choice(response_dict['food'])
                    bot_infos.remove('food')
                bot_response = self.generate_response(reaction, student.food)
                return bot_response

            # WEATHER
            for keyword in weather_keywords:
                for index, string in enumerate(splitMessage):
                    string.lower()
                    if string == keyword:
                        # TODO: process what the student mentioned about the weather
                        # differentiate between cold and warm weather in the bot's response
                        if self.check_whether_info_already_given('weather'):
                            reaction = 'aha... I already told you about the weather blabla'
                        else:
                            reaction = 'aha' + random.choice(response_dict['weather'])
                            bot_infos.remove('weather')
                        bot_response = self.generate_response(reaction, student.weather)
                        return bot_response
            
            for keyword in gift_keywords:
                for index, string in enumerate(splitMessage):
                    string.lower()
                    if string == keyword:
                        # TODO: process what the student mentioned about their gifts
                        if self.check_whether_info_already_given('gifts'):
                            reaction = 'aha (Geschenke). I already told you that I got gifts blabla'
                        else:
                            reaction = '¡Qué generoso!' + random.choice(response_dict['gifts'])
                            bot_infos.remove('gifts')
                        bot_response = self.generate_response(reaction, student.gifts)
                        return bot_response

        # TODO: what to do if student does not type anything?
        # if bot waited for student to type a message, process the message to find out what they asked a question about
        if bot_should_prompt_question == False:
            # check if user asked a question
            if last_user_message.__contains__("?"):
                # remove punctuation
                last_user_message = re.sub(r'[^\w\s]', '', last_user_message)

                # split message into word chunks
                splitMessage = last_user_message.split()

                # check if user asked about gifts
                for keyword in gift_keywords:
                    for index, string in enumerate(splitMessage):
                        if string == keyword:
                            if self.check_whether_info_already_given('gifts'):
                                bot_response = self.generate_response('Haha, I already told you: Tenía la figura en mi pieza este año. + hier einfügen was Alma als Geschenk bekommen hat (Geld, Videospiel, ...)', None)
                            current_attribute = student.gifts
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['gifts'])+ 'hier einfügen was Alma als Geschenk bekommen hat (Geld, Videospiel, ...)', current_attribute)
                            bot_infos.remove('gifts')
                            return bot_response

                # check if user asked about tree/decoration
                for keyword in tree_keywords:
                    for index, string in enumerate(splitMessage):
                        if string == keyword:
                            current_attribute = student.tree
                            bot_response = self.generate_response(random.choice(response_dict['tree']), current_attribute)
                            bot_infos.remove('tree')
                            return bot_response

                # check if user asked about food
                for keyword in food_keywords:
                    for index, string in enumerate(splitMessage):
                        if string == keyword:
                            current_attribute = student.food
                            bot_response = self.generate_response(random.choice(response_dict["food"]), current_attribute)
                            bot_infos.remove('food')
                            return bot_response

                # check if user asked about weather
                for keyword in weather_keywords:
                    for index, string in enumerate(splitMessage):
                        if string == keyword:
                            current_attribute = student.weather
                            bot_response = self.generate_response(random.choice(response_dict['weather']), current_attribute)
                            bot_infos.remove('weather')
                            return bot_response

                # fallback response
                return 'user asked a question'
            else:
                bot_should_prompt_question = True
                # bot_response = self.generate_response('', current_attribute)
                # return 'user did not ask a question' + ' ' + bot_response
                # continue with code below

        # NAME
        # TODO: if only one word is returned this must be the name
        for keyword in name_keywords:
            for index, string in enumerate(splitMessage):
                string = string.lower()
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
                            bot_should_prompt_question = True
                            return "¡Hola " + student.name.value + random.choice(response_dict['introduction'])
                        else:
                            return self.defaultResponse
            
        # RESPONSE KEYWORDS
        for keyword in response_keywords:
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if keyword == str('sí') or keyword == str('si'):
                        if current_attribute == student.religious:
                            student.religious.value = True
                            bot_response = self.generate_response(random.choice(response_dict['religious']), student.religious)
                            return bot_response
                        elif current_attribute == student.gifts:
                            student.got_gifts.value = True
                            student.gifts.value = 'GIFTS THE STUDENT MENTIONED'
                            if self.check_whether_info_already_given('gifts'):
                                reaction = '¡Cómo mola!'
                            else:
                                reaction = random.choice(response_dict['gifts'])
                                bot_infos.remove('gifts')
                            bot_response = self.generate_response(reaction, student.gifts)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = True
                            if self.check_whether_info_already_given('tree'):
                                reaction = 'Eso suena genial.'
                            else:
                                reaction = random.choice(response_dict['tree'])
                                bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = True
                            if self.check_whether_info_already_given('weather'):
                                reaction = '¡Guau, me encantaría ver eso!'
                            else:
                                reaction = '¡Guau, me encantaría ver eso!' + random.choice(response_dict['weather'])
                                bot_infos.remove('weather')
                            bot_response = self.generate_response(reaction, student.weather)
                    elif keyword == str('no'):
                        if current_attribute == student.religious:
                            student.religious.value = False
                            bot_response = self.generate_response('Si no celebras las Navidades, ¿hiciste algo más especial durante las vacaciones?', student.religious)
                            return bot_response
                            # next_question = self.update_attribute_todo_and_choose_next(student.religious)
                            # return "Oh, what do you normally do during the holiday season?"
                            # TODO: how to handle user that does not celebrate christmas?
                        elif current_attribute == student.gifts:
                            student.got_gifts.value = False
                            student.gifts.value = 'none'
                            if self.check_whether_info_already_given('gifts'):
                                reaction = 'Some response about how gifts are not important.'
                            else:
                                reaction = 'Some response about how gifts are not important.' + random.choice(response_dict['gifts'])
                                bot_infos.remove('gifts')
                            bot_response = self.generate_response(reaction, student.gifts)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = False
                            if self.check_whether_info_already_given('tree'):
                                reaction = 'No importa, no todas las familias tienen árbol de Navidad!'
                            else:
                                reaction = 'No importa, no todas las familias tienen árbol de Navidad!' + random.choice(response_dict['tree'])
                                bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = False
                            if self.check_whether_info_already_given('weather'):
                                reaction = 'some reaction to not cold weather without repeating that it was not cold for bot either'
                            else:
                                reaction = '¡Tampoco con nosotros!' + random.choice(response_dict['weather'])
                                bot_infos.remove('weather')
                            bot_response = self.generate_response(reaction, student.weather)
                            return bot_response
                    # fallback response
                    else:
                        return "??"

        # TODO: do the same for negation keywords --> check current attribute to find out what the student "negates"

        # FOOD
        for keyword in food_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: save what student mentioned about what they ate
                    if self.check_whether_info_already_given('food'):
                        reaction = '¡Suena delicioso!'
                    else:
                        reaction = '¡Suena delicioso!' + random.choice(response_dict['food'])
                        bot_infos.remove('food')
                    bot_response = self.generate_response(reaction, student.food)
                    return bot_response

        # WEATHER
        for keyword in weather_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about the weather
                    # differentiate between cold and warm weather in the bot's response
                    if self.check_whether_info_already_given('weather'):
                        reaction = 'aha...'
                    else:
                        reaction = '¡Qué interesante!' + random.choice(response_dict['weather'])
                        bot_infos.remove('weather')
                    bot_response = self.generate_response(reaction, student.weather)
                    return bot_response
        
        # GIFTS
        for keyword in gift_keywords:
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about their gifts
                    if self.check_whether_info_already_given('gifts'):
                        reaction = '¡Qué generoso!'
                    else:
                        # schauen, ob das mit dem plus hier funktioniert
                        reaction = '¡Qué generoso!' + random.choice(response_dict['gifts'])
                        bot_infos.remove('gifts')
                    bot_response = self.generate_response(reaction, student.gifts)
                    return bot_response


        # fallback response
        return ' '

    def welcome(self):
        return "¡Hola! Me llamo " + self.name + " y soy de " + self.country + " ¿Cómo te llamas?"
