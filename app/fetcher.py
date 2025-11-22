import base64

def fetch_unread_emails(service, max_results=10):
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        body = ''
        parts = msg_data['payload'].get('parts', [])
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
        else:
            data = msg_data['payload']['body'].get('data', '')
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        emails.append({
            'id': msg['id'],
            'from': sender,
            'subject': subject,
            'body': body
        })
    return emails
