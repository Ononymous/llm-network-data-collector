import os
import json
import time
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

class WorkflowGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        # Create directories if they don't exist
        os.makedirs("playwright_test", exist_ok=True)
        os.makedirs("generated_test", exist_ok=True)
        
    def get_user_inputs(self):
        """Step 1 & 2: Ask for URL and filename"""
        print("Welcome to the Playwright Test Generator Workflow!")
        print("-" * 50)
        
        existing = input("If you have an existing Playwright recording file, enter its path (or press Enter to skip): ").strip()
        url = None
        filename = None
        
        if not existing:
            url = input("Enter the URL for test generation: ").strip()
            filename = input("Enter the base filename (without .py extension): ").strip()
        else:
            filename = Path(existing).stem
        
        return existing, url, filename

    def generate_playwright_test(self, url, filename):
        """Step 3: Run Playwright codegen with the given URL and filename using os.system"""
        print(f"\nGenerating Playwright test for: {url}")
        
        output_file = f"playwright_test/{filename}.py"
        cmd = f"playwright codegen {url} --channel chrome -o \"{output_file}\""
        
        try:
            print(f"Running command: {cmd}")
            exit_code = os.system(cmd)
            if exit_code == 0:
                print(f"Successfully generated test in {output_file}")
                return output_file
            else:
                print(f"Error generating test. Exit code: {exit_code}")
                print("Ensure you completed interactions in the Playwright codegen window and closed it.")
                return None
        except Exception as e:
            print(f"Exception occurred while running Playwright codegen: {e}")
            return None

    def read_generated_code(self, filepath):
        """Read the generated code from the file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return None

    def get_test_guidelines(self):
        """Step 4: Ask user for a guidelines file path and read its contents"""
        path = input("\nEnter the path to a guidelines text file (or press Enter to skip): ").strip()
        if not path:
            return ""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                guidelines = f.read().strip()
            print(f"Loaded guidelines from {path}")
            return guidelines
        except Exception as e:
            print(f"Error reading guidelines file {path}: {e}")
            return ""

    def prompt_gemini_for_generalization(self, original_code, guidelines):
        """Step 5: Send recorded code and user guidelines to Gemini to generate a comprehensive test"""
        print("\nSending code and guidelines to Gemini for comprehensive test generation...")
        
        prompt = f"""
You are an expert Playwright test automation engineer. 

Below is the recorded Playwright test code. Use it as a basis to generate a new, more comprehensive test script according to the user guidelines. The response must be a standalone Python script that includes only code and inline comments. Do not include any explanatory text outside of comments.

Recorded Code:
{original_code}

User Guidelines:
{guidelines}

Requirements:
- Use the recorded code as a foundation.
- Incorporate the user guidelines into the new test.
- Ensure proper wait conditions for page loads.
- Add error handling and retry mechanisms.
- Introduce randomness where applicable (e.g., random selections, delays).
- Structure the script as a test class with multiple test methods.
- Include logging or progress indicators as comments.
- Add any data collection or metrics as specified by the user.
- The final output must be pure Python code with inline comments; do not include plaintext explanations.

