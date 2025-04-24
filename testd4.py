import random
import os
import sys
import time
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font as tkFont # Import font module

# --- Colorama Setup (CLI Colors) ---
try:
    import colorama
    colorama.init(autoreset=True) # Automatically reset style after each print
    # Define a richer color palette using colorama styles
    C = {
        "reset": colorama.Style.RESET_ALL,
        "bold": colorama.Style.BRIGHT,
        "dim": colorama.Style.DIM,
        # Foreground Colors
        "fg_black": colorama.Fore.BLACK,
        "fg_red": colorama.Fore.RED,
        "fg_green": colorama.Fore.GREEN,
        "fg_yellow": colorama.Fore.YELLOW,
        "fg_blue": colorama.Fore.BLUE,
        "fg_magenta": colorama.Fore.MAGENTA,
        "fg_cyan": colorama.Fore.CYAN,
        "fg_white": colorama.Fore.WHITE,
        "fg_lightblack_ex": colorama.Fore.LIGHTBLACK_EX, # Grey
        # Bright Foreground Colors
        "fg_bright_red": colorama.Fore.LIGHTRED_EX,
        "fg_bright_green": colorama.Fore.LIGHTGREEN_EX,
        "fg_bright_yellow": colorama.Fore.LIGHTYELLOW_EX,
        "fg_bright_blue": colorama.Fore.LIGHTBLUE_EX,
        "fg_bright_magenta": colorama.Fore.LIGHTMAGENTA_EX,
        "fg_bright_cyan": colorama.Fore.LIGHTCYAN_EX,
        "fg_bright_white": colorama.Fore.LIGHTWHITE_EX,
        # Background Colors (Use sparingly)
        "bg_red": colorama.Back.RED,
        "bg_green": colorama.Back.GREEN,
        "bg_yellow": colorama.Back.YELLOW,
        "bg_blue": colorama.Back.BLUE,
        "bg_magenta": colorama.Back.MAGENTA,
        "bg_cyan": colorama.Back.CYAN,
        "bg_white": colorama.Back.WHITE,
    }
    # Define semantic colors using the palette
    COLOR_QUESTION = C["fg_bright_cyan"] + C["bold"]
    COLOR_OPTIONS = C["fg_white"]
    COLOR_OPTION_NUM = C["fg_yellow"] + C["bold"]
    COLOR_CATEGORY = C["fg_bright_yellow"] + C["bold"]
    COLOR_CORRECT = C["fg_bright_green"] + C["bold"]
    COLOR_INCORRECT = C["fg_bright_red"] + C["bold"]
    COLOR_EXPLANATION = C["fg_lightblack_ex"] # Grey
    COLOR_PROMPT = C["fg_bright_magenta"] + C["bold"]
    COLOR_HEADER = C["fg_bright_blue"] + C["bold"]
    COLOR_SUBHEADER = C["fg_blue"] + C["bold"]
    COLOR_STATS_LABEL = C["fg_white"]
    COLOR_STATS_VALUE = C["fg_bright_yellow"]
    COLOR_STATS_ACC_GOOD = C["fg_bright_green"]
    COLOR_STATS_ACC_AVG = C["fg_yellow"]
    COLOR_STATS_ACC_BAD = C["fg_bright_red"]
    COLOR_BORDER = C["fg_blue"]
    COLOR_INPUT = C["fg_bright_white"]
    COLOR_ERROR = C["fg_white"] + C["bg_red"] + C["bold"]
    # Adjusted COLOR_WARNING: Bold yellow text, no background
    COLOR_WARNING = C["fg_bright_yellow"] + C["bold"]
    COLOR_INFO = C["fg_bright_cyan"]
    COLOR_RESET = C["reset"]
except ImportError:
    print("Warning: Colorama not found. Colored output will be disabled in CLI.")
    # Define empty strings if colorama is not available
    C = {k: "" for k in ["reset", "bold", "dim", "fg_black", "fg_red", "fg_green", "fg_yellow", "fg_blue", "fg_magenta", "fg_cyan", "fg_white", "fg_lightblack_ex", "fg_bright_red", "fg_bright_green", "fg_bright_yellow", "fg_bright_blue", "fg_bright_magenta", "fg_bright_cyan", "fg_bright_white", "bg_red", "bg_green", "bg_yellow", "bg_blue", "bg_magenta", "bg_cyan", "bg_white"]}
    COLOR_QUESTION = ""
    COLOR_OPTIONS = ""
    COLOR_OPTION_NUM = ""
    COLOR_CATEGORY = ""
    COLOR_CORRECT = ""
    COLOR_INCORRECT = ""
    COLOR_EXPLANATION = ""
    COLOR_PROMPT = ""
    COLOR_HEADER = ""
    COLOR_SUBHEADER = ""
    COLOR_STATS_LABEL = ""
    COLOR_STATS_VALUE = ""
    COLOR_STATS_ACC_GOOD = ""
    COLOR_STATS_ACC_AVG = ""
    COLOR_STATS_ACC_BAD = ""
    COLOR_BORDER = ""
    COLOR_INPUT = ""
    COLOR_ERROR = ""
    COLOR_WARNING = ""
    COLOR_INFO = ""
    COLOR_RESET = ""

# --- CLI Helper Functions ---
def cli_print_separator(char='-', length=60, color=COLOR_BORDER):
    """Prints a colored separator line."""
    print(f"{color}{char * length}{COLOR_RESET}")

def cli_print_header(text, char='=', length=60, color=COLOR_HEADER):
    """Prints a centered header with separators."""
    padding = (length - len(text) - 2) // 2
    print(f"{color}{char * padding} {text} {char * (length - len(text) - 2 - padding)}{COLOR_RESET}")

