

import streamlit as st
import json
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Intercambio Navideño 🎄", page_icon="🎁")
DATA_FILE = 'regalos_familia.json'

# --- FUNCIONES DE DATOS ---
def get_default_data():
    """Genera datos de prueba iniciales (Pantalón, Camisa, etc.)"""
    return {
        "Papá": [
            {"item": "Libro de historia", "tomado": False, "tomado_por": None}
        ],
        "Mamá": [],
        "Hijo/a Mayor": [
            {"item": "Pantalón", "tomado": False, "tomado_por": None},
            {"item": "Camisa", "tomado": False, "tomado_por": None},
            {"item": "Bicicleta", "tomado": False, "tomado_por": None},
            {"item": "Billetera", "tomado": False, "tomado_por": None}
        ],
        "Hijo/a Menor": []
    }

def load_data():
    if not os.path.exists(DATA_FILE):
        data = get_default_data()
        save_data(data)
        return data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return get_default_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- INICIO DE LA APP ---
data = load_data()

# --- BARRA LATERAL (LOGIN) ---
st.sidebar.title("🎅 Login Familiar")
users = list(data.keys())
usuario_actual = st.sidebar.selectbox("Soy:", users)

if st.sidebar.button("🔄 Reiniciar Todo"):
    save_data(get_default_data())
    st.rerun()

# --- TÍTULO ---
st.title(f"Hola, {usuario_actual} 👋")

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📝 Mi Lista (Pedir)", "🎁 Lista de los demás (Regalar)"])

# --- PESTAÑA 1: PEDIR ---
with tab1:
    st.header("¿Qué quieres recibir?")
    with st.form("nuevo_regalo"):
        nuevo = st.text_input("Escribe tu deseo:")
        if st.form_submit_button("Agregar") and nuevo:
            data[usuario_actual].append({"item": nuevo, "tomado": False, "tomado_por": None})
            save_data(data)
            st.success(f"¡{nuevo} agregado!")
            st.rerun()

    st.divider()
    st.subheader("Tu lista actual:")
    mi_lista = data[usuario_actual]
    if not mi_lista:
        st.info("No has pedido nada aún.")
    else:
        for i, regalo in enumerate(mi_lista):
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**• {regalo['item']}**")
            if c2.button("🗑️", key=f"del_{i}"):
                mi_lista.pop(i)
                save_data(data)
                st.rerun()

# --- PESTAÑA 2: REGALAR ---
with tab2:
    st.header("Escoge a quién regalar")
    otros = [u for u in users if u != usuario_actual]
    destinatario = st.selectbox("Ver lista de:", otros)
    
    if destinatario:
        st.subheader(f"Lista de {destinatario}:")
        lista_dest = data[destinatario]
        if not lista_dest:
            st.warning("No ha pedido nada todavía.")
        
        for i, regalo in enumerate(lista_dest):
            with st.container(border=True):
                c1, c2 = st.columns([3, 2])
                nombre = regalo['item']
                tomado = regalo['tomado']
                
                with c1:
                    if tomado:
                        st.markdown(f"~~{nombre}~~ (Seleccionado)")
                    else:
                        st.markdown(f"### {nombre}")
                with c2:
                    if not tomado:
                        if st.button("🎁 Lo regalo yo", key=f"pick_{destinatario}_{i}"):
                            regalo['tomado'] = True
                            regalo['tomado_por'] = usuario_actual
                            save_data(data)
                            st.rerun()
                    elif regalo['tomado_por'] == usuario_actual:
                        st.success("¡Tú lo regalas!")
                        if st.button("Cancelar", key=f"drop_{destinatario}_{i}"):
                            regalo['tomado'] = False
                            regalo['tomado_por'] = None
                            save_data(data)
                            st.rerun()
                    else:
                        st.error("Ya reservado")
