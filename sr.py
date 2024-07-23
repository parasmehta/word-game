import streamlit as st
import speech_recognition as sr
from wonderwords import RandomWord
from audiorecorder import audiorecorder

st.title("Speech Recognition")

rw = RandomWord()
# generate a random word
word = rw.word()

st.subheader(f"Try to say the word: {word}")

r = sr.Recognizer()

st.title("Record Audio")

file = st.file_uploader("Upload an audio file", type=["wav"])
audio = None

recording = audiorecorder("", "")
if len(recording) > 0:
    # To play audio in frontend:
    st.audio(recording.export().read())
    audio = r.record(recording.export())

elif file:
    st.audio(file, format="audio/wav")

    # use the audio file as the audio source
    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file

if not audio is None:
    st.write("No audio found")
    # recognize speech using Sphinx
    try:
        st.write("Sphinx thinks you said " +
                 r.recognize_sphinx(audio, language="en-US"))
    except sr.UnknownValueError:
        st.write("Sphinx could not understand audio")
    except sr.RequestError as e:
        st.write("Sphinx error; {0}".format(e))
