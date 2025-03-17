import google.generativeai as genai
import pygame
import random
import os
import re
import subprocess

# Configure the API key for Google's Gemini AI
genai.configure(api_key="api-key")

def clean_script(script):
    """Removes potential Markdown formatting from the generated script."""
    script = script.strip()
    script = re.sub(r"^```python", "", script)  # Remove ```python at the start
    script = re.sub(r"```$", "", script)  # Remove closing ```
    return script.strip()

def generate_game_script(level=1, previous_script=None):
    """Generates a game script using Google's Generative AI model, adapting for new levels."""
    model = genai.GenerativeModel("gemini-1.5-pro")  # Use the best available model
    prompt = (f"Create a Python video game with a graphical UI. Increase the complexity for level {level}. "
              "Ensure it builds on the previous version by adding new challenges, enemies, or mechanics. "
              "Avoid Markdown formatting or explanations—output only valid Python code. Don't use any external assets that I need to add, make it fully self-sufficient. Also get creative with the style, the UI, and the game mechanics. Make it imitate an already made game, even!")
    
    if previous_script:
        prompt += "\nModify this existing script to include the new level:\n" + previous_script
    
    response = model.generate_content(prompt)
    
    if response and response.text:
        return clean_script(response.text)
    return "print('Error generating game script.')"

def save_game_script(script):
    """Saves the generated script to a Python file."""
    with open("generated_game.py", "w", encoding="utf-8") as file:
        file.write(script)

def run_generated_game():
    """Executes the generated Python script using subprocess."""
    try:
        subprocess.run(["python", "generated_game.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running generated game: {e}")

def check_game_completion():
    """Checks if the game is completed and triggers a new level generation."""
    if os.path.exists("game_completed.txt"):
        os.remove("game_completed.txt")  # Reset for next time
        return True
    return False

if __name__ == "__main__":
    level = 1
    previous_script = None
    
    while True:
        game_script = generate_game_script(level, previous_script)
        save_game_script(game_script)
        run_generated_game()
        
        if check_game_completion():
            level += 1
            previous_script = game_script
            print(f"Level {level} unlocked! Generating new content...")
        else:
            break
