import random
import time

class BooleanAttribute():
    name = None
    status = None
    value = None

class StringAttribute():
    name = None
    status = None
    value = None

class Student():
    name = StringAttribute()
    name.status = 'unknown'
    religious = BooleanAttribute()
    religious.status = 'unknown'
    gifts = StringAttribute()
    gifts.status = 'unknown'
    tree = BooleanAttribute()
    tree.status = 'unknown'
    food = StringAttribute()
    food.status = 'unknown'

student = Student()
attributes = ['name', 'religious', 'gifts', 'tree', 'food']
name_keywords = ['llamo', 'nombre']
question_keywords = ['et tú', 'y tú']
category_keywords = ['regalos', 'árbol de Navidad', 'árbol', 'comistéis']
negation_keywords = ['no', 'nada', 'tampoco', 'nunca', 'ni']
response_keywords = ['sí', 'no']
bot_should_prompt_question = True
current_attribute = None

class Bot:
    name = random.choice(['José', 'Maria'])
    country = random.choice(['Spain', 'Mexico'])
    avatar = 'avatar/perroquet.png'
    defaultResponse = "Lo siento, no entiendo lo que me quieres decir... ¿Lo podrías repetir, por favor?"
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
        # splitInput = input.split()
        # for index, string in enumerate(splitInput):
        #     if string == 'llamo':
        #         value = splitInput[index + 1]
        #         return value
        # return " "
    
    # def process_user_input(self, input):
    #     input = input.lower()
    #     splitInput = input.split()
    #     for x in splitInput:
    #         if x == str('no'):
    #             return False
    #         elif x == str('sí'):
    #             return True
    #         else:
    #             return None

    def chat(self, last_user_message, session):
        global current_attribute

        if bot_should_prompt_question == False:
            time.sleep(random.randint(10,20))

        # response delay for authenticity
        time.sleep(3)
        
        splitMessage = last_user_message.split()
        # remove punctuation TODO! Does not work yet
        for string in splitMessage:
            string.replace(".", " ")
            string.replace(",", " ")
            string.replace("!", " ")
            string.replace("¡", " ")
            string.replace("?", " ")
            string.replace("¿", " ")

        # NAME
        for keyword in name_keywords:
            for index, string in enumerate(splitMessage):
                if string == keyword:
                    if student.name.status == str('finished'):
                        # TODO: check whether student changed their name ?
                        # alternatively, just say "Okay, NAME" and prompt the next question
                        return "¡Lo sé, " + student.name.value + "! "
                    else:
                        current_attribute = 'name'
                        student.name.value = self.process_user_name(keyword, index, splitMessage)
                        if student.name.value != None:
                            student.name.status = 'finished'
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
                            student.religious.status = 'finished'
                            attributes.remove('religious')
                            current_attribute = attributes[random.randint(0, len(attributes) - 1)]
                            return "Oh, I am curious how you celebrate christmas in your culture! + question about" + current_attribute
                    elif keyword == str('no'):
                        if current_attribute == str('religious'):
                            student.religious.value = False
                            student.religious.status = 'finished'
                            attributes.remove('religious')
                            current_attribute = attributes[random.randint(0, len(attributes) - 1)]
                            return "Oh, what do you normally do during the holiday season?"
                    else:
                        return "??"
                    
            
        
        # if self.student.name.status == str('unknown'):
        #     self.student.name.value = self.process_user_name(last_user_message)
        #     self.student.name.status = 'finished'
        #     return "¡Hola " + self.student.name.value + "! También bien, ¡gracias! ¿Qué tal las vacaciones? ¿Es la Navidad una fiesta religiosa para ti?"
        
        # elif self.student.religious.status == str('unknown'):
        #     self.student.religious.value = self.process_user_input(last_user_message)
        #     if self.student.religious.value == True:
        #         self.student.religious.status = 'finished'
        #         return "¡Eso suena estupendo! En México, las familias preparan una gran celebración para toda la familia para Nochebuena. Y hay muchos juegos para niños, como golpear piñatas rellenas con frutas, dulces y regalos pequeños. ¿Recibiste regalos también?"
        #     elif self.student.religious.value == False:
        #         self.student.religious.status = 'finished'
        #         return "(Decide what to do in case student did not celebrate christmas/it is not a religious holiday for them.) ¿Recibiste regalos también?"
        #     else:
        #           return self.defaultResponse 
        #           # and decide on how to proceed

        # elif self.student.gifts.status == str('unknown'):
        #     self.student.gifts.value = self.process_user_input(last_user_message)
        #     if self.student.gifts.value == True:
        #         self.student.gifts.status = 'finished'
        #         return "¡Qué padre! Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños. ¿También tenías un árbol de Navidad?"
        #     elif self.student.gifts.value == False:
        #         self.student.gifts.status = 'finished'
        #         return "No importa, blabla. ¿También tenías un árbol de Navidad?"
        #     else:
        #          return self.defaultResponse
        #          # and decide on how to proceed

        # elif self.student.tree.status == str('unknown'):
        #     self.student.tree.value = self.process_user_input(last_user_message)
        #     if self.student.tree.value == True:
        #         self.student.tree.status = 'finished'
        #         return "Eso suena genial. Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús"
        #     elif self.student.tree.value == False:
        #         self.student.tree.status = 'finished'
        #         return "No importa, no todas las familias tienen árbol de Navidad! Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús."
        #     else:
        #          return self.defaultResponse
        #          # and decide on how to proceed
                

    def welcome(self):
        return "¡Hola! Me llamo " + self.name + " y soy de " + self.country + " ¿Cómo te llamas?"
