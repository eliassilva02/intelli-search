# IntelliSearch

IntelliSearch é um projeto desenvolvido para fins de estudo, inspirado no Perplexity AI. O objetivo é responder perguntas dos usuários utilizando fontes encontradas online. O projeto utiliza scraping da web, modelos de linguagem e grafos de estado para coletar e processar informações.

## Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz e adicione suas variáveis de ambiente:

```
OPENAI_API_KEY=your_openai_api_key
```

## Uso

Execute o script principal para iniciar a aplicação de console:

```sh
python agent.py
```

## Como Funciona

1. **Entrada do Usuário**: O usuário fornece uma pergunta através do console.
2. **Geração de Consultas**: O sistema gera consultas de pesquisa com base na entrada do usuário.
3. **Pesquisa na Web**: O sistema realiza pesquisas na web e extrai informações relevantes.
4. **Síntese**: As informações extraídas são sintetizadas em um resumo conciso.
5. **Resposta Final**: Uma resposta final é gerada e exibida ao usuário.