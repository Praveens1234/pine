
import logging
from flask import Flask, render_template, request
import asyncio
from src.pine_script_generator import generate_pine_script
from src.validation_service import validate_pine_script

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
async def generate():
    user_description = request.form['description']
    logging.info(f"Received generation request for: '{user_description}'")
    
    max_attempts = 5
    error_message = None
    generated_script = ""
    logs = []

    for attempt in range(max_attempts):
        log_prefix = f"Attempt {attempt + 1}/{max_attempts}"
        logs.append(f"--- {log_prefix} ---")
        
        logs.append(f"[{log_prefix}] Generating Pine Script...")
        logging.info(f"[{log_prefix}] Calling Pine Script generator in a separate thread.")
        generated_script = await asyncio.to_thread(generate_pine_script, user_description, error_message=error_message)
        
        logs.append(f"[{log_prefix}] Validating Pine Script...")
        logging.info(f"[{log_prefix}] Calling validation service.")
        is_valid, message = await validate_pine_script(generated_script)
        
        if is_valid:
            logs.append(f"[{log_prefix}] Validation successful: {message}")
            logging.info(f"[{log_prefix}] Validation successful.")
            break
        else:
            logs.append(f"[{log_prefix}] Validation failed: {message}")
            logging.warning(f"[{log_prefix}] Validation failed: {message}")
            error_message = message
            if attempt < max_attempts - 1:
                logs.append(f"[{log_prefix}] Retrying with feedback...")
    
    return render_template('result.html', script=generated_script, logs=logs), 200

if __name__ == '__main__':
    logging.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=8080, debug=True)
