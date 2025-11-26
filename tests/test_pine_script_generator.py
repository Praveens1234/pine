
import unittest
from unittest.mock import patch, MagicMock

# Patch OpenAI before importing the module that uses it
with patch('openai.OpenAI', MagicMock()):
    from src.pine_script_generator import generate_pine_script

class TestLLMPineScriptGenerator(unittest.TestCase):

    @patch('src.pine_script_generator.client.chat.completions.create')
    def test_initial_script_generation_prompt(self, mock_create):
        """
        Test that the correct prompt is constructed for initial script generation.
        """
        # Mock the API response
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = 'plot(close)'
        mock_create.return_value = [mock_chunk]

        description = "A simple plot of the close price."
        generate_pine_script(description)

        # Verify that the API was called
        mock_create.assert_called_once()
        # Verify the content of the prompt
        called_args, called_kwargs = mock_create.call_args
        messages = called_kwargs['messages']
        self.assertEqual(len(messages), 1)
        self.assertIn("Your task is to create a complete and syntactically correct Pine Script", messages[0]['content'])
        self.assertIn(description, messages[0]['content'])

    @patch('src.pine_script_generator.client.chat.completions.create')
    def test_error_correction_prompt(self, mock_create):
        """
        Test that the correct prompt is constructed for error correction.
        """
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = 'plot(close)'
        mock_create.return_value = [mock_chunk]

        description = "Plot the close"
        error_message = "Syntax error: Undeclared identifier 'clse'"
        generate_pine_script(description, error_message=error_message)

        mock_create.assert_called_once()
        messages = mock_create.call_args.kwargs['messages']
        self.assertEqual(len(messages), 1)
        self.assertIn("Your previous attempt to generate a script failed", messages[0]['content'])
        self.assertIn(description, messages[0]['content'])
        self.assertIn(error_message, messages[0]['content'])

    @patch('src.pine_script_generator.client.chat.completions.create')
    def test_code_extraction_from_response(self, mock_create):
        """
        Test that the Pine Script code is correctly extracted from the LLM's response.
        """
        # Simulate a response with markdown formatting
        mock_response_content = """Here is the Pine Script you requested:
```pinescript
//@version=5
indicator("My Script")
plot(close)
```
I hope this helps!
"""
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = mock_response_content
        mock_create.return_value = [mock_chunk]
        
        result = generate_pine_script("Any description")
        
        expected_code = """
//@version=5
indicator("My Script")
plot(close)
""".strip()
        
        self.assertEqual(result, expected_code)

if __name__ == '__main__':
    unittest.main()
