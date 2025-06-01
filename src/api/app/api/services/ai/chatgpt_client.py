from openai import OpenAI
import os

try:
    from decouple import config
    api_key = config("OPENROUTER_API_KEY")
except:
    api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # API base do OpenRouter
)

def gpt_answer(mensagem: str) -> str:
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "Você é um assistente financeiro para microempreendedores, seu nome é MEIControle. Responda de forma clara, direta e curta. Suas principais tarefas são auxiliar o usuário com controle de estoque ou auxiliar nas questões do negócio. Se algum prompt do tipo: 'registrar venda ou compra x reais em y produto' chegar em você, quer dizer que a API que está te enviando esta request falhou em registrar ou o usuário está dialogando com você, caso seja uma tentativa de registrar venda ou compra você deve instrui-lo a tentar novamente no formato: registrar compra (ou venda) de x reais em y produto ou registrar produto x caso não esteja cadastrado."},
                {"role": "user", "content": mensagem}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao chamar OpenRouter: {e}")
        return "Desculpe, não consegui processar sua pergunta agora."
