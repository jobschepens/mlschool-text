"""
Cross-platform path utilities for the mlschool-text project.

This module provides functions to correctly resolve file paths regardless of
the execution environment (Colab, Binder, local development, etc.).

Usage:
    from path_utils import get_project_path, get_output_path
    
    # Load a config file
    config_path = get_project_path('models.json')
    
    # Save to output directory  
    output_path = get_output_path('results.csv')
"""

import os


def get_project_path(relative_path: str) -> str:
    """
    Get the correct path to project files regardless of working directory.
    
    This function handles different execution contexts:
    - Local development (from notebooks/ subdirectory)
    - Colab (from project root after cloning)
    - Binder (from project root)
    - Scripts (from scripts/ subdirectory)
    
    Args:
        relative_path (str): Path relative to project root (e.g., 'models.json', 'data/file.csv')
    
    Returns:
        str: Absolute path to the file
    """
    # If we're already in the project root, use the path directly
    if os.path.exists(relative_path):
        return relative_path
    
    # If we're in notebooks/ subdirectory, go up one level
    parent_path = os.path.join('..', relative_path)
    if os.path.exists(parent_path):
        return parent_path
    
    # If we're in scripts/ subdirectory, go up one level
    if os.getcwd().endswith('scripts'):
        parent_path = os.path.join('..', relative_path)
        if os.path.exists(parent_path):
            return parent_path
    
    # If we're in a cloned repo (like in Colab), try mlschool-text/ prefix
    colab_path = os.path.join('mlschool-text', relative_path)
    if os.path.exists(colab_path):
        return colab_path
    
    # Fallback to original path (will give clear error if file doesn't exist)
    return relative_path


def get_output_path(filename: str) -> str:
    """
    Get the correct path for output files (creates directory if needed).
    
    Args:
        filename (str): Output filename (e.g., 'corpus.txt', 'predictors.csv')
    
    Returns:
        str: Full path to output file
    """
    output_dir = get_project_path('output')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    return os.path.join(output_dir, filename)


def get_data_path(filename: str) -> str:
    """
    Get the correct path for data files.
    
    Args:
        filename (str): Data filename (e.g., 'file.csv', 'subdir/file.txt')
    
    Returns:
        str: Full path to data file
    """
    return get_project_path(os.path.join('data', filename))


def get_scripts_path(filename: str) -> str:
    """
    Get the correct path for script files.
    
    Args:
        filename (str): Script filename (e.g., 'config.json')
    
    Returns:
        str: Full path to script file
    """
    return get_project_path(os.path.join('scripts', filename))


def check_file_access(file_list: list) -> bool:
    """
    Check if a list of files are accessible and show their paths.
    
    Args:
        file_list (list): List of relative paths to check
        
    Returns:
        bool: True if all files are accessible
    """
    print("📁 File accessibility check:")
    all_good = True
    
    for file_path in file_list:
        full_path = get_project_path(file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}: {full_path}")
        else:
            print(f"   ❌ {file_path}: {full_path} (not found)")
            all_good = False
    
    return all_good
