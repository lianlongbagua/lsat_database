import json
import os
import subprocess
import tempfile
import shutil

# Path to the data file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'lr_metadata_enriched.json')

def load_data():
    """Load the JSON data from the file."""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DATA_PATH}")
        return None

def save_data(data):
    """Save the JSON data back to the file."""
    # Create a backup first
    backup_path = DATA_PATH + '.bak'
    try:
        shutil.copy2(DATA_PATH, backup_path)
        print(f"Backup created at {backup_path}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Data saved successfully.")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def open_in_editor(text, is_json=False):
    """Open text in Notepad and return the edited text."""
    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.json' if is_json else '.txt', text=True)
    try:
        # Write the initial text to the file
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Open Notepad and wait for it to close
        print("Opening Notepad. Make your edits, save, and close Notepad to continue...")
        subprocess.run(['notepad.exe', temp_path], check=True)
        
        # Read the edited text back
        with open(temp_path, 'r', encoding='utf-8') as f:
            edited_text = f.read()
            
        return edited_text
    finally:
        # Clean up the temporary file
        try:
            os.remove(temp_path)
        except OSError:
            pass

def print_question_summary(q_id, q_data):
    """Print a summary of the question data."""
    print(f"\n--- Question: {q_id} ---")
    print(f"Task Code: {q_data.get('task_code', 'N/A')}")
    print(f"Engine Code: {q_data.get('engine_code', 'N/A')}")
    print(f"Difficulty: {q_data.get('difficulty', 'N/A')}")
    print(f"Answer: {q_data.get('answer', 'N/A')}")
    
    stimulus = q_data.get('stimulus', '')
    if len(stimulus) > 100:
        print(f"Stimulus: {stimulus[:97]}...")
    else:
        print(f"Stimulus: {stimulus}")
        
    print("-" * 30)

def search_questions(data, query):
    """Search for questions by ID or text."""
    results = []
    query_lower = query.lower()
    
    # Check for exact ID match first
    if query in data:
        return [query]
        
    for q_id, q_data in data.items():
        if query_lower in q_id.lower():
            results.append(q_id)
            continue
            
        # Search in text fields if not found in ID
        text_fields = ['stimulus', 'stem', 'text']
        for field in text_fields:
            if field in q_data and isinstance(q_data[field], str):
                if query_lower in q_data[field].lower():
                    results.append(q_id)
                    break # Found in this question, move to next
    
    return results

def edit_field(q_data, field_path):
    """Edit a specific field in the question data."""
    parts = field_path.split('.')
    current = q_data
    
    # Navigate to the correct parent dictionary
    for part in parts[:-1]:
        if part not in current:
             print(f"Error: Path {'.'.join(parts[:-1])} not found.")
             return False
        current = current[part]
        
    final_field = parts[-1]
    
    if final_field not in current and len(parts) > 1:
        # It's an optional sub-field that might not exist yet
         print(f"Field {final_field} doesn't exist yet. Creating it.")
         current[final_field] = ""
    elif final_field not in current:
        print(f"Error: Field {final_field} not found.")
        return False
        
    current_value = current[final_field]
    
    if isinstance(current_value, str):
        print(f"\nEditing: {field_path}")
        new_value = open_in_editor(current_value)
        # Strip trailing newlines that editors often add
        new_value = new_value.strip()
        
        if new_value != current_value.strip():
            print(f"Field '{field_path}' updated.")
            current[final_field] = new_value
            return True
        else:
            print("No changes made.")
            return False
            
    elif isinstance(current_value, dict) or isinstance(current_value, list):
         print(f"\nEditing JSON structure: {field_path}")
         current_json = json.dumps(current_value, indent=2, ensure_ascii=False)
         new_json_str = open_in_editor(current_json, is_json=True)
         
         try:
             new_value = json.loads(new_json_str)
             if current_json != json.dumps(new_value, indent=2, ensure_ascii=False):
                  print(f"Structure '{field_path}' updated.")
                  current[final_field] = new_value
                  return True
             else:
                  print("No changes made.")
                  return False
         except json.JSONDecodeError as e:
             print(f"Error: Invalid JSON provided. Changes discarded. Details: {e}")
             return False
    else:
        # For simple types like ints, use standard input
        print(f"\nCurrent value of {field_path}: {current_value} (Type: {type(current_value).__name__})")
        new_input = input("Enter new value (or press Enter to keep current): ")
        if not new_input.strip():
            print("No changes made.")
            return False
            
        try:
            # Try to cast to the original type
            if isinstance(current_value, int):
                new_value = int(new_input)
            elif isinstance(current_value, bool):
                new_value = new_input.lower() in ('true', 'yes', '1', 'y')
            else:
                new_value = new_input
                
            current[final_field] = new_value
            print(f"Field '{field_path}' updated.")
            return True
        except ValueError:
            print(f"Error: Invalid value format. Expected {type(current_value).__name__}.")
            return False

