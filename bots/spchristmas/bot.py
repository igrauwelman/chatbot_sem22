import random

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

class Bot:
    name = random.choice(['José', 'Maria'])
    avatar = 'avatar/perroquet.png'
    defaultResponse = "Lo siento, no entiendo lo que me quieres decir... ¿Lo podrías repetir, por favor?"
    student = Student()
    age = random.choice([14,15,16])
    celebratedChristmas = True

    def process_user_name(self, input):
        splitInput = input.split()
        for index, string in enumerate(splitInput):
            if string == 'llamo':
                value = splitInput[index + 1]
                return value
        return " "
    
    def process_user_input(self, input):
        input = input.lower()
        splitInput = input.split()
        for x in splitInput:
            if x == str('no'):
                return False
            elif x == str('sí'):
                return True
            else:
                return None

    def chat(self, last_user_message, session):
        if self.student.name.status == str('unknown'):
            self.student.name.value = self.process_user_name(last_user_message)
            self.student.name.status = 'finished'
            return "¡Hola " + self.student.name.value + "! También bien, ¡gracias! ¿Qué tal las vacaciones? ¿Es la Navidad una fiesta religiosa para ti?"
        
        elif self.student.religious.status == str('unknown'):
            self.student.religious.value = self.process_user_input(last_user_message)
            if self.student.religious.value == True:
                self.student.religious.status = 'finished'
                return "¡Eso suena estupendo! En México, las familias preparan una gran celebración para toda la familia para Nochebuena. Y hay muchos juegos para niños, como golpear piñatas rellenas con frutas, dulces y regalos pequeños. ¿Recibiste regalos también?"
            elif self.student.religious.value == False:
                self.student.religious.status = 'finished'
                return "(Decide what to do in case student did not celebrate christmas/it is not a religious holiday for them.) ¿Recibiste regalos también?"
            else:
                  return self.defaultResponse 
                  # and decide on how to proceed

        elif self.student.gifts.status == str('unknown'):
            self.student.gifts.value = self.process_user_input(last_user_message)
            if self.student.gifts.value == True:
                self.student.gifts.status = 'finished'
                return "¡Qué padre! Los regalos sólo se desenvuelven a medianoche en México, lo que siempre hace más felices a los niños. ¿También tenías un árbol de Navidad?"
            elif self.student.gifts.value == False:
                self.student.gifts.status = 'finished'
                return "No importa, blabla. ¿También tenías un árbol de Navidad?"
            else:
                 return self.defaultResponse
                 # and decide on how to proceed

        elif self.student.tree.status == str('unknown'):
            self.student.tree.value = self.process_user_input(last_user_message)
            if self.student.tree.value == True:
                self.student.tree.status = 'finished'
                return "Eso suena genial. Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús"
            elif self.student.tree.value == False:
                self.student.tree.status = 'finished'
                return "No importa, no todas las familias tienen árbol de Navidad! Antes en México no se ponían árboles de Navidad, fue hasta que nos enteramos por los europeos que nos pareció una gran idea y ahora ¡también lo hacemos! Mucho más importante para nosotros es la cuna de Navidad, que recrea el nacimiento de Jesús."
            else:
                 return self.defaultResponse
                 # and decide on how to proceed
                

    def welcome(self):
        return "¡Hola! Me llamo " + self.name + " y soy de México ¿Cómo estás? ¿Cómo te llamas?"
