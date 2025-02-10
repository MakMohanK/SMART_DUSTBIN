# data = [[3, 0.73132044], [3, 0.73746955], [3, 0.6601949], [3, 0.6934062], [3, 0.554659], [3, 0.6151925], [11, 0.6368791], [11, 0.53130126], [3, 0.50032437], [3, 0.7338015], [3, 0.49550095], [11, 0.52574635], [3, 0.7138178], [3, 0.7919383], [6, 0.35174054], [8, 0.50491047], [3, 0.5314065], [11, 0.5744556], [3, 0.64253205], [11, 0.6323998], [3, 0.62508845], [3, 0.7424445], [11, 0.5144408], [3, 0.6895861], [3, 0.6566356], [11, 0.63161534], [3, 0.51384205], [3, 0.59737384], [3, 0.49087632], [3, 0.60372907], [11, 0.6847117], [7, 0.60201216], [3, 0.6552892], [11, 0.5514322], [11, 0.65495783], [3, 0.62218237], [3, 0.5045338], [3, 0.69860435], [3, 0.6613758], [3, 0.5490467], [11, 0.5008636], [3, 0.6194321], [7, 0.7330131], [3, 0.59414107], [11, 0.4905264], [11, 0.6826514], [3, 0.5033117], [3, 0.5589934], [3, 0.6978589], [3, 0.6522905]]


# last_conf = 0
# last_index = 0
# for x in data:
#     if x[1] > last_conf:
#         last_index = x[0]
#         last_conf = x[1]
    
# print("Confidence :", last_conf, "Index:",last_index)

# num = int(input("ENter Number"))

# num1 = (num*num)
# num2  = (num-1)*(num-1)

# output = num1+num2
# print(output)


from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    """
    Converts text to speech using Google Text-to-Speech (gTTS).
    :param text: String, the text to be spoken.
    :param lang: Language code (default is English).
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # You may need to install mpg321 with `sudo apt install mpg321`

# Example usage
if __name__ == "__main__":
    text = "Hello, welcome to text-to-speech conversion using gTTS!"
    text_to_speech(text)
