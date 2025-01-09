import streamlit as st
from PIL import Image
from services.auth_service import authenticate
from services.clients_service import init_clients_db, get_clients, add_client, update_client, delete_client
from services.cronogramas_service import init_cronogramas_db, add_cronograma, get_cronogramas, delete_cronograma
from services.crew_service import generate_schedule

# Iniciar personalização
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregar o CSS personalizado
load_css()

# Inicializar Bancos de Dados
init_clients_db()
init_cronogramas_db()

# Exibir o logotipo em todas as páginas
def render_logo():
    logo = Image.open("assets/logo.png")
    st.sidebar.image(logo, use_container_width=True)

# Função para atualizar a página
def reload_page():
    st.experimental_set_query_params(updated="true")

# Tela de Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("Login")
    render_logo()
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos!")
    st.stop()

# Navegação
st.sidebar.title("Navegação")
render_logo()
page = st.sidebar.selectbox("Selecione uma página", ["Cadastro de Clientes", "Gerar Cronograma", "Cronogramas Antigos"])

if page == "Cadastro de Clientes":
    st.title("Cadastro de Clientes")

    # Exibe clientes já cadastrados
    st.subheader("Clientes Cadastrados")
    clients = get_clients()
    for client in clients:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.write(f"**{client[1]}** - {client[2]}")  # Nome e Setor
        with col2:
            if st.button("Editar", key=f"edit_{client[0]}"):
                # Adiciona cliente selecionado ao estado da sessão
                st.session_state.editing_client = {
                    "id": client[0],
                    "name": client[1],
                    "sector": client[2],
                    "content_demand": client[3],
                    "description": client[4],
                }
        with col3:
            if st.button("Excluir", key=f"delete_{client[0]}"):
                delete_client(client[0])
                st.success(f"Cliente '{client[1]}' excluído com sucesso!")
                reload_page()  # Atualiza a página

    # Exibe formulário de edição se algum cliente estiver sendo editado
    if "editing_client" in st.session_state:
        st.markdown("---")
        st.subheader(f"Editando Cliente: {st.session_state.editing_client['name']}")
        with st.form(key="edit_client_form"):
            name = st.text_input("Nome do Cliente", value=st.session_state.editing_client["name"])
            sector = st.text_input("Setor", value=st.session_state.editing_client["sector"])
            content_demand = st.number_input("Demanda de Conteúdo", min_value=1, value=st.session_state.editing_client["content_demand"])
            description = st.text_area("Descrição", value=st.session_state.editing_client["description"])
            save_button = st.form_submit_button("Salvar Alterações")

            if save_button:
                update_client(
                    st.session_state.editing_client["id"],
                    name,
                    sector,
                    content_demand,
                    description,
                )
                st.success("Cliente atualizado com sucesso!")
                del st.session_state.editing_client  # Remove estado de edição
                reload_page()  # Atualiza a página

    # Formulário para adicionar novos clientes
    st.subheader("Adicionar Novo Cliente")
    name = st.text_input("Nome do Cliente")
    sector = st.text_input("Setor")
    content_demand = st.number_input("Demanda de Conteúdo", min_value=1)
    description = st.text_area("Descrição")
    if st.button("Salvar Cliente"):
        add_client(name, sector, content_demand, description)
        st.success("Cliente salvo com sucesso!")
        reload_page()  # Atualiza a página

elif page == "Gerar Cronograma":
    st.title("Gerar Cronograma")
    clients = get_clients()
    client_name = st.selectbox("Selecione o Cliente", [c[1] for c in clients])
    goal = st.text_input("Objetivo do Mês")
    video_count = st.number_input("Quantidade de Vídeos", min_value=1)
    static_post_count = st.number_input("Quantidade de Posts Estáticos", min_value=1)
    days_selected = st.multiselect("Dias de Postagem", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])

    if st.button("Gerar Cronograma"):
        client_description = next(c[4] for c in clients if c[1] == client_name)
        output = generate_schedule(client_name, client_description, goal, video_count, static_post_count, days_selected)
        st.subheader("Resultado do Cronograma")
        if output and hasattr(output, "raw"):
            st.markdown(output.raw)
        else:
            st.error("Erro ao gerar o cronograma. Verifique os parâmetros e tente novamente.")

elif page == "Cronogramas Antigos":
    st.title("Cronogramas Antigos")
    
    # Adicionar novo cronograma
    st.subheader("Adicionar Cronograma Antigo")
    clients = get_clients()
    client_name = st.selectbox("Selecione o Cliente", [c[1] for c in clients])
    client_id = next(c[0] for c in clients if c[1] == client_name)
    cronograma_content = st.text_area("Conteúdo do Cronograma")
    if st.button("Salvar Cronograma"):
        add_cronograma(client_id, client_name, cronograma_content)
        st.success("Cronograma salvo com sucesso!")
        reload_page()  # Atualiza a página

    # Listar cronogramas existentes
    st.subheader("Cronogramas Armazenados")
    cronogramas = get_cronogramas()
    for cronograma in cronogramas:
        with st.expander(f"Cronograma para {cronograma[1]}"):
            st.write(f"**Conteúdo:** {cronograma[2]}")
            if st.button("Excluir", key=f"delete_{cronograma[0]}"):
                delete_cronograma(cronograma[0])
                st.success("Cronograma excluído com sucesso!")
                reload_page()  # Atualiza a página
