import hmac

import streamlit as st


def senha_valida(senha: str | None) -> bool:
    if not senha:
        return False
    return hmac.compare_digest(str(senha), str(st.secrets["PASSWORD"]))


def esta_autenticado() -> bool:
    """Autentica pela sessão ou pelo parâmetro ?password= da URL (links salvos continuam funcionando)."""
    if not st.session_state.get("autenticado") and senha_valida(st.query_params.get("password")):
        st.session_state["autenticado"] = True
    return st.session_state.get("autenticado", False)


def tela_de_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.title(":material/lock: Contador de Horas")
        st.caption("Acesso restrito. Digite a senha para continuar.")

        with st.form("login"):
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)

        if entrar:
            if senha_valida(senha):
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")


def botao_sair():
    if st.sidebar.button("Sair", icon=":material/logout:"):
        st.session_state.clear()
        if "password" in st.query_params:
            del st.query_params["password"]
        st.rerun()
