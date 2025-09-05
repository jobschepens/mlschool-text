import os
import json
import random
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import argparse

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
    return {
        'total_words_generated': 0,
        'total_requests': 0,
        'estimated_cost': 0.0,
        'start_time': time.time()
    }

def save_state(state, state_path):
    """Saves the current generation state."""
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=4)

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
    
    # Add provider preference if specified in config
    if "provider_preference" in api_config:
        data["provider"] = {
            "order": api_config["provider_preference"]
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

# --- Cost Estimation ---
def estimate_request_cost(prompt_text, response_text, model_name):
    """Estimates the cost of a single API request based on token count and model pricing."""
    # Rough token estimation: ~4 characters per token
    input_tokens = len(prompt_text) // 4
    output_tokens = len(response_text) // 4
    
    # Nebius AI Studio pricing (based on your info): $0.10 input, $0.30 output per 1M tokens
    if "nebius" in model_name.lower() or "llama" in model_name.lower():
        input_cost = (input_tokens / 1_000_000) * 0.10
        output_cost = (output_tokens / 1_000_000) * 0.30
        return input_cost + output_cost
    
    # Default pricing for other models (rough estimate)
    input_cost = (input_tokens / 1_000_000) * 0.15
    output_cost = (output_tokens / 1_000_000) * 0.40
    return input_cost + output_cost

def check_budget_limit(state, config):
    """Checks if we've reached the budget limit."""
    max_cost = config.get('max_generation_cost', 10.0)
    current_cost = state.get('estimated_cost', 0.0)
    
    if current_cost >= max_cost:
        print(f"\n💰 Budget limit reached: ${current_cost:.4f} / ${max_cost:.2f}")
        print("Stopping generation to prevent overspending.")
        return True
    
    remaining = max_cost - current_cost
    print(f"💰 Budget status: ${current_cost:.4f} spent, ${remaining:.4f} remaining")
    return False

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

# --- Prompt Engineering ---
def get_diverse_prompts():
    """Returns a list of diverse prompts for generation that use seeds as inspiration."""
    return {
        "Technical/Scientific": "Write a clear, accessible explanation of a scientific concept. Draw inspiration from themes related to: {seed_words}. Focus on making complex ideas understandable.",
        "News/Informative": "Write a short, informative news-style article. Let the following concepts guide your topic choice: {seed_words}. Write naturally about current events or important information.",
        "Fiction/Creative": "Write a short, engaging creative story. Use these concepts as thematic inspiration: {seed_words}. Let the story flow naturally without forcing specific words.",
        "General Knowledge/How-To": "Write a helpful 'how-to' guide or educational explanation. Draw inspiration from these areas: {seed_words}. Focus on practical, useful information."
    }

def get_general_prompts():
    """Returns a list of diverse, self-contained prompts for generation."""
    return {
        "Technical/Scientific": "Write a clear, accessible explanation of a scientific concept like photosynthesis, black holes, or the theory of relativity. Focus on making complex ideas understandable to a general audience.",
        "News/Informative": "Write a short, informative news-style article about a recent technological breakthrough, a significant global event, or a cultural festival. Write in a neutral, factual tone.",
        "Fiction/Creative": "Write a short, engaging creative story about a character who makes an unexpected discovery, travels to a new place, or overcomes a personal challenge. Let the story flow naturally and use descriptive language.",
        "General Knowledge/How-To": "Write a helpful 'how-to' guide on a practical skill, such as how to bake bread, create a budget, or learn a new language. Focus on clear, step-by-step instructions."
    }

# --- Main Generation Logic ---
def main(config_path):
    """Main function to run the large-scale corpus generation."""
    # Load environment variables from .env file
    load_dotenv()
    
    config = load_config(config_path)
    
    # --- Ensure output directory exists before proceeding ---
    output_dir = os.path.dirname(config['output_corpus_path'])
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Ensured output directory exists: {output_dir}")

    state = load_state(config['state_file_path'])
    
    # --- Prompt and Seed Word Strategy ---
    use_seeds = config.get('use_seed_words', False)
    if use_seeds:
        print("🌱 Using seed word strategy for prompt generation.")
        seed_words = load_seed_words(config['ecp_word_list_path'])
        prompts = get_diverse_prompts()
        if not seed_words:
            print("Cannot proceed with seed word strategy without seed words. Exiting.")
            return
    else:
        print("📝 Using general prompt strategy.")
        prompts = get_general_prompts()
        seed_words = [] # Ensure it's an empty list if not used

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
    current_cost = state.get('estimated_cost', 0.0)
    total_requests = state.get('total_requests', 0)

    print(f"\n--- Starting Corpus Generation ---")
    print(f"Target Word Count: {target_words:,}")
    print(f"Current Word Count: {current_words:,}")
    print(f"Budget Limit: ${config.get('max_generation_cost', 10.0):.2f}")
    print(f"Current Cost: ${current_cost:.4f}")
    print(f"------------------------------------")

    try:
        with open(config['output_corpus_path'], 'a', encoding='utf-8') as f:
            while current_words < target_words:
                # Check budget before making request
                if check_budget_limit(state, config):
                    break
                
                # 1. Select a random prompt template
                genre, prompt_template = random.choice(list(prompts.items()))

                # 2. Construct the final prompt based on strategy
                if use_seeds:
                    selected_seeds = random.sample(seed_words, config['words_to_seed'])
                    seed_str = ", ".join(selected_seeds)
                    final_prompt = prompt_template.format(seed_words=seed_str)
                    print(f"-> Generating text for genre '{genre}' with seeds: {seed_str}")
                else:
                    final_prompt = prompt_template
                    selected_seeds = [] # No seeds used
                    print(f"-> Generating text for genre '{genre}'...")

                # 4. Generate text
                generated_text = generate_text(api_config, final_prompt)
                
                if generated_text:
                    # 5. Estimate cost for this request
                    request_cost = estimate_request_cost(final_prompt, generated_text, config['model_name'])
                    current_cost += request_cost
                    total_requests += 1
                    
                    # 6. Create story metadata
                    story_metadata = {
                        'story_id': f"story_{total_requests:04d}",
                        'genre': genre,
                        'seeds_used': selected_seeds,
                        'word_count': len(generated_text.split()),
                        'character_count': len(generated_text),
                        'timestamp': datetime.now().isoformat(),
                        'prompt_used': final_prompt,
                        'estimated_cost': request_cost
                    }
                    
                    # Save story metadata
                    if 'stories' not in state:
                        state['stories'] = []
                    state['stories'].append(story_metadata)
                    
                    # 7. Append to file with metadata header
                    f.write(f"<!-- Story Metadata: {json.dumps(story_metadata, ensure_ascii=False)} -->\n")
                    f.write(generated_text + "\n\n")
                    num_new_words = len(generated_text.split())
                    current_words += num_new_words
                    texts_generated_since_save += 1
                    
                    print(f"   ✅ Generated {num_new_words} words. Total: {current_words:,} / {target_words:,} ({current_words/target_words:.2%})")
                    print(f"   💰 Request cost: ${request_cost:.4f}, Total cost: ${current_cost:.4f}")
                    
                    if use_seeds:
                        print(f"   📝 Story ID: {story_metadata['story_id']}, Seeds: {seed_str}")
                    else:
                        print(f"   📝 Story ID: {story_metadata['story_id']}")

                # 7. Save state periodically
                if texts_generated_since_save >= config['texts_per_state_save']:
                    state.update({
                        'total_words_generated': current_words,
                        'estimated_cost': current_cost,
                        'total_requests': total_requests
                    })
                    save_state(state, config['state_file_path'])
                    print(f"   💾 Progress saved. {current_words:,} words, ${current_cost:.4f} spent.")
                    texts_generated_since_save = 0
                
                # 8. Brief pause to respect API rate limits
                time.sleep(2) # Adjust as needed

    except KeyboardInterrupt:
        print("\n🛑 Generation process interrupted by user.")
    finally:
        # Final save on exit
        state.update({
            'total_words_generated': current_words,
            'estimated_cost': current_cost,
            'total_requests': total_requests
        })
        save_state(state, config['state_file_path'])
        print(f"\n--- Generation Finished ---")
        print(f"Final word count: {current_words:,}")
        print(f"Total requests made: {total_requests}")
        print(f"Estimated total cost: ${current_cost:.4f}")
        print(f"Average cost per request: ${current_cost/max(1, total_requests):.6f}")
        print(f"Words per dollar: {current_words/max(0.001, current_cost):.0f}")
        print(f"Corpus saved to: {config['output_corpus_path']}")
        print(f"Final state saved to: {config['state_file_path']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a large text corpus using an LLM.")
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to the configuration file (e.g., config_2m_llama.json).'
    )
    args = parser.parse_args()
    main(args.config)
