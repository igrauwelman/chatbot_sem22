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
response_keywords = ['sí', 'si', 'no', 'tambien', 'tambíen', 'también', 'tampoco']
food_keywords = ['come', 'como', 'comemos', 'comiste', 'comistéis', 'comer', 'comisteis', 'comimos', 'comida', 'comido']
weather_keywords = ['nieve', 'sol', 'fría', 'fria', 'frio', 'frío', 'cálida', 'calida', 'cálido', 'calido', 'lluvia', 'lloviendo', 'lluvioso', 'tiempo', 'nevando', 'calor']
gift_keywords = ['regalos', 'regalo', 'regalaron', 'tengo', 'recibí', 'recibi', 'regalar', 'recibido']
tree_keywords = ['árbol', 'arbol', 'decoras', 'decora', 'adornos', 'decoración', 'decoracion']
# TODO: negation_keywords = ['nunca', 'jamás', 'jamas']

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
                    """¡Genial!""",
                    """¡Qué padre!""",
                    """¡Qué lindo!""",
                    """¡Qué bonito!"""],

    "tree_no": ["""¿Tenéis otra decoración tradicional?"""],

    "other_deco_inq": ["""¿Qué tipo de decoración?"""],

    "other_deco_si": ["""¡Muy interesante!"""],

    "other_deco_no": ["""Parece que la decoración no es importante en tu familia."""],

    "weather_si": ["""Bueno, ¿también nevó?"""],
    
    "snow_si": ["""¡No me digas!"""],

    "snow_no": ["""¡Qué pena!"""],

    "weather_no": ["""¿Has extrañado la nieve?"""],

    "missed_snow_si": ["""¡Entiendo!"""],

    "missed_snow_no": ["""Bueno, no a todos les gusta la nieve :)"""]
}

# dictionary with responses
response_dict = {
    "introduction": ["""Hablemos de las vacaciones. ¿Celebras Navidad?""",
                    """¿Qué tal las vacaciones? ¿Celebras la Navidad?"""],

    "religious": ["""También celebré la Navidad. 
                    En México , las familias preparan una gran celebración para toda la familia para Nochebuena. Y hay muchos juegos para niños, como golpear piñatas rellenas con frutas, dulces y regalos pequeños.""",
                 """Yo tambíen. TODO"""],

    "food": ["""En México, la mayoría de las familias come pavo con ensalada de manzana y pescado en salsa de tomate en Nochebuena, pero muchas otras familias también comen su propia comida tradicional, como tacos, enchiladas, quesadillas y burritos con guacamole. Y siempre hay salsa picante.""",
            """TODO"""],
# TODO: check if José's personal gifts are added in each response
    "gifts": ["""Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños.""",
            """TODO"""],

    "tree": ["""Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús""",
            """TODO"""],

    "weather": ["""Mucha gente pasó las Navidades en la playa porque hacía mucho calor. Entonces, ¡el árbol de Navidad está hecho con una palmera!""",
                """En nuestro país, mucha gente pasó las Navidades en la playa, ¡porque hacía mucho calor! Entonces, ¡el árbol de Navidad está hecho con una palmera!"""]

}

