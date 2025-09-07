import json

# Read the notebook file
with open('notebooks/test.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Go through each cell in the notebook
for cell in notebook['cells']:
    # Check if the cell is a code cell
    if cell['cell_type'] == 'code':
        # Go through each line in the cell's source
        for i, line in enumerate(cell['source']):
            # Fix the first occurrence of the division by zero error
            if 'print(f"  • Corpus/Types ratio: {llm_corpus_millions/llm_types_millions:.1f}")' in line:
                cell['source'][i] = '    if llm_types_millions > 0:\n'
                cell['source'].insert(i+1, '        print(f"  • Corpus/Types ratio: {llm_corpus_millions/llm_types_millions:.1f}")\n')
                cell['source'].insert(i+2, '    else:\n')
                cell['source'].insert(i+3, '        print(f"  • Corpus/Types ratio: undefined (no unique words found)")\n')
            
            # Fix the second occurrence of the division by zero error
            elif 'print(f"  LLM Corpus/Types ratio: {llm_corpus_millions/llm_types_millions:.1f}")' in line:
                cell['source'][i] = '    if llm_types_millions > 0:\n'
                cell['source'].insert(i+1, '        print(f"  LLM Corpus/Types ratio: {llm_corpus_millions/llm_types_millions:.1f}")\n')
                cell['source'].insert(i+2, '    else:\n')
                cell['source'].insert(i+3, '        print(f"  LLM Corpus/Types ratio: undefined (no unique words found)")\n')
            
            # Fix the third occurrence of the division by zero error
            elif 'print(f"  SUBTLEX ratio is {(subtlex_corpus_millions/subtlex_types_millions) / (llm_corpus_millions/llm_types_millions):.0f}x larger!")' in line:
                cell['source'][i] = '    if llm_types_millions > 0 and (llm_corpus_millions/llm_types_millions) > 0:\n'
                cell['source'].insert(i+1, '        print(f"  SUBTLEX ratio is {(subtlex_corpus_millions/subtlex_types_millions) / (llm_corpus_millions/llm_types_millions):.0f}x larger!")\n')
                cell['source'].insert(i+2, '    else:\n')
                cell['source'].insert(i+3, '        print(f"  SUBTLEX ratio comparison: undefined (no unique words in LLM corpus)")\n')

# Write the modified notebook back to file
with open('notebooks/test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)