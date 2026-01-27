import streamlit as st
import time

# 1. Configuração da Página (Layout Centralizado e Limpo)
st.set_page_config(
    page_title="OpenCanvas Pro | Coming Soon",
    page_icon="🍊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Customizado (Esconde menu e rodapé padrão para parecer SaaS Profissional)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Título Principal */
    h1 {
        text-align: center;
        color: #ff4b4b;
        font-weight: 800;
        font-size: 3.5rem !important;
        margin-bottom: 0px;
    }
    
    /* Subtítulo */
    .subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 30px;
    }
    
    /* Texto de destaque */
    .hero-text {
        text-align: center; 
        color: #374151; 
        font-size: 1.15em; 
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cabeçalho (Emoji como Logo Provisório)
st.markdown("<div style='text-align: center; font-size: 80px; margin-bottom: -20px;'>🍊</div>", unsafe_allow_html=True)
st.title("OpenCanvas Pro")
st.markdown("<div class='subtitle'>A Revolução do AutoML Local-First</div>", unsafe_allow_html=True)

st.divider()

# 4. Proposta de Valor (Generalista e Tecnológica)
c1, c2, c3 = st.columns([1, 8, 1])
with c2:
    st.info("🚀 **Estamos em fase final de testes (Beta Fechado).**")
    
    st.markdown("""
    <div class="hero-text">
        Transforme dados brutos em inteligência preditiva sem escrever uma linha de código.<br>
        Uma plataforma desenhada para <b>Cientistas de Dados</b>, <b>Analistas</b> e <b>Empresas</b> que valorizam privacidade.
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Espaço em branco
    
    # Ícones de Features (Sem nicho específico)
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    col_feat1.metric("Privacidade", "100%", "Dados Locais")
    col_feat2.metric("Modelagem", "AutoML", "No-Code")
    col_feat3.metric("Deploy", "Rápido", "One-Click")

# 5. Captura de Lead (Lista de Espera)
st.write("---")
st.markdown("<h3 style='text-align: center;'>Garanta seu acesso antecipado</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 0.9em;'>Junte-se a outros profissionais de alta performance na fila de espera.</p>", unsafe_allow_html=True)

with st.form("waitlist_form"):
    # Centralizando o input visualmente
    f_c1, f_c2, f_c3 = st.columns([1, 2, 1])
    with f_c2:
        email_input = st.text_input("Seu e-mail corporativo ou pessoal:", placeholder="nome@empresa.com")
        submit = st.form_submit_button("🔔 Avise-me quando lançar", use_container_width=True, type="primary")

    if submit:
        if email_input and "@" in email_input:
            # Simulação de processamento (UX)
            with st.spinner("Registrando seu interesse..."):
                time.sleep(1.5) # Um delayzinho pra parecer que foi pro servidor
            
            st.balloons() # Feedback positivo!
            st.success(f"Obrigado! O e-mail **{email_input}** foi adicionado à nossa lista prioritária.")
            st.info("Assim que virarmos a chave, você receberá um convite exclusivo.")
            
            # Nota para você (Lucindo): Aqui futuramente entra o código SMTP para enviar real
            # send_email_to_admin(email_input) 
        else:
            st.warning("Por favor, digite um endereço de e-mail válido.")

# 6. Rodapé Profissional
st.write("")
st.write("")
st.write("")
st.markdown(
    """
    <div style='text-align: center; color: #9ca3af; font-size: 0.85em; line-height: 1.8;'>
        © 2026 <b>OpenCanvas Pro</b> · Tecnologia Local-First<br>
        Dúvidas ou Parcerias? <a href="mailto:contato@opencanvaspro.com" style="color: #ff4b4b; text-decoration: none;">contato@opencanvaspro.com</a>
    </div>
    """, 
    unsafe_allow_html=True
)