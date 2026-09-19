# Code Converter

A Flask web application that converts code between different programming languages using AI (Groq API with Llama 3.3).

## Features

- Convert code between 40+ programming languages
- Generate comprehensive explanations of the conversion
- Show expected output of the converted code
- Clean and intuitive web interface
- Complete, executable code generation with proper boilerplate

## Supported Languages

The converter supports conversion between various programming languages including:
- Python, Java, C++, C#, JavaScript, Go, Rust, PHP, Ruby, Swift, Kotlin
- And many more...

## Prerequisites

- Python 3.7+
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/code-converter.git
cd code-converter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Running Locally

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Deploy to Render

1. Create a Render account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the environment variable `GROQ_API_KEY` in the Render dashboard
5. Deploy!

## Usage

1. Visit the web interface
2. Select your source and target programming languages
3. Paste your code in the source text area
4. Click "Convert Code"
5. View the converted code, explanation, and expected output

## API Endpoints

- `GET /` - Home page with conversion form
- `POST /convert` - Convert code between languages

## Technologies Used

- Flask - Web framework
- Groq API - AI code conversion
- Bootstrap - Frontend styling
- Gunicorn - WSGI server for production

## License

This project is open source and available under the MIT License.