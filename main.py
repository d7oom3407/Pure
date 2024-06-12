import vosk
import pyaudio
import google.generativeai as genai

MODEL_PATH = 'large-model'

options = ['خفف ضغط المياه','زد ضغط المياه','أنزل درجة الحرارة','أرفع درجة الحرارة']

promt = f'انت مساعد صوتي لجهاز, كل ما اريدك فعله هو ان تحول كلام المتحدث الى 4 احتمالات. سوف أعطيك كلام المتحدث, وأريدك تحويله الى واحدة من هذه الإحتمالات {options}. حين ترد على الرسالة, رد فقط بواحدة من هذه الاحتمالات, لا تكثر الكلام فقط قل واحده منهم. في حين انك لم تستطع ان تستخرج مقصد المتحدث وتحديد احد الإحتمالات, قل خطأ بالكلام.'


def recognize_speech(model_path):
    # Initialize the Vosk recognizer with the provided model
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Set up PyAudio for recording
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

    print("Listening...")

    # Process the real-time audio stream and print the recognized text
    i = 0
    
    while i < 1:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(result[14:-3])

            if len(result[14:-3]) <= 0:
                continue
                
            i+=1
            
            

    result = result[14:-3]
    
    return result
    # print(result)

def gemini(input):
    genai.configure(api_key="AIzaSyAUI26s-KxBPyaXnET1Q07Q1X9iMAIeaIM")

    # Set up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": [promt]
    },
    {
        "role": "model",
        "parts": ["بالـاكيد"]
    },
    ])

    convo.send_message(input)
    return convo.last.text

# recognize_speech(MODEL_PATH)
user_said = recognize_speech(MODEL_PATH)

if user_said not in options:
    
    gemini_said = gemini(user_said)
    print(gemini_said)