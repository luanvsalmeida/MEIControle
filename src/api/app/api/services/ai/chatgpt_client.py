import requests
import time
from decouple import config

# Modelos em ordem de prioridade (do mais confiável para o menos)
MODELS = [
    {
        "name": "huggingface/CodeBERTa-small-v1",
        "url": "https://api-inference.huggingface.co/models/huggingface/CodeBERTa-small-v1",
        "format": "simple"
    },
    {
        "name": "gpt2",
        "url": "https://api-inference.huggingface.co/models/gpt2",
        "format": "simple"
    },
    {
        "name": "facebook/bart-large-cnn",
        "url": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
        "format": "simple"
    },
    {
        "name": "t5-small",
        "url": "https://api-inference.huggingface.co/models/t5-small",
        "format": "t5"
    }
]

headers = {"Authorization": f"Bearer {config('HUGGINGFACE_API_KEY')}"}

def test_model(model_info, test_message="Hello"):
    """Testa se um modelo está disponível"""
    try:
        if model_info["format"] == "t5":
            payload = {"inputs": f"translate English to Portuguese: {test_message}"}
        else:
            payload = {"inputs": test_message}
        
        response = requests.post(
            model_info["url"], 
            headers=headers, 
            json=payload, 
            timeout=10
        )
        
        print(f"Testando {model_info['name']}: Status {response.status_code}")
        
        if response.status_code == 200:
            return True
        elif response.status_code == 503:
            print(f"  Modelo {model_info['name']} está carregando...")
            return "loading"
        else:
            print(f"  Erro: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"  Erro ao testar {model_info['name']}: {e}")
        return False

def find_working_model():
    """Encontra o primeiro modelo que funciona"""
    print("Procurando modelo disponível...")
    
    for model in MODELS:
        result = test_model(model)
        if result == True:
            print(f"✅ Modelo funcionando: {model['name']}")
            return model
        elif result == "loading":
            print(f"⏳ Tentando aguardar carregamento de {model['name']}...")
            time.sleep(15)
            if test_model(model) == True:
                print(f"✅ Modelo carregado: {model['name']}")
                return model
    
    print("❌ Nenhum modelo disponível")
    return None

def gpt_answer(mensagem: str) -> str:
    print("Mensagem:", mensagem)
    print("Token:", config('HUGGINGFACE_API_KEY')[:10] + "...")
    
    # Encontra modelo disponível
    working_model = find_working_model()
    
    if not working_model:
        return "Desculpe, nenhum modelo de IA está disponível no momento. Tente novamente mais tarde."
    
    try:
        # Prepara payload baseado no tipo de modelo
        if working_model["format"] == "t5":
            # T5 funciona melhor com tarefas específicas
            payload = {
                "inputs": f"Responda a pergunta: {mensagem}",
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7
                }
            }
        else:
            # Outros modelos
            payload = {
                "inputs": f"Pergunta: {mensagem}\nResposta:",
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
        
        print(f"Usando modelo: {working_model['name']}")
        
        response = requests.post(
            working_model["url"], 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 503:
            print("Modelo carregando, aguardando...")
            time.sleep(20)
            response = requests.post(
                working_model["url"], 
                headers=headers, 
                json=payload, 
                timeout=30
            )
        
        if response.status_code != 200:
            print(f"Erro HTTP {response.status_code}: {response.text}")
            return f"Erro na API: {response.text[:100]}"
        
        try:
            result = response.json()
            print(f"Resultado: {result}")
            
            # Processa diferentes formatos de resposta
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    text = result[0]["generated_text"]
                    # Remove a pergunta original se ela aparecer na resposta
                    if mensagem in text:
                        text = text.replace(f"Pergunta: {mensagem}\nResposta:", "").strip()
                    return text or "Não consegui gerar uma resposta adequada."
                elif "summary_text" in result[0]:
                    return result[0]["summary_text"]
                elif "translation_text" in result[0]:
                    return result[0]["translation_text"]
            
            return "Formato de resposta não reconhecido."
            
        except ValueError:
            print(f"Erro ao processar JSON: {response.text}")
            return "Erro ao processar resposta da API."
    
    except requests.exceptions.Timeout:
        return "Timeout na conexão com a API."
    except Exception as e:
        print(f"Erro geral: {e}")
        return f"Erro interno: {str(e)}"

# Função para testar manualmente
def test_connection():
    """Testa a conexão e mostra modelos disponíveis"""
    print("=== TESTE DE CONECTIVIDADE ===")
    working_models = []
    
    for model in MODELS:
        result = test_model(model)
        if result == True:
            working_models.append(model["name"])
        elif result == "loading":
            print(f"Aguardando {model['name']}...")
            time.sleep(10)
            if test_model(model) == True:
                working_models.append(model["name"])
    
    print(f"\n✅ Modelos funcionando: {working_models}")
    print(f"❌ Total testados: {len(MODELS)}")
    
    if working_models:
        print("\n🧪 Testando resposta...")
        response = gpt_answer("Olá, como você está?")
        print(f"Resposta de teste: {response}")
    
    return len(working_models) > 0

# Versão simplificada que sempre retorna algo
def simple_fallback_response(mensagem: str) -> str:
    """Fallback quando nenhuma API funciona"""
    responses = {
        "oi": "Olá! Como posso ajudar?",
        "olá": "Oi! Em que posso ser útil?",
        "como": "Estou aqui para ajudar com suas perguntas!",
        "obrigado": "De nada! Fico feliz em ajudar.",
        "tchau": "Até logo! Foi um prazer conversar."
    }
    
    mensagem_lower = mensagem.lower()
    for key, response in responses.items():
        if key in mensagem_lower:
            return response
    
    return "Desculpe, não consegui processar sua solicitação no momento. Os serviços de IA estão temporariamente indisponíveis."