import os
import io
import spacy
import pytesseract
from PIL import Image
import PyPDF2
import streamlit as st
from moviepy.editor import VideoFileClip
import speech_recognition as sr

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Function for audio transcription
import pydub

# Function for audio transcription
import os
import pydub


# Function for audio transcription
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    # Convert MP3 to WAV
    sound = pydub.AudioSegment.from_mp3(audio_file)
    wav_path = os.path.join(os.path.dirname(audio_file), "temp_audio.wav")  # Save the temporary WAV file in the same directory
    sound.export(wav_path, format="wav")

    with sr.AudioFile(wav_path) as source:
        audio_text = recognizer.recognize_google(source)

    # Remove temporary WAV file
    os.remove(wav_path)

    return audio_text




def video_to_text(video_file):
    clip = VideoFileClip(video_file)
    audio = clip.audio
    if audio is not None:
        audio.write_audiofile("temp_audio.wav")
        text = audio_to_text("temp_audio.wav")
        os.remove("temp_audio.wav")
        return text
    else:
        return "Error: Could not extract audio from video file."

# Function for text extraction (no additional libraries needed)

def text_to_text(text_file):
    with open(text_file, 'r') as file:
        text = file.read()
    return text  # Simply return the text as a string

import pytesseract
from PIL import Image


# Function for image to text
def image_to_text(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text

# Function for PDF to text
def pdf_to_text(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function for file to text
def file_to_text(file_path, file_type):
    if file_type == 'audio':
        return audio_to_text(file_path)
    elif file_type == 'video':
        return video_to_text(file_path)
    elif file_type == 'text':
        return text_to_text(file_path)
    elif file_type == 'image':
        return image_to_text(file_path)
    elif file_type == 'pdf':
        return pdf_to_text(file_path)
    else:
        return "Unsupported file type"
    
#def medical_transcription(text):
    # Perform medical entity extraction
    medical_entities = extract_medical_entities(text)
    
    # Print or log the extracted entities for debugging
    print("Extracted Medical Entities:", medical_entities)

    # Customize medical transcription as needed
    medical_transcription = "Medical Entities:\n"
    for entity in medical_entities:
        label = entity[1]
        if label == 'PATIENT':
            medical_transcription += "Patient: {}\n".format(entity[0])
        elif label == 'DOCTOR':
            medical_transcription += "Doctor: {}\n".format(entity[0])
        elif label == 'HOSPITAL':
            medical_transcription += "Hospital: {}\n".format(entity[0])
        elif label == 'DATE':
            medical_transcription += "Date: {}\n".format(entity[0])
        elif label == 'TIME':
            medical_transcription += "Time: {}\n".format(entity[0])
        elif label == 'YEAR':
            medical_transcription += "Year: {}\n".format(entity[0])
        elif label == 'PROBLEM':
            medical_transcription += "Problem: {}\n".format(entity[0])
        elif label == 'TREATMENT':
            medical_transcription += "Treatment: {}\n".format(entity[0])
        elif label == 'DIAGNOSIS':
            medical_transcription += "Diagnosis: {}\n".format(entity[0])
        elif label == 'MEDICINE_PRESCRIBED':
            medical_transcription += "Medicine Prescribed: {}\n".format(entity[0])
        elif label == 'NEXT_SCHEDULED_DATE':
            medical_transcription += "Next Scheduled Date: {}\n".format(entity[0])
    
    return medical_transcription

def medical_transcription(text):
    # Perform medical entity extraction
    medical_entities = extract_medical_entities(text)

    # Filter the entities to only include 'PROBLEM' and 'MEDICINE_PRESCRIBED' entities
    medical_entities = [ent for ent in medical_entities if ent[1] in ['PROBLEM', 'MEDICINE_PRESCRIBED']]

    # Print or log the extracted entities for debugging
    print("Extracted Medical Entities:", medical_entities)

    # Customize medical transcription as needed
    medical_transcription = "Medical Entities:\n"
    for entity in medical_entities:
        label = entity[1]
        if label == 'PROBLEM':
            medical_transcription += "Problem: {}\n".format(entity[0])
        elif label == 'MEDICINE_PRESCRIBED':
            medical_transcription += "Medicine Prescribed: {}\n".format(entity[0])

    return medical_transcription



def extract_medical_entities(text):
    doc = nlp(text)
    medical_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ['PATIENT', 'DOCTOR', 'HOSPITAL', 'DATE', 'TIME', 'YEAR', 'PROBLEM', 'TREATMENT', 'DIAGNOSIS', 'MEDICINE_PRESCRIBED', 'NEXT_SCHEDULED_DATE']]
    
    # Print or log the extracted entities for debugging
    print("Extracted Medical Entities:", medical_entities)

    return medical_entities






# Streamlit app
def main():
    # Set page header
    st.title("UPLOAD THE FILE FOR MEDICAL TRANSCRIPTION")
    st.markdown("Upload a file to extract medical entities and generate a medical transcription.")

    # Add file uploader
    uploaded_file = st.file_uploader("Upload a file", type=["mp3", "wav", "ogg", "mp4", "avi", "mov", "mkv", "txt", "pdf", "png", "jpg", "jpeg", "gif"])

    print(uploaded_file)

    if uploaded_file is not None:
        try:
            # Get file type
            file_type = uploaded_file.type.split('/')[0]
            print(file_type)
            # Save uploaded file to local directory
            file_path = os.path.join("", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Perform file to text conversion
            extracted_text = file_to_text(file_path, file_type)
           
            # Show extracted text
            st.write("Extracted Text:")
            st.write(extracted_text)

            # Perform medical transcription
            medical_transcription_result = medical_transcription(extracted_text)
            print('1',medical_transcription_result)
            # Show medical transcription
            st.write("Medical Transcription:")
            st.write(medical_transcription_result)

            # Convert the transcription result to bytes
            medical_transcription_bytes = medical_transcription_result.encode("utf-8")
            print(medical_transcription_bytes)
            st.download_button(
                label="Download Medical Transcription",
                data=medical_transcription_bytes,
                file_name="medical_transcription.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error("An error occurred: {}".format(str(e)))

if __name__ == "__main__":
    main()
