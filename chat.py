import streamlit as st
import json
import google.generativeai as genai

# Configurar la API de Generative AI
genai.configure(api_key="AIzaSyClHLf12XSGEBHZgKhVtSmPf6R68G_VLdg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Lista de archivos JSON a cargar
json_files = ["approval.json", "closingticket.json", "tools.json", "topics.json", "ticketsmanagement.JSON", "backlog.json", "approvalstan.json","approval.json","Failurepoint.json"]

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

# Variables de autenticación
USER_CREDENTIALS = {"admin": "1234"}  # Puedes cambiar esto por un sistema más seguro

# Crear columnas para notas e interfaz principal
col1, col2 = st.columns([1, 3])

with col1:
    st.header("📝 Important Notes")
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        username = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")
        if st.button("Iniciar sesión"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.success("Acceso concedido. Ahora puedes editar las notas.")
            else:
                st.error("Usuario o contraseña incorrectos.")
    
    if st.session_state.authenticated:
        notes = st.text_area("Edita las notas importantes aquí:", "Aquí puedes agregar notas importantes...")
        if st.button("Guardar Notas"):
            with open("important_notes.txt", "w", encoding="utf-8") as file:
                file.write(notes)
            st.success("Notas guardadas correctamente.")
    else:
        st.text("Aquí puedes agregar notas importantes...")

with col2:
    st.title("🤓 Infinite Assistant ")

    if json_content and txt_content:
        st.success("Hello 🖐️")

        # Agregar un apartado con los errores comunes
        st.sidebar.header("Errores Comunes")
        common_errors = [
            {"label": "Error 404: Página no encontrada", "description": "Este error ocurre cuando la página solicitada no se encuentra en el servidor."},
            {"label": "Error 500: Problema interno del servidor", "description": "Este error indica que hubo un problema en el servidor al intentar procesar la solicitud."},
            {"label": "Fallo de conexión: El nodo está desconectado", "description": "El nodo no puede conectarse correctamente a la red."},
            {"label": "Error de autenticación: Usuario o contraseña incorrectos", "description": "Este error ocurre cuando las credenciales de inicio de sesión no son válidas."},
            {"label": "Fallo de energía: El nodo no tiene energía", "description": "El nodo no está recibiendo energía, lo que impide su funcionamiento."},
            {"label": "Timeout: La solicitud ha excedido el tiempo límite", "description": "Este error ocurre cuando el tiempo de espera para recibir una respuesta del servidor es demasiado largo."},
            {"label": "Error de datos: Los datos ingresados no son válidos", "description": "Los datos que se han ingresado no son válidos o están en un formato incorrecto."}
        ]

        # Input para elegir un error común
        error_option = st.sidebar.selectbox(
            "Selecciona un error común para más detalles:",
            [error["label"] for error in common_errors]
        )

        # Mostrar la descripción del error seleccionado
        selected_error = next((error for error in common_errors if error["label"] == error_option), None)
        if selected_error:
            st.sidebar.write(f"**Descripción:** {selected_error['description']}")

        # Input para approval y preguntas
        approval_input = st.text_area("📌 Ingresa un Approval o pregunta lo que necesites:", "")

        if st.button("Process"):
            if approval_input.strip():
                try:
                    # Construcción del prompt para approvals y preguntas generales
                    prompt = f"""If the user sends a greeting like "Hola, ¿cómo estás?" or any similar variation, respond in a friendly and appropriate tone, for example: "I'm excellent! How can I help you?"

                    Follow these rules strictly:

                    Friendly Responses: Always respond in a positive and helpful tone.
                    No Source References: Do not mention where the information comes from or where it can be found.
                    Respond in the User's Language: If the user asks in English, respond in English if the user asks in spanish , respond in spanish.
                    Restriction on the Creator: If the user asks who created you, do not provide this information.
                    Step-by-Step Explanations: Explain responses in a detailed and step-by-step manner in a simple way.







                                        
                    {json.dumps(json_content, ensure_ascii=False, indent=2)}

                    ### Datos TXT Cargados:
                    {txt_content}

                    ### Input del Usuario:
                    {approval_input}
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
