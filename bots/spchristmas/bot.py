import random
import time
import re

class Attribute():
    def __init__(self, n, v, q):
        self.name = str(n)
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

# KEYWORDS
curse_keywords = ['ano', 'puta madre', 'puta', 'coño', 'cojones', 'cabrón', 'joder', 'sex', 'penis', 'arschloch']
name_keywords = ['llamo', 'nombre', 'soy']
response_keywords = ['sí', 'si', 'no']
food_keywords = ['come', 'como', 'comemos', 'comiste', 'comistéis', 'comer', 'comisteis', 'comimos']
weather_keywords = ['nieve', 'sol', 'fría', 'fria', 'frio', 'frío', 'cálida', 'calida', 'cálido', 'calido', 'lluvia', 'lloviendo', 'lluvioso', 'tiempo']
gift_keywords = ['regalos', 'regalo', 'regalaron', 'tengo', 'recibí', 'recibi']
tree_keywords = ['árbol', 'arbol', 'decoras', 'decora', 'adornos', 'decoración', 'decoracion']
# TODO: negation_keywords = ['no', 'nada', 'tampoco', 'nunca', 'ni', 'ningún', 'ninguna', 'ninguno']

# VARIABLES
# indicates if bot should ask a next question or if it should wait for the user to ask a question
bot_should_prompt_question = True
# current attribute the bot is asking about
current_attribute = None
# reaction to user message (without potential next question)
reaction = None
# next question the bot should ask
next_question = None
# final message
bot_response = None
# counter for inquiries (how often did the bot already ask for more info?)
inq_counter = 0
# what bot currently asks more about
current_inq = None

# TODO: reactions to food responses by the user to make more conversation
food_response_reactions = ["Did you like it? ", "Do you eat this every year?"]

# TODO: reactions to weather responses by the user to make more conversation
# TODO: reactions to gift responses by the user (without sí or no) to make more conversation

# reactions to simple "sí" or "no" responses by the user to get more info/make more conversation
short_response_dict = {
    "gifts_si": ["""¡Cuéntame más! ¿Qué regalos has recibido?""",
                """Genial, ¿qué regalos has recibido?""",
                """Guay, ¿cuál fue tu regalo favorito?""",
                """Genial, ¿cuál fue tu regalo favorito?"""],

    "gifts_si_response": ["""¡Suena genial!""",
                        """¡Suena increíble!""",
                        """Qué bien, seguro que ahora eres muy feliz."""],

    "gifts_no": ["""Los regalos no son importantes, ¿verdad? ¿Qué más hiciste en Nochebuena?"""],

    "gifts_no_response": ["""Entiendo. El objetivo principal de la Navidad es pasar tiempo con las personas que queremos, ¿verdad? :)"""],

    "tree_si": ["""Genial, ¿de qué color era la decoración?""",
                """¡Qué bien! ¿Cuándo lo decoráis normalmente? He oído que algunas familias alemanas decoran su árbol muy temprano, mientras que otras lo hacen sólo en Nochebuena.""",
                """¿Quién ha decorado el árbol?"""],

    "tree_si_response": ["""¡Qué bien!""",
                    """¡Qué guay!""",
                    """¡Genial!""",
                    """¡Qué lindo!""",
                    """¡Qué bonito!"""],

    "tree_no": ["""¿Tenéis otra decoración tradicional?"""],

    "other_deco_inq": ["""¿Qué tipo de decoración?"""],

    "other_deco_si": ["""¡Muy interesante!"""],

    "other_deco_no": ["""Parece que la decoración no es importante en tu familia."""],

    "weather_si": ["""Vaya, ¿también nevó?"""],
    
    "snow_si": ["""¡No me digas!"""],

    "snow_no": ["""¡Qué pena!""",
                """¡Qué lástima!"""],

    "weather_no": ["""¿Has echado de menos la nieve?"""],

    "missed_snow_si": ["""¡Entiendo!"""],

    "missed_snow_no": ["""Vale, no a todos les gusta la nieve :)"""]
}

