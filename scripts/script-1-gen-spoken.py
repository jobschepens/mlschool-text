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

# --- Load Movie Titles ---
def load_movie_titles(titles_path='scripts/watch.md'):
    """Loads movie titles from the watch.md file."""
    print(f"Loading movie titles from {titles_path}...")
    try:
        with open(titles_path, 'r') as f:
            titles = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(titles)} movie titles.")
        return titles
    except FileNotFoundError:
        print(f"❌ Error: Movie titles file '{titles_path}' not found.")
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
            
            # Handle different API response formats robustly
            if 'choices' in result and len(result['choices']) > 0:
                # Standard OpenAI/OpenRouter format
                return result['choices'][0]['message']['content'].strip()
            elif 'error' in result:
                # API error response
                error_msg = result.get('error', {}).get('message', str(result['error']))
                print(f"   ⚠️ API Error: {error_msg}")
                return ""
            else:
                # Unexpected response format - debug and handle gracefully
                print(f"   ⚠️ Unexpected API response format. Keys: {list(result.keys())}")
                print(f"   📝 Response content: {str(result)[:200]}...")
                
                # Try alternative response formats
                if 'data' in result and isinstance(result['data'], list) and len(result['data']) > 0:
                    return str(result['data'][0]).strip()
                elif 'text' in result:
                    return str(result['text']).strip()
                elif 'content' in result:
                    return str(result['content']).strip()
                else:
                    print(f"   ❌ Could not extract text from response")
                    return ""
                    
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ API request failed (Attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
        except KeyError as e:
            print(f"   ⚠️ Response format error (Attempt {attempt + 1}/{max_retries}): Missing key {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"   ⚠️ Unexpected error (Attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
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

# --- Spoken-Style Prompt Generation ---
def get_spoken_prompt(movie_titles):
    """Generates a prompt that encourages spoken-like text using movie titles."""
    
    # Randomly select a movie title
    movie_title = random.choice(movie_titles)
    
    # Conversational scenarios for spoken text
    scenarios = [
        "Imagine you're chatting with a friend about the movie '{movie}'. What would you say? Talk about your thoughts, feelings, and reactions in a casual, conversational way.",
        "Pretend you're discussing '{movie}' with someone at a party. Share your opinions, favorite parts, and why you like or dislike it, using everyday language.",
        "Think about '{movie}' as if you're telling a story to someone. Describe it in a natural, spoken style, like you're speaking to a friend over coffee.",
        "Recall '{movie}' and talk about it as if you're recommending it to someone. Use conversational language, pauses, and personal anecdotes.",
        "Picture yourself watching '{movie}' and then describing it to a family member. Speak naturally, with enthusiasm or criticism as it comes to mind.",
        "Discuss '{movie}' as if you're texting or calling a friend. Keep it informal, with short sentences and personal touches.",
        "Imagine '{movie}' sparked a debate. Argue your point casually, using spoken phrases like 'you know' or 'I mean'.",
        "Tell someone about '{movie}' as if you're recounting it after seeing it. Use a storytelling voice, with details that come up in conversation."
    ]
    
    # Select a random scenario
    scenario = random.choice(scenarios).format(movie=movie_title)
    
    # Add instructions for spoken style
    spoken_instructions = [
        "Use contractions, filler words like 'um' or 'you know', and make it sound like real speech.",
        "Include personal opinions, questions, and responses as if in a dialogue.",
        "Keep it natural and flowing, not too formal or structured.",
        "Vary sentence length and add enthusiasm or hesitation to mimic spoken language."
    ]
    
    instruction = random.choice(spoken_instructions)
    
    # Construct the final prompt
    prompt = f"{scenario} {instruction} Write in a way that feels like spoken conversation."
    
    # Create a genre label for tracking
    genre_label = f"spoken_{movie_title.replace(' ', '_').lower()}"
    
    return prompt, genre_label

# --- API Key Handling ---
def get_api_key():
    """Get API key from environment or Colab userdata"""
    # Try environment variable first (local/.env)
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    # If not found and we're in Colab, try userdata
    if (not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE") and 'google.colab' in sys.modules:
        try:
            from google.colab import userdata
            api_key = userdata.get('OPENROUTER_API_KEY')
            print("🔑 API key loaded from Colab userdata")
        except Exception as e:
            print(f"⚠️ Could not load API key from Colab userdata: {e}")
    
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE":
        raise ValueError("OPENROUTER_API_KEY not found. Please set it in .env file or Colab Secrets.")
    
    return api_key

# --- Main Generation Logic ---
def main(config_path):
    """Main function to run the spoken-style corpus generation."""
    # Load environment variables from .env file
    load_dotenv()
    
    config = load_config(config_path)
    
    # Load movie titles
    movie_titles = load_movie_titles('scripts/watch.md')
    
    # Create timestamped file names to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Modify file paths to include timestamp
    base_corpus_path = config['output_corpus_path']
    base_state_path = config['state_file_path']
    
    # Insert timestamp before file extension
    corpus_name, corpus_ext = os.path.splitext(base_corpus_path)
    state_name, state_ext = os.path.splitext(base_state_path)
    
    config['output_corpus_path'] = f"{corpus_name}_spoken_{timestamp}{corpus_ext}"
    config['state_file_path'] = f"{state_name}_spoken_{timestamp}{state_ext}"
    
    print(f"🎲 Spoken-style generation with timestamp: {timestamp}")
    print(f"📁 Corpus file: {config['output_corpus_path']}")
    print(f"💾 State file: {config['state_file_path']}")
    
    # --- Ensure output directory exists before proceeding ---
    output_dir = os.path.dirname(config['output_corpus_path'])
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Ensured output directory exists: {output_dir}")

    state = load_state(config['state_file_path'])

    # Get API key from environment or Colab userdata
    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"❌ {e}")
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

    print(f"\n--- Starting Spoken-Style Corpus Generation ---")
    print(f"🎲 Strategy: Conversational prompts based on movie titles")
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
                
                # Generate a spoken-style prompt using a movie title
                final_prompt, genre_label = get_spoken_prompt(movie_titles)
                print(f"-> Generating: {genre_label}")
                print(f"   Prompt: {final_prompt[:100]}...")

                # Generate text
                generated_text = generate_text(api_config, final_prompt)
                
                if generated_text:
                    # Estimate cost for this request
                    request_cost = estimate_request_cost(final_prompt, generated_text, config['model_name'])
                    current_cost += request_cost
                    total_requests += 1
                    
                    # Create story metadata
                    story_metadata = {
                        'story_id': f"spoken_{total_requests:04d}",
                        'genre': genre_label,
                        'word_count': len(generated_text.split()),
                        'character_count': len(generated_text),
                        'timestamp': datetime.now().isoformat(),
                        'prompt_used': final_prompt,
                        'estimated_cost': request_cost,
                        'generation_strategy': 'spoken_movie_discussion'
                    }
                    
                    # Save story metadata (memory-efficient for large corpora)
                    if 'stories' not in state:
                        state['stories'] = []
                    
                    # Keep only recent stories in memory (last 100)
                    state['stories'].append(story_metadata)
                    if len(state['stories']) > 100:
                        state['stories'] = state['stories'][-100:]  # Keep only last 100
                    
                    # Optionally save detailed metadata to separate file
                    if config.get('save_detailed_metadata', True):
                        metadata_file = config['state_file_path'].replace('.json', '_metadata.jsonl')
                        with open(metadata_file, 'a', encoding='utf-8') as meta_f:
                            meta_f.write(json.dumps(story_metadata, ensure_ascii=False) + '\n')
                    
                    # Append to file with metadata header
                    f.write(f"<!-- Story Metadata: {json.dumps(story_metadata, ensure_ascii=False)} -->\n")
                    f.write(generated_text + "\n\n")
                    num_new_words = len(generated_text.split())
                    current_words += num_new_words
                    texts_generated_since_save += 1
                    
                    print(f"   ✅ Generated {num_new_words} words. Total: {current_words:,} / {target_words:,} ({current_words/target_words:.2%})")
                    print(f"   💰 Request cost: ${request_cost:.4f}, Total cost: ${current_cost:.4f}")
                    
                    # Enhanced progress reporting for large corpora
                    if total_requests % 100 == 0:  # Every 100 requests
                        elapsed_time = time.time() - state.get('start_time', time.time())
                        words_per_hour = current_words / (elapsed_time / 3600) if elapsed_time > 0 else 0
                        estimated_time_remaining = (target_words - current_words) / words_per_hour if words_per_hour > 0 else 0
                        print(f"   📊 Milestone: {total_requests} requests, {words_per_hour:.0f} words/hour, ~{estimated_time_remaining:.1f}h remaining")
                    
                    print(f"   📝 Story ID: {story_metadata['story_id']}")

                # Save state periodically
                if texts_generated_since_save >= config['texts_per_state_save']:
                    state.update({
                        'total_words_generated': current_words,
                        'estimated_cost': current_cost,
                        'total_requests': total_requests
                    })
                    save_state(state, config['state_file_path'])
                    print(f"   💾 Progress saved. {current_words:,} words, ${current_cost:.4f} spent.")
                    texts_generated_since_save = 0
                
                # Adaptive rate limiting for free models
                if "free" in config.get('model_name', '').lower():
                    # More conservative for free models - increased delay to avoid rate limits
                    time.sleep(random.uniform(10, 20))  # 10-20 second random delay
                else:
                    time.sleep(2)  # Standard delay for paid models

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
        print(f"\n--- Spoken-Style Generation Finished ---")
        print(f"Final word count: {current_words:,}")
        print(f"Total requests made: {total_requests}")
        print(f"Estimated total cost: ${current_cost:.4f}")
        print(f"Average cost per request: ${current_cost/max(1, total_requests):.6f}")
        print(f"Words per dollar: {current_words/max(0.001, current_cost):.0f}")
        print(f"Corpus saved to: {config['output_corpus_path']}")
        print(f"Final state saved to: {config['state_file_path']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a spoken-style text corpus using movie titles.")
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to the configuration file (e.g., config_2m_llama.json).'
    )
    args = parser.parse_args()
    main(args.config)