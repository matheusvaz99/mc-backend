from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI(title="API MC Automatiza")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Buscando as credenciais de forma segura (Variáveis de Ambiente)
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "seu-email@gmail.com") 
SENHA_APP = os.getenv("SENHA_APP", "sua-senha-de-app")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO", "seu-email@gmail.com") # Onde você quer receber

def disparar_email(nome, email_cliente, demanda):
    assunto = f"🔥 Novo Lead: {nome} - MC Automatiza"
    corpo = f"""
    Você tem um novo pedido de diagnóstico!

    👤 Nome: {nome}
    ✉️ E-mail do Cliente: {email_cliente}
    
    📝 Demanda:
    {demanda}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINO
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # Conecta ao servidor do Gmail e envia
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.send_message(msg)
        server.quit()
        print("E-mail disparado com sucesso!")
    except Exception as e:
        print(f"Erro ao disparar e-mail: {e}")

@app.post("/webhook/contato")
async def receber_contato(
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...)
):
    # Chama a função que envia o e-mail em segundo plano
    disparar_email(nome, email, mensagem)

    return {"status": "sucesso", "mensagem": "Recebemos sua solicitação. Em breve entraremos em contato!"}