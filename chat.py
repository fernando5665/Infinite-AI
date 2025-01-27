import streamlit as st
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Ruta del archivo precargado en el código
file_path = "Infinite AI.txt"

# Leer el contenido del archivo precargado
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error("El archivo no se encontró. Por favor, verifica la ruta.")
        return None

file_content = read_file(file_path)

# Aplicación principal con Streamlit
st.title("🤓 Assistant Interface")

if file_content:
    st.success("El contenido del archivo está cargado exitosamente. Puedes hacer preguntas ahora.")

    # Input para preguntas del usuario
    user_input = st.text_input("Haz una pregunta basada en el contenido del archivo:", "")

    # Botón para procesar la pregunta
    if st.button("Submit"):
        if user_input.strip():
            try:
                # Generar respuesta con la API
                response = model.generate_content(f"{file_content}\n\nPregunta: {user_input}")
                st.write("Respuesta:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Ocurrió un error al generar la respuesta: {str(e)}")
        else:
            st.warning("Por favor, escribe una pregunta.")
else:
    st.error("El contenido del archivo no está disponible. Por favor, verifica el archivo.")
