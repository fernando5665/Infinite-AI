import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Rutas de los archivos
json_file_path = "file.json"
txt_file_path = "Infinite AI.txt"

# Función para cargar un archivo JSON
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("El archivo JSON no se encontró. Verifica la ruta.")
        return None
    except json.JSONDecodeError:
        st.error("El archivo no tiene un formato JSON válido.")
        return None

# Función para cargar un archivo TXT
def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return content  # Retorna el contenido del archivo como texto plano
    except FileNotFoundError:
        st.error("El archivo TXT no se encontró. Verifica la ruta.")
        return None
    except Exception as e:
        st.error(f"Error al cargar el archivo TXT: {str(e)}")
        return None

# Cargar los contenidos de los archivos
json_content = load_json(json_file_path)
txt_content = load_txt(txt_file_path)

# Configuración de la página
st.set_page_config(layout="wide", page_title="🤓 Assistant Interface")

# Crear dos columnas: una para apuntes y otra para la interfaz principal
col1, col2 = st.columns([1, 3])

# Mostrar notas importantes y ejemplos en la primera columna
with col1:
    st.header("📝 Important Notes")
    apuntes_importantes = """
    Etiqueta:
    Estas etiquetas deben usarse para los CSR (Tickets de Call Center), muy atentos:

    EXISTING TICKET:
    Ticket Duplicado, Falla trabajada bajo ticket numero 123456.

    NUMBER CMS DOESNT APPLY:
    Falla no cumple con Número de Cable Modems Offline requeridos: 5.

    GEOGRAPHIC DISTRIBUTION CMS:
    CMs solicitados no se encuentran relacionados en la misma zona geográfica.
    """
    st.text(apuntes_importantes)

    # Agregar una imagen de ejemplo en las notas
    st.image("Screenshot_6.jpg", caption="Ejemplo de imagen", use_container_width=True)

# Mostrar interfaz principal en la segunda columna
with col2:
    st.title("🤓 Assistant Interface")

    if json_content and txt_content:
        st.success("Hello 🖐️")

        # Input para preguntas del usuario
        user_input = st.text_input("Ask me a question:", "")

        # Procesar la pregunta con los dos contenidos
        if st.button("ok"):
            if user_input.strip():
                try:
                    # Preparar el prompt combinando los contenidos de ambos archivos
                    prompt = f"JSON Content:\n{json.dumps(json_content, ensure_ascii=False, indent=2)}\n\nTXT Content:\n{txt_content}\n\nPregunta: {user_input}"
                    response = model.generate_content(prompt)
                    st.write("Respuesta:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error al generar la respuesta: {str(e)}")
            else:
                st.warning("Por favor, escribe una pregunta.")
    else:
        st.error("No se pudieron cargar ambos archivos. Por favor, verifica los archivos.")
