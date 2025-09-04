# LLM-Powered Psycholinguistics: Corpus Generation and Analysis

This project provides a framework for generating large-scale text corpora using Large Language Models (LLMs) and analyzing their linguistic properties. It is designed to support psycholinguistic research by creating controlled, high-quality datasets for studying word processing, frequency, and familiarity effects.

The project is divided into two main components:
1.  **A Practical Session for a Summer School**: Two Jupyter notebooks that guide participants through generating linguistic predictors with LLMs and validating them against human reading time data.
2.  **A Scalable Corpus Generation Pipeline**: A standalone Python script for generating massive, contextually diverse text corpora for in-depth research.

## Project Structure

The project is organized into the following directories:

```
.
├── data/                 # For storing input data (e.g., seed words). (Not tracked by Git)
├── notebooks/            # Jupyter notebooks for analysis and the practical session.
├── output/               # For storing large generated files (e.g., corpora). (Not tracked by Git)
├── scripts/              # Python scripts for corpus generation.
├── .env                  # For storing API keys (e.g., OPENROUTER_API_KEY). (Not tracked by Git)
├── .gitignore            # Specifies files and directories to be ignored by Git.
├── README.md             # This file.
└── requirements.txt      # Python dependencies for the project.
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

### 1. Large-Scale Corpus Generation

The primary generation script allows for the creation of massive, resumable text corpora.

*   **Script:** `scripts/generate_large_corpus.py`
*   **Configuration:** `scripts/config.json`

**To run the generation:**
1.  **Configure:** Edit `scripts/config.json` to set the `target_word_count`, model parameters, and file paths. Ensure the `seed_words_file` points to a valid CSV or Excel file inside the `data/` directory.
2.  **Execute:** Run the script from the project's root directory:
    ```bash
    python scripts/generate_large_corpus.py
    ```
    The script will save its progress to `output/generation_state.json` and the final corpus to `output/large_corpus.txt`. It can be safely stopped and restarted.

### 2. Summer School Practical Session

The practical session is contained in two Jupyter notebooks.

*   **Notebook 1: LLM Generation**: `notebooks/notebook1_llm_generation.ipynb`
    *   **Purpose**: Generates a small corpus and calculates both word frequency and LLM-estimated "familiarity" scores.
    *   **Output**: A `.csv` file with words and their associated predictors.

*   **Notebook 2: Corpus Analysis**: `notebooks/notebook2_corpus_analysis.ipynb`
    *   **Purpose**: Analyzes the predictors from Notebook 1 and validates them against human reading time data using restricted cubic splines regression.

**To run the session:**
1.  Launch Jupyter Lab or Jupyter Notebook from your terminal.
2.  Open and run the cells in `notebook1_llm_generation.ipynb` first.
3.  Then, open and run the cells in `notebook2_corpus_analysis.ipynb`.

### 3. Corpus Quality Analysis

A dedicated notebook is available to analyze the quality of any generated corpus.

*   **Notebook:** `notebooks/analyze_corpus.ipynb`
*   **Purpose**: Performs quality checks, such as verifying Zipf's Law and inspecting the most frequent words, on a generated text file.
*   **To Use**: Place the corpus file (e.g., `large_corpus.txt`) in the `output/` directory and run the cells in the notebook.
