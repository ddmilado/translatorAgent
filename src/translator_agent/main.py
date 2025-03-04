#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
import argparse

from translator_agent.crew import TranslationCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the translation crew with file input.
    """
    parser = argparse.ArgumentParser(description='Translate a file from one language to another')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the file to translate')
    parser.add_argument('--source_language', type=str, required=True, help='Source language of the file')
    parser.add_argument('--target_language', type=str, required=True, help='Target language for translation')
    parser.add_argument('--topic', type=str, default='General', help='Subject matter of the text')
    parser.add_argument('--output_file', type=str, help='Path to save the translated file (default: auto-generated name)')
    
    args = parser.parse_args(sys.argv[1:])
    
    # Verify file exists
    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file not found: {args.input_file}")
    
    # Read the source file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source_text = f.read()
    except Exception as e:
        raise Exception(f"Error reading source file: {e}")
    
    # Generate output filename if not provided
    if not args.output_file:
        file_base = os.path.splitext(os.path.basename(args.input_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_file = f"{file_base}_{args.target_language}_{timestamp}.txt"
    
    inputs = {
        'source_text': source_text,
        'source_language': args.source_language,
        'target_language': args.target_language,
        'topic': source_text,
        'current_year': str(datetime.now().year)
    }
    
    print(f"Starting translation from {args.source_language} to {args.target_language}...")
    print(f"File: {args.input_file}")
    print(f"Topic: {args.topic}")
    
    try:
        result = TranslationCrew().crew().kickoff(inputs=inputs)
        
        # Extract the string content from CrewOutput
        if hasattr(result, 'output'):
            result_text = result.output
        elif hasattr(result, 'value'):
            result_text = result.value
        else:
            result_text = str(result)
        
        # Write the translation to the output file
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(result_text)
        
        print(f"\nTranslation complete! Saved to: {args.output_file}")
        
    except Exception as e:
        raise Exception(f"An error occurred during translation: {e}")

def batch_translate():
    """
    Translate multiple files in a directory.
    """
    parser = argparse.ArgumentParser(description='Batch translate files from a directory')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing files to translate')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save translated files')
    parser.add_argument('--source_language', type=str, required=True, help='Source language of all files')
    parser.add_argument('--target_language', type=str, required=True, help='Target language for translation')
    parser.add_argument('--file_ext', type=str, default='.txt', help='File extension to process (default: .txt)')
    parser.add_argument('--topic', type=str, default='General', help='Subject matter of the texts')
    
    args = parser.parse_args(sys.argv[1:])
    
    # Verify directories exist
    if not os.path.isdir(args.input_dir):
        raise NotADirectoryError(f"Input directory not found: {args.input_dir}")
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get list of files to translate
    files_to_translate = [f for f in os.listdir(args.input_dir) 
                         if f.endswith(args.file_ext) and os.path.isfile(os.path.join(args.input_dir, f))]
    
    if not files_to_translate:
        print(f"No {args.file_ext} files found in {args.input_dir}")
        return
    
    print(f"Found {len(files_to_translate)} files to translate from {args.source_language} to {args.target_language}")
    
    for i, filename in enumerate(files_to_translate):
        input_path = os.path.join(args.input_dir, filename)
        output_filename = f"{os.path.splitext(filename)[0]}_{args.target_language}.txt"
        output_path = os.path.join(args.output_dir, output_filename)
        
        print(f"\nTranslating file {i+1}/{len(files_to_translate)}: {filename}")
        
        try:
            # Read source file
            with open(input_path, 'r', encoding='utf-8') as f:
                source_text = f.read()
            
            inputs = {
                'source_text': source_text,
                'source_language': args.source_language,
                'target_language': args.target_language,
                'topic': args.topic,
                'current_year': str(datetime.now().year)
            }
            
            result = TranslationCrew().crew().kickoff(inputs=inputs)
            
            # Extract the string content from CrewOutput
            if hasattr(result, 'output'):
                result_text = result.output
            elif hasattr(result, 'value'):
                result_text = result.value
            else:
                result_text = str(result)
            
            # Write translation to output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result_text)
            
            print(f"Saved translation to: {output_path}")
            
        except Exception as e:
            print(f"Error translating {filename}: {e}")
    
    print("\nBatch translation complete!")

def train():
    """
    Train the translation crew for a given number of iterations.
    """
    parser = argparse.ArgumentParser(description='Train translation crew')
    parser.add_argument('iterations', type=int, help='Number of training iterations')
    parser.add_argument('filename', type=str, help='Filename to save training data')
    parser.add_argument('--source_language', type=str, default='English', help='Source language')
    parser.add_argument('--target_language', type=str, default='Spanish', help='Target language')
    
    args = parser.parse_args(sys.argv[1:])
    
    inputs = {
        'source_text': 'This is a sample text for training purposes.',
        'source_language': args.source_language,
        'target_language': args.target_language,
        'topic': 'Training'
    }
    
    try:
        TranslationCrew().crew().train(
            n_iterations=args.iterations, 
            filename=args.filename, 
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the translation crew: {e}")

def replay():
    """
    Replay the translation crew execution from a specific task.
    """
    parser = argparse.ArgumentParser(description='Replay a specific task')
    parser.add_argument('task_id', type=str, help='ID of task to replay')
    
    args = parser.parse_args(sys.argv[1:])
    
    try:
        TranslationCrew().crew().replay(task_id=args.task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the translation crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [translate|batch|train|replay] [options]")
        print("\nCommands:")
        print("  translate  - Translate a single file")
        print("  batch      - Translate multiple files from a directory")
        print("  train      - Train the translation crew")
        print("  replay     - Replay a specific task")
        print("\nFor command-specific help, use: python main.py [command] --help")
        sys.exit(1)
        
    command = sys.argv[1]
    sys.argv = sys.argv[1:]  # Shift arguments
    
    if command == "translate":
        run()
    elif command == "batch":
        batch_translate()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    else:
        print(f"Unknown command: {command}")
        print("Use: python main.py --help for available commands")