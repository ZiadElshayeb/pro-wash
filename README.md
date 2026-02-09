# Pro Wash WhatsApp Flow Integration

## Setup

1. **Clone and configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f webhook
   ```

4. **Stop the service**:
   ```bash
   docker-compose down
   ```

## Configuration

Set these environment variables in your `.env` file:

- `WHATSAPP_BUSINESS_PHONE_NUMBER_ID`: Your WhatsApp Business Phone Number ID
- `WHATSAPP_BUSINESS_ACCOUNT_ID`: Your WhatsApp Business Account ID (WABA ID)
- `ACCESS_TOKEN`: Your Meta Graph API access token
- `WEBHOOK_VERIFY_TOKEN`: A secure token for webhook verification

## Webhook Setup

1. Make sure your VPS is accessible from the internet
2. Set up a reverse proxy (nginx/caddy) with SSL
3. Configure the webhook URL in Meta's dashboard:
   - URL: `https://your-domain.com/webhook`
   - Verify Token: Use the same value as `WEBHOOK_VERIFY_TOKEN`

## Scripts

- `create_flow.py`: Create a new WhatsApp Flow
- `send_template.py`: Send a template message with flow button
- `webhook.py`: Receive and process flow responses

## Running Scripts Manually

```bash
# Create flow
python create_flow.py

# Send template
python send_template.py
```
# Pro-Wash
