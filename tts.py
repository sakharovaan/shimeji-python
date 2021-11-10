# import pyttsx3
# engine = pyttsx3.init() # object creation
#
# """ RATE"""
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 125)     # setting up new voice rate
#
#
# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
#
# """VOICE"""
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice)
#     if voice.languages[0] == 'ru_RU':
#         engine.setProperty('voice', voice.id)
#         break

#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
#
# engine.say("Hello World!")
# engine.say('My current speaking rate is ' + str(rate))
# engine.runAndWait()
# engine.stop()

# https://pyttsx3.readthedocs.io/en/latest/engine.html#the-engine-factory

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 150)     # setting up new voice rate

index = 0
for voice in voices:
   print(f'index-> {index} -- {voice.name} -- {voice.id}')
   index +=1


engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\Vocalizer Expressive milena premium-high 22kHz')
engine.say('<pitch middle="5">Саша, пора уже ложиться!</pitch>')
engine.runAndWait()
engine.stop()


# engine.runAndWait()