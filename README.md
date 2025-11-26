# AI Pine Script Generator

This project is a Flask-based web application that uses a powerful Large Language Model (LLM) to generate TradingView Pine Script from natural language descriptions. It features a self-correction mechanism where the generated script is validated, and any errors are fed back to the LLM for improvement, ensuring the final output is syntactically correct.

## Features

- **Natural Language to Pine Script:** Describe your trading strategy in plain English, and the application will generate the corresponding Pine Script code.
- **Self-Correction Loop:** The generated script is automatically validated. If syntax errors are found, the script is sent back to the LLM with the error message for correction.
- **Web-Based Interface:** A simple and intuitive UI for entering your script description and viewing the generated code.
- **Powered by NVIDIA API:** The backend is configured to use NVIDIA's API for code generation but is easily adaptable to other language models.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Prerequisites

- Python 3.8 or higher
- `pip` for package management

### 2. Installation

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

Next, it's recommended to create a virtual environment to manage the project's dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Now, install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configuration

The application requires environment variables to be set for the API key and the model name.

1.  In the project root, find the `.env.example` file. This file serves as a template.
2.  Create a copy of this file and rename it to `.env`.
3.  Open the new `.env` file and add your secret NVIDIA API key. You can also change the `MODEL_NAME` if you wish to use a different model.

```
# .env

# Paste your NVIDIA API key here
NVIDIA_API_KEY="your_nvidia_api_key_here"

# The name of the LLM model to use for generation
MODEL_NAME="qwen/qwen3-coder-480b-a35b-instruct"
```

**Important:** The `.env` file contains secrets and is ignored by Git (via `.gitignore`) to prevent accidental exposure. Do not commit this file to your repository.

### 4. Running the Application

Once the dependencies are installed and the API key is configured, you can start the Flask web server with the following command:

```bash
python app.py
```

The application will start in debug mode and be accessible at:
**http://127.0.0.1:8080**

Open this URL in your web browser to start generating Pine Script.

### 5. Running Tests

The project includes a suite of tests to ensure everything is working correctly. To run the tests, execute the following command in your terminal:

```bash
pytest
```

This will discover and run all the tests located in the `tests/` directory.

## How It Works

The application follows a generate-validate-correct loop to produce syntactically valid Pine Script.

1.  **Generate:** The user's natural language description is sent to the LLM to generate an initial version of the Pine Script.
2.  **Validate:** The generated script is passed to a syntax validation service, which checks for common errors.
3.  **Correct:** If the validation service finds an error, the error message is sent back to the LLM along with the original request. The LLM then attempts to correct the script based on the feedback.
4.  **Repeat:** This process is repeated up to 5 times until the script is valid or the maximum number of attempts is reached.

## Project Structure

```
.
├── app.py                  # Main Flask application file
├── requirements.txt        # Python package dependencies
├── README.md               # This documentation file
├── .env                    # Environment file for API key (created locally, ignored by git)
├── .gitignore              # Specifies files to be ignored by Git
├── src/                    # Source code for core application logic
│   ├── pine_script_generator.py  # Handles LLM interaction and script generation
│   └── validation_service.py     # Provides Pine Script syntax validation
├── templates/              # HTML templates for the web interface
│   ├── index.html          # The home page with the input form
│   └── result.html         # The page that displays the generated script and logs
└── tests/                  # Automated tests for the application
    ├── test_app.py         # Tests for the Flask application endpoints
    └── test_pine_script_generator.py # Tests for the script generation logic
```
