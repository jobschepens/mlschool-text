# Guiding Principles for AI in the Computational Psycholinguistics Summer School Project

This project develops a practical session for a summer school, based on the research published in `resubmitted.tex` (Schepens et al.). The session extends the paper's findings—which used LLM-generated corpora to derive word frequency for German child readers—to English. It incorporates the novel "familiarity" metric from Brysbaert et al. (2025) as a state-of-the-art predictor to compare against traditional frequency measures.

The core of the project lies in two Jupyter notebooks that guide participants from generating linguistic predictors with LLMs to validating them against human reading time data.

## Core Architecture & Data Flow

The project is structured around a two-part practical session, implemented in two separate Jupyter notebooks located in `summerschooldocs/`:

1.  **`notebook1_llm_generation.ipynb`**:
    *   **Purpose**: To generate linguistic predictors using LLMs. This involves two main approaches:
        1.  **Frequency-based**: Generating a text corpus to calculate word frequency, following the methodology of `resubmitted.tex`.
        2.  **Familiarity-based**: Directly estimating word "familiarity" using the prompt engineering techniques from Brysbaert et al. (2025).
    *   **Output**: A `.csv` file containing words and their associated frequency and familiarity scores.

2.  **`notebook2_corpus_analysis.ipynb`**:
    *   **Purpose**: To analyze the predictors from Notebook 1 and validate them against human behavioral data (English reading times).
    *   **Key Concepts**: Loading the generated data, loading multiple psycholinguistic reference datasets (e.g., ELP, BLP, ECP) and frequency measures (SUBTLEX, Multilex), and performing comparative statistical analysis.
    *   **Core Method**: The primary analysis involves using **restricted cubic splines regression** (with 4 knots) to model the relationship between different predictors (frequency, familiarity) and human reading times, while controlling for variables like word length.

**Data Flow**: `notebook1` produces a `generated_corpus_with_predictors.csv` -> `notebook2` consumes this file and compares its metrics against established reading time databases and frequency norms.

## Theoretical Foundation

The project synthesizes two key papers:

1.  **`summerschooldocs/resubmitted.tex` (Schepens et al.)**: This is the **foundational study**. It demonstrated that word frequency derived from LLM-generated corpora can be a better predictor of reading times for German children than traditional corpora.
2.  **`papers/ms AI-based estimates of word familiarity.md` (Brysbaert et al., 2025)**: This paper introduces a **new, superior method**. It argues that LLM-generated *familiarity* estimates are a better predictor of word processing difficulty than traditional word *frequency* counts.

- **Your Goal**: The practical session should guide participants to extend the findings of `resubmitted.tex` to English. The central question is to determine the best predictor for English reading times by comparing:
    - Traditional frequency (e.g., SUBTLEX)
    - LLM-corpus-derived frequency (the Schepens et al. method)
    - LLM-estimated familiarity (the Brysbaert et al. method)

## Development Workflow & Conventions

- **Environment**: All dependencies (`pandas`, `scikit-learn`, `matplotlib`, etc.) are managed and installed directly within the notebooks. There is no separate `requirements.txt` or global environment file.
- **No Formal Test Suite**: "Testing" in this project means validating the results from the notebooks against the findings reported in the Brysbaert et al. (2025) paper. For example, a successful test is replicating the high percentage of variance explained by familiarity estimates.
- **Data Management**: The `technical_prep.md` file outlines the strategy for data acquisition. Reference datasets (ELP, BLP, ECP, etc.) and frequency norms (SUBTLEX, Multilex) are expected to be in a `data/` directory (which may need to be created).
- **Modularity**: The two-notebook structure is a deliberate choice to fit into two 45-minute session slots. Do not merge them. Maintain the clear separation of concerns: Generation vs. Analysis.
- **Statistical Method**: When performing regression, the default method should be **restricted cubic splines with 4 knots**, as this is the method used in the key research paper to achieve state-of-the-art results.

## Key Files for Context

- **`summerschooldocs/resubmitted.tex`**: The foundational research paper for the practical session.
- **`summerschooldocs/plan.md`**: The high-level project plan, including goals and timelines.
- **`summerschooldocs/technical_prep.md`**: The guide for setting up the technical environment, including where to source datasets.
- **`papers/ms AI-based estimates of word familiarity.md`**: The paper providing the state-of-the-art "familiarity" method to be tested.