def interactive_edit(q_id, q_data):
    """Interactive loop for editing a specific question."""
    changes_made = False
    
    while True:
        print_question_summary(q_id, q_data)
        print("Fields available to edit:")
        print("1. stimulus")
        print("2. stem")
        print("3. choices (all as JSON)")
        print("4. answer")
        print("5. task_code")
        print("6. engine_code")
        print("7. difficulty")
        print("8. canonical_explanation.analysis")
        print("9. canonical_explanation.choices (as JSON)")
        print("10. reasoning")
        print("11. raw text (full original text block)")
        print("0. Return to search menu")
        
        choice = input("\nSelect a field to edit (0-11): ").strip()
        
        field_mapping = {
            '1': 'stimulus',
            '2': 'stem',
            '3': 'choices',
            '4': 'answer',
            '5': 'task_code',
            '6': 'engine_code',
            '7': 'difficulty',
            '8': 'canonical_explanation.analysis',
            '9': 'canonical_explanation.choices',
            '10': 'reasoning',
            '11': 'text'
        }
        
        if choice == '0':
            break
        elif choice in field_mapping:
            field_path = field_mapping[choice]
            if edit_field(q_data, field_path):
                changes_made = True
        else:
            print("Invalid choice. Please try again.")
            
    return changes_made

def main():
    print("Loading database...")
    data = load_data()
    if not data:
         return
         
    print(f"Successfully loaded {len(data)} questions.")
    
    unsaved_changes = False
    
    try:
        while True:
            if unsaved_changes:
                print("\n*** YOU HAVE UNSAVED CHANGES ***")
                
            print("\nMain Menu:")
            print("1. Search for a question")
            print("2. Save changes")
            print("3. Exit")
            
            choice = input("Select an option: ").strip()
            
            if choice == '1':
                query = input("\nEnter Question ID or search term: ").strip()
                if not query:
                    continue
                    
                results = search_questions(data, query)
                
                if not results:
                    print("No questions found matching your query.")
                elif len(results) == 1:
                    print("Found 1 match.")
                    q_id = results[0]
                    if interactive_edit(q_id, data[q_id]):
                        unsaved_changes = True
                else:
                    print(f"Found {len(results)} matches.")
                    # Cap display to 20 results to avoid terminal spam
                    display_limit = min(20, len(results))
                    for i, q_id in enumerate(results[:display_limit]):
                        print(f"{i+1}. {q_id}")
                    if len(results) > 20:
                        print(f"... and {len(results) - 20} more.")
                        
                    selection = input(f"\nSelect a number (1-{display_limit}) to edit, or 0 to cancel: ").strip()
                    try:
                        idx = int(selection) - 1
                        if 0 <= idx < display_limit:
                            q_id = results[idx]
                            if interactive_edit(q_id, data[q_id]):
                                unsaved_changes = True
                    except ValueError:
                        print("Invalid selection.")
                        
            elif choice == '2':
                if unsaved_changes:
                    if save_data(data):
                        unsaved_changes = False
                else:
                    print("No changes to save.")
                    
            elif choice == '3':
                if unsaved_changes:
                    confirm = input("You have unsaved changes. Are you sure you want to exit without saving? (y/n): ").strip().lower()
                    if confirm != 'y':
                        continue
                print("Exiting Question Editor.")
                break
            else:
                print("Invalid choice.")
                
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
        if unsaved_changes:
             print("WARNING: You had unsaved changes.")
             
if __name__ == "__main__":
    main()
