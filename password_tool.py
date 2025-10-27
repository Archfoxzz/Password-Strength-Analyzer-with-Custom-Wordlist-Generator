import argparse
import itertools
import math
import string
from zxcvbn import zxcvbn

# --- Password Analysis (Defensive Side) ---

def calculate_entropy(password):
    """Calculate password entropy in bits."""
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32
    
    if charset_size == 0:
        return 0
    
    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def analyze_password(password):
    """Analyzes password strength using zxcvbn and custom entropy calculations."""
    print("\n" + "="*60)
    print("           PASSWORD STRENGTH ANALYSIS")
    print("="*60)
    
    # Analyze the password
    results = zxcvbn(password)
    score = results['score']
    feedback = results['feedback']['suggestions']
    warning = results['feedback']['warning']
    crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
    
    # Custom entropy calculation
    entropy = calculate_entropy(password)

    # Determine status based on the zxcvbn score (0=Weak, 4=Strong)
    status_map = {
        0: ("VERY WEAK 🚨", "red"),
        1: ("WEAK 🚩", "red"),
        2: ("MODERATE 🤔", "yellow"),
        3: ("STRONG 💪", "green"),
        4: ("VERY STRONG 🛡️", "green")
    }
    status, _ = status_map.get(score, ("UNKNOWN", "gray"))

    print(f"\n📊 Password: {'*' * len(password)} (length: {len(password)})")
    print(f"🔐 Strength Score: {score}/4 - {status}")
    print(f"⏱️  Estimated Crack Time: {crack_time}")
    print(f"🎲 Entropy: {entropy} bits")
    
    # Character composition analysis
    print(f"\n🔤 Character Composition:")
    print(f"   • Lowercase: {'✓' if any(c.islower() for c in password) else '✗'}")
    print(f"   • Uppercase: {'✓' if any(c.isupper() for c in password) else '✗'}")
    print(f"   • Numbers: {'✓' if any(c.isdigit() for c in password) else '✗'}")
    print(f"   • Symbols: {'✓' if any(c in string.punctuation for c in password) else '✗'}")
    
    if warning:
        print(f"\n⚠️  Warning: {warning}")
    
    if feedback:
        print("\n💡 Suggestions to Improve:")
        for suggestion in feedback:
            print(f"   • {suggestion}")
    else:
        print("\n✅ Great job! No major suggestions needed.")
    
    # Additional recommendations based on entropy
    if entropy < 28:
        print("\n⚠️  Low Entropy Warning: Consider using a longer password with mixed character types.")
    
    print("\n" + "="*60 + "\n")

# --- Wordlist Generation (Offensive Side) ---

def apply_leet_speak(word):
    """Applies common leetspeak substitutions to a word."""
    leet_map = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7'],
        'l': ['1'],
        'g': ['9']
    }
    
    variations = [word]
    for char, replacements in leet_map.items():
        new_variations = []
        for variation in variations:
            for replacement in replacements:
                new_var = variation.replace(char, replacement)
                new_var_upper = variation.replace(char.upper(), replacement)
                if new_var != variation:
                    new_variations.append(new_var)
                if new_var_upper != variation:
                    new_variations.append(new_var_upper)
        variations.extend(new_variations)
    
    return list(set(variations))

