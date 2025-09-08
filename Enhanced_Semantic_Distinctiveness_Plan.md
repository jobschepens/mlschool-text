# Enhanced Semantic Distinctiveness Corpus Generator Plan

## 🎯 **Project Overview & Strategic Improvements**

Based on the analysis in notebook2, the seed-based strategy showed bias toward low-frequency words, which limited predictive power. This enhanced plan addresses those limitations by implementing a **balanced frequency sampling** approach combined with semantic distinctiveness filtering.

## 🔍 **Key Insights from Current Analysis**

1. **Seed Strategy Limitation**: Favored low-frequency words too heavily, reducing correlation with human reading times
2. **LLM Corpus Success**: +0.51% variance improvement validates the approach, but there's room for optimization
3. **Mathematical Foundation**: Corpus size/diversity ratio affects transformation behavior - we can leverage this
4. **Available Resources**: FastText wiki-news-300d-1M embeddings provide high-quality semantic vectors

## 🏗️ **Enhanced Architecture Design**

### **Core Innovation: Vocabulary-Stratified Semantic Sampling**

Instead of frequency-based sampling (which would contaminate validation), implement a **vocabulary-stratified sampling** approach that:
- Samples from ECP/SUBTLEX word lists WITHOUT using their frequency information
- Ensures balanced representation across word types (length, morphology, semantic categories)
- Maintains semantic distinctiveness within each vocabulary stratum
- Lets the LLM naturally determine frequency through generation patterns

### **Five-Module Architecture**

#### 1. **Enhanced Configuration Manager** (`semantic_config.json`)
```json
{
    "llm_config": {
        "api_key": "your_api_key",
        "model": "llama-3.1-8b-instant",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "embedding_config": {
        "model_path": "data/embeddings/wiki-news-300d-1M.vec",
        "vector_dim": 300,
        "cache_size": 100000
    },
    "semantic_config": {
        "similarity_threshold": 0.65,
        "context_window": 100,
        "min_context_gap": 0.3,
        "semantic_memory_size": 5
    },
    "sampling_config": {
        "vocabulary_source": "ecp_subtlex_wordlists",
        "stratification_method": "linguistic_features",
        "word_length_bins": [1, 3, 5, 8, 12, 20],
        "pos_categories": ["noun", "verb", "adjective", "adverb", "function"],
        "morphology_complexity": ["simple", "derived", "compound"],
        "semantic_categories": ["concrete", "abstract", "emotional", "technical"],
        "sampling_balance": 0.8
    },
    "generation_config": {
        "target_corpus_size": 3000000,
        "batch_size": 50,
        "quality_threshold": 0.7,
        "max_retries": 3
    }
}
```

#### 2. **Advanced State Manager** (`semantic_state.json`)
Enhanced state tracking for resumability and analysis:
```json
{
    "generation_progress": {
        "total_tokens": 0,
        "accepted_batches": 0,
        "rejected_batches": 0,
        "current_session": "session_20250907",
        "last_checkpoint": "2025-09-07T15:30:00Z"
    },
    "vocabulary_balance": {
        "target_categories": {...},
        "current_categories": {...},
        "completion_ratio": [...]
    },
    "semantic_history": {
        "word_vectors": {
            "circuit": [
                {"vector": [...], "context_snippet": "...", "timestamp": "..."},
                ...
            ]
        },
        "global_context_vectors": [...],
        "rejection_stats": {
            "too_similar": 0,
            "quality_low": 0,
            "frequency_imbalance": 0
        }
    }
}
```

#### 3. **Intelligent Embedding Engine**
```python
class EnhancedEmbeddingEngine:
    def __init__(self, config):
        self.fasttext_model = self.load_fasttext_model(config['model_path'])
        self.vector_cache = LRUCache(config['cache_size'])
        self.similarity_threshold = config['similarity_threshold']
    
    def get_document_embedding(self, text):
        """Get document-level embedding using TF-IDF weighted averaging"""
        
    def get_contextual_embedding(self, word, context, window_size=100):
        """Get word embedding in specific context"""
        
    def calculate_semantic_novelty(self, new_vector, history_vectors):
        """Calculate novelty score (0=identical, 1=completely novel)"""
        
    def find_optimal_contexts(self, word, candidate_texts, max_contexts=5):
        """Find most semantically diverse contexts for a word"""
```

