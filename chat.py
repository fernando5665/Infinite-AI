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

# Aplicación principal
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

# Espacio para apuntes importantes
st.header("📝 Apuntes Importantes")
with st.form("apuntes_form"):
    apuntes = st.text_area("Escribe tus apuntes aquí:", "", height=200)
    guardar = st.form_submit_button("Guardar Apuntes")

if guardar:
    # Guardar apuntes en un archivo de texto
    with open("apuntes_importantes.txt", "a", encoding="utf-8") as file:
        file.write(apuntes + "\n")
    st.success("¡Tus apuntes se han guardado correctamente!")
