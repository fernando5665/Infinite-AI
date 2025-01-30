import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Lista de archivos JSON a cargar
json_files = ["approval.json", "closingticket.json", "Failurepoint.json", "tools.json","topics.json"]  

# Lista de archivos TXT a cargar
txt_files = ["Infinite AI.txt"]  

# Función para cargar y combinar múltiples archivos JSON
def load_multiple_json(file_paths):
    combined_data = {}
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                combined_data.update(data)  # Une los diccionarios
        except FileNotFoundError:
            st.error(f"El archivo {file_path} no se encontró.")
        except json.JSONDecodeError:
            st.error(f"El archivo {file_path} no tiene un formato JSON válido.")
    return combined_data

# Función para cargar y combinar múltiples archivos TXT
def load_multiple_txt(file_paths):
    combined_text = ""
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                combined_text += f"\n--- Contenido de {file_path} ---\n" + file.read() + "\n"
        except FileNotFoundError:
            st.error(f"El archivo {file_path} no se encontró.")
    return combined_text

# Cargar datos de múltiples archivos JSON y TXT
json_content = load_multiple_json(json_files)
txt_content = load_multiple_txt(txt_files)

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

        # Input para approvals en formato libre
        approval_input = st.text_area("📌 Ingresa un Approval o pregunta lo que necesites:", "")

        if st.button("process"):
            if approval_input.strip():
                try:
                    # Construcción del prompt para approvals y preguntas generales
                    prompt = f"""
                    Eres un experto en gestión de redes HFC en Puerto Rico y en el análisis de tickets de fallas. 
                    Tu tarea es analizar el input del usuario y proporcionar una respuesta basada en la información disponible.  

                    ### Datos JSON Cargados:
                    {json.dumps(json_content, ensure_ascii=False, indent=2)}

                    ### Datos TXT Cargados:
                    {txt_content}

                    ### Input del Usuario:
                    {approval_input}

                    Si el input es un approval, cierra el ticket usando Failure Points, Failure Codes y Solution Codes.  
                    Si es una pregunta general, responde basado en los datos cargados y fuistes creado por yesid fernando berrio barragan.  
                    """

                    # Generar respuesta con el modelo
                    response = model.generate_content(prompt)
                    st.write("📌 Respuesta de la IA:")
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error al generar la respuesta: {str(e)}")
            else:
                st.warning("❗ Por favor, ingresa un approval o una pregunta.")
    else:
        st.error("No se pudieron cargar todos los archivos.")