def generate_wordlist(base_words, output_file="custom_wordlist.txt", max_combinations=50000):
    """
    Generates a comprehensive wordlist based on provided base words, including:
    - Capitalization variations
    - Leetspeak transformations
    - Common year/date suffixes
    - Number prefixes/suffixes
    - Common password patterns
    """
    print("\n" + "="*60)
    print("         CUSTOM WORDLIST GENERATOR")
    print("="*60)
    print(f"\n🔧 Base words provided: {', '.join(base_words)}")
    
    wordlist_set = set()
    
    # 1. Base words (all lowercase)
    for word in base_words:
        if word:
            wordlist_set.add(word.lower())
    
    # 2. Capitalization variations
    print("\n⚙️  Generating capitalization variations...")
    temp_list = list(wordlist_set)
    for word in temp_list:
        wordlist_set.add(word.capitalize())  # First letter capitalized
        wordlist_set.add(word.upper())       # ALL CAPS
        if len(word) > 1:
            wordlist_set.add(word[0].upper() + word[1:].lower())  # Title case

    # 3. Leetspeak variations
    print("⚙️  Applying leetspeak transformations...")
    leet_variations = set()
    for word in list(wordlist_set)[:100]:  # Limit to prevent explosion
        leet_vars = apply_leet_speak(word)
        leet_variations.update(leet_vars[:10])  # Limit variations per word
    wordlist_set.update(leet_variations)
    
    # 4. Common suffixes
    print("⚙️  Adding common suffixes...")
    years = [str(y) for y in range(1980, 2026)]
    common_numbers = ['1', '12', '123', '1234', '123456', '!', '!@', '!!', '@123']
    special_chars = ['!', '@', '#', '$', '!@', '123', '321']
    
    wordlist_with_suffixes = set()
    base_words_limited = list(wordlist_set)[:500]  # Limit to prevent massive expansion
    
    for word in base_words_limited:
        # Years
        for year in years:
            wordlist_with_suffixes.add(word + year)
            wordlist_with_suffixes.add(year + word)
        
        # Common numbers
        for num in common_numbers:
            wordlist_with_suffixes.add(word + num)
        
        # Special characters
        for char in special_chars:
            wordlist_with_suffixes.add(word + char)
    
    wordlist_set.update(wordlist_with_suffixes)
    
    # 5. Word combinations (for multiple base words)
    if len(base_words) > 1:
        print("⚙️  Creating word combinations...")
        for combo in itertools.permutations(base_words, 2):
            combined = ''.join(combo)
            wordlist_set.add(combined)
            wordlist_set.add(combined.capitalize())
            wordlist_set.add('_'.join(combo))
            wordlist_set.add('-'.join(combo))
    
    # Limit total size
    final_wordlist = sorted(list(wordlist_set))[:max_combinations]
    
    # Write to file
    with open(output_file, 'w') as f:
        for word in final_wordlist:
            f.write(f"{word}\n")

    # Calculate file size
    newline = '\n'
    file_content = newline.join(final_wordlist)
    file_size_kb = len(file_content) / 1024

    print(f"\n✅ Successfully generated {len(final_wordlist):,} unique passwords")
    print(f"📁 Wordlist saved to: {output_file}")
    print(f"📊 File size: {file_size_kb:.2f} KB")
    print("\n⚠️  ETHICAL USE ONLY: Use this list for authorized security testing only.")
    print("="*60 + "\n")

# --- Interactive Menu ---

def show_interactive_menu():
    """Display an interactive menu when no arguments are provided."""
    while True:
        print("\n" + "="*60)
        print("           PASSWORD SECURITY TOOL")
        print("="*60)
        print("\n  1. Launch GUI Mode")
        print("  2. Analyze a Password")
        print("  3. Generate Custom Wordlist")
        print("  4. Exit")
        print("\n" + "="*60)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            launch_gui()
            break
        elif choice == "2":
            password = input("\nEnter password to analyze: ")
            analyze_password(password)
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("\n--- Wordlist Generator ---")
            name = input("Enter name/nickname (or press Enter to skip): ").strip()
            pet = input("Enter pet name (or press Enter to skip): ").strip()
            date = input("Enter important date (or press Enter to skip): ").strip()
            output = input("Enter output filename (default: custom_wordlist.txt): ").strip()
            
            if not output:
                output = "custom_wordlist.txt"
            
            base_words = [w for w in [name, pet, date] if w]
            
            if not base_words:
                print("❌ Error: Please provide at least one input.")
                input("\nPress Enter to continue...")
            else:
                generate_wordlist(base_words, output)
                input("\nPress Enter to continue...")
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")
            input("\nPress Enter to continue...")

# --- GUI Mode (Basic Tkinter Interface) ---

