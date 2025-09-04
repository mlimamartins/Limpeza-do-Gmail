#descobrir as labels existentes na conta

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopo correto para modificar (ler e deletar) mensagens
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Autenticação OAuth2
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('gmail', 'v1', credentials=creds)

# Labels que queremos limpar
labels_to_clear = ['SPAM', 'CATEGORY_PROMOTIONS']

for label_id in labels_to_clear:
    # Listar todas as mensagens com o label
    results = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=500).execute()
    messages = results.get('messages', [])

    if not messages:
        print(f"Nenhuma mensagem encontrada no label {label_id}")
        continue

    print(f"{len(messages)} mensagens encontradas no label {label_id}:")

    # Mostrar assuntos das mensagens
    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "(sem assunto)")
        print(" -", subject)

    # Confirmar exclusão
    confirm = input(f"Deseja excluir todas as {len(messages)} mensagens do label {label_id}? (s/n) ")
    if confirm.lower() == 's':
        for msg in messages:
            service.users().messages().delete(userId='me', id=msg['id']).execute()
        print(f"Todas as mensagens do label {label_id} foram excluídas!")
    else:
        print(f"Nenhuma mensagem do label {label_id} foi excluída.")
