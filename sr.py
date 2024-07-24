import streamlit as st
import speech_recognition as sr
from wonderwords import RandomWord
import pyttsx3


word_generator = RandomWord()


def hear_pronunciation():
    if 'current_word' in st.session_state:
        engine = pyttsx3.init()
        engine.stop()
        engine.say(st.session_state.current_word)
        engine.runAndWait()


def generate_random_word():
    word = word_generator.word()
    st.session_state.current_word = word
    print("word", word)
    print("current_word", st.session_state.current_word)


def get_current_word():
    return st.session_state.current_word if 'current_word' in st.session_state else ""


def get_transcription():
    return st.session_state.transcription if 'transcription' in st.session_state else ""


def listener():
    ''' listen to the users speech to determine what the next step should be'''
    r = sr.Recognizer()  # initialize a recognizer object
    with sr.Microphone() as source:  # use the microphone
        r.adjust_for_ambient_noise(source)
        print("Speak Anything :")
        audio = r.listen(source)  # record the audio, store in audio wav file
        try:
            text = r.recognize_sphinx(audio)
            print("You said : {}".format(text))
        except:
            print("Sorry could not recognize what you said")
            text = ""
        st.session_state.transcription = text


def transcribe_from_file(file):
    r = sr.Recognizer()
    audio = None
    st.audio(file, format="audio/wav")

    # use the audio file as the audio source
    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file

    transcription = ""
    if audio:
        try:
            transcription = r.recognize_sphinx(audio)
            st.write("Sphinx thinks you said " +
                     transcription)
        except sr.UnknownValueError:
            st.write("Sphinx could not understand audio")
        except sr.RequestError as e:
            st.write("Sphinx error; {0}".format(e))
        st.session_state.transcription = transcription


"""
# Word speaking game 🎤

Pick any English word and test if you speak it correctly.
***

"""
col1, col2 = st.columns([1, 1], gap="medium")
st.markdown("***")

with col1:
    """
    **Enter a word or pick a random one**
    """
    word = st.text_input(label="Enter a word",
                         placeholder="Enter a word", label_visibility="hidden")
    if word:
        st.session_state.current_word = word

    st.button("Pick random word", on_click=generate_random_word)

    if len(get_current_word()) > 0:
        st.subheader(f"Try to say: {get_current_word()}")
        hear_pronunciation()

# st.button("Hear pronunciation", on_click=lambda: hear_pronunciation)
with col2:
    if len(get_current_word()) > 0:
        """
        **Record yourself or upload a recording**
        """
        file = st.file_uploader("Upload recording", type=[
                                "wav"], label_visibility="hidden")

        if file:
            transcribe_from_file(file)

        st.button("Record word", on_click=listener)

current_word = get_current_word()
transcription = get_transcription()

col11, col12 = st.columns([1, 1], gap="medium")

if current_word and transcription and len(current_word) > 0 and len(transcription) > 0:

    # col11.write(f"**We expected**")
    col11.write(f"#### {current_word}")
    # col12.write(f"**You said**")
    col12.write(f"#### {transcription}")

    if current_word.lower() == transcription.lower():
        st.write('<h3 style="color: green">You got it!</span>',
                 unsafe_allow_html=True)
    else:
        st.write('<h3 style="color: red">Try again.</span>',
                 unsafe_allow_html=True)

# recording = audiorecorder("", "")
# if len(recording) > 0:
#     # To play audio in frontend:
#     file = recording.export()
#     st.audio(file.read(), format="audio/wav")
#     buffer = io.BytesIO()
#     recording.export(buffer, format="wav")
#     buffer.seek(0)
#     with sr.AudioFile(buffer) as detection:
#         recording_transcription = r.recognize_sphinx(r.record(detection))
#         st.write("Sphinx thinks you said " + recording_transcription)
