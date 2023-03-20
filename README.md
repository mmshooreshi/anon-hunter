
## Installation

1. Clone the [serverless_gpt](https://github.com/mmshooreshi/serverless_gpt) repository on GitHub.
2. Go to [Vercel](https://vercel.com/) and authenticate with GitHub.
3. Go to the Dashboard page and click the "Overview" tab.
4. Click the "Add new" button, then select "Project", and select "Import Git Repository" from the list.
5. Select the cloned repository from the list.
6. Go to the [Environment Variables](https://vercel.com/{your-username}/serverless-gpt/settings/environment-variables) page and fill in the following variables:

```
INIT_LANGUAGE = fa
MSG_LIST_LIMIT = 20
OPENAI_MODEL = text-davinci-003
OPENAI_TEMPERATURE = 0.5
OPENAI_FREQUENCY_PENALTY = 0
OPENAI_PRESENCE_PENALTY = 0
OPENAI_MAX_TOKENS = 250
TELEGRAM_BOT_TOKEN = [bot token]
OPENAI_API_KEY = [openai_api_key]
```

7. To get the bot token, go to [@BotFather](https://t.me/BotFather), send `/newbot`, and complete the instructions.

8. Using a VPN (if you live in iran :D), go to the following URL to enable the webhook:

`https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url=https://{your-app-name-on-vercel}.vercel.app/callback`

## Usage

Once the installation is completed, you can start using ServerlessGPT to build secure and efficient dialogue flows for any task.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)