# dictionary with responses
response_dict = {
    "introduction": ["""Hablemos de las vacaciones. ¿Celebras Navidad?""",
                    """¿Qué tal las vacaciones? ¿Celebras la Navidad?"""],

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

    "gifts": ["""La entrega de regalos se celebra en España el 6 de enero. Es el día de los Reyes Magos. 
                Traen regalos a los niños. Tradicionalmente hay un "Resoco de Reyes". Es un pastel en forma de anillo 
                con una figura en su interior. Quien tenga la figura en su pieza puede llamarse rey durante todo el día.""",
            """En España, el día de los Reyes Magos, el 6 de enero, es cuando se celebra la entrega de regalos. 
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
                """Actualmente vivo en Málaga, que se encuentra en la costa del mar Mediterráneo. 
                    En diciembre, las temperaturas aquí suelen estar alrededor de los 16 grados, por lo que no nevamos. 
                    Sin embargo, a solo dos horas de distancia está Sierra Nevada, donde sí hay nieve en invierno y 
                    es posible esquiar. ¡Eso me encanta!"""]

}

class Bot:
    name = 'Alma'
    country = 'España'
    avatar = 'avatar/span_alma.jpeg'
    defaultResponse = 'Lo siento, no entiendo. ¿Puede repetir eso de nuevo?'
    endMessage = 'Ahora tengo deberes que hacer. Fue guay charlar contigo, aprendí mucho sobre las tradiciones alemanas. ¡Ojalá podamos repetirlo pronto!'
    age = 15

    # return the user name or None in case of failure
    def process_user_name(self, keyword, index, splitMessage):
        if keyword == 'llamo' or keyword == 'soy':
            # "Me llamo NAME"
            # 'Yo soy NAME'
            return splitMessage[index + 1]
        elif keyword == 'nombre':
            # "Mi nombre es NAME"
            return splitMessage[index + 2]
        else:
            return None

    # if attribute is still in attributes, the user did not talk about the attribute yet
    def check_whether_attribute_already_finished(self, attr):
        global attributes

        for a in attributes:
            if a == attr:
                return False
        return True

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
            # Null check
            if current_attribute.questions == None:
                return ' '
            else:
                return current_attribute.questions[random.randint(0, len(current_attribute.questions) - 1)]
        else:
            return self.endMessage
    
    # generate response based on bot_should_prompt_question
    def generate_response(self, response, current_attr):
        global next_question
        global attributes
        global bot_should_prompt_question 
        global response_dict

        if current_attr:
            self.update_attribute_todo_list(current_attr)
            if bot_should_prompt_question: 
                next_question = self.choose_next_attribute_and_question()
                return response + ' ' + next_question
            else:
                return response
        
    # generate direct response to an unprompted user question (bot should ask back if attribute not finished yet)
    def generate_response_to_user_question(self, response, current_attr):
        global next_question
        global bot_should_prompt_question

        # if student does not celebrate christmas, bot should not ask about gifts etc.
        if student.religious.value == False:
            return response
        else:
            if self.check_whether_attribute_already_finished(current_attr):
                if bot_should_prompt_question:
                    next_question = self.choose_next_attribute_and_question()
                    return response + ' ' + next_question
                return response
            next_question = random.choice(['¿Y tú?', current_attr.questions[random.randint(0, len(current_attr.questions) - 1)]])
            return response + ' ' + next_question

    # if info is still in bot_infos, the info was not given to the user yet
    def check_whether_info_already_given(self, info):
        global bot_infos

        for i in bot_infos:
            if i == info:
                return False
        return True

    # response delay for authenticity
    def delay_response(self, bot_message):
        delay = len(bot_message) * 0.01
        time.sleep(delay)

    def chat(self, last_user_message, session):
        global current_attribute
        global next_question
        global bot_response
        global bot_should_prompt_question
        global bot_infos
        global reaction
        global response_dict
        global inq_counter
        global current_inq

        # randomly select whether bot should prompt a question after reacting to user message
        bot_should_prompt_question = random.choice([True, False])
        
        # remove punctuation
        last_user_message_cleaned = re.sub(r'[^\w\s]', '', last_user_message)

        # split message into word chunks
        splitMessage = last_user_message_cleaned.split()

        for keyword in curse_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    # bot_response = 'Bitte antworte auf die Frage ohne unangemessene Ausdrücke.'
                    bot_response = 'Por favor, responda la pregunta sin usar lenguaje inapropiado.'
                    return bot_response

        # check whether user asked back
        if last_user_message.__contains__('tú?') or last_user_message.__contains__('tu?'):
            # for messages containing "sí" or "no" (or variations)
            for keyword in response_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        if keyword == str('sí') or keyword == str('si'):
                            if current_attribute == student.tree and inq_counter == 1 and len(splitMessage) > 3:
                                # TODO: not sure, because user could have said "Ah, muy interesante! Si, we have other decoration" for example
                                # we are here if user said that they do not have a tree, but said that they have other traditional decoration (probably already stated what kind of decoration due to the message length) and added "y tú?" (or variations)
                                inq_counter = 0
                                current_inq = None
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'I already told you that we have the Krippe blabla'
                                else:
                                    reaction = random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = random.choice(short_response_dict['other_deco_si']) + ' ' + str(self.generate_response(reaction, student.tree))
                                self.delay_response(bot_response)
                                return bot_response
                            # note: len("sí y tú?") = 3
                            if len(splitMessage) < 4:
                                if current_attribute == student.gifts:
                                    # we are here if the bot asked about gifts for the first time and the user answered "sí y tú?" (or variations)
                                    inq_counter += 1
                                    current_inq = 'gifts_si' 
                                    if self.check_whether_info_already_given('gifts'):
                                        reaction = 'I already told you about my gifts blabla'
                                    else:
                                        reaction = 'También recibí regalos.' + random.choice(response_dict['gifts'])
                                        bot_infos.remove('gifts')
                                    bot_response = random.choice(short_response_dict['gifts_si']) + ' ' + reaction
                                    self.delay_response(bot_response)
                                    return bot_response
                                elif current_attribute == student.tree:
                                    if inq_counter == 1:
                                        # we are here if user said that they do not have a tree, but said that they have other traditional decoration (just "sí") and added "y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'other_deco'
                                        if self.check_whether_info_already_given('tree'):
                                            reaction = 'I already told you that we have the Krippe blabla'
                                        else:
                                            reaction = random.choice(response_dict['tree'])
                                            bot_infos.remove('tree')
                                        bot_response = random.choice(short_response_dict['other_deco_inq']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                                    elif inq_counter == 0:
                                        # we are here if the bot asked about the tree for the first time and the user answered "sí y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'tree_si' 
                                        if self.check_whether_info_already_given('tree'):
                                            reaction = 'I already told you that I did not have a christmas tree blabla'
                                        else:
                                            reaction = random.choice(response_dict['tree'])
                                            bot_infos.remove('tree')
                                        bot_response = random.choice(short_response_dict['tree_si']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                                elif current_attribute == student.weather:
                                    if inq_counter == 1 and current_inq == 'weather_si':
                                        # we are here if user said that it was cold and that it snowed and added "y tú?" (or variations)
                                        inq_counter = 0
                                        current_inq = None
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it is warm were I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['snow_si']) + ' ' + str(self.generate_response(reaction, student.weather))
                                        self.delay_response(bot_response)
                                        return bot_response
                                    elif inq_counter == 1 and current_inq == 'weather_no':
                                        # we are here if the user said that it was not cold and that they missed the snow and added "y tú?" (or variations)
                                        inq_counter = 0
                                        current_inq = None
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it is warm were I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['missed_snow_si']) + ' ' + str(self.generate_response(reaction, student.weather))
                                        self.delay_response(bot_response)
                                        return bot_response
                                    elif inq_counter == 0:
                                        # we are here if the bot asked whether it was cold for the first time and the user answered "sí y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'weather_si' 
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it is warm were I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['weather_si']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                            if current_attribute == student.religious:
                                student.religious.value = True
                                bot_response = self.generate_response(random.choice(response_dict['religious']), student.religious)
                                self.delay_response(bot_response)
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
                                self.delay_response(bot_response)
                                return  bot_response
                            elif current_attribute == student.tree:
                                student.tree.value = True
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'Eso suena genial. I already told you that I did not have a christmas tree blabla'
                                else:
                                    reaction = 'Eso suena genial. ' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.weather:
                                student.weather.value = True
                                if self.check_whether_info_already_given('weather'):
                                    reaction = '¡Wow, me encantaría ver eso! I already told you that it was warm blabla'
                                else:
                                    reaction = '¡Wow, me encantaría ver eso! ' + random.choice(response_dict['weather'])
                                    bot_infos.remove('weather')
                                bot_response = self.generate_response(reaction, student.weather)
                                self.delay_response(bot_response)
                                return bot_response
                        elif keyword == str('no'):
                            if len(splitMessage) < 4:
                                if current_attribute == student.gifts:
                                    if inq_counter == 0:
                                        # we are here if the bot asked about gifts for the first time and the user answered "no y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'gifts_no' 
                                        if self.check_whether_info_already_given('gifts'):
                                            reaction = 'I already told you that I got gifts, but the most important thing is enjoying the time with family blabla'
                                        else:
                                            reaction = random.choice(response_dict["gifts"])
                                            bot_infos.remove('gifts')
                                        bot_response = random.choice(short_response_dict['gifts_no']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                                elif current_attribute == student.tree:
                                    if inq_counter == 1:
                                        # we are here if user said that they do not have a tree, and said that they do not have other traditional decoration (just "no") and added "y tú?" (or variations)
                                        inq_counter = 0
                                        current_inq = None
                                        if self.check_whether_info_already_given('tree'):
                                            reaction = 'I already told you that we have the Krippe blabla'
                                        else:
                                            reaction = random.choice(response_dict['tree'])
                                            bot_infos.remove('tree')
                                        bot_response = random.choice(short_response_dict['other_deco_no']) + ' ' + str(self.generate_response(reaction, student.tree))
                                        self.delay_response(bot_response)
                                        return bot_response
                                    if inq_counter == 0:
                                        # we are here if the bot asked about the tree for the first time and the user answered "no y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'tree_no' 
                                        if self.check_whether_info_already_given('tree'):
                                            reaction = 'I already told you that we did not have a tree as well'
                                        else:
                                            reaction = random.choice(response_dict['tree'])
                                            bot_infos.remove('tree')
                                        bot_response = random.choice(short_response_dict['tree_no']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                                elif current_attribute == student.weather:
                                    if inq_counter == 1 and current_inq == 'weather_si':
                                        # we are here if user said that it was cold, but that it did not snow and added "y tú?" (or variations)
                                        inq_counter = 0
                                        current_inq = None
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it is warm where I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['snow_no']) + ' ' + str(self.generate_response(reaction, student.weather))
                                        self.delay_response(bot_response)
                                        return bot_response
                                    elif inq_counter == 1 and current_inq == 'weather_no':
                                        # we are here if user said that it was not cold, and that they did not miss the snow and added "y tú?" (or variations)
                                        inq_counter = 0
                                        current_inq = None
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it is warm where I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['missed_snow_no']) + ' ' + str(self.generate_response(reaction, student.weather))
                                        self.delay_response(bot_response)
                                        return bot_response
                                    elif inq_counter == 0:
                                        # we are here if the bot asked whether it was cold for the first time and the user answered "no y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'weather_no' 
                                        if self.check_whether_info_already_given('weather'):
                                            reaction = 'I already told you that it was warm where I live blabla'
                                        else:
                                            reaction = random.choice(response_dict['weather'])
                                            bot_infos.remove('weather')
                                        bot_response = random.choice(short_response_dict['weather_no']) + ' ' + reaction
                                        self.delay_response(bot_response)
                                        return bot_response
                            if current_attribute == student.religious:
                                student.religious.value = False
                                bot_should_prompt_question = False
                                current_inq = 'non_religious_holidays'
                                bot_response = self.generate_response('I do celebrate christmas! What do you normally do during the holiday season?', student.religious)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.gifts:
                                student.got_gifts.value = False
                                student.gifts.value = 'none'
                                if self.check_whether_info_already_given('gifts'):
                                    reaction = 'Some response about how gifts are not important. I already told you that I got gifts, but the most important thing is enjoying the time with family blabla'
                                else:
                                    reaction = 'Some response about how gifts are not important.' + random.choice(response_dict["gifts"])
                                    bot_infos.remove('gifts')
                                bot_response = self.generate_response(reaction, student.gifts)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.tree:
                                student.tree.value = False
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'No importa, no todas las familias tienen árbol de Navidad! I already told you that we did not have a tree as well'
                                else:
                                    reaction = 'No importa, no todas las familias tienen árbol de Navidad!' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.weather:
                                student.weather.value = False
                                if self.check_whether_info_already_given('weather'):
                                    reaction = 'some reaction to not cold weather without repeating that it was not cold for bot either... I already told you that it was warm blabla'
                                else:
                                    reaction = '¡Tampoco con nosotros!' + random.choice(response_dict['weather'])
                                    bot_infos.remove('weather')
                                bot_response = self.generate_response(reaction, student.weather)
                                self.delay_response(bot_response)
                                return bot_response
                        # fallback response
                        else:
                            return self.defaultResponse

            # for messsages containing only "y tú?" or variations
            if current_attribute == student.food:
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('food'):
                    reaction = 'I already told you that we eat blabla'
                else:
                    reaction = random.choice(response_dict['food'])
                    bot_infos.remove('food')
                bot_response = self.generate_response(reaction, student.food)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.weather: 
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('weather'):
                    reaction = 'I already told you that it was warm. Sometimes I am jealous of those that experience snow on Christmas Eve!'
                else:
                    reaction = random.choice(response_dict['weather'])
                    bot_infos.remove('weather')
                bot_response = self.generate_response(reaction, student.weather)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.tree:
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('tree'):
                    reaction = 'I already told you that we did not have a tree but instead our Krippe. I sometimes think about how it would be if we had a christmas tree. It would certainly be strange, but I think I would love to help decorate it fully in red!'
                else:
                    reaction = random.choice(response_dict['tree'])
                    bot_infos.remove('tree')
                bot_response = self.generate_response(reaction, student.tree)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.gifts:
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('gifts'):
                    reaction = 'I already told you about my gifts: Almas gifts. I think my favorite thing this year was that the figure was in my piece of cake :)'
                else:
                    reaction = random.choice(response_dict['gifts'])
                    bot_infos.remove('gifts')
                bot_response = self.generate_response(reaction, student.gifts)
                self.delay_response(bot_response)
                return bot_response
            
            # for messages containing keywords
            for keyword in weather_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string.lower()
                    if string == keyword:
                        # TODO: process what the student mentioned about the weather
                        # differentiate between cold and warm weather in the bot's response
                        if self.check_whether_info_already_given('weather'):
                            reaction = 'aha... I already told you about the weather blabla'
                        else:
                            reaction = 'aha ' + random.choice(response_dict['weather'])
                            bot_infos.remove('weather')
                        bot_response = self.generate_response(reaction, student.weather)
                        self.delay_response(bot_response)
                        return bot_response
            
            for keyword in gift_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string.lower()
                    if string == keyword:
                        # TODO: process what the student mentioned about their gifts
                        if self.check_whether_info_already_given('gifts'):
                            reaction = 'aha (Geschenke). I already told you that I got gifts blabla'
                        else:
                            reaction = '¡Qué generoso! ' + random.choice(response_dict['gifts'])
                            bot_infos.remove('gifts')
                        bot_response = self.generate_response(reaction, student.gifts)
                        self.delay_response(bot_response)
                        return bot_response 
            
            # for messages that are responses to the bot's inquiries about an attribute
            if current_attribute == student.gifts and inq_counter == 1 and current_inq == 'gifts_si':
                # we are here if the bot asked about gifts for the first time, the user answered "sí" (or variations), the bot asked for more information, the user (probably) answered with what they got and "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                if self.check_whether_info_already_given('gifts'):
                    reaction = 'I already told you about my gifts blabla'
                else:
                    reaction = 'También recibí regalos.' + random.choice(response_dict['gifts'])
                    bot_infos.remove('gifts')
                bot_response = random.choice(short_response_dict['gifts_si_response']) + ' ' + str(self.generate_response(reaction, student.gifts))
                self.delay_response(bot_response)
                return bot_response
            elif current_attribute == student.gifts and inq_counter == 1 and current_inq == 'gifts_no':
                # we are here if the bot asked about gifts for the first time, the user answered "no" (or variations), the bot asked what they did instead on christmas eve, the user (probably) answered what they did and "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                # TODO: what to answer about what the bot did on christmas eve?
                # if self.check_whether_info_already_given('gifts'):
                #     reaction = 'I already told you about my gifts blabla'
                # else:
                #     reaction = 'También recibí regalos.' + random.choice(response_dict['gifts'])
                #     bot_infos.remove('gifts')
                reaction = 'I played with my siblings. '
                bot_response = random.choice(short_response_dict['gifts_no_response']) + ' ' + str(self.generate_response(reaction, student.gifts))
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.tree and inq_counter == 1 and current_inq == 'tree_si':
                # we are here if the bot asked about the tree for the first time, the user answered "sí" (or variations), the bot asked for more information, the user (probably) answered with more information and "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                if self.check_whether_info_already_given('tree'):
                    reaction = 'I already told you that we did not have a tree blabla'
                else:
                    reaction = random.choice(response_dict['tree'])
                    bot_infos.remove('tree')
                bot_response = random.choice(short_response_dict['tree_si_response']) + ' ' + str(self.generate_response(reaction, student.tree))
                self.delay_response(bot_response)
                return bot_response
            elif (current_attribute == student.tree and inq_counter == 1) or (current_attribute == student.tree and inq_counter == 2):
                # we are here if the bot asked about the tree for the first time, the user answered "no" (or variations), the bot asked about other traditional decoration, and 
                # case inq_counter == 1: the user (probably) answered what kind of decoration they had (without "sí") and added "y tú?" (or variations)
                # case inq_counter == 2: the user answered that they had other decoration, the bot asked what kind of decoration they had, the user (probably) answered with their decoration and added "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                if self.check_whether_info_already_given('tree'):
                    reaction = 'I already told you about the Krippe blabla'
                else:
                    reaction = random.choice(response_dict['tree'])
                    bot_infos.remove('tree')
                bot_response = random.choice(short_response_dict['other_deco_si']) + ' ' + str(self.generate_response(reaction, student.tree))
                self.delay_response(bot_response)
                return bot_response

        # check if user asked a question
        if last_user_message.__contains__("?"):
            # check if user asked about gifts
            for keyword in gift_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        current_attribute = student.gifts
                        if self.check_whether_info_already_given('gifts'):
                            bot_response = self.generate_response_to_user_question('Haha, I already told you: Tenía la figura en mi pieza este año. + hier einfügen was Alma als Geschenk bekommen hat (Geld, Videospiel, ...)', student.gifts)
                        else:
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['gifts'])+ 'hier einfügen was Alma als Geschenk bekommen hat (Geld, Videospiel, ...)', student.gifts)
                            bot_infos.remove('gifts')
                        self.delay_response(bot_response)
                        return bot_response

            # check if user asked about tree/decoration
            for keyword in tree_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        current_attribute = student.tree
                        if self.check_whether_info_already_given('tree'):
                            bot_response = self.generate_response_to_user_question('Haha, I already told you that we did not had a tree', student.tree)
                            self.delay_response(bot_response)
                        else:
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['tree']), current_attribute)
                            bot_infos.remove('tree')
                        self.delay_response(bot_response)
                        return bot_response

            # check if user asked about food
            for keyword in food_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        current_attribute = student.food
                        if self.check_whether_info_already_given('food'):
                            bot_response = self.generate_response_to_user_question('Haha, I already told you what we ate: blabla', student.food)
                        else:
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['food']), current_attribute)
                            bot_infos.remove('food')
                        self.delay_response(bot_response)
                        return bot_response

            # check if user asked about weather
            for keyword in weather_keywords:
                keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        current_attribute = student.weather
                        if self.check_whether_info_already_given('weather'):
                            bot_response = self.generate_response_to_user_question('Haha, I already told you that it was warm here in Spain', student.weather)
                        else:
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['weather']), current_attribute)
                            bot_infos.remove('weather')
                        self.delay_response(bot_response)
                        return   bot_response

            if last_user_message_cleaned.__contains__("cómo") or last_user_message_cleaned.__contains__('Cómo'):
                current_inq = 'mood'
                bot_response = 'Soy bien, ¿y tú?'
                self.delay_response(bot_response)
                return bot_response

            # fallback response
            return 'Sorry, I did not understand your question. Could you repeat it please?'
        else:
            bot_should_prompt_question = True

        # check keywords (message did not contain any question)
        # TODO: if only one word is returned this must be the name
        for keyword in name_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if student.name.value != None:
                        # TODO: check whether student changed their name ?
                        # alternatively, just say "Okay, NAME" and prompt the next question
                        return '¡Lo sé, ' + student.name.value + '! '
                    else:
                        current_attribute = student.name
                        student.name.value = self.process_user_name(keyword, index, splitMessage)
                        if student.name.value != None:
                            attributes.remove(student.name)
                            current_attribute = student.religious
                            # bot_should_prompt_question = True
                            bot_response = '¡Hola ' + student.name.value + '! ' + random.choice(response_dict['introduction'])
                            self.delay_response(bot_response)
                            return bot_response
                        else:
                            return self.defaultResponse
            
        for keyword in response_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if keyword == str('sí') or keyword == str('si'):
                        if current_attribute == student.tree and inq_counter == 1 and len(splitMessage) > 3:
                            # we are here if user said that they do not have a tree, but said that they have other traditional decoration (probably already stated what kind of decoration due to the message length)
                            inq_counter = 0
                            current_inq = None
                            bot_response = self.generate_response(random.choice(short_response_dict['other_deco_si']), student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        if len(splitMessage) < 3:
                            if current_attribute == student.gifts:
                                inq_counter += 1
                                current_inq = 'gifts_si' 
                                bot_response = random.choice(short_response_dict['gifts_si'])
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.tree:
                                if inq_counter == 1:
                                    if len(splitMessage) == 1:
                                        # we are here if user said that they do not have a tree, but said that they have other traditional decoration (just "sí")
                                        inq_counter += 1
                                        current_inq = 'other_deco'
                                        bot_response = random.choice(short_response_dict['other_deco_inq'])
                                        self.delay_response(bot_response)
                                        return bot_response                                        
                                elif inq_counter == 0:
                                    inq_counter += 1
                                    current_inq = 'tree_si'
                                    bot_response = random.choice(short_response_dict['tree_si'])
                                    self.delay_response(bot_response)
                                    return bot_response
                            elif current_attribute == student.weather:
                                if inq_counter == 1 and current_inq == 'weather_si':
                                    # we are here if user said that it was cold and said that it did snow
                                    self.update_attribute_todo_list(student.weather)
                                    inq_counter = 0
                                    current_inq = None
                                    bot_response = self.generate_response(random.choice(short_response_dict['snow_si']), student.weather)
                                    self.delay_response(bot_response)
                                    return bot_response
                                elif inq_counter == 1 and current_inq == 'weather_no':
                                    # we are here if user said that it was not cold and said that they missed the snow
                                    self.update_attribute_todo_list(student.weather)
                                    inq_counter = 0
                                    current_inq = None
                                    bot_response = self.generate_response(random.choice(short_response_dict['missed_snow_si']), student.weather)
                                    self.delay_response(bot_response)
                                    return bot_response
                                elif inq_counter == 0:
                                    inq_counter += 1
                                    current_inq = 'weather_si'
                                    bot_response = random.choice(short_response_dict['weather_si'])
                                    self.delay_response(bot_response)
                                    return bot_response
                        if current_attribute == student.religious:
                            student.religious.value = True
                            bot_response = self.generate_response(random.choice(response_dict['religious']), student.religious)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.gifts:
                            student.got_gifts.value = True
                            student.gifts.value = 'GIFTS THE STUDENT MENTIONED'
                            if self.check_whether_info_already_given('gifts'):
                                reaction = '¡Cómo mola!'
                            else:
                                reaction = '¡Cómo mola! ' + random.choice(response_dict['gifts'])
                                bot_infos.remove('gifts')
                            bot_response = self.generate_response(reaction, student.gifts)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = True
                            if self.check_whether_info_already_given('tree'):
                                reaction = 'Eso suena genial.'
                            else:
                                reaction = 'Eso suena genial. ' + random.choice(response_dict['tree'])
                                bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = True
                            if self.check_whether_info_already_given('weather'):
                                reaction = '¡Guau, me encantaría ver eso!'
                            else:
                                reaction = '¡Guau, me encantaría ver eso!' + random.choice(response_dict['weather'])
                                bot_infos.remove('weather')
                            bot_response = self.generate_response(reaction, student.weather)
                            self.delay_response(bot_response)
                            return bot_response
                    elif keyword == str('no'):
                        if len(splitMessage) < 4:
                            if current_attribute == student.gifts:
                                inq_counter += 1
                                current_inq = 'gifts_no'
                                bot_response = random.choice(short_response_dict['gifts_no'])
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.tree:
                                if inq_counter == 1:
                                    # we are here if user said that they do not have a tree, and said that they do not have other traditional decoration
                                    self.update_attribute_todo_list(student.tree)
                                    inq_counter = 0
                                    current_inq = None
                                    bot_response = self.generate_response(random.choice(short_response_dict['other_deco_no']), student.tree)
                                    self.delay_response(bot_response)
                                    return bot_response
                                inq_counter += 1
                                current_inq = 'tree_no'
                                return random.choice(short_response_dict['tree_no'])
                            elif current_attribute == student.weather:
                                if inq_counter == 1 and current_inq == 'weather_si':
                                    # we are here if user said that it was cold, but that it did not snow
                                    self.update_attribute_todo_list(student.weather)
                                    inq_counter = 0
                                    current_inq = None
                                    bot_response = self.generate_response(random.choice(short_response_dict['snow_no']), student.weather)
                                    self.delay_response(bot_response)
                                    return bot_response
                                elif inq_counter == 1 and current_inq == 'weather_no':
                                    # we are here if user said that it was not cold and that they did not miss the snow
                                    self.update_attribute_todo_list(student.weather)
                                    inq_counter = 0
                                    current_inq = None
                                    bot_response = self.generate_response(random.choice(short_response_dict['missed_snow_no']), student.weather)
                                    self.delay_response(bot_response)
                                    return bot_response 
                                elif inq_counter == 0:
                                    inq_counter += 1
                                    current_inq = 'weather_no'
                                    bot_response = random.choice(short_response_dict['weather_no'])
                                    self.delay_response(bot_response)
                                    return bot_response
                        if current_attribute == student.religious:
                            student.religious.value = False
                            bot_should_prompt_question = False
                            current_inq = 'non_religious_holidays'
                            bot_response = self.generate_response('Si no celebras las Navidades, ¿hiciste algo más especial durante las vacaciones?', student.religious)
                            self.delay_response(bot_response) 
                            return bot_response
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
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = False
                            if self.check_whether_info_already_given('tree'):
                                reaction = 'No importa, no todas las familias tienen árbol de Navidad!'
                            else:
                                reaction = 'No importa, no todas las familias tienen árbol de Navidad! ' + random.choice(response_dict['tree'])
                                bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = False
                            if self.check_whether_info_already_given('weather'):
                                reaction = 'some reaction to not cold weather without repeating that it was not cold for bot either'
                            else:
                                reaction = '¡Tampoco con nosotros! ' + random.choice(response_dict['weather'])
                                bot_infos.remove('weather')
                            bot_response = self.generate_response(reaction, student.weather)
                            self.delay_response(bot_response)
                            return bot_response
                    # fallback response
                    else:
                        return self.defaultResponse

        # TODO: do the same for negation keywords --> check current attribute to find out what the student "negates"

        # messages that are responses to the bot's inquiries about an attribute (without the user asking back or asking another question)
        if current_inq == 'gifts_si':
            # save what user mentioned about gift
            self.update_attribute_todo_list(student.gifts)
            inq_counter = 0
            current_inq = None
            bot_response = self.generate_response(random.choice(short_response_dict['gifts_si_response']), student.gifts)
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'gifts_no':
            # save what user mentioned about other activities
            self.update_attribute_todo_list(student.gifts)
            inq_counter = 0
            current_inq = None
            bot_response = self.generate_response(random.choice(short_response_dict['gifts_no_response']), student.gifts)
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'tree_si':
            # save what user mentioned about tree
            self.update_attribute_todo_list(student.tree)
            inq_counter = 0
            current_inq = None
            bot_response = self.generate_response(random.choice(short_response_dict['tree_si_response']), student.tree)
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'other_deco':
            # save what user mentioned about other deco
            self.update_attribute_todo_list(student.tree)
            inq_counter = 0
            current_inq = None
            bot_response = random.choice(short_response_dict['other_deco_si']) + ' ' + str(self.generate_response(reaction, student.tree))
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'mood':
            current_inq = None
            current_attribute = student.religious
            bot_should_prompt_question = True
            if last_user_message_cleaned.__contains__('también') or last_user_message_cleaned.__contains__('tambien') or last_user_message_cleaned.__contains__('bien') or last_user_message_cleaned.__contains__('También') or last_user_message_cleaned.__contains__('Tambien') or last_user_message_cleaned.__contains__('Bien'):
                bot_response = 'Nice! ' + random.choice(response_dict['introduction'])
            else:
                bot_response = "Sorry to hear that :( " + random.choice(response_dict['introduction'])
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'non_religious_holidays':
            current_inq = None
            bot_response = "That sounds interesting! (or other generic response to what the student did during the holidays) My teacher told me that we are chatting about christmas traditions in our cultures, so maybe I tell you about Spanish traditions nevertheless. What do you want to know?"
            self.delay_response(bot_response)
            return bot_response

        # FOOD
        for keyword in food_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: save what student mentioned about what they ate
                    if self.check_whether_info_already_given('food'):
                        # if student is not religious they might write "Tell me something about the food you eat on Christmas" for getting information about food
                        if student.religious.value == False:
                            reaction = 'I already told you that we ate blabla :)'
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Suena delicioso!'
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['food'])
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Suena delicioso! ' + random.choice(response_dict['food'])
                        bot_infos.remove('food')
                    bot_response = self.generate_response(reaction, student.food)
                    self.delay_response(bot_response)
                    return bot_response

        # WEATHER
        for keyword in weather_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about the weather
                    # differentiate between cold and warm weather in the bot's response
                    if self.check_whether_info_already_given('weather'):
                        if student.religious.value == False:
                            reaction = 'I already told you that it was warm in Spain :)'
                            bot_should_prompt_question = False
                        else:
                            reaction = 'aha... '
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['weather'])
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Qué interesante! ' + random.choice(response_dict['weather'])
                        bot_infos.remove('weather')
                    bot_response = self.generate_response(reaction, student.weather)
                    self.delay_response(bot_response)
                    return bot_response

         # TREE
        for keyword in tree_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    if self.check_whether_info_already_given('tree'):
                        if student.religious.value == False:
                            reaction = 'I already told you about our decoration :)'
                            bot_should_prompt_question = False
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['tree'])
                            bot_should_prompt_question = False
                        bot_infos.remove('tree')
                    bot_response = self.generate_response(reaction, student.tree) 
                    self.delay_response(bot_response)
                    return bot_response
        
        # GIFTS
        for keyword in gift_keywords:
            keyword.lower()
            for index, string in enumerate(splitMessage):
                string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about their gifts
                    if self.check_whether_info_already_given('gifts'):
                        if student.religious.value == False:
                            reaction = 'I already told you that I got blabla :)'
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Qué generoso!'
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['gifts'])
                            bot_should_prompt_question = False
                        else: 
                            reaction = '¡Qué generoso! ' + random.choice(response_dict['gifts'])
                        bot_infos.remove('gifts')
                    bot_response = self.generate_response(reaction, student.gifts)
                    self.delay_response(bot_response)
                    return bot_response

        # fallback response: smiley
        return '\U0001F60A'

    def welcome(self):
        return '¡Hola! Me llamo ' + self.name + ' y soy de ' + self.country + ' ¿Cómo te llamas?' 
