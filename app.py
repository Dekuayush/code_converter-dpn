from groq import Groq
from flask import Flask, render_template, request
import os
import markdown
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)  # .env wins over stale system variables

# Model is configurable: set GROQ_MODEL in .env to switch without editing code
MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

app = Flask(__name__)

def get_groq_client():
    """Initialize and return Groq client"""
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("API_KEY")
    
    if not api_key:
        raise ValueError("API key is not set. Please set it as an environment variable.")
    return Groq(api_key=api_key)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def translate():
    if request.method == "POST":
        try:
            source_language = request.form.get("source")
            target_language = request.form.get("target")
            code = request.form.get("code")

            # Initialize client only when needed
            client = get_groq_client()

            # First API call: Convert code
            convert_prompt = [
                {
                   "role": "user",
                   "content": f"""Convert this {source_language} code to {target_language}.

IMPORTANT REQUIREMENTS:
1. Generate COMPLETE, EXECUTABLE code with all necessary boilerplate
2. For Java: Include full class definition with public static void main(String[] args)
3. For C/C++: Include necessary headers (#include) and int main() function
4. For C#: Include using statements, namespace, class, and Main method
5. For Python: Include proper if __name__ == "__main__": if needed
6. For Go: Include package main and func main()
7. For other languages: Include proper entry points and required imports/includes

OUTPUT FORMAT:
- Provide ONLY the raw code, nothing else
- DO NOT wrap the code in markdown code fences (NO ```java, ```python, etc.)
- DO NOT include any explanations, comments about the conversion, or markdown formatting
- Just the pure executable code

Code to convert:
{code}"""
                }
            ]

            convert_response = client.chat.completions.create(
                model=MODEL,
                messages=convert_prompt,
                temperature=0.7,
                max_tokens=4096,
                top_p=1,
                stream=False,
                stop=None
            )

            converted_code = convert_response.choices[0].message.content
            
            # Strip markdown code fences if present (fallback)
            converted_code = re.sub(r'^```[a-zA-Z]*\n?', '', converted_code)
            converted_code = re.sub(r'\n?```$', '', converted_code)
            converted_code = converted_code.strip()
            
            # Second API call: Generate comprehensive explanation
            explain_prompt = [
                {
                   "role": "user",
                   "content": f"""Provide a comprehensive, well-structured explanation of the code conversion from {source_language} to {target_language}.

The converted code includes complete boilerplate (main functions, imports, class definitions, etc.) to make it immediately executable.

Format your response with proper structure using Markdown:

## 📋 Code Conversion Analysis

### 🔄 Line-by-Line Explanation

Explain each important line of the converted code, including:
- Boilerplate elements (imports, main function, class structure)
- Core logic conversion
- How it differs from the original {source_language} code
- Why this specific syntax is used in {target_language}

### 🔑 Key Differences

List the major differences between {source_language} and {target_language} for this code:
- **Boilerplate Requirements**: Entry points, imports, class structure needed in {target_language}
- **Syntax Changes**: How function calls, variables, loops, etc. differ
- **Library/Import Differences**: Different modules or packages used
- **Structural Modifications**: Changes in code organization or patterns
- **Language-Specific Features**: Unique features used in {target_language}

### ⚡ Execution Flow

Explain step-by-step how the complete code executes:
1. Program initialization (imports, class loading)
2. Main function/entry point execution
3. Core logic steps
4. Final result

### 💡 Best Practices

Mention any best practices or conventions followed in the {target_language} version.

Original {source_language} code:
```{source_language.lower()}
{code}
```

Converted {target_language} code (with complete boilerplate):
```{target_language.lower()}
{converted_code}
```"""
                }
            ]

            explain_response = client.chat.completions.create(
                model=MODEL,
                messages=explain_prompt,
                temperature=0.8,
                max_tokens=4096,
                top_p=1,
                stream=False,
                stop=None
            )

            explanation_markdown = explain_response.choices[0].message.content
            # Convert markdown to HTML for proper formatting
            explanation = markdown.markdown(explanation_markdown, extensions=['fenced_code', 'tables', 'nl2br'])
            
            # Third API call: Generate expected output
            output_prompt = [
                {
                   "role": "user",
                   "content": f"""Analyze this complete, executable {target_language} code and provide the expected output when executed.

The code includes all necessary boilerplate (main function, imports, class structure).

Guidelines:
- Show the actual console/terminal output
- If the code requires input, show example inputs and corresponding outputs
- For simple programs, show the direct output
- Show only the actual output, no extra explanations

{target_language} code:
{converted_code}"""
                }
            ]

            output_response = client.chat.completions.create(
                model=MODEL,
                messages=output_prompt,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )

            expected_output = output_response.choices[0].message.content
            
            return render_template("translate.html", 
                                 output=converted_code, 
                                 original_code=code,
                                 explanation=explanation,
                                 expected_output=expected_output,
                                 source_lang=source_language,
                                 target_lang=target_language)
        
        except ValueError as e:
            return render_template("translate.html", 
                                 output=f"Error: {str(e)}\n\nPlease set your API key environment variable and restart the application.",
                                 original_code="",
                                 explanation="",
                                 expected_output="",
                                 source_lang="",
                                 target_lang="")
        except Exception as e:
            return render_template("translate.html", 
                                 output=f"Error occurred: {str(e)}",
                                 original_code="",
                                 explanation="",
                                 expected_output="",
                                 source_lang="",
                                 target_lang="")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Code Converter Server Starting...")
    print("="*60)
    
    # Check if API key is set
    try:
        client = get_groq_client()
        print("[OK] API key is configured and ready!")
    except:
        print("[WARNING] API key is not set!")
        print("   Set it using: $env:GROQ_API_KEY='your_key_here'")
    
    print("\nOpen your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))