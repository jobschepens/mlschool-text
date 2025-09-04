import os
import json
import random
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# --- Configuration Loading ---
def load_config(config_path='config.json'):
    """Loads the generation configuration from a JSON file."""
    print(f"Loading configuration from {config_path}...")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✅ Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        print(f"❌ Error: Configuration file '{config_path}' not found.")
        exit()
    except json.JSONDecodeError:
        print(f"❌ Error: Configuration file '{config_path}' is not valid JSON.")
        exit()

# --- State Management ---
def load_state(state_path):
    """Loads the generation state to allow for resuming."""
    if os.path.exists(state_path):
        print(f"Found existing state file at {state_path}. Resuming...")
        with open(state_path, 'r') as f:
            return json.load(f)
    print("No state file found. Starting a new generation process.")
    return {'total_words_generated': 0}

def save_state(state, state_path):
    """Saves the current generation state."""
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=4)

# --- Data Loading ---
def load_seed_words(ecp_path):
    """Loads the word list from the ECP data file for seeding prompts."""
    print(f"Loading seed words from {ecp_path}...")
    try:
        # Read from CSV instead of Excel
        df = pd.read_csv(ecp_path)
        # Use 'spelling' column instead of 'Word'
        words = df['spelling'].dropna().astype(str).tolist()
        print(f"✅ Loaded {len(words):,} unique words for seeding.")
        return words
    except FileNotFoundError:
        print(f"❌ Error: ECP word list not found at '{ecp_path}'.")
        return []
    except Exception as e:
        print(f"❌ Error loading ECP file: {e}")
        return []

# --- LLM Interaction ---
def generate_text(api_config, prompt, max_retries=3, retry_delay=5):
    """Generates text using the configured LLM API with retry logic."""
    headers = {
        'Authorization': f'Bearer {api_config["api_key"]}',
        'Content-Type': 'application/json',
        "HTTP-Referer": "http://localhost:3000", # Optional, for OpenRouter analytics
        "X-Title": "Psycholinguistics Summer School" # Optional, for OpenRouter analytics
    }
    data = {
        'model': api_config["model_name"],
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 400,
        'temperature': 0.75
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                api_config["api_base_url"],
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ API request failed (Attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
    
    print(f"   ❌ API request failed after {max_retries} attempts. Skipping this prompt.")
    return ""

# --- Prompt Engineering ---
def get_diverse_prompts():
    """Returns a list of diverse prompts for generation."""
    return {
        "Technical/Scientific": "Explain a complex scientific concept ({seed_words}) in a clear, accessible way.",
        "News/Informative": "Write a short, informative news-style article that includes the following terms: {seed_words}.",
        "Fiction/Creative": "Write a short, creative story that naturally incorporates these words: {seed_words}.",
        "General Knowledge/How-To": "Write a 'how-to' guide or a general explanation on a topic, making sure to use the words: {seed_words}."
    }

# --- Main Generation Logic ---
def main():
    """Main function to run the large-scale corpus generation."""
    # Load environment variables from .env file
    load_dotenv()
    
    config = load_config()
    state = load_state(config['state_file_path'])
    seed_words = load_seed_words(config['ecp_word_list_path'])
    prompts = get_diverse_prompts()
    
    if not seed_words:
        print("Cannot proceed without seed words. Exiting.")
        return

    # Get API key from environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE":
        print("❌ OPENROUTER_API_KEY not found or not set in .env file. Please add it to proceed.")
        return

    api_config = {
        "api_key": api_key,
        "api_base_url": config.get("api_base_url"),
        "model_name": config.get("model_name")
    }

    current_words = state.get('total_words_generated', 0)
    target_words = config['target_word_count']
    texts_generated_since_save = 0

    print(f"\n--- Starting Corpus Generation ---")
    print(f"Target Word Count: {target_words:,}")
    print(f"Current Word Count: {current_words:,}")
    print(f"------------------------------------")

    try:
        with open(config['output_corpus_path'], 'a', encoding='utf-8') as f:
            while current_words < target_words:
                # 1. Select a random prompt template
                genre, prompt_template = random.choice(list(prompts.items()))

                # 2. Select random seed words
                selected_seeds = random.sample(seed_words, config['words_to_seed'])
                seed_str = ", ".join(selected_seeds)

                # 3. Construct the final prompt
                final_prompt = prompt_template.format(seed_words=seed_str)
                
                print(f"-> Generating text for genre '{genre}' with seeds: {seed_str}")

                # 4. Generate text
                generated_text = generate_text(api_config, final_prompt)
                
                if generated_text:
                    # 5. Append to file and update state
                    f.write(generated_text + "\n\n")
                    num_new_words = len(generated_text.split())
                    current_words += num_new_words
                    texts_generated_since_save += 1
                    
                    print(f"   ✅ Generated {num_new_words} words. Total: {current_words:,} / {target_words:,} ({current_words/target_words:.2%})")

                # 6. Save state periodically
                if texts_generated_since_save >= config['texts_per_state_save']:
                    save_state({'total_words_generated': current_words}, config['state_file_path'])
                    print(f"   💾 Progress saved. {current_words:,} words generated.")
                    texts_generated_since_save = 0
                
                # 7. Brief pause to respect API rate limits
                time.sleep(2) # Adjust as needed

    except KeyboardInterrupt:
        print("\n🛑 Generation process interrupted by user.")
    finally:
        # Final save on exit
        save_state({'total_words_generated': current_words}, config['state_file_path'])
        print(f"\n--- Generation Finished ---")
        print(f"Final word count: {current_words:,}")
        print(f"Corpus saved to: {config['output_corpus_path']}")
        print(f"Final state saved to: {config['state_file_path']}")

if __name__ == "__main__":
    main()
