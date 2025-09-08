# Summer School: Computational Psycholinguistics - Practical Session

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jobschepens/mlschool-text/HEAD?labpath=notebooks)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jobschepens/mlschool-text/blob/main/)

## Quick Start Options

### Option 1: Google Colab (Recommended)
Click the "Open in Colab" badge above, then:
- Navigate to the `notebooks/` folder
- Open either:
  - `notebook1_llm_generation.ipynb` - Generate linguistic predictors with LLMs
  - `notebook2_corpus_analysis.ipynb` - Analyze predictors vs. human reading data

### Option 2: Binder
Click the "Binder" badge above for a ready-to-run environment (may take 2-3 minutes to load)

### Option 3: Local Installation
```bash
git clone https://github.com/jobschepens/mlschool-text.git
cd mlschool-text
pip install -r requirements.txt
jupyter lab notebooks/
```

## About This Project

This repository contains materials for a computational psycholinguistics summer school practical session, extending the research from Schepens et al. to English using LLM-generated linguistic predictors. It provides both interactive notebooks for learning and a scalable corpus generation pipeline for research.

### Key Files
- **Notebooks**: Interactive Jupyter notebooks in `notebooks/`
- **Generated Data**: Pre-computed corpus and predictors in `output/` 
- **Reference Data**: Psycholinguistic datasets in `data/`
- **Scripts**: Standalone generation scripts in `scripts/`

## Recommended Workflow

Follow this step-by-step progression through the notebooks and scripts:

### 1. **Start Here**: `notebook1_llm_generation.ipynb`
- Introduction to LLM-based corpus generation
- Learn the basic concepts and setup

### 2. **Generate Large Corpus**: Choose one script
- `script-1-gen.py` - Original approach with fixed genre prompts
- `script-1-gen-dynamic.py` - New approach with more prompt variety (recommended)
- Or create your own version using the provided templates
- **Important**: Use an updated config file (e.g., `config_2m_llama.json`)

### 3. **Quality Check** (Optional): `quick_check_corpus.ipynb`
- Verify your generated corpus quality
- Check word frequency distributions

### 4. **Export Data** (Optional): `export_with_metadata.py`
- Extract and format corpus data with metadata
- Prepare data for analysis

### 5. **Merge Data**: `notebook1b_merge.ipynb`
- Combine multiple corpus sources
- Create unified predictor datasets

### 6. **Frequency Analysis** (Optional): `notebook1c_frequency_analysis.ipynb`
- Deep dive into frequency calculations
- Compare different frequency measures

### 7. **Compare Transformations** (Optional): `notebook1d_comparetransformations.ipynb`
- Analyze different data transformation approaches
- Validate preprocessing steps

### 8. **Final Analysis**: `notebook2_corpus_analysis.ipynb`
- Validate predictors against human reading times
- Load multiple psycholinguistic databases (ELP, BLP, ECP)
- Compare LLM-derived vs. traditional frequency measures
- Statistical analysis using restricted cubic splines

## Data Availability

All generated corpora and derived predictors are included in this repository for immediate use:
- `output/generated_corpus_with_predictors.csv` - Main predictor file
- `output/large_corpus_*.txt` - Generated text corpora
- `data/` - Reference psycholinguistic datasets

This allows you to run the analysis notebooks immediately without needing to generate new corpora (which can take hours and requires API keys).

## Project Structure

The project is organized into the following directories:

