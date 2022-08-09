from voice_assistant import *
from my_calendar import *
from notion import *
import pywhatkit
import pyjokes

WAKE = 'jarvis'

speak('Hello sir, I am your virtual assistant - Jarvis')
speak('Is there anything I can help you with')
while True:
    text = listen_once()

    if 'thanks' in text:
        # speak('I am stopping the session, sir. Bye bye')
        break

    if text.count(WAKE) > 0:
        speak('Yes, sir')
        text = listen().lower()
        if 'thanks' in text.split():
            speak('I am stopping the session, sir. Bye bye')
            break

        if 'calendar' in text.split():
            speak('Opening your calendar, sir')
            speak('How can I help you')
            while True:
                try:
                    text = listen().lower()
                    if 'thanks' in text.split():
                        print('I am stopping the calendar session')
                        speak('I am stopping the calendar session')
                        break
                    print(text)
                    if 'schedule' in text.split():
                        print(get_date(text))
                        get_events(get_date(text), SERVICE)

                    if 'create' in text.split():
                        try:
                            speak('What is the name of the event')

                            summary = listen().lower()
                            speak('What date does it start')
                            date = listen().lower()
                            speak('What time does it start')
                            start_time = listen().lower()
                            speak('What time does it end')
                            end_time = listen().lower()
                            print('Creating an event...')
                            create_event(summary=summary,date=get_date(date),start_time=start_time,end_time=end_time)
                        except:
                            pass
                except TypeError:
                    speak('Please repeat the date')

        if 'notion' in text.split():
            speak('Opening notion, sir')
            speak('How can I help you')
            while True:
                text = listen().lower()
                if 'to-do' in text.split():
                    speak('What should I add, sir')
                    item = listen()
                    createPage(item, 'Not done')
                    speak(item + 'has been added to Notion to-do list')

                if 'thanks' in text.split():
                    speak('Closing the notion session, sir')
                    break

        if 'play' in text:
            song = text.split('play')[1]
            print('Playing ' + song + ' on youtube')
            speak('Playing' + song + ' on youtube')
            pywhatkit.playonyt(song)

        if 'search' in text:
            search = text.split('search')[1]
            speak('Searching for ' + search)
            try:
                info = pywhatkit.info(search, return_value=True)
                speak(info)
            except Exception:
                speak('Could not find information on given topic')
                pass

        if 'jokes' in text:
            joke = pyjokes.get_joke(category='all')
            print(joke)
            speak(joke)



