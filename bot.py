import gpt
import speech_recognition as sr
import subprocess
import webbrowser
import pyowm
import translators as ts
import gtts
import pygame
import os
import tkinter as tk
from tkinter import simpledialog
import pyaudio

pygame.init()
pygame.mixer.init()
owm = pyowm.OWM('5817d6a145c443107efc34417e35c2ac')
recognizer = sr.Recognizer()

anigdot = pygame.mixer.Sound("./anigdot.mp3")

# Лічильник для незрозумілих команд
unknown_command_count = 0

# Індекс мікрофона за замовчуванням
default_mic_index = 0

def list_connected_microphones():
    p = pyaudio.PyAudio()
    mic_list = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info.get('maxInputChannels') > 0:  # фільтруємо тільки вхідні аудіо пристрої
            mic_list.append(device_info.get('name'))
    p.terminate()
    return mic_list

def capture_voice_input(mic_index):
    with sr.Microphone(device_index=mic_index) as source:
        print("Слухаю...")
        audio = recognizer.listen(source)
    return audio

def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio, language="uk-UK")
        print("Ви сказали: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Вибачте, але я Вас не розумію.")
    except sr.RequestError as e:
        text = ""
        print("Помилка; {0}".format(e))
    return text

def process_voice_command(text):
    global unknown_command_count
    if "привіт" in text.lower():
        print("Привіт! Як я можу Вам допомогти?")
        unknown_command_count = 0
    elif "прощавай" in text.lower() or "до побачення" in text.lower():
        print("До побачення! Гарного дня!")
        return True
    elif "калькулятор" in text.lower():
        subprocess.call(['calc'])
    elif "хром" in text.lower() or "chrome" in text.lower():
        subprocess.call(["C:\Program Files\Google\Chrome\Application\chrome.exe"])
    elif "динозаврик" in text.lower():
        print("він зламався(((")
    elif "логіка" in text.lower():
        webbrowser.open("https://learn.logikaschool.com/login")
    elif "youtube" in text.lower():
        webbrowser.open(f"https://youtube.com/results?search_query={text.lower()[7:]}")
    elif "погода" in text.lower():
        if len(text) > 7:  # перевірка, чи є після "погода" щось ще
            place = text[7:]
            place = ts.translate_text(place, from_language='uk', to_language='en')
            observation = owm.weather_manager().weather_at_place(place)
            location = observation.location
            weather = observation.weather
            weather = "Температура (градусів Цельсію): " + str(int(weather.temperature('celsius')['temp']))
            print(weather)
        else:
            print("Введіть місто для перевірки погоди.")
    elif "розкажи анекдот" in text.lower():
        print("Розкажи анекдот")
        tts = gtts.gTTS(text=('Програміст приходить в магазин з написом \"Знижка 50% на другий товар\".Скільки коштує цей монітор? - запитує він у продавця. 5000 гривень. Добре, я візьму два за 7500!'), lang='fr')
        tts.save('anigdot.mp3')
        anigdot.play()
    elif "гігабайт" in text.lower():
        webbrowser.open(f"https://www.youtube.com/watch?v=Nh7N2F-9ZbY&ab_channel=KirillDmitriev")
    elif "код" in text.lower():
        code = gpt.generate(text + ' і виведи тільки код')[4:-4]
        with open('code.py', 'w', encoding='utf-8') as file:
            file.write(code)
    elif "саня" in text.lower():
        result = gpt.generate(text + " and translate into Ukrainian. Don't print English words")
        print(result)
        try:
            myobj = gtts.gTTS(text=result, lang='uk', slow=True)
            myobj.save("result.mp3")
            os.system("result.mp3")
        except Exception as ex:
            print(ex)
            input()
    else:
        print("Я Вас не розумію. Повторіть Ваш запит.")
        unknown_command_count += 1

    return False

def choose_microphone():
    root = tk.Tk()
    root.withdraw()  # ховаємо основне вікно

    mic_list = list_connected_microphones()

    # Виведення вікна вибору мікрофона
    mic_choice = simpledialog.askstring("Вибір мікрофона", "Виберіть номер мікрофона:\n\n" +
                                        "\n".join([f"{i+1}: {mic}" for i, mic in enumerate(mic_list)]))

    if mic_choice.isdigit():
        selected_index = int(mic_choice) - 1
        if 0 <= selected_index < len(mic_list):
            return selected_index
    return default_mic_index

def main():
    global default_mic_index, unknown_command_count
    end_program = False
    silent_duration = 0

    print(f"Зараз вибраний мікрофон: {list_connected_microphones()[default_mic_index]}")
    print("Якщо виникли проблеми зі звуком, натисніть 'Q', щоб вибрати інший мікрофон.")

    while not end_program:
        if unknown_command_count >= 2 or silent_duration > 10:
            default_mic_index = choose_microphone()
            unknown_command_count = 0
            silent_duration = 0
            print(f"Використовую мікрофон: {list_connected_microphones()[default_mic_index]}")

        audio = capture_voice_input(default_mic_index)
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

        silent_duration += 1  # збільшення лічильника часу бездіяльності

if __name__ == "__main__":
    main()
