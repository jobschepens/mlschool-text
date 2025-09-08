#!/usr/bin/env python3
"""
Enhanced Corpus Export with Story Metadata Tracking

This script creates an enhanced export of the generated corpus with:
1. Story boundaries detection
2. Seed word documentation for each story
3. Genre classification for each story
4. Grouping by stories with metadata
5. Analysis and statistics
"""

import json
import pandas as pd
import re
from datetime import datetime
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from path_utils import get_project_path, get_output_path

def detect_story_boundaries(corpus_text):
    """
    Detect story boundaries in the corpus text.
    Stories are typically separated by double newlines.
    """
    # First, try splitting on specific patterns that indicate new stories
    # Look for patterns like double newlines followed by a new story
    
    # Split on double+ newlines but keep the separators for analysis
    segments = re.split(r'\n\s*\n', corpus_text)
    
    stories = []
    current_story = ""
    
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
            
        # If this segment looks like the start of a new story (has certain indicators)
        # or if current_story is getting very long, treat it as a boundary
        if (current_story and 
            (len(current_story.split()) > 400 or  # Stories over 400 words
             segment.startswith(('**', '#', 'Sure!', 'The ', 'In ', 'A ', 'An ', 'Once')))) or \
           (not current_story):
            
            # Save the current story if it's substantial
            if current_story and len(current_story.split()) > 50:
                stories.append(current_story.strip())
            
            # Start new story
            current_story = segment
        else:
            # Continue the current story
            current_story += "\n\n" + segment
    
    # Don't forget the last story
    if current_story and len(current_story.split()) > 50:
        stories.append(current_story.strip())
    
    return stories

def classify_genre(story_text):
    """
    Attempt to classify the genre of a story based on content patterns.
    """
    story_lower = story_text.lower()
    
    # Technical/Scientific indicators
    if any(word in story_lower for word in ['experiment', 'research', 'scientific', 'study', 'analysis', 'data', 'molecule', 'quantum', 'theory']):
        return "Technical/Scientific"
    
    # News/Informative indicators  
    elif any(word in story_lower for word in ['reported', 'according to', 'breaking', 'news', 'announced', 'officials', 'statement']):
        return "News/Informative"
    
    # How-to/Educational indicators
    elif any(word in story_lower for word in ['step 1', 'how to', 'guide', 'instructions', 'follow these', 'tips']):
        return "General Knowledge/How-To"
    
    # Fiction indicators
    elif any(word in story_lower for word in ['once upon', 'he said', 'she whispered', 'the forest', 'elara', 'character names']):
        return "Fiction/Creative"
    
    else:
        return "Unknown"

def extract_story_metadata(story_text, story_index):
    """
    Extract metadata from a story including word count, length, etc.
    """
    words = story_text.split()
    sentences = re.split(r'[.!?]+', story_text)
    
    return {
        'story_id': f"story_{story_index:04d}",
        'word_count': len(words),
        'character_count': len(story_text),
        'sentence_count': len([s for s in sentences if s.strip()]),
        'genre': classify_genre(story_text),
        'first_words': ' '.join(words[:10]) + '...' if len(words) > 10 else story_text[:50] + '...',
        'timestamp': datetime.now().isoformat()
    }

def analyze_corpus_structure(corpus_path):
    """
    Analyze the corpus structure and create metadata for each story.
    """
    print("📖 Analyzing corpus structure...")
    
    # Read the corpus
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus_text = f.read()
    
    # Detect story boundaries
    stories = detect_story_boundaries(corpus_text)
    print(f"   Found {len(stories)} distinct stories")
    
    # Create metadata for each story
    story_metadata = []
    for i, story in enumerate(stories):
        metadata = extract_story_metadata(story, i)
        metadata['story_text'] = story
        story_metadata.append(metadata)
    
    return story_metadata