def launch_gui():
    """Launch a simple GUI interface for the tool."""
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext, messagebox, filedialog
    except ImportError:
        print("❌ Error: tkinter is not available. Please use CLI mode.")
        return
    
    def analyze_gui():
        password = password_entry.get()
        if not password:
            messagebox.showwarning("Input Required", "Please enter a password to analyze.")
            return
        
        output_text.delete(1.0, tk.END)
        
        # Capture analysis output
        results = zxcvbn(password)
        score = results['score']
        crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
        entropy = calculate_entropy(password)
        
        output = f"Password Length: {len(password)}\n"
        output += f"Strength Score: {score}/4\n"
        output += f"Crack Time: {crack_time}\n"
        output += f"Entropy: {entropy} bits\n\n"
        
        if results['feedback']['warning']:
            output += f"Warning: {results['feedback']['warning']}\n\n"
        
        if results['feedback']['suggestions']:
            output += "Suggestions:\n"
            for suggestion in results['feedback']['suggestions']:
                output += f"  • {suggestion}\n"
        
        output_text.insert(1.0, output)
    
    def generate_gui():
        name = name_entry.get()
        pet = pet_entry.get()
        date = date_entry.get()
        
        base_words = [w.strip() for w in [name, pet, date] if w.strip()]
        
        if not base_words:
            messagebox.showwarning("Input Required", "Please provide at least one input.")
            return
        
        output_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if output_file:
            generate_wordlist(base_words, output_file)
            messagebox.showinfo("Success", f"Wordlist generated successfully!\nSaved to: {output_file}")
    
    # Create main window
    root = tk.Tk()
    root.title("Password Security Tool")
    root.geometry("600x500")
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # --- Analyzer Tab ---
    analyzer_frame = ttk.Frame(notebook)
    notebook.add(analyzer_frame, text="Analyze Password")
    
    ttk.Label(analyzer_frame, text="Enter Password:", font=('Arial', 12)).pack(pady=10)
    password_entry = ttk.Entry(analyzer_frame, width=50, show="*")
    password_entry.pack(pady=5)
    
    show_password_var = tk.BooleanVar()
    def toggle_password():
        password_entry.config(show="" if show_password_var.get() else "*")
    
    ttk.Checkbutton(analyzer_frame, text="Show Password", variable=show_password_var, 
                    command=toggle_password).pack(pady=5)
    
    ttk.Button(analyzer_frame, text="Analyze", command=analyze_gui).pack(pady=10)
    
    output_text = scrolledtext.ScrolledText(analyzer_frame, width=70, height=15)
    output_text.pack(pady=10)
    
    # --- Generator Tab ---
    generator_frame = ttk.Frame(notebook)
    notebook.add(generator_frame, text="Generate Wordlist")
    
    ttk.Label(generator_frame, text="Base Word Inputs:", font=('Arial', 12, 'bold')).pack(pady=10)
    
    ttk.Label(generator_frame, text="Name/Nickname:").pack()
    name_entry = ttk.Entry(generator_frame, width=40)
    name_entry.pack(pady=5)
    
    ttk.Label(generator_frame, text="Pet Name:").pack()
    pet_entry = ttk.Entry(generator_frame, width=40)
    pet_entry.pack(pady=5)
    
    ttk.Label(generator_frame, text="Important Date:").pack()
    date_entry = ttk.Entry(generator_frame, width=40)
    date_entry.pack(pady=5)
    
    ttk.Button(generator_frame, text="Generate Wordlist", command=generate_gui).pack(pady=20)
    
    ttk.Label(generator_frame, text="⚠️ For authorized security testing only", 
              foreground="red").pack(pady=10)
    
    root.mainloop()

# --- Main Entry Point (CLI) ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Password Security Tool: Analyze strength or generate custom wordlists.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Add GUI mode flag
    parser.add_argument('--gui', action='store_true', help='Launch GUI interface')
    
    # Subparsers for the two different modes
    subparsers = parser.add_subparsers(dest='command')

    # --- Analyzer Mode ---
    analyze_parser = subparsers.add_parser('analyze', help='Analyze the strength of a given password.')
    analyze_parser.add_argument('password', type=str, help='The password string to analyze.')

    # --- Generator Mode ---
    generate_parser = subparsers.add_parser('generate', help='Generate a custom wordlist based on personal inputs.')
    generate_parser.add_argument('--name', type=str, default="", help='User name or nickname.')
    generate_parser.add_argument('--pet', type=str, default="", help='Pet name.')
    generate_parser.add_argument('--date', type=str, default="", help='Important date (e.g., a birthday).')
    generate_parser.add_argument('--output', type=str, default="custom_wordlist.txt", help='Output file name.')
    generate_parser.add_argument('--max', type=int, default=50000, help='Maximum wordlist size.')

    # If no arguments provided, show interactive menu
    import sys
    if len(sys.argv) == 1:
        show_interactive_menu()
    else:
        args = parser.parse_args()

        # GUI mode
        if args.gui:
            launch_gui()
        elif args.command == 'analyze':
            analyze_password(args.password)
        elif args.command == 'generate':
            inputs = [args.name, args.pet, args.date]
            base_words = [item.strip() for item in inputs if item.strip()]
            
            if not base_words:
                print("❌ Error: Please provide at least one input (--name, --pet, or --date).")
            else:
                generate_wordlist(base_words, args.output, args.max)
        else:
            parser.print_help()