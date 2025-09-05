# Notebook 1 Development Plan: LLM Corpus Generation & Analysis

## 🎯 **Overall Objective**
Transform `notebook1_llm_generation.ipynb` into a focused 45-minute practical session teaching **corpus-derived frequency** methodology through hands-on LLM text generation and analysis.

## 📋 **Session Structure Overview**

### **Core Learning Goals:**
1. **Understand** LLM corpus generation methodology (Schepens et al.)
2. **Experiment** with different text generation strategies  
3. **Analyze** frequency distributions and lexical richness
4. **Compare** LLM-derived vs traditional frequency measures

---

## 🔧 **Implementation Strategy**

### **Phase 1: Setup Simplification** 
**⏱️ Time allocation:** 5 minutes

**Goal:** Streamline API and environment setup for participants
- **Action:** Replace complex `LLMManager` class with single OpenRouter API function
- **Rationale:** Align with `scripts/generate_large_corpus.py` for consistency
- **Outcome:** Quick, easy setup reducing technical barriers

### **Phase 2: Interactive Text Generation** 
**⏱️ Time allocation:** 20 minutes *(notebook-1a-pilot)*

**Goal:** Hands-on experimentation with LLM text generation
- **Activities:**
  - Test different models (GPT-4, Claude, etc.)
  - Experiment with generation parameters
  - Try various prompt strategies
  - Observe output quality and characteristics
- **Learning Focus:** Understanding how generation choices affect corpus properties
- **Interactive Elements:** Live model comparison, parameter tuning

--------------done-----------

### **Phase 3: Frequency Analysis & Lexical Richness** 
**⏱️ Time allocation:** 20 minutes *(notebook-1c-table)*

**Goal:** Analyze generated corpus and compute frequency measures
- **Activities:**
  - Tokenize and process generated text
  - Compute word frequency distributions
  - Calculate lexical richness metrics
  - Compare with traditional frequency norms
- **Learning Focus:** From raw text to psycholinguistic predictors
- **Validation:** Connect to behavioral data (preview of Notebook 2)

---

## 🔄 **Supporting Development Components**

### **Background Processing Scripts**

#### **script-1-gen: Enhanced Corpus Generation**
- **Purpose:** Adapt `scripts/generate_large_corpus.py` for multiple corpus strategies
- **Features:** 
  - Organize different generation approaches
  - Store metadata for each corpus variant
  - Enable systematic comparison across methods
- **Timeline:** Develop post-session for extended research

#### **script-2-merge: Data Integration Pipeline**  
- **Purpose:** Convert `prepare_predictors_from_corpus.ipynb` to standalone script
- **Features:**
  - Automated frequency measure computation
  - Multi-corpus data merging
  - Export to standardized format for Notebook 2
- **Rationale:** Separates data processing from interactive analysis

### **Optional Advanced Components**

#### **notebook-1b-growth: Corpus Growth Analysis** *(Optional)*
- **Purpose:** Advanced analysis using LNRE models (R `zipfR` package)
- **Features:**
  - Model vocabulary growth curves
  - Compare generation strategies statistically
  - Predict corpus completeness
- **Target Audience:** Instructor/advanced participants
- **Timeline:** Post-session development

---

## 📚 **Educational Narrative Strategy**

### **Clear Motivation:**
- Explain **why** pre-generated corpus and familiarity scores are used
- Connect to broader computational psycholinguistics methodology
- Emphasize hands-on learning over complex setup

### **Progressive Complexity:**
1. **Simple generation** → Understanding LLM capabilities
2. **Parameter exploration** → Seeing impact of choices  
3. **Frequency analysis** → Connecting to psycholinguistics
4. **Validation preview** → Bridging to behavioral data

### **Learning Reinforcement:**
- Visual feedback throughout generation process
- Immediate analysis of generated content
- Clear connections between methodology and research applications

---

## ✅ **Success Criteria**

**Participants will be able to:**
1. Generate text corpora using LLMs with different strategies
2. Compute and interpret word frequency distributions
3. Understand the connection between corpus properties and psycholinguistic research
4. Critically evaluate different text generation approaches

**Technical Outcomes:**
- Streamlined 45-minute session flow
- Robust, easy-to-use codebase
- Clear educational progression
- Foundation for advanced corpus research