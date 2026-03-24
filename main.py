from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import resend

app = FastAPI(title="API MC Automatiza")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pegando as chaves do Render
resend.api_key = os.getenv("RESEND_API_KEY")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO", "seu-email@gmail.com") # Coloque lá no Render o e-mail que você usou para entrar no Resend

def disparar_email(nome, email_cliente, demanda):
    try:
        # O Resend exige o remetente onboarding@resend.dev para contas em teste
        params = {
            "from": "MC Automatiza <onboarding@resend.dev>",
            "to": [EMAIL_DESTINO],
            "subject": f"🔥 Novo Lead: {nome}",
            "html": f"""
            <h2>Novo pedido de diagnóstico!</h2>
            <p><strong>Nome:</strong> {nome}</p>
            <p><strong>E-mail do Cliente:</strong> {email_cliente}</p>
            <p><strong>Demanda:</strong><br>{demanda}</p>
            """
        }
        resend.Emails.send(params)
        print("E-mail disparado com sucesso via Resend!")
    except Exception as e:
        print(f"Erro no Resend: {e}")

@app.post("/webhook/contato")
async def receber_contato(
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...)
):
    disparar_email(nome, email, mensagem)
    return {"status": "sucesso", "mensagem": "Recebemos sua solicitação. Em breve entraremos em contato!"}