#### 4. **Vocabulary-Stratified Sampling Module**
```python
class VocabularyStratifiedSampler:
    def __init__(self, ecp_words, subtlex_wordlist, config):
        # Use word lists but NOT frequency information
        self.vocabulary_pool = self.merge_wordlists(ecp_words, subtlex_wordlist)
        self.linguistic_strata = self.create_linguistic_strata(self.vocabulary_pool)
        self.current_balance = self.initialize_balance_tracker()
    
    def create_linguistic_strata(self, wordlist):
        """Stratify by linguistic features, NOT frequency"""
        strata = {
            'length': self.bin_by_length(wordlist),
            'pos': self.categorize_by_pos(wordlist), 
            'morphology': self.analyze_morphology(wordlist),
            'semantic': self.categorize_semantically(wordlist)
        }
        return strata
    
    def get_next_word_batch(self, batch_size=10):
        """Get linguistically-balanced sample (frequency-blind)"""
        
    def update_balance(self, generated_words):
        """Update linguistic balance after successful generation"""
        
    def get_undersampled_categories(self):
        """Identify linguistic categories that need more samples"""
```

#### 5. **Main Orchestration with Quality Control**
```python
class SemanticCorpusGenerator:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.embedding_engine = EnhancedEmbeddingEngine(self.config['embedding_config'])
        self.vocabulary_sampler = VocabularyStratifiedSampler(...)
        self.state_manager = AdvancedStateManager(...)
        
    def generate_corpus(self):
        """Main generation loop with vocabulary-blind sampling"""
        while not self.target_reached():
            # 1. Get linguistically-balanced word sample (NO frequency info used)
            word_batch = self.vocabulary_sampler.get_next_word_batch()
            
            # 2. Generate multiple candidate texts
            candidates = self.generate_candidate_texts(word_batch)
            
            # 3. Semantic quality filtering
            accepted_texts = self.filter_by_semantic_distinctiveness(candidates)
            
            # 4. Linguistic balance checking (NOT frequency balance)
            balanced_texts = self.ensure_linguistic_balance(accepted_texts)
            
            # 5. Save and update state
            self.save_accepted_texts(balanced_texts)
            self.update_state(balanced_texts)
```

## 📊 **Strategic Improvements Over Original Plan**

Perfect! I've created a comprehensive enhanced plan that addresses the key issues you identified from your notebook2 analysis. Here are the main improvements over the original plan:

## 🔄 **Key Strategic Changes**

### **🚨 CRITICAL: No Frequency Contamination**
- **Constraint**: Can sample from ECP/SUBTLEX **word lists** but CANNOT use their frequency information
- **Reason**: SUBTLEX frequencies are our **validation target** - using them would invalidate comparison
- **Solution**: Stratify by linguistic features (length, POS, morphology, semantics) instead of frequency

### **📝 Sampling Strategy Visualization:**
```
ECP/SUBTLEX Word Lists (frequency-blind sampling)
        ↓
Short words (1-4) ←→ Medium words (5-8) ←→ Long words (9+)
Nouns ←→ Verbs ←→ Adjectives ←→ Function words  
Simple ←→ Derived ←→ Compound morphology
Concrete ←→ Abstract ←→ Technical ←→ Emotional
        ↓
   LLM Generation
        ↓
Natural frequency emergence → Compare with SUBTLEX for validation
```

### **1. Vocabulary Sampling Without Frequency Contamination**
- **Problem**: Using SUBTLEX frequencies would contaminate our validation target
- **Solution**: **Vocabulary-Stratified Semantic Sampling** - sample from word lists using linguistic features only
- **Method**: Stratify by word length, POS, morphology, semantic categories (NOT frequency)
- **Benefit**: Unbiased frequency generation that can be validly compared against SUBTLEX

### **2. Multi-Level Semantic Filtering**
- **Document Level**: Overall semantic coherence and quality
- **Word Level**: Context distinctiveness for specific target words
- **Global Level**: Ensure corpus-wide semantic diversity
- **Temporal Level**: Track semantic drift over generation sessions

