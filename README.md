# Sistema de Direitos Autorais

Este é um exemplo simples de aplicação web para cadastrar e consultar informações de direitos autorais de artistas. Não requer autenticação e funciona como uma pequena wiki aberta.

## Como executar

1. Instale as dependências (Flask e requests).
   ```bash
   pip install flask requests
   ```
2. Inicie a aplicação:
   ```bash
   python app/app.py
   ```
3. Acesse `http://localhost:5000` no navegador.

Os dados são armazenados em um banco SQLite em `app/data.db`.

## Integração com Shoutcast

Envie dados de reprodução via POST para `/api/shoutcast/plays` no formato JSON:

```json
{
  "artist": "Nome do artista",
  "title": "Título da música",
  "played_at": "2024-01-01T12:00:00Z"
}
```

Essas informações serão gravadas na tabela `plays`.

## Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
