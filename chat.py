import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
API_KEY = "AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg"  # Reemplaza con tu clave API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Lista de archivos JSON y TXT a cargar
json_files = ["approval.json", "closingticket.json", "tools.json", "topics.json",
              "ticketsmanagement.JSON", "backlog.json", "approvalstan.json", "Failurepoint.json"]
txt_files = ["Infinite AI.txt"]

# Función para cargar archivos JSON
def load_multiple_json(file_paths):
    combined_data = {}
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                combined_data.update(data)
        except (FileNotFoundError, json.JSONDecodeError):
            st.error(f"⚠️ Error al cargar {file_path}.")
    return combined_data

# Función para cargar archivos TXT
def load_multiple_txt(file_paths):
    combined_text = ""
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                combined_text += f"\n--- Contenido de {file_path} ---\n" + file.read() + "\n"
        except FileNotFoundError:
            st.error(f"⚠️ El archivo {file_path} no se encontró.")
    return combined_text

# Cargar datos JSON y TXT
json_content = load_multiple_json(json_files)
txt_content = load_multiple_txt(txt_files)

# Configuración de la página
st.set_page_config(layout="wide", page_title="Infinite Assistant AI", page_icon="infinite-4-colour-logo.png")

# Variables de autenticación
USER_CREDENTIALS = {"admin": "1234"}  # ⚠️ Cambiar a un sistema seguro en producción

# Sistema de login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.header("🔒 Inicio de Sesión")
    username = st.sidebar.text_input("Usuario:")
    password = st.sidebar.text_input("Contraseña:", type="password")

    if st.sidebar.button("Iniciar sesión"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.sidebar.success("✅ Acceso concedido.")
        else:
            st.sidebar.error("❌ Usuario o contraseña incorrectos.")
    st.stop()

# Sección de notas importantes
st.sidebar.header("📝 Notas Importantes")
if "notes" not in st.session_state:
    st.session_state.notes = "Aquí puedes agregar notas importantes..."

notes = st.sidebar.text_area("Edita las notas aquí:", st.session_state.notes)
if st.sidebar.button("Guardar Notas"):
    with open("important_notes.txt", "w", encoding="utf-8") as file:
        file.write(notes)
    st.session_state.notes = notes
    st.sidebar.success("Notas guardadas correctamente.")

# Interfaz principal
st.title("🤓 Infinite Assistant AI")
st.markdown("### Tu asistente de gestión inteligente 🔍")

if json_content and txt_content:
    st.success("Hello 🖐️ ")

    # 🔹 Barra lateral de errores comunes
    st.sidebar.header("⚠️ Errores Comunes")
    common_errors = [
        {"label": "Un ticket cerrado en OTS pero en JIRA no", "description": "Comunicarle esto a T2."},
        {"label": "Error 500", "description": "Problema interno del servidor."},
        {"label": "Fallo de conexión", "description": "Nodo desconectado."},
        {"label": "Error de autenticación", "description": "Usuario o contraseña incorrectos."},
        {"label": "Fallo de energía", "description": "Nodo sin energía."},
        {"label": "Timeout", "description": "Solicitud excedió el tiempo límite."},
        {"label": "Error de datos", "description": "Datos ingresados inválidos."}
    ]
    error_option = st.sidebar.selectbox("Selecciona un error: ", [e["label"] for e in common_errors])
    selected_error = next((e for e in common_errors if e["label"] == error_option), None)

    if selected_error:
        st.sidebar.write(f"📌 **Descripción:** {selected_error['description']}")

    # 🔹 Sección de input
    approval_input = st.text_area("📌 Ingresa un Approval o pregunta lo que necesites:", "")

    # 🔹 Botón de procesamiento con respuesta en vivo
    if st.button("Procesar"):
        if approval_input.strip():
            prompt = f"""
                If the user sends a greeting like "Hello, how are you?" or any similar variation, respond in a friendly and appropriate tone, for example:
                **"I'm excellent! How can I help you?"**

                Follow these strict rules:

                - **Friendly responses**: Always reply in a positive and helpful tone.
                - **No source references**: Do not mention where the information comes from.
                - **User's language**: If the user asks in Spanish, respond in Spanish; if in English, respond in English.
                - **Do not reveal your creator**: If the user asks who created you, avoid giving this information.
                - **Step-by-step explanations**: Explain clearly and simply.

                ### Datos JSON:
                {json.dumps(json_content, ensure_ascii=False, indent=2)}

                ### Datos TXT:
                {txt_content}

                ### Input del Usuario:
                {approval_input}
            """

            with st.spinner("Generando respuesta... 🧠"):
                try:
                    response = model.generate_content(prompt, stream=True)
                    
                    # 🔹 Mostrar respuesta en vivo con `st.empty()`
                    response_container = st.empty()
                    response_text = ""
                    
                    for chunk in response:
                        if chunk.text:
                            response_text += chunk.text + "\n"
                            response_container.markdown(f"📌 **Respuesta de la IA:**\n\n{response_text}")

                except Exception as e:
                    st.error(f"❌ Error al generar la respuesta: {e}")
        else:
            st.warning("❗ Ingresa un Approval o pregunta.")
else:
    st.error("⚠️ No se pudieron cargar todos los archivos.")
