import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Ruta del archivo JSON precargado
file_path = "file.json"

# Leer el archivo JSON precargado
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("El archivo JSON precargado no se encontró. Por favor, verifica la ruta.")
        return None
    except json.JSONDecodeError:
        st.error("El archivo precargado no es un JSON válido. Por favor, corrige el archivo.")
        return None

# Cargar contenido JSON
file_content = load_json(file_path)

# Definir apuntes importantes en el código
apuntes_importantes = """
Etiqueta:
Estas etiquetas deben usarse para los CSR (Tickets de Call Center), muy atentos

EXISTING TICKET: 
Ticket Duplicado, Falla trabajada bajo ticket numero 123456
	
NUMBER CMS DOESNT APPLY: 
Falla no cumple con Numero de Cable Modems Offline requeridos: 5
	
GEOGRAPHIC DISTRIBUTION CMS: 
CMs solicitados no se encuentran relacionados en la misma zona geográfica.
👌
"""

# Configurar el diseño de la aplicación
st.set_page_config(layout="wide", page_title="🤓 Assistant Interface")

# Crear dos columnas: una para apuntes y otra para la interfaz principal
col1, col2 = st.columns([1, 3])

# Mostrar los apuntes importantes en la primera columna
with col1:
    st.header("📝 Apuntes Importantes")
    st.text(apuntes_importantes)

# Mostrar la interfaz principal en la segunda columna
with col2:
    st.title("🤓 Assistant Interface")

    if file_content:
        st.success("El archivo JSON precargado se cargó exitosamente.")

        # Input para preguntas del usuario
        user_input = st.text_input("Haz una pregunta basada en el contenido del archivo:", "")

        # Botón para procesar la pregunta
        if st.button("Submit"):
            if user_input.strip():
                try:
                    # Generar respuesta con la API usando el contenido del archivo
                    file_content_str = json.dumps(file_content, ensure_ascii=False, indent=4)
                    response = model.generate_content(f"{file_content_str}\n\nPregunta: {user_input}")
                    st.write("Respuesta:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Ocurrió un error al generar la respuesta: {str(e)}")
            else:
                st.warning("Por favor, escribe una pregunta.")
    else:
        st.error("El contenido del archivo JSON no está disponible. Por favor, verifica el archivo.")
