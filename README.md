# Code Converter

A Flask web app that converts code from one programming language to another using AI through the [Groq API](https://console.groq.com). Paste your code, pick the source and target languages, and get:

- **Converted code**: complete and runnable, including entry points, imports, and boilerplate
- **Explanation**: line-by-line breakdown, key differences between the languages, execution flow, and best practices
- **Expected output**: what the converted program should print when run

## Tech Stack

- Python and Flask
- Groq API (default model: `openai/gpt-oss-120b`)
- Python-Markdown for rendering explanations
- Gunicorn for production

## Project Structure

```
.
├── app.py              # Flask app and Groq API calls
├── templates/          # HTML templates (index.html, translate.html)
├── requirements.txt    # Python dependencies
├── Procfile            # Production start command
├── .env                # Your secrets (never commit this)
└── .gitignore
```

## Setup

### 1. Get a Groq API key

Create a free key at https://console.groq.com/keys.

### 2. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/code-converter.git
cd code-converter

python -m venv .venv
# Windows:  .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a file named exactly `.env` (with the leading dot) in the project root:

```
GROQ_API_KEY=your_api_key_here
```

Optional: choose a different model without touching the code:

```
GROQ_MODEL=openai/gpt-oss-120b
```

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Your Groq API key |
| `GROQ_MODEL` | No | Groq model ID. Defaults to `openai/gpt-oss-120b` |
| `PORT` | No | Server port. Defaults to `5000` |

> The app also accepts `API_KEY` as a fallback, but `GROQ_API_KEY` is preferred. Values in `.env` override system environment variables.

### 4. Run

```bash
python app.py
```

You should see `[OK] API key is configured and ready!`. Open http://localhost:5000.

## Usage

1. Choose the source and target languages.
2. Paste your code.
3. Click **Convert Code**.
4. Review the converted code, explanation, and expected output. Use the copy and download buttons as needed.

Each conversion makes three sequential API calls (convert, explain, predict output), so it can take a few seconds.

## Deployment (Render)

1. Push the project to GitHub. Make sure `.env` is **not** included.
2. On [render.com](https://render.com), create a new **Web Service** from your repo.
3. Set these:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app --timeout 120`
4. In the **Environment** tab, add `GROQ_API_KEY` (and optionally `GROQ_MODEL`).
5. Deploy.

The `--timeout 120` matters: the default 30 seconds can cut off conversions that make three AI calls.

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `ModuleNotFoundError: No module named 'groq'` | Dependencies not installed in the Python you're running. Run `python -m pip install -r requirements.txt` (activate your virtual environment first). |
| `API key is not set` | `.env` is missing, misnamed (`env`, `.env.txt`), or in the wrong folder. It must be named `.env` and sit next to `app.py`. Restart the app after editing it. |
| `401 invalid_api_key` | The key is wrong, revoked, or has extra spaces or quotes. Create a new key and paste it without quotes. |
| `404 model_not_found` | Groq retired the model. List available models (below) and set `GROQ_MODEL` in `.env`. |
| `429` rate limit | You've hit Groq's free-tier limits. Wait a minute and retry. |
| Worker timeout on the deployed site | Use `--timeout 120` in the start command. |

List the models your key can access:

```bash
python -c "import os;from dotenv import load_dotenv;from groq import Groq;load_dotenv(override=True);print('\n'.join(sorted(m.id for m in Groq(api_key=os.environ['GROQ_API_KEY']).models.list().data)))"
```

## Security

- Never commit `.env` or share your API key. `.gitignore` already excludes `.env`.
- If a key is ever exposed, delete it in the Groq console and create a new one.

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Home page with the conversion form |
| `POST` | `/convert` | Converts code (form fields: `source`, `target`, `code`) |

## Notes

- AI-generated conversions and expected outputs can contain mistakes. Always review and test the converted code before relying on it.

## License

MIT License