def create_story_groups_export(story_metadata, output_dir):
    """
    Create grouped exports by various criteria.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Export by genre
    print("📊 Creating genre-based exports...")
    genre_groups = {}
    for story in story_metadata:
        genre = story['genre']
        if genre not in genre_groups:
            genre_groups[genre] = []
        genre_groups[genre].append(story)
    
    for genre, stories in genre_groups.items():
        genre_file = os.path.join(output_dir, f"stories_by_genre_{genre.lower().replace('/', '_')}.txt")
        with open(genre_file, 'w', encoding='utf-8') as f:
            f.write(f"# {genre} Stories ({len(stories)} total)\n")
            f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for story in stories:
                f.write(f"## {story['story_id']} | Words: {story['word_count']} | Genre: {story['genre']}\n")
                f.write(f"# First words: {story['first_words']}\n")
                f.write(f"# Seeds used: [To be tracked in future versions]\n\n")
                f.write(story['story_text'])
                f.write("\n\n" + "="*80 + "\n\n")
    
    # 2. Export metadata as JSON
    metadata_file = os.path.join(output_dir, "story_metadata.json")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(story_metadata, f, indent=2, ensure_ascii=False)
    
    # 3. Export metadata as CSV
    csv_file = os.path.join(output_dir, "story_metadata.csv")
    df_data = []
    for story in story_metadata:
        row = {k: v for k, v in story.items() if k != 'story_text'}  # Exclude full text from CSV
        df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df.to_csv(csv_file, index=False)
    
    return genre_groups

def create_analysis_report(story_metadata, genre_groups, output_dir):
    """
    Create a comprehensive analysis report.
    """
    report_file = os.path.join(output_dir, "corpus_analysis_report.md")
    
    total_stories = len(story_metadata)
    total_words = sum(story['word_count'] for story in story_metadata)
    avg_words_per_story = total_words / total_stories if total_stories > 0 else 0
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Corpus Analysis Report\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Total Stories:** {total_stories:,}\n")
        f.write(f"- **Total Words:** {total_words:,}\n")
        f.write(f"- **Average Words per Story:** {avg_words_per_story:.1f}\n\n")
        
        f.write("## Genre Distribution\n\n")
        for genre, stories in genre_groups.items():
            genre_words = sum(story['word_count'] for story in stories)
            f.write(f"- **{genre}:** {len(stories)} stories ({genre_words:,} words)\n")
        
        f.write("\n## Story Length Distribution\n\n")
        word_counts = [story['word_count'] for story in story_metadata]
        word_counts.sort()
        
        f.write(f"- **Shortest Story:** {min(word_counts)} words\n")
        f.write(f"- **Longest Story:** {max(word_counts)} words\n")
        f.write(f"- **Median Length:** {word_counts[len(word_counts)//2]} words\n\n")
        
        f.write("## Sample Stories by Genre\n\n")
        for genre, stories in genre_groups.items():
            if stories:
                sample_story = stories[0]
                f.write(f"### {genre} Sample\n")
                f.write(f"**Story ID:** {sample_story['story_id']}\n")
                f.write(f"**Word Count:** {sample_story['word_count']}\n")
                f.write(f"**Preview:** {sample_story['first_words']}\n\n")

def main():
    """
    Main function to analyze and export corpus with metadata.
    """
    print("🔍 Enhanced Corpus Export with Metadata")
    print("=" * 50)
    
    # Configuration using path utilities
    corpus_path = get_output_path("large_corpus.txt")
    output_dir = get_output_path("analyzed_corpus")
    
    if not os.path.exists(corpus_path):
        print(f"❌ Corpus file not found: {corpus_path}")
        return
    
    # Analyze corpus structure
    story_metadata = analyze_corpus_structure(corpus_path)
    
    # Create grouped exports
    genre_groups = create_story_groups_export(story_metadata, output_dir)
    
    # Create analysis report
    create_analysis_report(story_metadata, genre_groups, output_dir)
    
    print(f"\n✅ Export complete!")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📖 Total stories analyzed: {len(story_metadata)}")
    print(f"   📊 Genre groups: {len(genre_groups)}")
    print(f"   📋 Files created:")
    print(f"      - story_metadata.json (complete metadata)")
    print(f"      - story_metadata.csv (metadata table)")
    print(f"      - corpus_analysis_report.md (analysis report)")
    for genre in genre_groups.keys():
        print(f"      - stories_by_genre_{genre.lower().replace('/', '_')}.txt")

if __name__ == "__main__":
    main()