```
.
├── data/                 # Reference psycholinguistic datasets
├── notebooks/            # Interactive Jupyter notebooks for the practical session
├── output/               # Pre-generated corpora and predictors (included for sharing)
├── scripts/              # Python scripts for corpus generation
├── .env                  # For storing API keys (create locally, not tracked by Git)
├── .gitignore            # Specifies files and directories to be ignored by Git
├── README.md             # This file
├── requirements.txt      # Python dependencies for local installation
├── requirements_colab.txt # Dependencies for Google Colab
└── environment.yml       # Conda environment for Binder
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    *   Create a file named `.env` in the project root.
    *   Add your API key to the file, like this:
        ```
        OPENROUTER_API_KEY="your_api_key_here"
        ```

## How to Use

### Quick Start (Using Pre-generated Data)
If you want to jump straight to analysis without generating new corpora:
1. Open `notebook2_corpus_analysis.ipynb` 
2. Run all cells to see the complete analysis using our pre-generated data

### Full Workflow (Generate Your Own Data)
For the complete experience and to understand the full pipeline:

1. **Start with the basics**: Open `notebook1_llm_generation.ipynb` to understand LLM generation concepts

2. **Generate a large corpus**: 
   Run the generation scripts with configuration files that specify model, target size, and other parameters.
   
   **Basic syntax:**
   ```bash
   python scripts/<script-name> --config <config-file-path>
   ```
   
   **Examples:**
   ```bash
   # Recommended: Dynamic generation with infinite prompt variety
   python scripts/script-1-gen-dynamic.py --config scripts/config_2m_qwen_30b.json
   
   # Alternative: Original approach with fixed prompts
   python scripts/script-1-gen.py --config scripts/config_2m_llama.json
   
   # With full Python path (useful on Windows)
   & c:/Python313/python.exe c:/GitHub/mlschool-text/scripts/script-1-gen.py --config ./scripts/config_2m_qwen_30b.json
   ```
   
   **Available config files:**
   - `config_2m_qwen_30b.json` - 2M tokens using Qwen 30B model (free tier)
   - `config_2m_llama.json` - 2M tokens using Llama 3.3 8B model (free tier)
   - `config_2m_gpt_oss20b.json` - 2M tokens using GPT model
   - Create custom configs by copying and modifying existing ones

3. **Process and analyze**: Follow the notebook sequence (1b → 1c → 1d → 2) as outlined in the workflow above

## Running Generation Scripts

### Command Syntax
All generation scripts use configuration files to specify their behavior:
```bash
python scripts/<script-name> --config <config-file-path>
```

### Platform-Specific Examples

**Linux/macOS:**
```bash
cd mlschool-text
python scripts/script-1-gen-dynamic.py --config scripts/config_2m_qwen_30b.json
```

**Windows (PowerShell):**
```powershell
cd mlschool-text
python scripts/script-1-gen-dynamic.py --config scripts/config_2m_qwen_30b.json

# Or with full Python path:
& c:/Python313/python.exe scripts/script-1-gen.py --config ./scripts/config_2m_qwen_30b.json
```

**Windows (Command Prompt):**
```cmd
cd mlschool-text
python scripts\script-1-gen-dynamic.py --config scripts\config_2m_qwen_30b.json
```

### Script Options

**Recommended: `script-1-gen-dynamic.py`**
- Infinite prompt variety using combinatorial generation
- Eliminates genre bias from fixed prompt categories
- More diverse vocabulary coverage

**Alternative: `script-1-gen.py`**
- Original approach with predefined genre categories
- More predictable content distribution
- Faster execution due to simpler prompt selection

### Configuration Files
Available config files for different models and scales:
- `config_2m_llama.json` - 2M tokens using Llama model (recommended)
- `config_2m_gpt_oss20b.json` - Alternative using GPT model
- Create your own config file following the provided templates

### Resuming Interrupted Generation

The generation scripts are fully resumable! If a generation process is interrupted, simply run the same command again:

#### Check Available State Files
```bash
python -c "
import json, os
state_files = [f for f in os.listdir('output/') if f.startswith('generation_state_') and f.endswith('.json')]
print('Available state files for resuming:')
for state_file in state_files:
    try:
        with open(f'output/{state_file}', 'r') as f:
            state = json.load(f)
        words = state.get('total_words_generated', 0)
        requests = state.get('total_requests', 0)
        print(f'📁 {state_file}')
        print(f'   Progress: {words:,} words | {requests} requests')
    except: pass
"
```

#### Resume Generation
Use the **exact same command** that was used originally:
```bash
# The script will automatically detect and continue from the existing state file
python scripts/script-1-gen-dynamic.py --config scripts/config_2m_qwen_30b.json
python scripts/script-1-gen.py --config scripts/config_2m_llama.json
```

**How it works:**
- Scripts automatically detect existing state files matching the config
- Progress is loaded: words generated, requests made, estimated cost
- Generation continues by appending to the same corpus file
- State is saved periodically (every 10 texts by default) for fault tolerance