# --- CLI Game Class ---
class LinuxPlusStudyGame:
    """Handles the logic and Command-Line Interface for the study game."""
    def __init__(self):
        self.questions = []
        self.score = 0
        self.total_questions_session = 0 # Track questions in the current session
        self.categories = set()
        self.answered_indices_session = []  # Track answered question indices in this session
        self.history_file = "linux_plus_history.json"
        self.study_history = self.load_history()
        self.load_questions() # Load questions after initializing history

    def _default_history(self):
        """Returns the default structure for study history."""
        return {
            "sessions": [],
            "questions": {},
            "categories": {},
            "total_correct": 0,
            "total_attempts": 0
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_history(self):
        """Load study history from file if it exists."""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                default = self._default_history()
                for key in default:
                    history.setdefault(key, default[key])
                if not isinstance(history.get("questions"), dict): history["questions"] = {}
                if not isinstance(history.get("categories"), dict): history["categories"] = {}
                if not isinstance(history.get("sessions"), list): history["sessions"] = []
                return history
        except (FileNotFoundError, json.JSONDecodeError):
            # Use COLOR_INFO for non-critical warnings
            print(f"{COLOR_INFO} History file not found or invalid. Starting fresh. {COLOR_RESET}")
            return self._default_history()

    def save_history(self):
        """Save study history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.study_history, f, indent=2)
        except IOError as e:
            print(f"{COLOR_ERROR} Error saving history: {e} {COLOR_RESET}")

    def load_questions(self):
        """Load sample Linux+ questions, commands, and definitions."""
        # --- Existing Questions (Truncated for brevity) ---
        existing_questions = [
            (
                "A system administrator notices that a production server is experiencing significant slowdowns. Upon further investigation using the top command, it's observed that the I/O wait percentage is consistently above 30%. Considering that the server's disk activity is not excessively high, what could be a probable cause for the high I/O wait?",
                [
                    "The hard drive is failing, causing read/write operations to take longer than usual.",
                    "A misconfigured network firewall is limiting incoming connections.",
                    "The I/O scheduler is configured for a single-threaded process, leading to a bottleneck.",
                    "Insufficient memory available for buffer/cache leading to frequent disk access."
                ],
                3,
                "Troubleshooting",
                "Having insufficient memory available for buffer/cache can lead to high I/O wait times because the system has to commit to disk I/O more frequently than if it had enough memory to cache operations. This leads to higher wait times as processes are queued while the I/O bottleneck is resolved. Optimizing memory usage or adding more memory can help reduce I/O wait times. A failing hard drive or misconfigured I/O scheduler may also cause increased I/O wait, but these options are less likely if disk activity is not high and the hardware was previously functioning correctly."
            ),
            (
                "A system administrator needs to obtain information about which server versions are running on open ports of a remote host. However, the administrator must avoid performing an intrusive scan that could disrupt network services. Which of the following commands should the administrator run to best meet these requirements?",
                [
                    "nmap -sV --version-light target_host",
                    "nmap -A target_host",
                    "nmap -sT --top-ports=10 target_host",
                    "nmap --top-ports=100 -sV target_host"
                ],
                0,
                "Troubleshooting",
                "The correct answer is nmap -sV --version-light target_host because this command line option tells Nmap to perform a service/version detection scan (-sV) using a light intensity, which is less intrusive and less likely to cause disruptions (--version-light). On the other hand, -sT performs a Connect scan that could potentially be more disruptive by completing the TCP three-way handshake; -A aggressively performs OS detection, script scanning, and traceroute, which is more intrusive; and --top-ports does not specify the intensity for version scanning and is primarily used for scanning a certain number of the most common ports."
            )
        ]
        # --- Command Questions (Truncated) ---
        command_questions = [
            ("What is the primary function of the `mkinitrd` command?", ["Create an initial RAM disk image used during boot", "Install the GRUB bootloader", "Configure network interfaces", "Manage kernel modules"], 0, "Commands (System Management)", "`mkinitrd` creates an initial RAM disk (initrd) image..."),
            ("Which command installs the GRUB2 bootloader to a specified device?", ["grub2-mkconfig", "grub2-install", "update-grub", "dracut"], 1, "Commands (System Management)", "`grub2-install` installs the GRUB2 bootloader files..."),
            # ... more command questions ...
        ]
        # --- Definition Questions (Truncated) ---
        definition_questions = [
             ("What does ACL stand for in Linux security?", ["Access Configuration Layer", "Advanced Control List", "Access Control List", "Allowed Command List"], 2, "Concepts & Terms (Security)", "ACL (Access Control List) provides a more flexible permission mechanism..."),
             ("In Kubernetes, what is an Ambassador container?", ["A container that monitors network traffic", "A container acting as an outbound proxy for external services", "A primary application container", "A container managing storage volumes"], 1, "Concepts & Terms (Containers)", "An Ambassador container acts as a proxy within a Pod..."),
             # ... more definition questions ...
        ]

        self.questions = existing_questions + command_questions + definition_questions
        random.shuffle(self.questions)

        self.categories = set(q[3] for q in self.questions)
        for category in self.categories:
            self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        self.save_history() # Save potentially updated history

    def update_history(self, question_text, category, is_correct):
        """Update study history with the result of the answered question."""
        timestamp = datetime.now().isoformat()
        self.study_history["total_attempts"] = self.study_history.get("total_attempts", 0) + 1
        if is_correct:
            self.study_history["total_correct"] = self.study_history.get("total_correct", 0) + 1

        q_stats = self.study_history["questions"].setdefault(question_text, {"correct": 0, "attempts": 0, "history": []})
        q_stats["attempts"] += 1
        if is_correct: q_stats["correct"] += 1
        q_stats["history"].append({"timestamp": timestamp, "correct": is_correct})
        # q_stats["history"] = q_stats["history"][-10:] # Optional: limit history

        cat_stats = self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        cat_stats["attempts"] += 1
        if is_correct: cat_stats["correct"] += 1

    def select_question(self, category_filter=None):
        """Select a question, optionally filtered, avoiding recent repeats and using weighting."""
        possible_indices = [
            idx for idx, q in enumerate(self.questions)
            if (category_filter is None or q[3] == category_filter)
        ]

        if not possible_indices:
            print(f"{COLOR_INFO} No questions found for filter: {category_filter} {COLOR_RESET}") # Use INFO
            return None, -1

        available_indices = [idx for idx in possible_indices if idx not in self.answered_indices_session]

        if not available_indices:
            print(f"{COLOR_INFO} All questions in this category answered this session. Resetting session list for this category. {COLOR_RESET}")
            self.answered_indices_session = [idx for idx in self.answered_indices_session if self.questions[idx][3] != category_filter]
            available_indices = possible_indices
            if not available_indices:
                 print(f"{COLOR_ERROR} Error: Still no available questions after reset. {COLOR_RESET}")
                 return None, -1

        weights = []
        indices_for_weighting = []
        for q_idx in available_indices:
            q_text = self.questions[q_idx][0]
            q_stats = self.study_history.get("questions", {}).get(q_text, {"correct": 0, "attempts": 0})
            attempts = q_stats.get("attempts", 0)
            correct = q_stats.get("correct", 0)
            accuracy = (correct / attempts) if attempts > 0 else 0.5
            weight = (1.0 - accuracy) * 5 + (1.0 / (attempts + 1)) * 2
            weights.append(max(0.1, weight))
            indices_for_weighting.append(q_idx)

        if not indices_for_weighting or not weights or len(weights) != len(indices_for_weighting):
            print(f"{COLOR_INFO} Weighting error. Falling back to random choice. {COLOR_RESET}") # Use INFO
            chosen_original_index = random.choice(available_indices)
        else:
            try:
                chosen_original_index = random.choices(indices_for_weighting, weights=weights, k=1)[0]
            except (IndexError, ValueError) as e:
                 print(f"{COLOR_INFO} Weighted choice error: {e}. Falling back to random choice. {COLOR_RESET}") # Use INFO
                 chosen_original_index = random.choice(available_indices)

        self.answered_indices_session.append(chosen_original_index)
        chosen_question = self.questions[chosen_original_index]
        return chosen_question, chosen_original_index

    def display_question(self, question_data):
        """Display the question and options with enhanced CLI formatting."""
        question_text, options, _, category, _ = question_data
        cli_print_separator(char='~', color=COLOR_CATEGORY)
        print(f"{COLOR_CATEGORY}Category: {category}{COLOR_RESET}")
        cli_print_separator(char='~', color=COLOR_CATEGORY)
        print(f"\n{COLOR_QUESTION}Q: {question_text}{COLOR_RESET}\n")
        cli_print_separator(length=40, color=COLOR_BORDER + C["dim"])
        for i, option in enumerate(options):
            print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_OPTIONS}{option}{COLOR_RESET}")
        cli_print_separator(length=40, color=COLOR_BORDER + C["dim"])
        print() # Add a blank line for spacing

    def get_user_answer(self, num_options):
        """Get and validate user input for CLI with better prompting."""
        while True:
            try:
                # FIX 1: Changed color for 'q' from COLOR_WARNING to COLOR_INFO
                prompt = (f"{COLOR_PROMPT}Your choice ({COLOR_OPTION_NUM}1-{num_options}{COLOR_PROMPT}), "
                          f"'{COLOR_INFO}s{COLOR_PROMPT}' to skip, "
                          f"'{COLOR_INFO}q{COLOR_PROMPT}' to quit session: {COLOR_INPUT}")
                answer = input(prompt).lower().strip()
                print(COLOR_RESET, end='') # Reset color after input
                if answer == 'q': return 'q'
                if answer == 's': return 's'
                choice = int(answer)
                if 1 <= choice <= num_options:
                    return choice - 1  # Return 0-based index
                else:
                    print(f"{COLOR_INFO} Invalid choice. Please enter a number between 1 and {num_options}. {COLOR_RESET}") # Use INFO
            except ValueError:
                print(f"{COLOR_INFO} Invalid input. Please enter a number, 's', or 'q'. {COLOR_RESET}") # Use INFO
            except EOFError:
                 print(f"\n{COLOR_ERROR} Input interrupted. Exiting session. {COLOR_RESET}")
                 return 'q' # Treat EOF as quit

    def show_feedback(self, question_data, user_answer_index, original_index):
        """Show feedback based on the user's answer with enhanced CLI formatting."""
        question_text, options, correct_answer_index, category, explanation = question_data
        original_question_text = self.questions[original_index][0]
        is_correct = (user_answer_index == correct_answer_index)

        print() # Add spacing before feedback
        if is_correct:
            print(f"{COLOR_CORRECT}>>> Correct! \U0001F389 <<<{COLOR_RESET}")
            self.score += 1
        else:
            correct_option_text = options[correct_answer_index]
            print(f"{COLOR_INCORRECT}>>> Incorrect! \U0001F61E <<<")
            print(f"{COLOR_INCORRECT}    The correct answer was: {COLOR_OPTION_NUM}{correct_answer_index + 1}.{COLOR_RESET} {COLOR_OPTIONS}{correct_option_text}{COLOR_RESET}")
            if explanation:
                 print(f"\n{C['bold']}Explanation:{COLOR_RESET}")
                 print(f"{COLOR_EXPLANATION}{explanation}{COLOR_RESET}")

        self.update_history(original_question_text, category, is_correct)
        self.total_questions_session += 1
        print()
        input(f"{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")

    def show_stats(self):
        """Display overall and category-specific statistics with enhanced CLI formatting."""
        self.clear_screen()
        cli_print_header("Study Statistics")
        history = self.study_history

        # Overall Performance
        total_attempts = history.get("total_attempts", 0)
        total_correct = history.get("total_correct", 0)
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        acc_color = COLOR_STATS_ACC_GOOD if overall_accuracy >= 75 else (COLOR_STATS_ACC_AVG if overall_accuracy >= 50 else COLOR_STATS_ACC_BAD)

        print(f"\n{COLOR_SUBHEADER}Overall Performance (All Time):{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Total Questions Answered:{COLOR_RESET} {COLOR_STATS_VALUE}{total_attempts}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Total Correct:           {COLOR_RESET} {COLOR_STATS_VALUE}{total_correct}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Overall Accuracy:        {COLOR_RESET} {acc_color}{overall_accuracy:.2f}%{COLOR_RESET}")

        # Performance by Category
        print(f"\n{COLOR_SUBHEADER}Performance by Category:{COLOR_RESET}")
        categories_data = history.get("categories", {})
        sorted_categories = sorted(categories_data.items())

        if not sorted_categories:
            print(f"  {COLOR_EXPLANATION}No category data recorded yet.{COLOR_RESET}")
        else:
            max_len = max((len(cat) for cat in categories_data.keys()), default=10) if categories_data else 10
            # Adjusted header for alignment
            header = f"  {COLOR_STATS_LABEL}{'Category'.ljust(max_len)} │ {'Correct'.rjust(7)} │ {'Attempts'.rjust(8)} │ {'Accuracy'.rjust(9)}{COLOR_RESET}"
            print(header)
            print(f"  {COLOR_BORDER}{'-' * max_len}─┼─────────┼──────────┼──────────{COLOR_RESET}") # Use box drawing chars
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0)
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) if cat_attempts > 0 else 0
                acc_color = COLOR_STATS_ACC_GOOD if cat_accuracy >= 75 else (COLOR_STATS_ACC_AVG if cat_accuracy >= 50 else COLOR_STATS_ACC_BAD)
                print(f"  {category.ljust(max_len)} │ {COLOR_STATS_VALUE}{str(cat_correct).rjust(7)}{COLOR_RESET} │ {COLOR_STATS_VALUE}{str(cat_attempts).rjust(8)}{COLOR_RESET} │ {acc_color}{f'{cat_accuracy:.1f}%'.rjust(9)}{COLOR_RESET}")

        # Performance on Specific Questions
        print(f"\n{COLOR_SUBHEADER}Performance on Specific Questions (All History):{COLOR_RESET}")
        question_stats = history.get("questions", {})
        if not question_stats:
            print(f"  {COLOR_EXPLANATION}No specific question data recorded yet.{COLOR_RESET}")
        else:
            sorted_questions = sorted(question_stats.items())
            print(f"  {COLOR_STATS_LABEL}Showing all questions with recorded history:{COLOR_RESET}")
            for i, (q_text, stats) in enumerate(sorted_questions):
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                acc_color = COLOR_STATS_ACC_GOOD if accuracy >= 75 else (COLOR_STATS_ACC_AVG if accuracy >= 50 else COLOR_STATS_ACC_BAD)

                last_result = "N/A"
                last_color = COLOR_EXPLANATION
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_color = COLOR_CORRECT if last_correct else COLOR_INCORRECT

                display_text = (q_text[:75] + '...') if len(q_text) > 75 else q_text
                print(f"\n  {COLOR_QUESTION}{i+1}. \"{display_text}\"{COLOR_RESET}")
                # Use C['dim'] for the less important details part
                print(f"     {C['dim']}({COLOR_STATS_VALUE}{attempts}{C['dim']} attempts, {acc_color}{accuracy:.1f}%{C['dim']} acc.) Last: {last_color}{last_result}{C['dim']}){COLOR_RESET}")

        print()
        cli_print_separator(color=COLOR_BORDER)
        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def select_category(self):
        """Allow the user to select a category to focus on, using enhanced CLI."""
        self.clear_screen()
        cli_print_header("Select a Category")
        sorted_categories = sorted(list(self.categories))
        if not sorted_categories:
            print(f"{COLOR_ERROR} No categories found! {COLOR_RESET}")
            time.sleep(2)
            return None

        print(f"\n{COLOR_OPTIONS}Available Categories:{COLOR_RESET}")
        print(f"  {COLOR_OPTION_NUM}0.{COLOR_RESET} {COLOR_OPTIONS}All Categories{COLOR_RESET}")
        for i, category in enumerate(sorted_categories):
            print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_OPTIONS}{category}{COLOR_RESET}")
        print()

        while True:
            try:
                # FIX 1: Changed color for 'b' from COLOR_WARNING to COLOR_INFO
                prompt = f"{COLOR_PROMPT}Enter category number ({COLOR_OPTION_NUM}0-{len(sorted_categories)}{COLOR_PROMPT}), or '{COLOR_INFO}b{COLOR_PROMPT}' to go back: {COLOR_INPUT}"
                choice = input(prompt).lower().strip()
                print(COLOR_RESET, end='') # Reset color
                if choice == 'b': return 'b'
                num_choice = int(choice)
                if num_choice == 0: return None # All Categories
                elif 1 <= num_choice <= len(sorted_categories):
                    return sorted_categories[num_choice - 1]
                else:
                    print(f"{COLOR_INFO} Invalid choice. {COLOR_RESET}") # Use INFO
            except ValueError:
                print(f"{COLOR_INFO} Invalid input. Please enter a number or 'b'. {COLOR_RESET}") # Use INFO
            except EOFError:
                 print(f"\n{COLOR_ERROR} Input interrupted. Returning to main menu. {COLOR_RESET}")
                 return 'b' # Treat EOF as back

    def clear_stats(self):
        """Clear all stored statistics after confirmation with enhanced CLI."""
        self.clear_screen()
        cli_print_header("Clear Statistics", char='!', color=COLOR_ERROR)
        # Keep COLOR_WARNING for the confirmation text itself as it's a destructive action
        print(f"\n{COLOR_WARNING} This action will permanently delete ALL study history. {COLOR_RESET}")
        confirm = input(f"{COLOR_PROMPT}Are you sure you want to proceed? ({COLOR_OPTIONS}yes{COLOR_PROMPT}/{COLOR_OPTIONS}no{COLOR_PROMPT}): {COLOR_INPUT}").lower().strip()
        print(COLOR_RESET, end='') # Reset color

        if confirm == 'yes':
            self.study_history = self._default_history()
            for category in self.categories:
                 self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.save_history()
            print(f"\n{COLOR_CORRECT}>>> Study history has been cleared. <<<{COLOR_RESET}")
        else:
            print(f"\n{COLOR_INFO}Operation cancelled. History not cleared.{COLOR_RESET}")

        print()
        input(f"{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def run_quiz(self, category_filter=None):
        """Run the main quiz loop for the CLI with enhanced display."""
        self.score = 0
        self.total_questions_session = 0
        self.answered_indices_session = []

        while True:
            self.clear_screen()
            category_display = category_filter if category_filter else "All Categories"
            cli_print_header(f"Quiz Mode: {category_display}")
            print(f"{COLOR_STATS_LABEL}Session Score: {COLOR_STATS_VALUE}{self.score} / {self.total_questions_session}{COLOR_RESET}\n")

            question_data, original_index = self.select_question(category_filter)

            if question_data is None:
                 print(f"{COLOR_INFO} Could not select a question (possibly none left?). Returning to menu. {COLOR_RESET}") # Use INFO
                 time.sleep(3)
                 break

            self.display_question(question_data)
            user_answer = self.get_user_answer(len(question_data[1]))

            if user_answer == 'q':
                break
            elif user_answer == 's':
                print(f"\n{COLOR_INFO}Skipping question...{COLOR_RESET}")
                self.total_questions_session += 1 # Count skipped question
                input(f"\n{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
                continue

            self.show_feedback(question_data, user_answer, original_index)

        print(f"\n{COLOR_HEADER}Quiz session finished.{COLOR_RESET}")
        print(f"{COLOR_STATS_LABEL}Your final score for this session: {COLOR_STATS_VALUE}{self.score} / {self.total_questions_session}{COLOR_RESET}")
        self.save_history()
        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def main_menu(self):
        """Display the main menu and handle user choices for CLI with enhanced display."""
        while True:
            self.clear_screen()
            cli_print_header("Linux+ Study Game - Main Menu")
            print(f"\n{COLOR_OPTIONS}Please choose an option:{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}1.{COLOR_RESET} {COLOR_OPTIONS}Start Quiz (All Categories){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}2.{COLOR_RESET} {COLOR_OPTIONS}Start Quiz (Select Category){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}3.{COLOR_RESET} {COLOR_OPTIONS}View Statistics{COLOR_RESET}")
            # FIX 1: Keep COLOR_WARNING for the Clear Stats option text itself, as the color definition was adjusted
            print(f"  {COLOR_OPTION_NUM}4.{COLOR_RESET} {COLOR_WARNING}Clear Statistics{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}5.{COLOR_RESET} {COLOR_OPTIONS}Quit{COLOR_RESET}")
            cli_print_separator(color=COLOR_BORDER)

            choice = input(f"{COLOR_PROMPT}Enter your choice: {COLOR_INPUT}")
            print(COLOR_RESET, end='') # Reset color

            if choice == '1':
                self.run_quiz(category_filter=None)
            elif choice == '2':
                selected_category = self.select_category()
                if selected_category != 'b': # Proceed if not 'back'
                    self.run_quiz(category_filter=selected_category)
            elif choice == '3':
                self.show_stats()
            elif choice == '4':
                self.clear_stats()
            elif choice == '5':
                print(f"\n{COLOR_INFO}Saving history and quitting. Goodbye!{COLOR_RESET}")
                self.save_history()
                sys.exit()
            else:
                print(f"{COLOR_INFO} Invalid choice. Please try again. {COLOR_RESET}") # Use INFO
                time.sleep(1.5)

# --- GUI Game Class ---
class LinuxPlusStudyGUI:
    """Handles the Tkinter Graphical User Interface for the study game with improved styling."""
    def __init__(self, root, game_logic):
        self.root = root
        self.game_logic = game_logic

        self.current_question_index = -1
        self.current_question_data = None
        self.selected_answer_var = tk.IntVar(value=-1)
        self.quiz_active = False
        self.current_category_filter = None

        # --- Enhanced Styling ---
        self.colors = {
            "bg": "#2B2B2B",          # Dark background
            "fg": "#D3D3D3",          # Light grey text
            "bg_widget": "#3C3F41",   # Slightly lighter background for widgets
            "fg_header": "#A9B7C6",   # Lighter text for headers
            "accent": "#FFC66D",      # Amber/Yellow accent
            "accent_dark": "#E8A44C",
            "button": "#4E5254",      # Darker button background
            "button_fg": "#D4D4D4",   # Light button text
            "button_hover": "#5F6365",
            "correct": "#6A8759",     # Muted green
            "incorrect": "#AC4142",   # Muted red
            "explanation_bg": "#313335", # Dark background for explanation text widget
            "border": "#555555",
            "disabled_fg": "#888888", # Grey for disabled text
            "status_fg": "#BBBBBB",
            "category_fg": "#808080", # Grey for category
            # FIX 3: Added missing 'dim' color key, reusing disabled_fg
            "dim": "#888888",
        }
        self.fonts = {
            "base": tkFont.Font(family="Segoe UI", size=10),
            "bold": tkFont.Font(family="Segoe UI", size=10, weight="bold"),
            "header": tkFont.Font(family="Segoe UI", size=16, weight="bold"),
            "subheader": tkFont.Font(family="Segoe UI", size=12, weight="bold"),
            "italic": tkFont.Font(family="Segoe UI", size=9, slant="italic"),
            "question": tkFont.Font(family="Segoe UI", size=12),
            "option": tkFont.Font(family="Segoe UI", size=11),
            "feedback": tkFont.Font(family="Segoe UI", size=11, weight="bold"),
            "explanation": tkFont.Font(family="Consolas", size=10), # Monospace
            "stats": tkFont.Font(family="Consolas", size=10),
            "button": tkFont.Font(family="Segoe UI", size=10, weight="bold"),
        }
        self._setup_styles()
        self._setup_ui()
        self._load_initial_state()

    def _setup_styles(self):
        """Configure ttk styles for a modern dark theme."""
        self.style = ttk.Style()
        self.style.theme_use('clam') # Clam is often best for custom styling

        # --- Configure Base Styles ---
        self.style.configure(".",
                             background=self.colors["bg"],
                             foreground=self.colors["fg"],
                             font=self.fonts["base"],
                             borderwidth=0,
                             focuscolor=self.colors["accent"]) # Outline on focus

        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"], font=self.fonts["base"])
        self.style.configure("Header.TLabel", font=self.fonts["header"], foreground=self.colors["fg_header"])
        self.style.configure("Category.TLabel", font=self.fonts["italic"], foreground=self.colors["category_fg"])
        self.style.configure("Status.TLabel", font=self.fonts["base"], foreground=self.colors["status_fg"])

        # --- Button Styling ---
        self.style.configure("TButton",
                             font=self.fonts["button"],
                             padding=(10, 5), # Wider padding
                             background=self.colors["button"],
                             foreground=self.colors["button_fg"],
                             borderwidth=1, # Subtle border
                             bordercolor=self.colors["border"],
                             relief="flat") # Flat look
        self.style.map("TButton",
                       background=[('active', self.colors["button_hover"]), ('!disabled', self.colors["button"])],
                       foreground=[('disabled', self.colors["disabled_fg"])])

        self.style.configure("Accent.TButton", # For Submit/Next
                             background=self.colors["accent"],
                             foreground=self.colors["bg"], # Dark text on accent
                             font=self.fonts["button"])
        self.style.map("Accent.TButton",
                       background=[('active', self.colors["accent_dark"]), ('!disabled', self.colors["accent"])])

        # --- Radiobutton Styling ---
        self.style.configure("TRadiobutton",
                             background=self.colors["bg_widget"], # Different background
                             foreground=self.colors["fg"],
                             font=self.fonts["option"],
                             indicatorrelief=tk.FLAT,
                             indicatormargin=5,
                             padding=(5, 3))
        # Note: Indicator color mapping can be tricky across themes/OS
        self.style.map("TRadiobutton",
                       background=[('selected', self.colors["bg_widget"]), ('active', self.colors["bg_widget"])],
                       indicatorbackground=[('selected', self.colors["accent"]), ('!selected', self.colors["border"])],
                       foreground=[('disabled', self.colors["disabled_fg"])])

        # --- Feedback Label Styling ---
        self.style.configure("Feedback.TLabel", font=self.fonts["feedback"], padding=5)
        self.style.configure("Correct.Feedback.TLabel", foreground=self.colors["correct"])
        self.style.configure("Incorrect.Feedback.TLabel", foreground=self.colors["incorrect"])

        # --- Scrollbar Styling (Subtle) ---
        self.style.configure("Vertical.TScrollbar",
                             background=self.colors["bg_widget"],
                             troughcolor=self.colors["bg"],
                             bordercolor=self.colors["border"],
                             arrowcolor=self.colors["fg"],
                             relief="flat")
        self.style.map("Vertical.TScrollbar",
                       background=[('active', self.colors["border"])])

        # --- OptionMenu Styling (Dropdown) ---
        # Requires setting tk_setPalette for the menu itself
        self.style.configure("TMenubutton",
                             font=self.fonts["base"],
                             padding=(10, 5),
                             background=self.colors["button"],
                             foreground=self.colors["button_fg"],
                             arrowcolor=self.colors["accent"],
                             relief="flat")
        self.style.map("TMenubutton",
                       background=[('active', self.colors["button_hover"])])


    def _setup_ui(self):
        """Create the main UI elements with enhanced layout."""
        self.root.title("Linux+ Study Game")
        self.root.geometry("900x750") # Larger window
        self.root.configure(bg=self.colors["bg"])
        self.root.minsize(700, 600) # Minimum size

        # --- Main Frame with Padding ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1) # Make content area expand
        main_frame.rowconfigure(1, weight=1)    # Make quiz area expand

        # --- Header ---
        header_frame = ttk.Frame(main_frame, padding=(0, 0, 0, 15))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ttk.Label(header_frame, text="Linux+ Study Game", style="Header.TLabel").pack(side=tk.LEFT)
        self.status_label = ttk.Label(header_frame, text="Status: Idle", style="Status.TLabel")
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # --- Quiz Area Frame (Content Area) ---
        quiz_frame_outer = tk.Frame(main_frame, bg=self.colors["bg_widget"], bd=1, relief="solid")
        quiz_frame_outer.grid(row=1, column=0, sticky="nsew", pady=10)
        quiz_frame_outer.columnconfigure(0, weight=1)
        # Make row 1 (question) and row 3 (feedback/explanation) expand vertically
        quiz_frame_outer.rowconfigure(1, weight=1)
        quiz_frame_outer.rowconfigure(3, weight=1) # Allow explanation area to expand

        quiz_frame = ttk.Frame(quiz_frame_outer, padding="20", style="TFrame")
        quiz_frame.grid(row=0, column=0, sticky="nsew")
        quiz_frame.columnconfigure(0, weight=1)
        # Make row 1 (question) and row 3 (feedback/explanation) expand vertically
        quiz_frame.rowconfigure(1, weight=1)
        quiz_frame.rowconfigure(3, weight=1) # Allow explanation area to expand

        # Category Label
        self.category_label = ttk.Label(quiz_frame, text="Category: N/A", style="Category.TLabel")
        self.category_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Question Text (Scrollable Text Widget)
        q_frame = tk.Frame(quiz_frame, bd=0, relief="flat", bg=self.colors["bg_widget"])
        q_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        q_frame.columnconfigure(0, weight=1)
        q_frame.rowconfigure(0, weight=1)

        q_scroll = ttk.Scrollbar(q_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.question_text = tk.Text(q_frame, wrap=tk.WORD, height=5,
                                     yscrollcommand=q_scroll.set,
                                     font=self.fonts["question"], relief="flat",
                                     bg=self.colors["bg_widget"], fg=self.colors["fg"],
                                     bd=0, state=tk.DISABLED,
                                     padx=10, pady=10,
                                     selectbackground=self.colors["accent"],
                                     selectforeground=self.colors["bg"])
        q_scroll.config(command=self.question_text.yview)
        q_scroll.grid(row=0, column=1, sticky="ns")
        self.question_text.grid(row=0, column=0, sticky="nsew")

        # Options Frame (Radio Buttons)
        self.options_frame = ttk.Frame(quiz_frame, padding=(0, 15, 0, 10), style="TFrame")
        self.options_frame.grid(row=2, column=0, sticky="ew", pady=10)
        self.options_frame.columnconfigure(0, weight=1)

        # Feedback & Explanation Area (Combined Frame)
        feedback_exp_frame = ttk.Frame(quiz_frame, style="TFrame")
        # Make this frame expand vertically within the quiz_frame grid
        feedback_exp_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 5))
        feedback_exp_frame.columnconfigure(0, weight=1)
        feedback_exp_frame.rowconfigure(1, weight=1) # Allow explanation text widget to expand

        self.feedback_label = ttk.Label(feedback_exp_frame, text="", style="Feedback.TLabel", anchor=tk.W)
        self.feedback_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # FIX 4: Explanation Label replaced with scrollable Text widget
        exp_frame = tk.Frame(feedback_exp_frame, bd=1, relief="solid", bg=self.colors["explanation_bg"])
        exp_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        exp_frame.columnconfigure(0, weight=1)
        exp_frame.rowconfigure(0, weight=1)

        exp_scroll = ttk.Scrollbar(exp_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
        self.explanation_text = tk.Text(exp_frame, wrap=tk.WORD, height=4, # Initial height for explanation
                                         yscrollcommand=exp_scroll.set,
                                         font=self.fonts["explanation"], relief="flat",
                                         bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                                         bd=0, state=tk.DISABLED,
                                         padx=10, pady=10,
                                         selectbackground=self.colors["accent"],
                                         selectforeground=self.colors["bg"])
        exp_scroll.config(command=self.explanation_text.yview)
        exp_scroll.grid(row=0, column=1, sticky="ns")
        self.explanation_text.grid(row=0, column=0, sticky="nsew")
        # Hide the entire frame initially
        exp_frame.grid_remove()
        self.explanation_frame = exp_frame # Keep reference to hide/show

        # --- Control Frame ---
        control_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0))
        control_frame.grid(row=2, column=0, sticky="ew")
        control_frame.columnconfigure(1, weight=1) # Push main actions to the right

        # Left side (Quiz Controls)
        quiz_controls = ttk.Frame(control_frame)
        quiz_controls.grid(row=0, column=0, sticky="w")
        self.submit_button = ttk.Button(quiz_controls, text="Submit Answer", command=self._submit_answer_gui, state=tk.DISABLED, style="Accent.TButton", width=15)
        self.submit_button.pack(side=tk.LEFT, padx=(0, 10))
        self.next_button = ttk.Button(quiz_controls, text="Next Question", command=self._next_question_gui, state=tk.DISABLED, style="Accent.TButton", width=15)
        self.next_button.pack(side=tk.LEFT)

        # Right side (Main Actions)
        main_actions = ttk.Frame(control_frame)
        main_actions.grid(row=0, column=2, sticky="e") # Use column 2
        ttk.Button(main_actions, text="Start Quiz", command=self._start_quiz_dialog, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="View Stats", command=self._show_stats_gui, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Clear Stats", command=self._clear_stats_gui, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Quit", command=self._quit_app, style="TButton").pack(side=tk.LEFT, padx=(5, 0))

    def _load_initial_state(self):
        """Set the initial welcome message."""
        self._update_status("Ready. Click 'Start Quiz' to begin.")
        self._clear_quiz_area()
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END) # Clear first
        self.question_text.insert(tk.END, "Welcome to the Linux+ Study Game!\n\n"
                                          "Select 'Start Quiz' to choose a category and begin.")
        self.question_text.config(state=tk.DISABLED)

    def _clear_quiz_area(self):
        """Clear question, options, and feedback."""
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.config(state=tk.DISABLED)

        for widget in self.options_frame.winfo_children():
            widget.destroy() # Destroy all widgets in options frame

        self.feedback_label.config(text="", style="Feedback.TLabel")

        # FIX 4: Clear and hide the explanation Text widget frame
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.config(state=tk.DISABLED)
        self.explanation_frame.grid_remove() # Hide explanation frame

        self.selected_answer_var.set(-1)

    def _update_status(self, message):
        """Update the status bar label."""
        self.status_label.config(text=f"Status: {message}")

    def _start_quiz_dialog(self):
        """Show dialog to select category and start quiz with improved styling."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Start Quiz")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg"])

        # Apply dark theme to the dialog window itself (may require OS-specific calls)
        try:
            dialog.tk_setPalette(background=self.colors["bg"], foreground=self.colors["fg"])
        except tk.TclError:
            print("Warning: Could not set Toplevel palette (might be OS dependent).")


        ttk.Label(dialog, text="Select Category:", font=self.fonts["subheader"],
                  background=self.colors["bg"], foreground=self.colors["fg_header"])\
            .pack(pady=(25, 10))

        categories = ["All Categories"] + sorted(list(self.game_logic.categories))
        category_var = tk.StringVar(value=categories[0])

        # --- Styled OptionMenu ---
        menu_style = {"background": self.colors["button"],
                      "foreground": self.colors["button_fg"],
                      "activebackground": self.colors["button_hover"],
                      "activeforeground": self.colors["button_fg"],
                      "font": self.fonts["base"]}

        option_menu = ttk.OptionMenu(dialog, category_var, categories[0], *categories, style="TMenubutton")
        option_menu.config(width=35)
        menu = option_menu["menu"]
        menu.config(**menu_style)
        option_menu.pack(pady=15, padx=30)

        def on_start():
            selected = category_var.get()
            self.current_category_filter = None if selected == "All Categories" else selected
            dialog.destroy()
            self._start_quiz_session()

        button_frame = ttk.Frame(dialog, style="TFrame")
        button_frame.pack(pady=(20, 25))
        ttk.Button(button_frame, text="Start", command=on_start, style="Accent.TButton", width=12).pack(side=tk.LEFT, padx=15)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy, style="TButton", width=12).pack(side=tk.LEFT, padx=15)

        self.root.wait_window(dialog)

    def _start_quiz_session(self):
        """Begin a new quiz session."""
        self.quiz_active = True
        self.game_logic.score = 0
        self.game_logic.total_questions_session = 0
        self.game_logic.answered_indices_session = []
        self.current_question_index = -1
        cat_display = self.current_category_filter or 'All'
        self._update_status(f"Quiz started (Category: {cat_display}).")
        self._next_question_gui()

    def _display_question_gui(self):
        """Update the GUI with the current question data."""
        if not self.current_question_data:
            self._clear_quiz_area()
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END) # Clear first
            self.question_text.insert(tk.END, "Quiz session complete or no more questions found.\n\n"
                                          "Start a new quiz or view statistics.")
            self.question_text.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.quiz_active = False
            self._update_status("Quiz finished or no questions found.")
            # Save history at the end of the session run
            self.game_logic.save_history()
            messagebox.showinfo("Quiz Complete", "You've answered all available questions in this category for this session!", parent=self.root)
            return

        self._clear_quiz_area()
        q_text, options, _, category, _ = self.current_question_data

        self.category_label.config(text=f"Category: {category}")
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END) # Clear first
        self.question_text.insert(tk.END, q_text)
        self.question_text.config(state=tk.DISABLED)

        self.selected_answer_var.set(-1)
        for i, option in enumerate(options):
            rb = ttk.Radiobutton(self.options_frame, text=option, variable=self.selected_answer_var,
                                 value=i, style="TRadiobutton", takefocus=False) # Don't take focus initially
            rb.pack(anchor=tk.W, padx=5, pady=4, fill=tk.X)

        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.submit_button.focus_set()


    def _next_question_gui(self):
        """Select and display the next question."""
        if not self.quiz_active:
             messagebox.showinfo("Quiz Over", "The quiz session is not active. Please start a new quiz.", parent=self.root)
             return

        question_data, original_index = self.game_logic.select_question(self.current_category_filter)

        if question_data is None:
            self.current_question_data = None
            self.current_question_index = -1
            self._display_question_gui() # Shows end message and saves history
        else:
            self.current_question_data = question_data
            self.current_question_index = original_index
            self._display_question_gui()

    def _submit_answer_gui(self):
        """Process the user's submitted answer with enhanced feedback."""
        user_answer_index = self.selected_answer_var.get()

        if user_answer_index == -1:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.", parent=self.root)
            return

        if not self.current_question_data:
            messagebox.showerror("Error", "No current question data available.", parent=self.root)
            return

        q_text, options, correct_answer_index, category, explanation = self.current_question_data
        original_question_text = self.game_logic.questions[self.current_question_index][0]
        is_correct = (user_answer_index == correct_answer_index)

        # Update feedback label and style
        if is_correct:
            self.feedback_label.config(text="Correct! \U0001F389", style="Correct.Feedback.TLabel")
            self.game_logic.score += 1
        else:
            correct_option_text = options[correct_answer_index]
            feedback_text = f"Incorrect. \U0001F61E Correct was: {correct_answer_index + 1}. {correct_option_text}"
            self.feedback_label.config(text=feedback_text, style="Incorrect.Feedback.TLabel")

            # FIX 4: Show explanation in Text widget if incorrect and available
            if explanation:
                 self.explanation_text.config(state=tk.NORMAL)
                 self.explanation_text.delete(1.0, tk.END) # Clear previous
                 self.explanation_text.insert(tk.END, f"Explanation:\n{explanation}")
                 self.explanation_text.config(state=tk.DISABLED)
                 self.explanation_frame.grid() # Show explanation frame
            else:
                 self.explanation_frame.grid_remove() # Hide if no explanation

        # Update history and session state
        self.game_logic.update_history(original_question_text, category, is_correct)
        self.game_logic.total_questions_session += 1
        self.game_logic.save_history()

        # Update UI state
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.config(state=tk.DISABLED)

        self._update_status(f"Answer submitted. Score: {self.game_logic.score}/{self.game_logic.total_questions_session}")
        self.next_button.focus_set()


    def _show_stats_gui(self):
        """Display statistics in a Toplevel window with improved styling."""
        stats_win = tk.Toplevel(self.root)
        stats_win.title("Study Statistics")
        stats_win.geometry("900x650")
        stats_win.transient(self.root)
        stats_win.grab_set()
        stats_win.configure(bg=self.colors["bg"])
        stats_win.minsize(700, 500)

        try:
            stats_win.tk_setPalette(background=self.colors["bg"], foreground=self.colors["fg"])
        except tk.TclError:
            print("Warning: Could not set Toplevel palette for stats window.")

        stats_frame = ttk.Frame(stats_win, padding="15")
        stats_frame.pack(fill=tk.BOTH, expand=True)

        stats_text = tk.Text(stats_frame, wrap=tk.WORD, font=self.fonts["stats"],
                             relief="solid", bd=1, borderwidth=1,
                             bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                             padx=15, pady=15,
                             selectbackground=self.colors["accent"],
                             selectforeground=self.colors["bg"])
        stats_scroll = ttk.Scrollbar(stats_frame, orient=tk.VERTICAL, command=stats_text.yview, style="Vertical.TScrollbar")
        stats_text.config(yscrollcommand=stats_scroll.set)

        stats_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Define tags for coloring/styling in the Text widget ---
        stats_text.tag_configure("header", font=self.fonts["subheader"], foreground=self.colors["fg_header"], spacing1=10, spacing3=10)
        stats_text.tag_configure("subheader", font=self.fonts["bold"], foreground=self.colors["accent"], spacing1=8, spacing3=5)
        stats_text.tag_configure("label", foreground=self.colors["status_fg"])
        stats_text.tag_configure("value", foreground=self.colors["fg"])
        stats_text.tag_configure("correct", foreground=self.colors["correct"])
        stats_text.tag_configure("incorrect", foreground=self.colors["incorrect"])
        stats_text.tag_configure("neutral", foreground=self.colors["accent_dark"])
        # FIX 3: Configure the 'dim' tag using the color defined in self.colors
        stats_text.tag_configure("dim", foreground=self.colors["dim"])
        stats_text.tag_configure("q_text", foreground=self.colors["fg"], spacing1=5)
        # FIX 3: Use the 'dim' tag for q_details instead of configuring a separate tag
        # stats_text.tag_configure("q_details", foreground=self.colors["dim"], spacing3=10) # Removed this line

        # --- Populate Stats Text ---
        stats_text.insert(tk.END, "--- Study Statistics ---\n", "header")

        # Overall Performance
        history = self.game_logic.study_history
        total_attempts = history.get("total_attempts", 0)
        total_correct = history.get("total_correct", 0)
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        acc_tag = "correct" if overall_accuracy >= 75 else ("neutral" if overall_accuracy >= 50 else "incorrect")

        stats_text.insert(tk.END, "Overall Performance (All Time):\n", "subheader")
        stats_text.insert(tk.END, "  Total Questions Answered: ", "label")
        stats_text.insert(tk.END, f"{total_attempts}\n", "value")
        stats_text.insert(tk.END, "  Total Correct:            ", "label")
        stats_text.insert(tk.END, f"{total_correct}\n", "value")
        stats_text.insert(tk.END, "  Overall Accuracy:         ", "label")
        stats_text.insert(tk.END, f"{overall_accuracy:.2f}%\n\n", acc_tag)

        # Performance by Category
        stats_text.insert(tk.END, "Performance by Category:\n", "subheader")
        categories_data = history.get("categories", {})
        sorted_categories = sorted(categories_data.items())

        if not sorted_categories:
            stats_text.insert(tk.END, "  No category data yet.\n", "dim")
        else:
            max_len = max((len(cat) for cat in categories_data.keys()), default=10) if categories_data else 10
            header_line = f"  {'Category'.ljust(max_len)} | {'Correct'.rjust(7)} | {'Attempts'.rjust(8)} | {'Accuracy'.rjust(9)}\n"
            stats_text.insert(tk.END, header_line, "label")
            stats_text.insert(tk.END, f"  {'-' * max_len}-+---------+----------+----------\n", "dim")
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0)
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) if cat_attempts > 0 else 0
                acc_tag = "correct" if cat_accuracy >= 75 else ("neutral" if cat_accuracy >= 50 else "incorrect")

                stats_text.insert(tk.END, f"  {category.ljust(max_len)} | ")
                stats_text.insert(tk.END, f"{str(cat_correct).rjust(7)}", "value")
                stats_text.insert(tk.END, " | ")
                stats_text.insert(tk.END, f"{str(cat_attempts).rjust(8)}", "value")
                stats_text.insert(tk.END, " | ")
                stats_text.insert(tk.END, f"{f'{cat_accuracy:.1f}%'.rjust(9)}\n", acc_tag)
        stats_text.insert(tk.END, "\n")

        # Performance on Specific Questions
        stats_text.insert(tk.END, "Performance on Specific Questions (All History):\n", "subheader")
        question_stats = history.get("questions", {})
        if not question_stats:
            stats_text.insert(tk.END, "  No specific question data yet.\n", "dim")
        else:
            sorted_questions = sorted(question_stats.items())
            for i, (q_text, stats) in enumerate(sorted_questions):
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                acc_tag = "correct" if accuracy >= 75 else ("neutral" if accuracy >= 50 else "incorrect")

                last_result = "N/A"
                last_tag = "dim"
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_tag = "correct" if last_correct else "incorrect"

                display_text = (q_text[:100] + '...') if len(q_text) > 100 else q_text
                stats_text.insert(tk.END, f"{i+1}. \"{display_text}\"\n", "q_text")
                # FIX 3: Use the 'dim' tag for the details line
                stats_text.insert(tk.END, f"      ({attempts} attempts, ", "dim")
                stats_text.insert(tk.END, f"{accuracy:.1f}%", acc_tag)
                stats_text.insert(tk.END, " acc.) Last: ", "dim")
                stats_text.insert(tk.END, f"{last_result}\n\n", last_tag) # Keep last_tag for result color
        # --- End Populate ---

        stats_text.config(state=tk.DISABLED) # Make text read-only

        # Close button frame
        button_frame = ttk.Frame(stats_win, style="TFrame")
        button_frame.pack(pady=(10, 15))
        close_button = ttk.Button(button_frame, text="Close", command=stats_win.destroy, style="TButton", width=12)
        close_button.pack()

        self.root.wait_window(stats_win)


    def _clear_stats_gui(self):
        """Ask for confirmation and clear stats via game logic."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete ALL study history? This cannot be undone.", parent=self.root, icon='warning'):
            self.game_logic.study_history = self.game_logic._default_history()
            for category in self.game_logic.categories:
                 self.game_logic.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.game_logic.save_history()
            messagebox.showinfo("Stats Cleared", "Study history has been cleared.", parent=self.root)
            self._update_status("Study history cleared.")

    def _quit_app(self):
        """Save history before quitting."""
        self.game_logic.save_history()
        self.root.quit()


# --- Main Execution Block ---
if __name__ == "__main__":
    # Initialize colorama (if available) for CLI
    if 'colorama' in sys.modules:
        colorama.init(autoreset=True)

    # Create instance of the game logic class
    game_engine = LinuxPlusStudyGame()

    # Ask user for interface preference (improved prompt)
    interface_choice = ""
    is_interactive = sys.stdin.isatty() and len(sys.argv) == 1

    if not is_interactive:
        print("Non-interactive environment detected or arguments provided. Defaulting to CLI.")
        interface_choice = 'cli'
    else:
        while interface_choice not in ['cli', 'gui']:
            print(f"{COLOR_PROMPT}Choose interface ({COLOR_OPTIONS}CLI{COLOR_PROMPT} or {COLOR_OPTIONS}GUI{COLOR_PROMPT}): {COLOR_INPUT}", end='')
            sys.stdout.flush()
            try:
                interface_choice = input().lower().strip()
                print(COLOR_RESET, end='') # Reset color after input
            except EOFError:
                 print(f"\n{COLOR_ERROR} Input interrupted. Exiting. {COLOR_RESET}")
                 sys.exit(1)
            if interface_choice not in ['cli', 'gui']:
                 print(f"{COLOR_INFO} Invalid choice. Please type 'cli' or 'gui'. {COLOR_RESET}") # Use INFO

    if interface_choice == 'gui':
        root = tk.Tk()
        app = LinuxPlusStudyGUI(root, game_engine)
        # Set protocol handler for window close to ensure saving
        root.protocol("WM_DELETE_WINDOW", app._quit_app)
        root.mainloop()
    else:
        # Run the CLI version
        try:
            game_engine.main_menu()
        except KeyboardInterrupt:
            print(f"\n{COLOR_WARNING} Keyboard interrupt detected. Saving history and exiting. {COLOR_RESET}")
            game_engine.save_history()
            sys.exit(0)