Return only the complete Python script.
Start with ```python
"""
        try:
            response = self.model.generate_content(prompt)
            generated_code = response.text
            # Strip markdown fences if present
            if generated_code.startswith("```python"):
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif generated_code.startswith("```"):
                generated_code = generated_code.split("```")[1].split("```")[0].strip()
            return generated_code
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None

    def save_generalized_code(self, code, filename):
        """Step 5 (continued): Save the generated code to a new file"""
        output_file = f"generated_test/{filename}_gen.py"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"Generalized code saved to {output_file}")
            return output_file
        except Exception as e:
            print(f"Error saving generalized code: {e}")
            return None

    def run_test(self, test_file):
        """Step 6: Run the generated test directly so headless=False browser can show"""
        print(f"\nLaunching test script: {test_file}")
        cmd = f"python3 {test_file}"
        print(f"Executing: {cmd}")
        try:
            exit_code = os.system(cmd)
            print(f"Test script exited with code: {exit_code}")
            if exit_code == 0:
                print("Test executed successfully.")
                return True, "", ""
            else:
                print("Test completed with non-zero exit code; inspect browser window for details.")
                return False, "", f"Exit code {exit_code}"
        except Exception as e:
            print(f"Exception occurred while launching test: {e}")
            return False, "", str(e)

    def get_feedback_from_file(self):
        """Step 7: Ask for a feedback file path and read its contents"""
        path = input("\nIf you have feedback saved in a file, enter the file path (or press Enter if satisfied): ").strip()
        if not path:
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                feedback = f.read().strip()
            print(f"Loaded feedback from {path}")
            return feedback
        except Exception as e:
            print(f"Error reading feedback file {path}: {e}")
            return None

    def update_code_with_feedback(self, current_code, feedback, error_message, filename):
        """Step 8: Send feedback (and any error details) back to Gemini to update the test code"""
        print("\nUpdating code based on feedback file...")
        error_section = f"\n\nIf the last run failed, here is the error message:\n{error_message}" if error_message else ""
        prompt = f"""
You are an expert Playwright test automation engineer. 

Below is the current test code:
{current_code}

User Feedback:
{feedback}
{error_section}

Requirements:
- Incorporate the user feedback.
- Fix any issues that caused errors if provided.
- Keep all existing functionality unless explicitly asked to remove it.
- Maintain randomness and robustness.
- Add any new error handling needed for new features.
- The final output must be a standalone Python script with inline comments. Do not include explanatory text outside of comments.

Return only the complete updated Python script.
Start with ```python
"""
        try:
            response = self.model.generate_content(prompt)
            updated_code = response.text
            # Strip markdown fences if present
            if updated_code.startswith("```python"):
                updated_code = updated_code.split("```python")[1].split("```")[0].strip()
            elif updated_code.startswith("```"):
                updated_code = updated_code.split("```")[1].split("```")[0].strip()
            output_file = f"generated_test/{filename}_gen.py"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(updated_code)
            print(f"Code updated and saved to {output_file}")
            return updated_code
        except Exception as e:
            print(f"Error updating code with Gemini: {e}")
            return current_code

    def run_workflow(self):
        """Main workflow orchestrator following the specified steps"""
        try:
            # Steps 1-2: Ask for recording path or URL and filename
            existing, url, filename = self.get_user_inputs()
            # Step 3: Use existing recording or generate a new one
            if existing:
                print(f"Using existing recording file: {existing}")
                initial_file = existing
            else:
                initial_file = self.generate_playwright_test(url, filename)
            if not initial_file:
                print("Failed to obtain initial test. Exiting workflow.")
                return
            # Read the recorded code
            original_code = self.read_generated_code(initial_file)
            if not original_code:
                print("Failed to read recorded code. Exiting workflow.")
                return
            # Step 4: Ask user for guidelines via file
            guidelines = self.get_test_guidelines()
            # Step 5: Generate a comprehensive test via Gemini
            generalized_code = self.prompt_gemini_for_generalization(original_code, guidelines)
            if not generalized_code:
                print("Failed to generate comprehensive test. Exiting workflow.")
                return
            # Save the generated code
            gen_file = self.save_generalized_code(generalized_code, filename)
            if not gen_file:
                print("Failed to save generated code. Exiting workflow.")
                return
            current_code = generalized_code
            # Step 6: Run the test
            success, _, stderr = self.run_test(gen_file)
            # Steps 7-9: Iterative feedback loop via feedback files
            while True:
                feedback = self.get_feedback_from_file()
                if not feedback:
                    print(f"\nWorkflow completed. Final test file: {gen_file}")
                    break
                error_message = stderr if not success else ""
                current_code = self.update_code_with_feedback(current_code, feedback, error_message, filename)
                print("\nRunning updated test...")
                success, _, stderr = self.run_test(gen_file)
        except KeyboardInterrupt:
            print("\nWorkflow interrupted by user.")
        except Exception as e:
            print(f"\nUnexpected error in workflow: {e}")

def main():
    """Entry point for the workflow"""
    print("Checking prerequisites...")
    # Check if Playwright is installed via os.system
    exit_code = os.system("playwright --version > /dev/null 2>&1")
    if exit_code == 0:
        print("Playwright is installed.")
    else:
        print("Playwright not found. Please install it with:")
        print("  pip install playwright && playwright install")
        return
    # Start the workflow
    workflow = WorkflowGenerator()
    workflow.run_workflow()

if __name__ == "__main__":
    main()
