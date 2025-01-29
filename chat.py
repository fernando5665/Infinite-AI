import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="TU_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Lista de archivos JSON a cargar
json_files = ["approval.json", "closingticket.json"]  # Agrega los archivos que necesitas
txt_file_path = "Infinite AI.txt"

# Función para cargar y combinar múltiples archivos JSON
def load_multiple_json(file_paths):
    combined_data = {}
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                combined_data.update(data)  # Une los diccionarios
        except FileNotFoundError:
            st.error(f"El archivo {file_path} no se encontró. Verifica la ruta.")
        except json.JSONDecodeError:
            st.error(f"El archivo {file_path} no tiene un formato JSON válido.")
    return combined_data

# Función para cargar un archivo TXT
def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error("El archivo TXT no se encontró. Verifica la ruta.")
        return None

# Cargar datos de múltiples archivos JSON
json_content = load_multiple_json(json_files)
txt_content = load_txt(txt_file_path)

# Configuración de la página
st.set_page_config(layout="wide", page_title="🤓 Assistant Interface")

# Crear columnas para notas e interfaz principal
col1, col2 = st.columns([1, 3])

with col1:
    st.header("📝 Important Notes")
    st.text("Aquí puedes agregar notas importantes...")
    st.image("Screenshot_6.jpg", caption="Ejemplo de imagen", use_container_width=True)

with col2:
    st.title("🤓 Assistant Interface")

    if json_content and txt_content:
        st.success("Hello 🖐️")

        # Input para preguntas del usuario
        user_input = st.text_input("Ask me a question:", "")

        if st.button("ok"):
            if user_input.strip():
                try:
                    # Crear el prompt combinando los datos de los JSONs y el TXT
                    prompt = f"JSON Content:\n{json.dumps(json_content, ensure_ascii=False, indent=2)}\n\nTXT Content:\n{txt_content}\n\nPregunta: {user_input}"
                    response = model.generate_content(prompt)
                    st.write("Respuesta:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error al generar la respuesta: {str(e)}")
            else:
                st.warning("Por favor, escribe una pregunta.")
    else:
        st.error("No se pudieron cargar todos los archivos.")
