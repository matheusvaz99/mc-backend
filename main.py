from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API MC Automatiza")

# Configuração de CORS (Permite que o seu site acesse esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # DICA: Em produção, limitaremos isso ao seu domínio oficial
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/webhook/contato")
async def receber_contato(
    nome: str = Form(...),
    email: str = Form(...),
    mensagem: str = Form(...)
):
    """
    Endpoint (Webhook) que recebe os dados do site.
    """
    # Aqui é onde vamos conectar o disparo de e-mails ou banco de dados depois.
    # Por enquanto, vamos imprimir no terminal para validar que chegou:
    print("\n" + "="*40)
    print("🔥 NOVO LEAD RECEBIDO 🔥")
    print(f"Nome: {nome}")
    print(f"E-mail: {email}")
    print(f"Demanda: {mensagem}")
    print("="*40 + "\n")

    # Retorno de sucesso para o navegador do cliente
    return {"status": "sucesso", "mensagem": "Recebemos sua solicitação. Em breve entraremos em contato!"}