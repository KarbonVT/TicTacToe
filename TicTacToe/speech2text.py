from scipy.io.wavfile import write
import sounddevice as sd
import whisper
import keyboard
from game import Game
from interpreter import interpret
import requests


def start_recording():
    print("Recording started!")
    
    freq = 32000
    duration = 3
    # Record audio with shared access to the microphone
    try:
        wasapi_exclusive = sd.WasapiSettings(exclusive=False)
        print("Recording...")
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2) 
        sd.wait()     
        print("Done.")
        # This will convert the NumPy array to an audio file with the given sampling frequency
        write(r"B:\Karbon Projects\Audio\recording0.wav", freq, recording)

    except sd.PortAudioError as e:
        print(f"An error occurred while recording: {e}")  

    # Trancsribe audio 
    result = model.transcribe(r"B:\Karbon Projects\Audio\recording0.wav", fp16=False, language='English')
 
    # Get coordinates from interpreter
    x_coords, y_coords = interpret(result["text"])
    url = "http://127.0.0.1:5000/consolelog/" + result["text"]
    requests.get(url)

    if x_coords is None or y_coords is None: 
        #url = "http://127.0.0.1:5000/consolelog/" + "Sorry I didnt understand you"
        requests.get(url) 
 
        wait_for_spacebar()
        return
    else:
        game.move("X", (y_coords, x_coords)) 
    
def wait_for_spacebar():
    while True:
        keyboard.wait('space') 
        start_recording()

# Load all models and device connections         

#------------------------------
# AUDIO
#------------------------------
# Query and print all available audio devices
input_device = None
try:
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        if "HD Pro Webcam C920" in device['name']:
            input_device = idx  

except sd.PortAudioError as e:
    print(f"An error occurred while querying devices: {e}")

# Using input device
print(f"Using input device: {sd.query_devices(input_device)}")

# Set the default input device
sd.default.device = input_device

#------------------------------                
# SPEECH2TEXT     
#------------------------------
model = whisper.load_model("base")

#------------------------------
# Tic-Tac-Toe
#------------------------------
game = Game("A1")



if __name__ == "__main__":
    wait_for_spacebar()