### **3. Quality Control Pipeline**
```python
def quality_control_pipeline(self, text, target_words):
    """Multi-stage quality assessment"""
    
    # Stage 1: Basic quality (grammar, coherence)
    basic_score = self.assess_basic_quality(text)
    if basic_score < self.config['quality_threshold']:
        return False, "basic_quality"
    
    # Stage 2: Semantic distinctiveness
    for word in target_words:
        novelty_score = self.assess_semantic_novelty(word, text)
        if novelty_score < self.config['min_novelty']:
            return False, f"semantic_similarity_{word}"
    
    # Stage 3: Linguistic balance impact  
    if self.would_imbalance_linguistic_categories(text, target_words):
        return False, "linguistic_balance"
    
    return True, "accepted"
```

### **4. Advanced Embedding Utilization**
- **FastText Integration**: Leverage pre-trained wiki-news-300d-1M vectors
- **Contextual Awareness**: Consider word context, not just isolated embeddings
- **Similarity Metrics**: Multiple similarity measures (cosine, Euclidean, custom weighted)
- **Vector Caching**: Efficient memory management for large-scale generation

## 🎯 **Implementation Roadmap**

### **Phase 1: Foundation Setup** (Days 1-2)
1. Create enhanced configuration system
2. Implement FastText embedding loader with caching
3. Build vocabulary analysis and linguistic stratification system
4. Set up advanced state management

### **Phase 2: Core Engine Development** (Days 3-4)
1. Develop EnhancedEmbeddingEngine with multiple similarity metrics
2. Build VocabularyStratifiedSampler with linguistic-based sampling  
3. Implement quality control pipeline
4. Create comprehensive logging and monitoring

### **Phase 3: Integration & Testing** (Days 5-6)
1. Integrate all components into main orchestration loop
2. Test with small-scale generation (10K tokens)
3. Validate linguistic balance and semantic diversity
4. Performance optimization and memory management

### **Phase 4: Production & Validation** (Days 7-8)
1. Large-scale corpus generation (1M+ tokens)
2. Validation against notebook2 analysis framework
3. Compare with existing LLM corpus results
4. Document and package final system

## 📈 **Expected Improvements**

### **Quantitative Targets**
- **Linguistic Balance**: <5% deviation from target distribution across all word categories
- **Semantic Diversity**: >0.65 average pairwise similarity score within word contexts
- **Quality Consistency**: >85% acceptance rate in quality control pipeline
- **Predictive Power**: Target >+1.0% variance improvement over current LLM corpus

### **Qualitative Benefits**
- **Balanced Representation**: Equal attention to different linguistic word categories
- **Research Validity**: No contamination from target frequency measures
- **Reproducibility**: Comprehensive state tracking and resumability
- **Scalability**: Efficient handling of large-scale generation

## 🔬 **Research Validation Strategy**

### **A/B Testing Framework**
1. **Baseline**: Current LLM corpus (shows +0.51% improvement)
2. **Enhanced**: Semantic distinctiveness corpus (target >+1.0% improvement)
3. **Metrics**: R² improvement in reading time prediction, correlation with human ratings

### **Comparative Analysis**
- **Vocabulary Coverage**: Compare word types covered vs. ECP/SUBTLEX vocabulary
- **Semantic Coherence**: Validate against human semantic judgments  
- **Psycholinguistic Validity**: Test with multiple behavioral datasets (ECP, BLP, ELP)
- **Frequency Independence**: Verify no correlation between sampling and SUBTLEX frequencies

## 🎛️ **Configuration Flexibility**

### **Tunable Parameters**
- **Similarity Threshold**: Adjust semantic distinctiveness requirement
- **Linguistic Balance**: Control how strictly to enforce vocabulary category distribution  
- **Quality Gates**: Set minimum quality thresholds at multiple stages
- **Batch Size**: Optimize for API efficiency vs. quality control

### **Research Adaptability**
- **Target Categories**: Easily switch between different linguistic stratification schemes
- **Embedding Models**: Support for different pre-trained vectors
- **Quality Metrics**: Pluggable quality assessment modules
- **Export Formats**: Multiple output formats for different research needs

---

## 🚀 **Implementation Priority**

**High Priority**: Vocabulary-stratified sampling and semantic distinctiveness core
**Medium Priority**: Advanced quality control and monitoring  
**Low Priority**: Multi-embedding support and research export tools

This enhanced plan addresses the key limitation (low-frequency word bias) while **avoiding frequency contamination** that would invalidate comparison with SUBTLEX. The vocabulary-stratified sampling approach should produce a corpus with better predictive power for human reading behavior while maintaining methodological rigor.

Would you like me to start implementing any specific component of this enhanced plan?
