
import asyncio
from pinescript_syntax_checker.pinescript_checker import PineScriptChecker

async def validate_pine_script(pine_code: str) -> tuple[bool, str]:
    """
    Validates a Pine Script string using the pinescript-syntax-checker.
    """
    try:
        checker = PineScriptChecker()
        result = await checker.check_syntax(pine_code)
        
        # Handle top-level failures (e.g., version errors)
        if not result.get("success", False) and "reason" in result:
             return False, f"Validation failed: {result['reason']}"

        # Check for compilation errors
        if "result" in result and result["result"] and "errors" in result["result"]:
            errors = result["result"]["errors"]
            if errors:
                error = errors[0]
                return False, f"Syntax error: {error.get('message', 'Unknown error')}"
        
        # If no errors are found, the script is valid
        if result.get("success", False):
            return True, "Pine Script syntax is valid."
        else:
            return False, "Validation failed with an unknown error."
            
    except Exception as e:
        return False, f"An unexpected error occurred during validation: {e}"

async def main():
    # Example usage:
    # 1. A valid script string
    valid_script = """
//@version=5
indicator("My Script", overlay=true)
plot(close)
"""
    print("--- Validating valid script ---")
    is_valid, message = await validate_pine_script(valid_script.strip())
    print(f"Result: {is_valid}, Message: {message}\\n")

    # 2. An invalid script string
    invalid_script = """
//@version=5
indicator("My Script", overlay=true)
plot(clse) 
"""
    print("--- Validating invalid script ---")
    is_valid, message = await validate_pine_script(invalid_script.strip())
    print(f"Result: {is_valid}, Message: {message}")

if __name__ == "__main__":
    asyncio.run(main())
