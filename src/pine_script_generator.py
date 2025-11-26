
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client for NVIDIA API
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key=os.getenv("NVIDIA_API_KEY")
)

def _construct_prompt(description: str, error_message: str = None) -> str:
    """Constructs the prompt for the LLM based on user input and optional error feedback."""
    if error_message:
        # Create a prompt for correcting a script
        return f"""You are an expert programmer specializing in TradingView Pine Script.
Your previous attempt to generate a script failed with an error. Your task is to correct the script based on the user's original request and the provided error message.
The corrected script must be a complete and syntactically correct Pine Script Version 5.
Do not include any explanations, comments, or markdown formatting outside of the Pine Script code itself. Just provide the raw code.

User's original request: "{description}"
Error message from validator: "{error_message}"
"""
    else:
        # Create a prompt for initial script generation
        return f"""You are an expert programmer specializing in TradingView Pine Script.
Your task is to create a complete and syntactically correct Pine Script Version 5 script based on the user's request.
The script should be ready to copy and paste directly into TradingView.
Do not include any explanations, comments, or markdown formatting outside of the Pine Script code itself. Just provide the raw code.

User's request: "{description}"
"""

def generate_pine_script(description: str, error_message: str = None) -> str:
    """
    Generates Pine Script using an LLM based on a user's description and error feedback.
    """
    # Step 1: Construct the prompt
    prompt = _construct_prompt(description, error_message)

    # Step 2: Call the LLM API
    logging.info("Sending prompt to LLM...")
    try:
        model_name = os.getenv("MODEL_NAME", "qwen/qwen3-coder-480b-a35b-instruct")
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role":"user", "content": prompt}],
            temperature=0.2, # Lower temperature for more deterministic code generation
            top_p=0.8,
            max_tokens=4096,
            stream=True
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        
        logging.info("LLM response received successfully.")
        
        # --- Step 3: Extract the code from the response ---
        # Clean up the response to extract only the Pine Script code
        if "```pinescript" in full_response:
            code = full_response.split("```pinescript")[1].split("```")[0]
        elif "```" in full_response:
            code = full_response.split("```")[1]
        else:
            code = full_response
            
        return code.strip()

    except Exception as e:
        logging.error(f"An error occurred while calling the LLM API: {e}")
        return f"// Error generating script: {e}"

if __name__ == "__main__":
    # Example 1: Generate a new script
    desc1 = "A simple strategy that goes long when the RSI is below 30 and sells when it's above 70."
    logging.info(f"--- Generating script for: '{desc1}' ---")
    script1 = generate_pine_script(desc1)
    print("--- Generated Script ---")
    print(script1)
    
    # Example 2: Correct a script with a fake error message
    desc2 = "An indicator with an EMA crossover."
    error = "Syntax error: The function `ta.crossover` should have 2 arguments, but got 1."
    logging.info(f"\n--- Correcting script for: '{desc2}' with error: '{error}' ---")
    script2 = generate_pine_script(desc2, error_message=error)
    print("--- Corrected Script ---")
    print(script2)