class Bot:
    name = 'José '
    country = 'México'
    avatar = 'avatar/mex_jose.jpeg'
    defaultResponse = 'Lo siento, no entiendo. ¿Puedes repetir de nuevo?'
    endMessage = 'Ahora tengo deberes que hacer. Fue guay charlar contigo, ¡ojalá podamos repetirlo pronto!'
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

    def check_whether_conversation_should_end(self):
        global attributes
        global bot_infos

        for attribute in attributes:
            if self.check_whether_attribute_already_finished(attribute) == False:
                return False
        
        for info in bot_infos:
            if self.check_whether_info_already_given(info) == False:
                return False

        return True

    # remove finished attribute
    def update_attribute_todo_list(self, attribute_to_be_removed):
        global attributes
        global current_attribute

        current_attribute = None

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
        # FALSE should be 2 times more likely
        bot_should_prompt_question = random.choice([True, False, False])
        
        # remove punctuation
        last_user_message_cleaned = re.sub(r'[^\w\s]', '', last_user_message)

        # split message into word chunks
        splitMessage = last_user_message_cleaned.split()

        # check for curse words
        for keyword in curse_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    bot_response = 'Por favor, responda la pregunta sin usar lenguaje inapropiado.'
                    return bot_response

        # if student did not celebrate christmas, they should ask bot questions -> if bot gave all infos, end the conversation
        if student.religious.value == False and not bot_infos:
            bot_response = self.endMessage
            self.delay_response(bot_response)
            return bot_response

        # check whether user asked back
        if last_user_message.__contains__('tú?') or last_user_message.__contains__('tu?'):
            # for messages containing "sí" or "no" (or variations)
            for keyword in response_keywords:
                keyword = keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        if keyword == str('sí') or keyword == str('si') or keyword == str('tambien') or keyword == str('tambíen') or keyword == str('también'):
                            if current_attribute == student.tree and inq_counter == 1 and len(splitMessage) > 3:
                                # TODO: not sure, because user could have said "Ah, muy interesante! Si, we have other decoration" for example
                                # we are here if user said that they do not have a tree, but said that they have other traditional decoration (probably already stated what kind of decoration due to the message length) and added "y tú?" (or variations)
                                inq_counter = 0
                                current_inq = None
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'Wir haben mittlerweile auch einen Weihnachtsbaum, wie ich dir erzählt habe, aber die Weihnachtskrippe ist uns am wichtigsten. (la cuna de Navidad, que recrea el nacimiento de Jesús)'
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
                                        reaction = 'Wie ich dir erzählt habe, habe ich eine neue Gitarre und mehrere Bücher bekommen. '
                                    else:
                                        reaction = 'También recibí regalos. ' + random.choice(response_dict['gifts'])
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
                                            reaction = 'Das Wichtigste ist für uns jedes Jahr die Weihnachtskrippe, wie ich vorhin erwähnt habe. Aber mittlerweile haben wir auch einen Weihnachtsbaum!'
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
                                            reaction = 'Wie ich vorhin erwähnt habe, hatten wir auch einen Weihnachtsbaum, ja.'
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
                                            reaction = '¡Estoy celoso! Bei mir war es wie gesagt sehr heiß, keine Chance auf Schnee an Weihnachten.'
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
                                            reaction = 'Manchmal würde ich auch gerne Schnee an Weihnachten haben, ja! In meiner Stadt ist es ja wie gesagt immer sehr heiß, aber ich gehe auch gerne an den Strand an Weihnachten.'
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
                                            reaction = 'In meiner Stadt in Mexiko ist es wie gesagt immer sehr heiß.'
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
                                    reaction = '¡Cómo mola! Wie ich dir erzählt habe, habe ich eine neue Gitarre und mehrere Bücher bekommen.'
                                else:
                                    reaction = '¡Cómo mola! También recibí regalos. ' + random.choice(response_dict['gifts'])
                                    bot_infos.remove('gifts')
                                bot_response = self.generate_response(reaction, student.gifts)
                                self.delay_response(bot_response)
                                return  bot_response
                            elif current_attribute == student.tree:
                                # TODO: check if inq==0 if clause is the same (see above)
                                student.tree.value = True
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'Eso suena genial. Wie ich vorhin erwähnt habe, hatten wir auch einen Weihnachtsbaum, ja.'
                                else:
                                    reaction = 'Eso suena genial. ' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.weather:
                                # TODO: check if if-clause above is the same
                                student.weather.value = True
                                if self.check_whether_info_already_given('weather'):
                                    reaction = '¡Wow, me encantaría ver eso! Como te dije antes, en mi ciudad suele hacer calor.'
                                else:
                                    reaction = '¡Wow, me encantaría ver eso! ' + random.choice(response_dict['weather'])
                                    bot_infos.remove('weather')
                                bot_response = self.generate_response(reaction, student.weather)
                                self.delay_response(bot_response)
                                return bot_response
                        elif keyword == str('no') or keyword == str('tampoco'):
                            if len(splitMessage) < 4:
                                if current_attribute == student.gifts:
                                    if inq_counter == 0:
                                        # we are here if the bot asked about gifts for the first time and the user answered "no y tú?" (or variations)
                                        inq_counter += 1
                                        current_inq = 'gifts_no' 
                                        if self.check_whether_info_already_given('gifts'):
                                            reaction = 'Ich hab dir schon erzählt, dass ich Geschenke zu Weihnachten bekommen habe, aber ich glaube, das Wichtigste ist, die schöne freie Zeit zusammen mit der Familie oder Freunden zu genießen.'
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
                                            reaction = 'Wie ich dir erzählt habe, stellen wir jedes Jahr die Weihnachtskrippe auf. Das ist das Wichtigste für uns. '
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
                                            reaction = 'Wie ich dir erzählt habe, hatten wir einen Weihnachtsbaum, auch wenn es ganz lange keine Tradition in Mexiko war.'
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
                                            reaction = 'Wie ich vorhin gesagt habe, ist es immer sehr heiß an Weihnachten in Mexiko, also gibt es hier auch nie Schnee.'
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
                                            reaction = 'Wir haben keinen Schnee in Mexiko. Manchmal frage ich mich, wie es wäre mit Schnee Weihnachten zu feiern, aber ich finde es auch schön, Weihnachten am Strand zu feiern.'
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
                                            reaction = 'Kalt war es wie gesagt bei uns auch nicht, es ist meistens sehr heiß an Weihnachten.'
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
                                bot_response = self.generate_response('Celebré la Navidad. ¿Cómo pasas tu tiempo de vacaciones?', student.religious)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.gifts:
                                student.got_gifts.value = False
                                student.gifts.value = 'none'
                                if self.check_whether_info_already_given('gifts'):
                                    reaction = 'Ich habe dir schon von meinen Geschenken erzählt, aber ich glaube, dass das nicht das Wichtigste ist. Das Beste ist doch, die freie Zeit zu genießen!'
                                else:
                                    reaction = '¡De todos modos, no creo que los regalos sean lo más importante de la Navidad! ' + random.choice(response_dict["gifts"])
                                    bot_infos.remove('gifts')
                                bot_response = self.generate_response(reaction, student.gifts)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.tree:
                                # TODO: check above if already a case
                                student.tree.value = False
                                if self.check_whether_info_already_given('tree'):
                                    reaction = 'Das ist ja nicht schlimm, hier in Mexiko hatten wir auch ganz lange keinen Weihnachtsbaum. Aber mittlerweile haben wir einen, wie ich dir ja schon erzählt habe!'
                                else:
                                    reaction = 'No importa, no todas las familias tienen árbol de Navidad! ' + random.choice(response_dict['tree'])
                                    bot_infos.remove('tree')
                                bot_response = self.generate_response(reaction, student.tree)
                                self.delay_response(bot_response)
                                return bot_response
                            elif current_attribute == student.weather:
                                student.weather.value = False
                                if self.check_whether_info_already_given('weather'):
                                    reaction = 'Entonces, ¡tuvimos un clima similar!'
                                else:
                                    reaction = '¡Tampoco con nosotros! ' + random.choice(response_dict['weather'])
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
                    reaction = 'Como te dije, la mayoría de la gente come pavo con ensalada de manzana y pescado en salsa de tomate, pero muchos también comen tacos, enchiladas, quesadillas y burritos con guacamole. ¡Pero siempre hay salsa picante!'
                else:
                    reaction = random.choice(response_dict['food'])
                    bot_infos.remove('food')
                bot_response = self.generate_response(reaction, student.food)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.weather: 
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('weather'):
                    reaction = 'Wie gesagt, es war wie jedes Jahr ziemlich heiß hier in Mexiko. Ich glaube, es wäre sehr komisch für mich, wenn es plötzlich Schnee geben würde!'
                else:
                    reaction = random.choice(response_dict['weather'])
                    bot_infos.remove('weather')
                bot_response = self.generate_response(reaction, student.weather)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.tree:
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('tree'):
                    reaction = 'Unseren Baum haben wir zusammen eine Woche vor Weihnachten geschmückt, er war sehr bunt. So mögen wir es am liebsten! Aber die Weihnachtskrippe bleibt das Wichtigste für uns.'
                else:
                    reaction = random.choice(response_dict['tree'])
                    bot_infos.remove('tree')
                bot_response = self.generate_response(reaction, student.tree)
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.gifts:
                bot_should_prompt_question = False
                if self.check_whether_info_already_given('gifts'):
                    reaction = 'Wie ich dir vorhin gesagt habe, habe ich eine neue Gitarre und mehrere Bücher bekommen. Ich habe mich über alles sehr gefreut!'
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
                            reaction = 'Ah, interessant! Wie gesagt war es bei uns sehr heiß wie jedes Jahr.'
                        else:
                            reaction = '¡Ay interesante! ' + random.choice(response_dict['weather'])
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
                            reaction = 'Ah, ich verstehe! Wie gesagt, habe ich eine neue Gitarre und mehrere Bücher bekommen.'
                        else:
                            reaction = '¡Ah, ya entiendo! ' + random.choice(response_dict['gifts'])
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
                    reaction = 'Wie gesagt, habe ich eine neue Gitarre und mehrere Bücher bekommen, darüber habe ich mich sehr gefreut.'
                else:
                    reaction = 'También recibí regalos. ' + random.choice(response_dict['gifts'])
                    bot_infos.remove('gifts')
                bot_response = random.choice(short_response_dict['gifts_si_response']) + ' ' + str(self.generate_response(reaction, student.gifts))
                self.delay_response(bot_response)
                return bot_response
            elif current_attribute == student.gifts and inq_counter == 1 and current_inq == 'gifts_no':
                # we are here if the bot asked about gifts for the first time, the user answered "no" (or variations), the bot asked what they did instead on christmas eve, the user (probably) answered what they did and "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                reaction = 'Ich war mit meiner Familie am Strand und wir haben zusammen mit Freunden viele Spiele gespielt.'
                bot_response = random.choice(short_response_dict['gifts_no_response']) + ' ' + str(self.generate_response(reaction, student.gifts))
                self.delay_response(bot_response)
                return bot_response

            if current_attribute == student.tree and inq_counter == 1 and current_inq == 'tree_si':
                # we are here if the bot asked about the tree for the first time, the user answered "sí" (or variations), the bot asked for more information, the user (probably) answered with more information and "y tú?" (or variations)
                inq_counter = 0
                current_inq = None
                if self.check_whether_info_already_given('tree'):
                    reaction = 'Unseren Baum haben wir zusammen eine Woche vor Weihnachten ganz bunt geschmückt. Das macht mir immernoch sehr viel Spaß! '
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
                    reaction = 'Das Wichtigste ist für uns jedes Jahr die Weihnachtskrippe, wie ich vorhin erwähnt habe. Aber mittlerweile haben wir auch einen Weihnachtsbaum!'
                else:
                    reaction = random.choice(response_dict['tree'])
                    bot_infos.remove('tree')
                bot_response = random.choice(short_response_dict['other_deco_si']) + ' ' + str(self.generate_response(reaction, student.tree))
                self.delay_response(bot_response)
                return bot_response

        if last_user_message.__contains__("?"):
            # check if user asked about gifts
            for keyword in gift_keywords:
                keyword = keyword.lower()
                for index, string in enumerate(splitMessage):
                    string = string.lower()
                    if string == keyword:
                        current_attribute = student.gifts
                        if self.check_whether_info_already_given('gifts'):
                            bot_response = self.generate_response_to_user_question('Das habe ich vorhin schon einmal erwähnt: Ich habe eine neue Gitarre und mehrere Bücher zu Weihnachten bekommen.', student.gifts)
                        else:
                            bot_response = self.generate_response_to_user_question(random.choice(response_dict['gifts'])+ ' Ich habe eine neue Gitarre und mehrere Bücher zu Weihnachten bekommen.', student.gifts)
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
                            bot_response = self.generate_response_to_user_question('Wie ich bereits erzählt habe, haben wir auch einen Weihnachtsbaum geschmückt, aber das Wichtigste ist für uns die Weihnachtskrippe.', student.tree)
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
                            bot_response = self.generate_response_to_user_question('Ya he dicho que solemos comer pavo con ensalada de manzana y pescado en salsa de tomate, o nuestros propios platos tradicionales como tacos, enchiladas, quesadillas y burritos con guacamole. Pero en cualquier caso, ¡la salsa picante no debe faltar!', student.food)
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
                            bot_response = self.generate_response_to_user_question('Como dije, por lo general hace bastante calor en México en Navidad.', student.weather)
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
            return self.defaultResponse

        # check keywords (message did not contain any question)
        for keyword in name_keywords:
            keyword = keyword.lower()
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
                            bot_response = '¡Hola ' + student.name.value + '! ' + random.choice(response_dict['introduction'])
                            self.delay_response(bot_response)
                            return bot_response
                        else:
                            return self.defaultResponse
            
        for keyword in response_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if keyword == str('sí') or keyword == str('si') or keyword == str('tambien') or keyword == str('tambíen') or keyword == str('también'):
                        if current_attribute == student.tree and inq_counter == 1 and len(splitMessage) > 3:
                            # we are here if user said that they do not have a tree, but said that they have other traditional decoration (probably already stated what kind of decoration due to the message length)
                            inq_counter = 0
                            current_inq = None
                            bot_response = self.generate_response(random.choice(short_response_dict['other_deco_si']), student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        if len(splitMessage) < 4:
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
                                reaction = '¡Qué padre!'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['¡Qué padre! ' + random.choice(response_dict['gifts']), '¡Qué padre!'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 3:
                                    bot_infos.remove('gifts')
                            bot_response = self.generate_response(reaction, student.gifts)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = True
                            if self.check_whether_info_already_given('tree'):
                                reaction = '¡Eso suena estupendo!'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['¡Eso suena estupendo! ' + random.choice(response_dict['tree']), '¡Eso suena estupendo!'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 3:
                                    bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = True
                            if self.check_whether_info_already_given('weather'):
                                reaction = '¡Guau, me encantaría ver eso!'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['¡Guau, me encantaría ver eso! ' + random.choice(response_dict['weather']), '¡Guau, me encantaría ver eso!'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 3:
                                    bot_infos.remove('weather')
                            bot_response = self.generate_response(reaction, student.weather)
                            self.delay_response(bot_response)
                            return bot_response
                    elif keyword == str('no') or keyword == str('tampoco'):
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
                            bot_response = self.generate_response('Si no celebras la Navidad, ¿hiciste algo especial durante las vacaciones?', student.religious)
                            self.delay_response(bot_response) 
                            return bot_response
                        elif current_attribute == student.gifts: 
                            student.got_gifts.value = False
                            student.gifts.value = 'none'
                            if self.check_whether_info_already_given('gifts'):
                                reaction = 'Los regalos no son tan importantes de todos modos.'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['Los regalos no son tan importantes de todos modos. ' + random.choice(response_dict['gifts']), 'Los regalos no son tan importantes de todos modos.'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 10, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 10:
                                    bot_infos.remove('gifts')
                            bot_response = self.generate_response(reaction, student.gifts)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.tree:
                            student.tree.value = False
                            if self.check_whether_info_already_given('tree'):
                                reaction = 'No importa, no todas las familias tienen árbol de Navidad!'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['No importa, no todas las familias tienen árbol de Navidad! ' + random.choice(response_dict['tree']), 'No importa, no todas las familias tienen árbol de Navidad!'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 10, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 10:
                                    bot_infos.remove('tree')
                            bot_response = self.generate_response(reaction, student.tree)
                            self.delay_response(bot_response)
                            return bot_response
                        elif current_attribute == student.weather:
                            student.weather.value = False
                            if self.check_whether_info_already_given('weather'):
                                reaction = '¡Entonces ambos tuvimos un clima similar en Navidad!'
                            else:
                                # decide if bot should give own info
                                reaction = random.choices(population=['¡Tampoco con nosotros! ' + random.choice(response_dict['weather']), '¡Entonces ambos tuvimos un clima similar en Navidad!'],weights=[0.2, 0.8],k=1)[0]
                                # if length of the reaction is greater than 10, the bot gave own info -> remove attribute from bot info todo list
                                if len(reaction.split()) > 10:
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
                bot_response = '¡Bonito! ' + random.choice(response_dict['introduction'])
            else:
                bot_response = "Siento escuchar eso! :( " + random.choice(response_dict['introduction'])
            self.delay_response(bot_response)
            return bot_response
        elif current_inq == 'non_religious_holidays':
            current_inq = None
            bot_response = "Ah, ich verstehe! Ich kann dir ja trotzdem etwas über die Weihnachtstraditionen in Mexiko erzählen, weil das ja unsere Aufgabe ist. Was möchtest du wissen?"
            self.delay_response(bot_response)
            return bot_response

        # FOOD
        for keyword in food_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    # TODO: save what student mentioned about what they ate
                    if self.check_whether_info_already_given('food'):
                        # if student is not religious they might write "Tell me something about the food you eat on Christmas" for getting information about food
                        if student.religious.value == False:
                            reaction = 'Ya he dicho que solemos comer pavo con ensalada de manzana y pescado en salsa de tomate, o nuestros propios platos tradicionales como tacos, enchiladas, quesadillas y burritos con guacamole. Pero en cualquier caso, ¡la salsa picante no debe faltar!'
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Suena delicioso!'
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['food'])
                            bot_should_prompt_question = False
                            bot_infos.remove('food')
                        else:
                            # decide if bot should give own info
                            reaction = random.choices(population=['¡Suena delicioso! ' + random.choice(response_dict['food']), '¡Suena delicioso!'],weights=[0.2, 0.8],k=1)[0]
                            # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                            if len(reaction.split()) > 3:
                                bot_infos.remove('food')
                    bot_response = self.generate_response(reaction, student.food)
                    self.delay_response(bot_response)
                    return bot_response

        # WEATHER
        for keyword in weather_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about the weather
                    # differentiate between cold and warm weather in the bot's response
                    if self.check_whether_info_already_given('weather'):
                        if student.religious.value == False:
                            reaction = 'Wie gesagt, war es sehr heiß bei uns.'
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Entiendo!'
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['weather'])
                            bot_should_prompt_question = False
                            bot_infos.remove('weather')
                        else:
                            # decide if bot should give own info
                            reaction = random.choices(population=['¡Qué interesante! ' + random.choice(response_dict['weather']), '¡Qué interesante!'],weights=[0.2, 0.8],k=1)[0]
                            # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                            if len(reaction.split()) > 3:
                                bot_infos.remove('weather')
                    bot_response = self.generate_response(reaction, student.weather)
                    self.delay_response(bot_response)
                    return bot_response

         # TREE
        for keyword in tree_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    if self.check_whether_info_already_given('tree'):
                        if student.religious.value == False:
                            bot_should_prompt_question = False
                        reaction = 'Wie gesagt, wir hatten einen Weihnachtsbaum, aber die Weihnachtskrippe ist uns am Wichtigsten.'
                    else:
                        if student.religious.value == False:
                            bot_should_prompt_question = False
                        reaction = random.choice(response_dict['tree'])
                        bot_infos.remove('tree')
                    bot_response = self.generate_response(reaction, student.tree) 
                    self.delay_response(bot_response)
                    return bot_response
        
        # GIFTS
        for keyword in gift_keywords:
            keyword = keyword.lower()
            for index, string in enumerate(splitMessage):
                string = string.lower()
                if string == keyword:
                    # TODO: process what the student mentioned about their gifts
                    if self.check_whether_info_already_given('gifts'):
                        if student.religious.value == False:
                            reaction = 'Wie gesagt, ich habe eine neue Gitarre und mehrere Bücher bekommen.'
                            bot_should_prompt_question = False
                        else:
                            reaction = '¡Qué generoso!'
                    else:
                        if student.religious.value == False:
                            reaction = random.choice(response_dict['gifts'])
                            bot_should_prompt_question = False
                            bot_infos.remove('gifts')
                        else: 
                            # decide if bot should give own info
                            reaction = random.choices(population=['¡Qué generoso! ' + random.choice(response_dict['gifts']), '¡Qué generoso!'],weights=[0.2, 0.8],k=1)[0]
                            # if length of the reaction is greater than 3, the bot gave own info -> remove attribute from bot info todo list
                            if len(reaction.split()) > 3:
                                bot_infos.remove('gifts')
                    bot_response = self.generate_response(reaction, student.gifts)
                    self.delay_response(bot_response)
                    return bot_response

        if self.check_whether_conversation_should_end():
            bot_response = self.endMessage
            self.delay_response(bot_response)
            return bot_response

        # fallback response: smiley
        return '\U0001F60A'

    def welcome(self):
        return '¡Hola! Me llamo ' + self.name + ' y soy de ' + self.country + ' ¿Cómo te llamas?'