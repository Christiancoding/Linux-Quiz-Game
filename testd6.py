import random
import os
import sys
import time
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font as tkFont, scrolledtext # Import scrolledtext

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
    COLOR_WARNING = C["fg_bright_yellow"] + C["bold"] # Bold yellow, no background
    COLOR_INFO = C["fg_bright_cyan"]
    COLOR_WELCOME_BORDER = C["fg_bright_yellow"] + C["bold"]
    COLOR_WELCOME_TEXT = C["fg_white"]
    COLOR_WELCOME_TITLE = C["fg_bright_yellow"] + C["bold"]
    COLOR_RESET = C["reset"]
except ImportError:
    print("Warning: Colorama not found. Colored output will be disabled in CLI.")
    # Define empty strings if colorama is not available
    C = {k: "" for k in ["reset", "bold", "dim", "fg_black", "fg_red", "fg_green", "fg_yellow", "fg_blue", "fg_magenta", "fg_cyan", "fg_white", "fg_lightblack_ex", "fg_bright_red", "fg_bright_green", "fg_bright_yellow", "fg_bright_blue", "fg_bright_magenta", "fg_bright_cyan", "fg_bright_white", "bg_red", "bg_green", "bg_yellow", "bg_blue", "bg_magenta", "bg_cyan", "bg_white"]}
    COLOR_QUESTION, COLOR_OPTIONS, COLOR_OPTION_NUM, COLOR_CATEGORY = "", "", "", ""
    COLOR_CORRECT, COLOR_INCORRECT, COLOR_EXPLANATION, COLOR_PROMPT = "", "", "", ""
    COLOR_HEADER, COLOR_SUBHEADER, COLOR_STATS_LABEL, COLOR_STATS_VALUE = "", "", "", ""
    COLOR_STATS_ACC_GOOD, COLOR_STATS_ACC_AVG, COLOR_STATS_ACC_BAD = "", "", ""
    COLOR_BORDER, COLOR_INPUT, COLOR_ERROR, COLOR_WARNING, COLOR_INFO = "", "", "", "", ""
    COLOR_WELCOME_BORDER, COLOR_WELCOME_TEXT, COLOR_WELCOME_TITLE = "", "", ""
    COLOR_RESET = ""

# --- Constants ---
HISTORY_FILE = "linux_plus_history.json"
QUIZ_MODE_STANDARD = "standard"
QUIZ_MODE_VERIFY = "verify"

# --- CLI Helper Functions ---
def cli_print_separator(char='-', length=60, color=COLOR_BORDER):
    """Prints a colored separator line."""
    print(f"{color}{char * length}{COLOR_RESET}")

def cli_print_header(text, char='=', length=60, color=COLOR_HEADER):
    """Prints a centered header with separators."""
    padding = (length - len(text) - 2) // 2
    print(f"{color}{char * padding} {text} {char * (length - len(text) - 2 - padding)}{COLOR_RESET}")

def cli_print_box(lines, title="", width=60, border_color=COLOR_BORDER, title_color=COLOR_HEADER, text_color=COLOR_WELCOME_TEXT):
    """Prints text within a colored box."""
    border = f"{border_color}{'=' * width}{COLOR_RESET}"
    print(border)
    if title:
        padding = (width - len(title) - 4) // 2
        print(f"{border_color}* { ' ' * padding }{title_color}{title}{border_color}{ ' ' * (width - len(title) - 4 - padding)} *{COLOR_RESET}")
        print(border)

    for line in lines:
        # Calculate needed padding, ensuring it's not negative
        line_len_no_color = len(line.encode('ascii', 'ignore').decode('ascii')) # Basic way to estimate length without color codes
        padding_right = width - line_len_no_color - 4
        if padding_right < 0: padding_right = 0
        print(f"{border_color}* {text_color}{line}{' ' * padding_right}{border_color} *{COLOR_RESET}")
    print(border)


# --- CLI Game Class ---
class LinuxPlusStudyGame:
    """Handles the logic and Command-Line Interface for the study game."""
    def __init__(self):
        self.questions = []
        self.score = 0
        self.total_questions_session = 0 # Track questions answered in the current session
        self.categories = set()
        self.answered_indices_session = []  # Track answered question indices in this session
        self.history_file = HISTORY_FILE
        self.study_history = self.load_history()
        self.load_questions() # Load questions after initializing history
        # For Verify Knowledge mode
        self.verify_session_answers = [] # List of tuples: (question_data, user_answer_index, is_correct)

    def _default_history(self):
        """Returns the default structure for study history."""
        return {
            "sessions": [], # Could store session summaries later
            "questions": {}, # Stores stats per question text
            "categories": {}, # Stores stats per category name
            "total_correct": 0,
            "total_attempts": 0,
            "incorrect_review": [] # List of question texts answered incorrectly
        }

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_history(self):
        """Load study history from file if it exists."""
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
                # Ensure all default keys exist
                default = self._default_history()
                for key, default_value in default.items():
                    history.setdefault(key, default_value)
                # Basic type validation
                if not isinstance(history.get("questions"), dict): history["questions"] = {}
                if not isinstance(history.get("categories"), dict): history["categories"] = {}
                if not isinstance(history.get("sessions"), list): history["sessions"] = []
                if not isinstance(history.get("incorrect_review"), list): history["incorrect_review"] = []
                return history
        except (FileNotFoundError, json.JSONDecodeError):
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
        # --- (Question data remains the same - truncated for brevity) ---
        # Note: Add your actual questions here
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
            ),
            # Add more troubleshooting questions...
            (
                 "Which file typically contains information about mounted filesystems?",
                 ["/etc/fstab", "/etc/mtab", "/proc/mounts", "Both /etc/mtab and /proc/mounts"],
                 3,
                 "Filesystems",
                 "/etc/fstab defines static filesystem mounts. /etc/mtab used to be a regular file showing current mounts but is often a symlink to /proc/mounts. /proc/mounts is a virtual file reflecting the kernel's current view of mounted filesystems."
            ),
            (
                "What command is used to check and repair a Linux filesystem?",
                ["mount", "checkfs", "fsck", "format"],
                2,
                "Filesystems",
                "`fsck` (filesystem check) is the standard utility for checking and repairing Linux filesystems."
            ),
        ]
        command_questions = [
            ("What is the primary function of the `mkinitrd` command?", ["Create an initial RAM disk image used during boot", "Install the GRUB bootloader", "Configure network interfaces", "Manage kernel modules"], 0, "Commands (System Management)", "`mkinitrd` creates an initial RAM disk (initrd) image containing kernel modules needed to mount the root filesystem."),
            ("Which command installs the GRUB2 bootloader to a specified device?", ["grub2-mkconfig", "grub2-install", "update-grub", "dracut"], 1, "Commands (System Management)", "`grub2-install` installs the GRUB2 bootloader files onto the specified device (e.g., /dev/sda). `grub2-mkconfig` generates the configuration file."),
            ("What command displays the current directory?", ["pwd", "cd", "ls", "whereami"], 0, "Commands (Navigation)", "`pwd` (print working directory) displays the full path of the current directory."),
            ("Which command is used to change file permissions?", ["chown", "chgrp", "chmod", "setfacl"], 2, "Commands (Permissions)", "`chmod` (change mode) is used to change the read, write, and execute permissions of files and directories."),
             (
                "Which command is used to view the contents of a compressed tar archive (`.tar.gz`) without extracting it?",
                ["tar -cvf archive.tar.gz /path", "gzip -d archive.tar.gz", "tar -tvf archive.tar.gz", "gunzip -l archive.tar.gz"],
                2,
                "Commands (Archiving)",
                "`tar -tvf archive.tar.gz` lists (-t) the contents verbosely (-v) from the specified file (-f). `-c` creates, `gzip -d` or `gunzip` decompresses."
            ),
        ]
        definition_questions = [
             ("What does ACL stand for in Linux security?", ["Access Configuration Layer", "Advanced Control List", "Access Control List", "Allowed Command List"], 2, "Concepts & Terms (Security)", "ACL (Access Control List) provides a more flexible permission mechanism for file systems than traditional user/group/other permissions."),
             ("In Kubernetes, what is an Ambassador container?", ["A container that monitors network traffic", "A container acting as an outbound proxy for external services", "A primary application container", "A container managing storage volumes"], 1, "Concepts & Terms (Containers)", "An Ambassador container acts as a proxy within a Pod, simplifying communication between the application container and external services or resources."),
             ("What is the purpose of the `/etc/skel` directory?", ["Stores user skeleton files for new accounts", "Contains system kernel modules", "Temporary file storage", "System-wide configuration files"], 0, "Concepts & Terms (System Structure)", "The `/etc/skel` directory contains files and directories that are copied to a new user's home directory when the account is created."),
             ("What is 'copy-on-write' (CoW) in the context of filesystems or storage?", ["A technique where data is duplicated before modification", "A method for compressing files", "A file permission setting", "A network file sharing protocol"], 0, "Concepts & Terms (Filesystems)", "Copy-on-write (CoW) is an optimization strategy where shared data is not copied until one of the users modifies it. This is used in filesystems like Btrfs and ZFS, and also in memory management."),
        ]

        self.questions = existing_questions + command_questions + definition_questions
        random.shuffle(self.questions) # Shuffle once on load

        self.categories = set(q[3] for q in self.questions)
        # Ensure all categories from questions exist in history
        for category in self.categories:
            self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        self.save_history() # Save potentially updated history

    def update_history(self, question_text, category, is_correct):
        """Update study history with the result of the answered question."""
        timestamp = datetime.now().isoformat()
        history = self.study_history

        # Overall totals
        history["total_attempts"] = history.get("total_attempts", 0) + 1
        if is_correct:
            history["total_correct"] = history.get("total_correct", 0) + 1

        # Question specific stats
        q_stats = history["questions"].setdefault(question_text, {"correct": 0, "attempts": 0, "history": []})
        q_stats["attempts"] += 1
        if is_correct:
            q_stats["correct"] += 1
        else:
            # Add to review list if incorrect and not already there
            if question_text not in history.get("incorrect_review", []):
                 history.setdefault("incorrect_review", []).append(question_text)

        q_stats["history"].append({"timestamp": timestamp, "correct": is_correct})
        # q_stats["history"] = q_stats["history"][-10:] # Optional: limit history length

        # Category specific stats
        cat_stats = history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        cat_stats["attempts"] += 1
        if is_correct:
            cat_stats["correct"] += 1

        # Note: Saving happens after a session or explicit action, not every question

    def select_question(self, category_filter=None):
        """Select a question, optionally filtered, avoiding recent repeats and using weighting."""
        possible_indices = [
            idx for idx, q in enumerate(self.questions)
            if (category_filter is None or q[3] == category_filter)
        ]

        if not possible_indices:
            # Use COLOR_WARNING for potentially problematic situations
            print(f"{COLOR_WARNING} No questions found for filter: {category_filter} {COLOR_RESET}")
            return None, -1

        available_indices = [idx for idx in possible_indices if idx not in self.answered_indices_session]

        # If all questions in the category/filter have been answered this session, reset for that filter
        if not available_indices and possible_indices:
            print(f"{COLOR_INFO} All questions in this category/filter answered this session. Resetting session list for this filter. {COLOR_RESET}")
            # Keep indices from other categories, remove those matching the current filter
            self.answered_indices_session = [idx for idx in self.answered_indices_session if idx not in possible_indices]
            available_indices = possible_indices # Try again with all possible indices for this filter

        if not available_indices:
             # This indicates no questions are left even after reset (should only happen if possible_indices was empty initially)
             # print(f"{COLOR_INFO} No available questions left for this filter in this session. {COLOR_RESET}") # More informative message
             return None, -1 # Return None to signal end of questions for this filter

        # --- Weighting Logic ---
        weights = []
        indices_for_weighting = []
        for q_idx in available_indices:
            # Use the actual question text (index 0) as the key for history
            q_text = self.questions[q_idx][0]
            q_stats = self.study_history.get("questions", {}).get(q_text, {"correct": 0, "attempts": 0})
            attempts = q_stats.get("attempts", 0)
            correct = q_stats.get("correct", 0)
            # Avoid division by zero; treat 0 attempts as 50% accuracy for weighting
            accuracy = (correct / attempts) if attempts > 0 else 0.5
            # Weight: higher for incorrect, higher for less attempted
            # Increased weight for incorrect answers, moderate weight for less attempted
            weight = (1.0 - accuracy) * 10 + (1.0 / (attempts + 1)) * 3
            weights.append(max(0.1, weight)) # Ensure a minimum weight
            indices_for_weighting.append(q_idx)

        chosen_original_index = -1
        if not indices_for_weighting or not weights or len(weights) != len(indices_for_weighting):
            # Use COLOR_WARNING as it's falling back, not necessarily a fatal error
            print(f"{COLOR_WARNING} Weighting error or no questions to weight. Falling back to random choice. {COLOR_RESET}")
            if available_indices: # Ensure there's something to choose from
                 chosen_original_index = random.choice(available_indices)
        else:
            try:
                # Use random.choices (plural) which returns a list, take the first element
                chosen_original_index = random.choices(indices_for_weighting, weights=weights, k=1)[0]
            except (IndexError, ValueError) as e:
                 # Use COLOR_WARNING as it's falling back
                 print(f"{COLOR_WARNING} Weighted choice error: {e}. Falling back to random choice. {COLOR_RESET}")
                 if available_indices: # Ensure there's something to choose from
                     chosen_original_index = random.choice(available_indices)

        if chosen_original_index != -1:
            self.answered_indices_session.append(chosen_original_index)
            chosen_question = self.questions[chosen_original_index]
            return chosen_question, chosen_original_index
        else:
            # Use COLOR_ERROR as selecting a question failed
            print(f"{COLOR_ERROR} Failed to select a question index. {COLOR_RESET}")
            return None, -1


    def display_question(self, question_data, question_num=None, total_questions=None):
        """Display the question and options with enhanced CLI formatting."""
        question_text, options, _, category, _ = question_data
        cli_print_separator(char='~', color=COLOR_CATEGORY)
        header_info = f"Category: {COLOR_OPTIONS}{category}{COLOR_RESET}" # Apply color to category name
        if question_num is not None and total_questions is not None:
             # Display like "Question: 5 / 12"
             header_info += f"{COLOR_CATEGORY}  |  Question: {COLOR_STATS_VALUE}{question_num}{COLOR_CATEGORY} / {COLOR_STATS_VALUE}{total_questions}{COLOR_RESET}"
        print(f"{COLOR_CATEGORY}{header_info}{COLOR_RESET}")
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
                    # Use COLOR_INFO for user guidance
                    print(f"{COLOR_INFO} Invalid choice. Please enter a number between 1 and {num_options}. {COLOR_RESET}")
            except ValueError:
                 # Use COLOR_INFO for user guidance
                print(f"{COLOR_INFO} Invalid input. Please enter a number, 's', or 'q'. {COLOR_RESET}")
            except EOFError:
                 # Use COLOR_ERROR for unexpected termination
                 print(f"\n{COLOR_ERROR} Input interrupted. Exiting session. {COLOR_RESET}")
                 return 'q' # Treat EOF as quit

    def show_feedback(self, question_data, user_answer_index, original_index):
        """Show feedback based on the user's answer with enhanced CLI formatting."""
        question_text, options, correct_answer_index, category, explanation = question_data
        # Use the original question text from the loaded list for history consistency
        original_question_text = self.questions[original_index][0]
        is_correct = (user_answer_index == correct_answer_index)

        print() # Add spacing before feedback
        if is_correct:
            print(f"{COLOR_CORRECT}>>> Correct! \U0001F389 <<<{COLOR_RESET}")
            self.score += 1
        else:
            correct_option_text = options[correct_answer_index]
            print(f"{COLOR_INCORRECT}>>> Incorrect! \U0001F61E <<<")
            print(f"{COLOR_INCORRECT}    Your answer:      {COLOR_OPTION_NUM}{user_answer_index + 1}.{COLOR_RESET} {COLOR_OPTIONS}{options[user_answer_index]}{COLOR_RESET}")
            print(f"{COLOR_CORRECT}    Correct answer was: {COLOR_OPTION_NUM}{correct_answer_index + 1}.{COLOR_RESET} {COLOR_OPTIONS}{correct_option_text}{COLOR_RESET}")
            if explanation:
                 print(f"\n{C['bold']}Explanation:{COLOR_RESET}")
                 # Indent explanation for clarity
                 explanation_lines = explanation.split('\n')
                 for line in explanation_lines:
                     print(f"  {COLOR_EXPLANATION}{line}{COLOR_RESET}")


        # Update history using the original question text key
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
        # Filter out categories with 0 attempts before sorting
        sorted_categories = sorted(
            [(cat, stats) for cat, stats in categories_data.items() if stats.get("attempts", 0) > 0],
            key=lambda item: item[0] # Sort by category name
        )


        if not sorted_categories:
            print(f"  {COLOR_EXPLANATION}No category data recorded yet (or no attempts made).{COLOR_RESET}")
        else:
            # Calculate max_len based only on categories with attempts
            max_len = max((len(cat) for cat, stats in sorted_categories), default=10)
            header = f"  {COLOR_STATS_LABEL}{'Category'.ljust(max_len)} │ {'Correct'.rjust(7)} │ {'Attempts'.rjust(8)} │ {'Accuracy'.rjust(9)}{COLOR_RESET}"
            print(header)
            print(f"  {COLOR_BORDER}{'-' * max_len}─┼─────────┼──────────┼──────────{COLOR_RESET}") # Use box drawing chars
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0) # Should be > 0 due to filtering
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) # No need for zero check here
                acc_color = COLOR_STATS_ACC_GOOD if cat_accuracy >= 75 else (COLOR_STATS_ACC_AVG if cat_accuracy >= 50 else COLOR_STATS_ACC_BAD)
                print(f"  {category.ljust(max_len)} │ {COLOR_STATS_VALUE}{str(cat_correct).rjust(7)}{COLOR_RESET} │ {COLOR_STATS_VALUE}{str(cat_attempts).rjust(8)}{COLOR_RESET} │ {acc_color}{f'{cat_accuracy:.1f}%'.rjust(9)}{COLOR_RESET}")

        # Performance on Specific Questions
        print(f"\n{COLOR_SUBHEADER}Performance on Specific Questions (All History):{COLOR_RESET}")
        question_stats = history.get("questions", {})
        # Filter out questions with 0 attempts before sorting
        attempted_questions = {q: stats for q, stats in question_stats.items() if stats.get("attempts", 0) > 0}

        if not attempted_questions:
            print(f"  {COLOR_EXPLANATION}No specific question data recorded yet (or no attempts made).{COLOR_RESET}")
        else:
            # Sort questions by accuracy (lowest first) then attempts (highest first)
            def sort_key(item):
                q_text, stats = item
                attempts = stats.get("attempts", 0) # Should be > 0
                correct = stats.get("correct", 0)
                accuracy = correct / attempts # No zero check needed
                return (accuracy, -attempts) # Sort by accuracy ascending, then attempts descending

            sorted_questions = sorted(attempted_questions.items(), key=sort_key)

            print(f"  {COLOR_STATS_LABEL}Showing questions sorted by lowest accuracy first:{COLOR_RESET}")
            for i, (q_text, stats) in enumerate(sorted_questions):
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                accuracy = (correct / attempts * 100) # No zero check needed
                acc_color = COLOR_STATS_ACC_GOOD if accuracy >= 75 else (COLOR_STATS_ACC_AVG if accuracy >= 50 else COLOR_STATS_ACC_BAD)

                last_result = "N/A"
                last_color = COLOR_EXPLANATION
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_color = COLOR_CORRECT if last_correct else COLOR_INCORRECT

                display_text = (q_text[:75] + '...') if len(q_text) > 75 else q_text
                print(f"\n  {COLOR_QUESTION}{i+1}. \"{display_text}\"{COLOR_RESET}")
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
            return None # Indicate no category selected

        print(f"\n{COLOR_OPTIONS}Available Categories:{COLOR_RESET}")
        print(f"  {COLOR_OPTION_NUM}0.{COLOR_RESET} {COLOR_OPTIONS}All Categories{COLOR_RESET}")
        for i, category in enumerate(sorted_categories):
            print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_OPTIONS}{category}{COLOR_RESET}")
        print()

        while True:
            try:
                prompt = f"{COLOR_PROMPT}Enter category number ({COLOR_OPTION_NUM}0-{len(sorted_categories)}{COLOR_PROMPT}), or '{COLOR_INFO}b{COLOR_PROMPT}' to go back: {COLOR_INPUT}"
                choice = input(prompt).lower().strip()
                print(COLOR_RESET, end='') # Reset color
                if choice == 'b': return 'b' # Special value for 'back'
                num_choice = int(choice)
                if num_choice == 0: return None # None represents 'All Categories'
                elif 1 <= num_choice <= len(sorted_categories):
                    return sorted_categories[num_choice - 1] # Return the category name
                else:
                    print(f"{COLOR_INFO} Invalid choice. {COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_INFO} Invalid input. Please enter a number or 'b'. {COLOR_RESET}")
            except EOFError:
                 print(f"\n{COLOR_ERROR} Input interrupted. Returning to main menu. {COLOR_RESET}")
                 return 'b' # Treat EOF as back

    def clear_stats(self):
        """Clear all stored statistics after confirmation with enhanced CLI."""
        self.clear_screen()
        cli_print_header("Clear Statistics", char='!', color=COLOR_ERROR)
        print(f"\n{COLOR_WARNING} This action will permanently delete ALL study history,")
        print(f"{COLOR_WARNING} including question performance and the list of incorrect answers.")
        print(f"{COLOR_WARNING} This cannot be undone. {COLOR_RESET}")
        confirm = input(f"{COLOR_PROMPT}Are you sure you want to proceed? ({COLOR_OPTIONS}yes{COLOR_PROMPT}/{COLOR_OPTIONS}no{COLOR_PROMPT}): {COLOR_INPUT}").lower().strip()
        print(COLOR_RESET, end='') # Reset color

        if confirm == 'yes':
            self.study_history = self._default_history()
            # Re-populate categories with 0 stats
            for category in self.categories:
                 self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.save_history()
            print(f"\n{COLOR_CORRECT}>>> Study history has been cleared. <<<{COLOR_RESET}")
        else:
            print(f"\n{COLOR_INFO}Operation cancelled. History not cleared.{COLOR_RESET}")

        print()
        input(f"{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def run_quiz(self, category_filter=None, mode=QUIZ_MODE_STANDARD):
        """Run the main quiz loop for the CLI with enhanced display and modes."""
        self.score = 0
        self.total_questions_session = 0 # Reset session counter
        self.answered_indices_session = []
        self.verify_session_answers = [] # Clear verify answers for new session

        quiz_title = "Quiz Mode"
        if mode == QUIZ_MODE_VERIFY:
            quiz_title = "Verify Knowledge Mode"
            self.clear_screen()
            cli_print_header("VERIFY YOUR KNOWLEDGE", char='*', length=60, color=COLOR_HEADER)
            verify_intro = [
                "",
                "This mode will test your knowledge and verify your answers.",
                "You won't be told if you're right or wrong until the end.",
                "",
                "Ready?",
            ]
            cli_print_box(verify_intro, width=60, border_color=COLOR_BORDER, text_color=COLOR_INFO)
            input(f"{COLOR_PROMPT}Press Enter to start...{COLOR_RESET}")

        # --- Calculate total questions for the current filter ---
        if category_filter is None:
            # If no filter, total is all questions
            total_questions_in_filter = len(self.questions)
        else:
            # Count questions matching the filter
            total_questions_in_filter = sum(1 for q in self.questions if q[3] == category_filter)

        if total_questions_in_filter == 0:
             print(f"{COLOR_WARNING}Warning: No questions found for the selected filter: {category_filter}. Returning to menu.{COLOR_RESET}")
             time.sleep(3)
             # No need to proceed if there are no questions
             self.save_history() # Save history before returning
             # No need for input prompt here as we are exiting the function
             return # Exit run_quiz function

        question_count = 0 # Tracks the number displayed (1-based)
        while True:
            self.clear_screen()
            category_display = category_filter if category_filter else "All Categories"
            session_header = f"{quiz_title}: {category_display}"
            cli_print_header(session_header)

            # Display score differently based on mode
            if mode == QUIZ_MODE_STANDARD:
                # Show score based on questions *answered* so far
                print(f"{COLOR_STATS_LABEL}Session Score: {COLOR_STATS_VALUE}{self.score} / {self.total_questions_session}{COLOR_RESET}\n")
            else: # Verify mode
                # Show number of questions *answered* so far
                print(f"{COLOR_STATS_LABEL}Questions Answered: {COLOR_STATS_VALUE}{self.total_questions_session}{COLOR_RESET}\n")


            question_data, original_index = self.select_question(category_filter)


            if question_data is None:
                 # This now correctly indicates no more *available* questions for this filter/session
                 print(f"{COLOR_INFO} No more questions available in this filter for this session. Ending session. {COLOR_RESET}")
                 time.sleep(3)
                 break # Exit the while loop

            question_count += 1 # Increment display count only if a question was successfully selected
            # --- Pass the calculated total ---
            self.display_question(question_data, question_num=question_count, total_questions=total_questions_in_filter)

            user_answer = self.get_user_answer(len(question_data[1])) # question_data[1] is the options list

            if user_answer == 'q':
                break # Exit the while loop
            elif user_answer == 's':
                print(f"\n{COLOR_INFO}Skipping question...{COLOR_RESET}")
                # Skipping does NOT increment total_questions_session (answered count)
                # It also doesn't update history
                input(f"\n{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
                continue # Go to next iteration of the while loop

            # --- Process Answer (Only if not skipped or quit) ---
            question_text, _, correct_answer_index, category, _ = question_data
            original_question_text = self.questions[original_index][0] # Use the canonical text
            is_correct = (user_answer == correct_answer_index)

            # Update history and session *answered* count
            self.update_history(original_question_text, category, is_correct)
            # self.total_questions_session is updated within show_feedback or here for verify mode

            if mode == QUIZ_MODE_STANDARD:
                # show_feedback updates total_questions_session internally
                self.show_feedback(question_data, user_answer, original_index) # Shows feedback immediately
            else: # QUIZ_MODE_VERIFY
                # Store the result, don't show feedback yet
                self.verify_session_answers.append((question_data, user_answer, is_correct))
                # Manually update session answered count for verify mode
                self.total_questions_session += 1
                print(f"\n{COLOR_INFO}Answer recorded. Next question...{COLOR_RESET}")
                time.sleep(1) # Brief pause before clearing screen

        # --- End of Session ---
        print(f"\n{COLOR_HEADER}Quiz session finished.{COLOR_RESET}")

        if mode == QUIZ_MODE_STANDARD:
             if self.total_questions_session > 0: # Avoid division by zero if no questions were answered
                 accuracy = (self.score / self.total_questions_session * 100)
                 acc_color = COLOR_STATS_ACC_GOOD if accuracy >= 75 else (COLOR_STATS_ACC_AVG if accuracy >= 50 else COLOR_STATS_ACC_BAD)
                 print(f"{COLOR_STATS_LABEL}Your final score for this session: {COLOR_STATS_VALUE}{self.score} / {self.total_questions_session}{COLOR_RESET} ({acc_color}{accuracy:.1f}%{COLOR_RESET})")
             else:
                 print(f"{COLOR_STATS_LABEL}No questions were answered in this session.{COLOR_RESET}")
        elif mode == QUIZ_MODE_VERIFY:
            self.show_verify_results() # This displays the results

        self.save_history() # Save history at the end of the session
        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")


    def show_verify_results(self):
        """Displays the results after a 'Verify Knowledge' session."""
        self.clear_screen()
        cli_print_header("Verification Results")

        if not self.verify_session_answers:
            print(f"{COLOR_INFO}No questions were answered in this verification session.{COLOR_RESET}")
            return

        num_correct = sum(1 for _, _, is_correct in self.verify_session_answers if is_correct)
        total_answered = len(self.verify_session_answers)
        accuracy = (num_correct / total_answered * 100) if total_answered > 0 else 0
        acc_color = COLOR_STATS_ACC_GOOD if accuracy >= 75 else (COLOR_STATS_ACC_AVG if accuracy >= 50 else COLOR_STATS_ACC_BAD)

        print(f"\n{COLOR_SUBHEADER}Session Summary:{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Total Questions Answered:{COLOR_RESET} {COLOR_STATS_VALUE}{total_answered}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Correct Answers:         {COLOR_RESET} {COLOR_STATS_VALUE}{num_correct}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Accuracy:                {COLOR_RESET} {acc_color}{accuracy:.2f}%{COLOR_RESET}\n")
        cli_print_separator()

        print(f"\n{COLOR_SUBHEADER}Detailed Review:{COLOR_RESET}")
        for i, (q_data, user_answer_idx, is_correct) in enumerate(self.verify_session_answers):
            q_text, options, correct_idx, _, explanation = q_data
            print(f"\n{COLOR_QUESTION}{i+1}. {q_text}{COLOR_RESET}")
            user_choice_text = options[user_answer_idx]
            correct_choice_text = options[correct_idx]

            if is_correct:
                print(f"  {COLOR_CORRECT}Your answer: {user_answer_idx+1}. {user_choice_text} (Correct! \U0001F389){COLOR_RESET}")
            else:
                print(f"  {COLOR_INCORRECT}Your answer: {user_answer_idx+1}. {user_choice_text} (Incorrect \U0001F61E){COLOR_RESET}")
                print(f"  {COLOR_CORRECT}Correct answer: {correct_idx+1}. {correct_choice_text}{COLOR_RESET}")
                if explanation:
                    print(f"  {C['bold']}Explanation:{COLOR_RESET}")
                    explanation_lines = explanation.split('\n')
                    for line in explanation_lines:
                        print(f"    {COLOR_EXPLANATION}{line}{COLOR_RESET}")
            cli_print_separator(char='.', length=50, color=COLOR_BORDER + C["dim"])


    def review_incorrect_answers(self):
        """Allows the user to review questions they previously answered incorrectly (CLI - Basic View)."""
        self.clear_screen()
        cli_print_header("Review Incorrect Answers")
        incorrect_list = self.study_history.get("incorrect_review", [])

        if not incorrect_list:
            print(f"\n{COLOR_INFO}You haven't marked any questions as incorrect yet, or your history was cleared.{COLOR_RESET}")
            print(f"{COLOR_INFO}Keep practicing!{COLOR_RESET}")
            input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
            return

        # Find the full question data based on the text stored in incorrect_review
        questions_to_review = []
        not_found_questions = []
        # Create a temporary copy to iterate over, allowing removal from original
        incorrect_list_copy = list(incorrect_list)
        for incorrect_text in incorrect_list_copy:
            found = False
            for q_data in self.questions:
                if q_data[0] == incorrect_text:
                    questions_to_review.append(q_data)
                    found = True
                    break
            if not found:
                 not_found_questions.append(incorrect_text)
                 print(f"{COLOR_WARNING} Could not find full data for question: {incorrect_text[:50]}... (Maybe removed from source?){COLOR_RESET}")
                 # Remove from the actual history list if not found in current questions
                 if incorrect_text in self.study_history["incorrect_review"]:
                     self.study_history["incorrect_review"].remove(incorrect_text)


        if not questions_to_review:
             print(f"\n{COLOR_ERROR} Could not load data for any incorrect questions. {COLOR_RESET}")
             self.save_history() # Save history if items were removed
             input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
             return

        # --- Interactive Review Loop ---
        current_choice = '' # Define outside the loop for the final check
        while True:
            self.clear_screen()
            cli_print_header("Review Incorrect Answers")
            print(f"\n{COLOR_OPTIONS}Select a question to review (displays info):{COLOR_RESET}")
            if not questions_to_review: # Check if list became empty during loop
                 print(f"\n{COLOR_INFO}All incorrect questions cleared from review.{COLOR_RESET}")
                 time.sleep(2)
                 break # Exit loop if list is now empty

            for i, q_data in enumerate(questions_to_review):
                 q_text_short = (q_data[0][:60] + '...') if len(q_data[0]) > 60 else q_data[0]
                 print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_OPTIONS}{q_text_short}{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}c.{COLOR_RESET} {COLOR_WARNING}Clear an item from this review list{COLOR_RESET} (Enter 'c' then the number)")

            try:
                prompt = f"\n{COLOR_PROMPT}Enter question number ({COLOR_OPTION_NUM}1-{len(questions_to_review)}{COLOR_PROMPT}), '{COLOR_INFO}c[num]{COLOR_PROMPT}' to clear, or '{COLOR_INFO}b{COLOR_PROMPT}' to go back: {COLOR_INPUT}"
                choice = input(prompt).lower().strip()
                current_choice = choice # Store the latest choice
                print(COLOR_RESET, end='')

                if choice == 'b':
                    break # Exit the review loop

                clear_mode = False
                item_to_clear = -1
                if choice.startswith('c') and len(choice) > 1:
                    try:
                        item_to_clear = int(choice[1:]) -1 # Get number after 'c' (0-based)
                        if 0 <= item_to_clear < len(questions_to_review):
                            clear_mode = True
                        else:
                            print(f"{COLOR_INFO} Invalid number after 'c'. {COLOR_RESET}")
                            time.sleep(1.5)
                            continue
                    except ValueError:
                        print(f"{COLOR_INFO} Invalid format for clear. Use 'c' followed by the number (e.g., c3). {COLOR_RESET}")
                        time.sleep(1.5)
                        continue

                if clear_mode:
                    question_to_clear_text = questions_to_review[item_to_clear][0]
                    confirm_clear = input(f"{COLOR_PROMPT}Clear question {item_to_clear+1} from the incorrect review list? ({COLOR_OPTIONS}yes{COLOR_PROMPT}/{COLOR_OPTIONS}no{COLOR_PROMPT}): {COLOR_INPUT}").lower().strip()
                    if confirm_clear == 'yes':
                        if question_to_clear_text in self.study_history["incorrect_review"]:
                             self.study_history["incorrect_review"].remove(question_to_clear_text)
                             self.save_history()
                             print(f"{COLOR_CORRECT}Question removed from review list.{COLOR_RESET}")
                             # Remove from the current display list as well
                             del questions_to_review[item_to_clear]
                             # No need to break here, loop will re-check list emptiness
                             time.sleep(1.5)
                        else:
                             print(f"{COLOR_ERROR}Error: Question text not found in history's incorrect list anymore?{COLOR_RESET}")
                             # Also remove from display list if it's somehow missing from history
                             del questions_to_review[item_to_clear]
                             time.sleep(2)
                    else:
                        print(f"{COLOR_INFO}Clear cancelled.{COLOR_RESET}")
                        time.sleep(1)
                    continue # Go back to list display


                # --- Display selected question ---
                num_choice = int(choice)
                if 1 <= num_choice <= len(questions_to_review):
                    self.clear_screen()
                    cli_print_header("Reviewing Question")
                    selected_q_data = questions_to_review[num_choice-1]
                    q_text, options, correct_idx, category, explanation = selected_q_data
                    print(f"{COLOR_CATEGORY}Category: {category}{COLOR_RESET}\n")
                    print(f"{COLOR_QUESTION}Q: {q_text}{COLOR_RESET}\n")
                    for i, option in enumerate(options):
                         prefix = f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} "
                         if i == correct_idx:
                             print(f"{prefix}{COLOR_CORRECT}{option} (Correct Answer){COLOR_RESET}")
                         else:
                             print(f"{prefix}{COLOR_OPTIONS}{option}{COLOR_RESET}")
                    if explanation:
                         print(f"\n{C['bold']}Explanation:{COLOR_RESET}")
                         explanation_lines = explanation.split('\n')
                         for line in explanation_lines:
                             print(f"  {COLOR_EXPLANATION}{line}{COLOR_RESET}")
                    cli_print_separator()
                    input(f"\n{COLOR_PROMPT}Press Enter to return to the review list...{COLOR_RESET}")
                    # Loop continues, will re-display the list

                else:
                    print(f"{COLOR_INFO} Invalid choice. {COLOR_RESET}")
                    time.sleep(1.5)

            except ValueError:
                print(f"{COLOR_INFO} Invalid input. Please enter a number, 'c[num]', or 'b'. {COLOR_RESET}")
                time.sleep(1.5)
            except EOFError:
                print(f"\n{COLOR_ERROR} Input interrupted. Returning to main menu. {COLOR_RESET}")
                current_choice = 'b' # Treat EOF as back
                break # Exit loop on EOF

        # Final prompt only if the loop wasn't exited by 'b' or EOF and list wasn't empty
        # if current_choice != 'b' and questions_to_review: # Check if list is non-empty
        #      input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        # Save history in case items were removed due to not being found
        self.save_history()


    def export_study_data(self):
        """Exports study data (Basic JSON export)."""
        self.clear_screen()
        cli_print_header("Export Study Data")

        default_filename = f"linux_plus_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        prompt = f"{COLOR_PROMPT}Enter filename for export ({COLOR_INFO}default: {default_filename}{COLOR_PROMPT}): {COLOR_INPUT}"
        filename_input = input(prompt).strip()
        print(COLOR_RESET, end='')

        export_filename = filename_input if filename_input else default_filename

        # Basic validation
        if not export_filename.endswith(".json"):
             export_filename += ".json"

        try:
            export_path = os.path.abspath(export_filename) # Get full path
            print(f"\n{COLOR_INFO}Attempting to export data to: {COLOR_STATS_VALUE}{export_path}{COLOR_RESET}")
            with open(export_filename, 'w') as f:
                json.dump(self.study_history, f, indent=2)
            print(f"\n{COLOR_CORRECT}>>> Study data successfully exported to {export_filename} <<<{COLOR_RESET}")
        except IOError as e:
            print(f"\n{COLOR_ERROR}Error exporting data: {e}{COLOR_RESET}")
            print(f"{COLOR_ERROR}Please check permissions and filename.{COLOR_RESET}")
        except Exception as e:
             print(f"\n{COLOR_ERROR}An unexpected error occurred during export: {e}{COLOR_RESET}")


        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def display_welcome_message(self):
        """Displays the initial welcome screen for the CLI."""
        self.clear_screen()
        title = "LINUX+ STUDY GAME"
        welcome_lines = [
            "",
            "Welcome to the CompTIA Linux+ Study Game!",
            "",
            "Test your knowledge with multiple-choice questions.",
            "Choose between:",
            f"  - {COLOR_OPTIONS}Standard Quiz{COLOR_WELCOME_TEXT} (Immediate feedback)",
            f"  - {COLOR_OPTIONS}Verify Knowledge{COLOR_WELCOME_TEXT} (Feedback at the end)",
            "",
            "Track your progress with statistics and review incorrect answers.",
            ""
        ]
        cli_print_box(welcome_lines, title=title, width=60, border_color=COLOR_WELCOME_BORDER, title_color=COLOR_WELCOME_TITLE, text_color=COLOR_WELCOME_TEXT)
        input(f"{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")


    def main_menu(self):
        """Display the main menu and handle user choices for CLI."""
        while True:
            self.clear_screen()
            cli_print_header("MAIN MENU", char='*', length=60) # Use specified header style
            print(f"\n{COLOR_OPTIONS}Please choose an option:{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}1.{COLOR_RESET} {COLOR_OPTIONS}Start Quiz (Standard){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}2.{COLOR_RESET} {COLOR_OPTIONS}Quiz by Category (Standard){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}3.{COLOR_RESET} {COLOR_OPTIONS}Verify Knowledge (Category/All){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}4.{COLOR_RESET} {COLOR_OPTIONS}Review Incorrect Answers{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}5.{COLOR_RESET} {COLOR_OPTIONS}View Statistics{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}6.{COLOR_RESET} {COLOR_OPTIONS}Export Study Data{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}7.{COLOR_RESET} {COLOR_OPTIONS}Exit{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}8.{COLOR_RESET} {COLOR_WARNING}Clear All Statistics{COLOR_RESET}") # Keep warning color
            cli_print_separator(color=COLOR_BORDER)

            choice = input(f"{COLOR_PROMPT}Enter your choice: {COLOR_INPUT}")
            print(COLOR_RESET, end='') # Reset color

            if choice == '1':
                self.run_quiz(category_filter=None, mode=QUIZ_MODE_STANDARD)
            elif choice == '2':
                selected_category = self.select_category()
                if selected_category != 'b': # Proceed if not 'back'
                    self.run_quiz(category_filter=selected_category, mode=QUIZ_MODE_STANDARD)
            elif choice == '3':
                # Verify knowledge mode - ask for category or all
                selected_category = self.select_category() # Reuse category selection
                if selected_category != 'b':
                    self.run_quiz(category_filter=selected_category, mode=QUIZ_MODE_VERIFY)
            elif choice == '4':
                self.review_incorrect_answers() # Call the review function
            elif choice == '5':
                self.show_stats()
            elif choice == '6':
                self.export_study_data() # Call the export function
            elif choice == '7':
                print(f"\n{COLOR_INFO}Saving history and quitting. Goodbye!{COLOR_RESET}")
                self.save_history()
                sys.exit()
            elif choice == '8':
                self.clear_stats()
            else:
                print(f"{COLOR_INFO} Invalid choice. Please try again. {COLOR_RESET}")
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
        self.current_quiz_mode = QUIZ_MODE_STANDARD # Default mode
        self.gui_verify_session_answers = [] # For storing answers in GUI verify mode
        self.total_questions_in_filter_gui = 0 # Store total for GUI display
        self.questions_answered_in_session_gui = 0 # Track answered count for GUI status

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
            "button_disabled_bg": "#3C3F41", # Match widget bg for disabled button
            "correct": "#6A8759",     # Muted green
            "incorrect": "#AC4142",   # Muted red
            "explanation_bg": "#313335", # Dark background for explanation text widget
            "border": "#555555",
            "disabled_fg": "#888888", # Grey for disabled text
            "status_fg": "#BBBBBB",
            "category_fg": "#808080", # Grey for category
            "dim": "#888888",
            "welcome_title": "#FFC66D", # Use accent for welcome title
            "welcome_text": "#D3D3D3", # Use standard fg for welcome text
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
            "welcome_title": tkFont.Font(family="Segoe UI", size=14, weight="bold"),
            "welcome_text": tkFont.Font(family="Segoe UI", size=11),
        }
        self._setup_styles()
        self._setup_ui()
        self._load_initial_state() # Display welcome message

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
                             padding=(10, 5),
                             background=self.colors["button"],
                             foreground=self.colors["button_fg"],
                             borderwidth=1,
                             bordercolor=self.colors["border"],
                             relief="flat")
        self.style.map("TButton",
                       background=[('disabled', self.colors["button_disabled_bg"]),
                                   ('active', self.colors["button_hover"]),
                                   ('!disabled', self.colors["button"])],
                       foreground=[('disabled', self.colors["disabled_fg"])])

        self.style.configure("Accent.TButton", # For Submit/Next/Start
                             background=self.colors["accent"],
                             foreground=self.colors["bg"],
                             font=self.fonts["button"])
        self.style.map("Accent.TButton",
                       background=[('disabled', self.colors["button_disabled_bg"]),
                                   ('active', self.colors["accent_dark"]),
                                   ('!disabled', self.colors["accent"])],
                       foreground=[('disabled', self.colors["disabled_fg"])])

        # --- Radiobutton Styling ---
        self.style.configure("TRadiobutton",
                             background=self.colors["bg_widget"],
                             foreground=self.colors["fg"],
                             font=self.fonts["option"],
                             indicatorrelief=tk.FLAT,
                             indicatormargin=5,
                             padding=(5, 3))
        self.style.map("TRadiobutton",
                       background=[('selected', self.colors["bg_widget"]), ('active', self.colors["bg_widget"])],
                       # Use a subtle indicator color change on selection
                       indicatorbackground=[('selected', self.colors["accent"]), ('!selected', self.colors["border"])],
                       foreground=[('disabled', self.colors["disabled_fg"])])

        # --- Feedback Label Styling ---
        self.style.configure("Feedback.TLabel", font=self.fonts["feedback"], padding=5)
        self.style.configure("Correct.Feedback.TLabel", foreground=self.colors["correct"])
        self.style.configure("Incorrect.Feedback.TLabel", foreground=self.colors["incorrect"])
        self.style.configure("Info.Feedback.TLabel", foreground=self.colors["status_fg"]) # For verify mode

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
        self.root.geometry("950x800") # Slightly larger window
        self.root.configure(bg=self.colors["bg"])
        self.root.minsize(750, 650) # Minimum size

        # --- Main Frame with Padding ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1) # Make content area expand
        main_frame.rowconfigure(1, weight=1)    # Make quiz area expand

        # --- Header ---
        header_frame = ttk.Frame(main_frame, padding=(0, 0, 0, 15))
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15)) # Span 2 cols
        header_frame.columnconfigure(1, weight=1) # Allow status label area to expand

        ttk.Label(header_frame, text="Linux+ Study Game", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        # Frame for status and question count
        status_count_frame = ttk.Frame(header_frame)
        status_count_frame.grid(row=0, column=1, sticky="e")

        self.question_count_label = ttk.Label(status_count_frame, text="", style="Status.TLabel")
        self.question_count_label.pack(side=tk.RIGHT, padx=(10,0))

        self.status_label = ttk.Label(status_count_frame, text="Status: Idle", style="Status.TLabel")
        self.status_label.pack(side=tk.RIGHT, padx=(0, 10))


        # --- Quiz Area Frame (Content Area) ---
        # Use a standard tk.Frame for the border effect
        quiz_frame_outer = tk.Frame(main_frame, bg=self.colors["border"], bd=1, relief="solid")
        quiz_frame_outer.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10) # Span 2 cols
        quiz_frame_outer.columnconfigure(0, weight=1)
        quiz_frame_outer.rowconfigure(0, weight=1) # Make inner frame expand

        quiz_frame = ttk.Frame(quiz_frame_outer, padding="20", style="TFrame")
        quiz_frame.grid(row=0, column=0, sticky="nsew")
        quiz_frame.columnconfigure(0, weight=1)
        # Configure rows for expansion: Question(1), Options(2), Feedback/Explanation(3)
        quiz_frame.rowconfigure(1, weight=2) # Question text gets more weight
        quiz_frame.rowconfigure(2, weight=1) # Options area
        quiz_frame.rowconfigure(3, weight=2) # Feedback/Explanation area gets more weight

        # Category Label
        self.category_label = ttk.Label(quiz_frame, text="", style="Category.TLabel")
        self.category_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Question Text (Scrollable Text Widget)
        self.question_text = scrolledtext.ScrolledText(quiz_frame, wrap=tk.WORD, height=6,
                                     font=self.fonts["question"], relief="flat",
                                     bg=self.colors["bg_widget"], fg=self.colors["fg"],
                                     bd=0, state=tk.DISABLED,
                                     padx=10, pady=10,
                                     selectbackground=self.colors["accent"],
                                     selectforeground=self.colors["bg"])
        self.question_text.grid(row=1, column=0, sticky="nsew", pady=5)
        try:
            self.question_text.vbar.configure(style="Vertical.TScrollbar")
        except tk.TclError:
            print("Note: Could not apply custom style to ScrolledText scrollbar.")


        # Options Frame (Radio Buttons will be added dynamically)
        self.options_frame = ttk.Frame(quiz_frame, padding=(0, 15, 0, 10), style="TFrame")
        self.options_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        self.options_frame.columnconfigure(0, weight=1)

        # Feedback & Explanation Area (Combined Frame)
        feedback_exp_frame = ttk.Frame(quiz_frame, style="TFrame")
        feedback_exp_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 5))
        feedback_exp_frame.columnconfigure(0, weight=1)
        feedback_exp_frame.rowconfigure(1, weight=1) # Allow explanation text widget to expand

        self.feedback_label = ttk.Label(feedback_exp_frame, text="", style="Feedback.TLabel", anchor=tk.W, wraplength=600) # Allow wrapping for the label
        self.feedback_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Explanation Text (Scrollable Text Widget)
        self.explanation_text = scrolledtext.ScrolledText(feedback_exp_frame, wrap=tk.WORD, height=4,
                                         font=self.fonts["explanation"], relief="flat",
                                         bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                                         bd=0, state=tk.DISABLED,
                                         padx=10, pady=10,
                                         selectbackground=self.colors["accent"],
                                         selectforeground=self.colors["bg"])
        try:
            self.explanation_text.vbar.configure(style="Vertical.TScrollbar")
        except tk.TclError:
            print("Note: Could not apply custom style to ScrolledText scrollbar.")
        self.explanation_text.grid(row=1, column=0, sticky="nsew", pady=5)
        self.explanation_text.grid_remove() # Hide initially


        # --- Control Frame ---
        control_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0))
        control_frame.grid(row=2, column=0, columnspan=2, sticky="ew") # Span 2 cols
        control_frame.columnconfigure(0, weight=0) # Quiz controls fixed size
        control_frame.columnconfigure(1, weight=1) # Spacer expands
        control_frame.columnconfigure(2, weight=0) # Main actions fixed size

        # Left side (Quiz Controls)
        quiz_controls = ttk.Frame(control_frame)
        quiz_controls.grid(row=0, column=0, sticky="w")
        self.submit_button = ttk.Button(quiz_controls, text="Submit Answer", command=self._submit_answer_gui, state=tk.DISABLED, style="Accent.TButton", width=15)
        self.submit_button.pack(side=tk.LEFT, padx=(0, 10))
        self.next_button = ttk.Button(quiz_controls, text="Next Question", command=self._next_question_gui, state=tk.DISABLED, style="Accent.TButton", width=15)
        self.next_button.pack(side=tk.LEFT)
        self.show_results_button = ttk.Button(quiz_controls, text="Show Results", command=self._show_verify_results_gui, state=tk.DISABLED, style="Accent.TButton", width=15)
        self.show_results_button.pack(side=tk.LEFT, padx=(10, 0))
        self.show_results_button.pack_forget() # Hide initially


        # Right side (Main Actions) - Add new buttons here
        main_actions = ttk.Frame(control_frame)
        main_actions.grid(row=0, column=2, sticky="e") # Use column 2
        ttk.Button(main_actions, text="Start Quiz", command=lambda: self._start_quiz_dialog(QUIZ_MODE_STANDARD), style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Verify Knowledge", command=lambda: self._start_quiz_dialog(QUIZ_MODE_VERIFY), style="TButton").pack(side=tk.LEFT, padx=5)
        # Enable Review Incorrect button (basic functionality added)
        self.review_button = ttk.Button(main_actions, text="Review Incorrect", command=self._review_incorrect_gui, style="TButton")
        self.review_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="View Stats", command=self._show_stats_gui, style="TButton").pack(side=tk.LEFT, padx=5)
        # Enable Export Data button (basic functionality added)
        self.export_button = ttk.Button(main_actions, text="Export Data", command=self._export_data_gui, style="TButton")
        self.export_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Clear Stats", command=self._clear_stats_gui, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Quit", command=self._quit_app, style="TButton").pack(side=tk.LEFT, padx=(5, 0))
        # Initially disable review/export if history is empty? - Let's check in _load_initial_state

    def _load_initial_state(self):
        """Set the initial welcome message and check button states."""
        self._update_status("Ready.")
        self._update_question_count_label() # Clear count label
        self._clear_quiz_area(clear_options=True) # Clear everything initially
        self.category_label.config(text="") # No category initially

        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)

        # Add welcome message with basic formatting
        self.question_text.tag_configure("welcome_title", font=self.fonts["welcome_title"], foreground=self.colors["welcome_title"], justify='center', spacing3=15)
        self.question_text.tag_configure("welcome_body", font=self.fonts["welcome_text"], foreground=self.colors["welcome_text"], justify='center', spacing1=5, lmargin1=20, lmargin2=20) # Add margins

        self.question_text.insert(tk.END, "LINUX+ STUDY GAME\n", "welcome_title")
        self.question_text.insert(tk.END, "Welcome to the CompTIA Linux+ Study Game!\n\n", "welcome_body")
        self.question_text.insert(tk.END, "This game will test your knowledge with questions similar to those you might encounter on the CompTIA Linux+ certification exam.\n\n", "welcome_body")
        self.question_text.insert(tk.END, "Use the buttons below to start a standard quiz, verify your knowledge (feedback delayed), view statistics, or manage your study data.\n\n", "welcome_body")
        self.question_text.insert(tk.END, "Let's get started!", "welcome_body")

        self.question_text.config(state=tk.DISABLED)

        # Ensure quiz control buttons are initially disabled
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.show_results_button.pack_forget() # Ensure hidden

        # Enable/Disable Review/Export based on history content
        if not self.game_logic.study_history.get("incorrect_review", []):
             self.review_button.config(state=tk.DISABLED)
        else:
             self.review_button.config(state=tk.NORMAL)

        # Export can always be enabled as it exports the current state, even if empty
        self.export_button.config(state=tk.NORMAL)


    def _clear_quiz_area(self, clear_question=True, clear_options=True, clear_feedback=True, clear_explanation=True):
        """Clear specific parts of the quiz area."""
        if clear_question:
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END)
            self.question_text.config(state=tk.DISABLED)
            self.category_label.config(text="") # Clear category too

        if clear_options:
            for widget in self.options_frame.winfo_children():
                widget.destroy() # Destroy all widgets in options frame
            self.selected_answer_var.set(-1) # Reset radio button variable

        if clear_feedback:
            self.feedback_label.config(text="", style="Feedback.TLabel") # Reset style too

        if clear_explanation:
            self.explanation_text.config(state=tk.NORMAL)
            self.explanation_text.delete(1.0, tk.END)
            self.explanation_text.config(state=tk.DISABLED)
            self.explanation_text.grid_remove() # Hide explanation widget

    def _update_status(self, message):
        """Update the status bar label."""
        self.status_label.config(text=f"Status: {message}")

    def _update_question_count_label(self, current=None, total=None):
        """Update the question count label in the header."""
        if current is not None and total is not None:
             self.question_count_label.config(text=f"Question: {current} / {total}")
        else:
             self.question_count_label.config(text="") # Clear if no quiz active

    def _start_quiz_dialog(self, mode):
        """Show dialog to select category and start quiz in the specified mode."""
        self.current_quiz_mode = mode # Set the mode for the upcoming session

        dialog_title = "Start Quiz"
        prompt_text = "Select Category for Standard Quiz:"
        if mode == QUIZ_MODE_VERIFY:
             dialog_title = "Verify Knowledge"
             prompt_text = "Select Category to Verify:"


        dialog = tk.Toplevel(self.root)
        dialog.title(dialog_title)
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors["bg"])

        try:
            dialog.tk_setPalette(background=self.colors["bg"], foreground=self.colors["fg"])
        except tk.TclError:
            print("Warning: Could not set Toplevel palette (might be OS dependent).")


        ttk.Label(dialog, text=prompt_text, font=self.fonts["subheader"],
                  background=self.colors["bg"], foreground=self.colors["fg_header"])\
            .pack(pady=(25, 10))

        categories = ["All Categories"] + sorted(list(self.game_logic.categories))
        category_var = tk.StringVar(value=categories[0])

        menu_style = {"background": self.colors["button"],
                      "foreground": self.colors["button_fg"],
                      "activebackground": self.colors["button_hover"],
                      "activeforeground": self.colors["button_fg"],
                      "font": self.fonts["base"],
                      "relief": "flat", "bd": 0}

        option_menu = ttk.OptionMenu(dialog, category_var, categories[0], *categories, style="TMenubutton")
        option_menu.config(width=35)
        # Apply style to the dropdown menu itself
        try:
             menu = option_menu["menu"]
             menu.config(**menu_style)
        except tk.TclError as e:
            print(f"Warning: Could not configure OptionMenu dropdown: {e}")

        option_menu.pack(pady=15, padx=30)

        def on_start():
            selected = category_var.get()
            self.current_category_filter = None if selected == "All Categories" else selected

            # --- Calculate total questions for the filter (GUI) ---
            if self.current_category_filter is None:
                self.total_questions_in_filter_gui = len(self.game_logic.questions)
            else:
                self.total_questions_in_filter_gui = sum(1 for q in self.game_logic.questions if q[3] == self.current_category_filter)

            if self.total_questions_in_filter_gui == 0:
                 messagebox.showwarning("No Questions", f"No questions found for the selected filter: {self.current_category_filter}.\nPlease select another category or add questions.", parent=self.root) # Show warning in main window
                 dialog.destroy() # Close dialog, but don't start quiz
                 return

            dialog.destroy()
            self._start_quiz_session() # Calls the session starter which knows the mode

        button_frame = ttk.Frame(dialog, style="TFrame")
        button_frame.pack(pady=(20, 25))
        ttk.Button(button_frame, text="Start", command=on_start, style="Accent.TButton", width=12).pack(side=tk.LEFT, padx=15)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy, style="TButton", width=12).pack(side=tk.LEFT, padx=15)

        self.root.wait_window(dialog)

    def _start_quiz_session(self):
        """Begin a new quiz session based on self.current_quiz_mode."""
        self.quiz_active = True
        self.game_logic.score = 0 # Reset score for standard mode
        self.game_logic.total_questions_session = 0 # Reset answered count (logic)
        self.questions_answered_in_session_gui = 0 # Reset answered count (GUI)
        self.game_logic.answered_indices_session = []
        self.gui_verify_session_answers = [] # Clear verify answers
        self.current_question_index = -1

        cat_display = self.current_category_filter or 'All Categories'
        mode_display = "Quiz" if self.current_quiz_mode == QUIZ_MODE_STANDARD else "Verify"
        self._update_status(f"{mode_display} started.")
        self._update_question_count_label(current=0, total=self.total_questions_in_filter_gui) # Show 0 / total

        # Clear previous quiz state visually
        self._clear_quiz_area(clear_question=False, clear_options=True, clear_feedback=True, clear_explanation=True)

        # Show Verify intro if applicable
        if self.current_quiz_mode == QUIZ_MODE_VERIFY:
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END)
            self.question_text.tag_configure("verify_title", font=self.fonts["subheader"], foreground=self.colors["accent"], justify='center', spacing3=10)
            self.question_text.tag_configure("verify_body", font=self.fonts["base"], foreground=self.colors["fg"], justify='center', spacing1=5, lmargin1=20, lmargin2=20)
            self.question_text.insert(tk.END, "VERIFY YOUR KNOWLEDGE\n", "verify_title")
            self.question_text.insert(tk.END, f"Category: {cat_display}\n\n", "verify_body")
            self.question_text.insert(tk.END, "This mode will test your knowledge.\n", "verify_body")
            self.question_text.insert(tk.END, "You won't be told if you're right or wrong until the end.\n\n", "verify_body")
            self.question_text.insert(tk.END, "Click 'Next Question' to begin.", "verify_body")
            self.question_text.config(state=tk.DISABLED)
            self.category_label.config(text=f"Category: {cat_display}") # Show category
            # Enable only the Next button to start
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
            self.show_results_button.pack_forget() # Hide results button
            self.next_button.focus_set()
        else:
            # Start standard quiz immediately
            self._next_question_gui()


    def _display_question_gui(self):
        """Update the GUI with the current question data."""
        if not self.current_question_data:
            # This case handles end of questions for BOTH modes
            self._clear_quiz_area(clear_options=True, clear_feedback=True, clear_explanation=True)
            self.question_text.config(state=tk.NORMAL)
            self.question_text.delete(1.0, tk.END)
            self.question_text.insert(tk.END, "Session Complete!\n\n", ("welcome_title",)) # Reuse title tag
            self.question_text.insert(tk.END, "You've answered all available questions in this category/filter for this session.", "welcome_body")

            if self.current_quiz_mode == QUIZ_MODE_STANDARD:
                 final_score_msg = ""
                 if self.game_logic.total_questions_session > 0:
                     accuracy = (self.game_logic.score / self.game_logic.total_questions_session * 100)
                     final_score_msg = f"\n\nFinal Score: {self.game_logic.score} / {self.game_logic.total_questions_session} ({accuracy:.1f}%)"
                 else:
                     final_score_msg = "\n\nNo questions were answered in this session."
                 self.question_text.insert(tk.END, final_score_msg, "welcome_body")
                 self.submit_button.config(state=tk.DISABLED)
                 self.next_button.config(state=tk.DISABLED)
                 self.show_results_button.pack_forget()
                 self._update_status("Quiz finished.")
            elif self.current_quiz_mode == QUIZ_MODE_VERIFY:
                 self.question_text.insert(tk.END, "\n\nClick 'Show Results' to see your performance.", "welcome_body")
                 self.submit_button.config(state=tk.DISABLED)
                 self.next_button.config(state=tk.DISABLED)
                 self.show_results_button.config(state=tk.NORMAL) # Enable results button
                 self.show_results_button.pack(side=tk.LEFT, padx=(10, 0)) # Show results button
                 self.show_results_button.focus_set()
                 self._update_status("Verification finished. Ready for results.")


            self.question_text.config(state=tk.DISABLED)
            self.quiz_active = False
            # self._update_question_count_label() # Clear count label after session ends
            self.game_logic.save_history() # Save history at the end
            return

        # --- Display the actual question ---
        self._clear_quiz_area(clear_question=True, clear_options=True, clear_feedback=True, clear_explanation=True)
        q_text, options, _, category, _ = self.current_question_data

        self.category_label.config(text=f"Category: {category}")
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.insert(tk.END, q_text)
        self.question_text.config(state=tk.DISABLED)

        self.selected_answer_var.set(-1) # Reset selection
        for i, option in enumerate(options):
            rb = ttk.Radiobutton(self.options_frame, text=option, variable=self.selected_answer_var,
                                 value=i, style="TRadiobutton", takefocus=False, command=lambda: self.submit_button.config(state=tk.NORMAL)) # Enable submit on selection
            rb.pack(anchor=tk.W, padx=5, pady=4, fill=tk.X)

        # Enable submit (if an option is selected), disable next/results
        # Submit is initially disabled until a radio button is clicked (handled by lambda above)
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.show_results_button.pack_forget() # Hide results button during question display
        # self.submit_button.focus_set() # Focus might be better on the options initially


    def _next_question_gui(self):
        """Select and display the next question."""
        if not self.quiz_active:
             # This might happen if user clicks Next after session ended but before results shown
             if self.current_quiz_mode == QUIZ_MODE_VERIFY and self.gui_verify_session_answers:
                  # If in verify mode and answers exist, likely waiting for results
                  messagebox.showinfo("Session Complete", "Verification session is complete. Click 'Show Results'.", parent=self.root)
             else:
                  # Otherwise, truly inactive
                  messagebox.showinfo("Quiz Over", "The quiz session is not active or has ended. Please start a new quiz.", parent=self.root)
                  self._load_initial_state() # Reset to welcome screen
             return

        question_data, original_index = self.game_logic.select_question(self.current_category_filter)

        if question_data is None:
            # No more questions available
            self.current_question_data = None
            self.current_question_index = -1
            self._display_question_gui() # This will show the end-of-session message
        else:
            # Display the fetched question
            self.current_question_data = question_data
            self.current_question_index = original_index
            # Update status with question number (use GUI counter + 1 because it's 0-based)
            self._update_question_count_label(current=self.questions_answered_in_session_gui + 1, total=self.total_questions_in_filter_gui)
            self._update_status(f"Displaying question {self.questions_answered_in_session_gui + 1}...")
            self._display_question_gui()


    def _submit_answer_gui(self):
        """Process the user's submitted answer based on the current quiz mode."""
        user_answer_index = self.selected_answer_var.get()

        if user_answer_index == -1:
            # This check might be redundant if submit is only enabled on selection, but good safeguard
            messagebox.showwarning("No Answer", "Please select an answer before submitting.", parent=self.root)
            return

        if not self.current_question_data:
            messagebox.showerror("Error", "No current question data available. Cannot submit.", parent=self.root)
            return

        # --- Get question details ---
        q_text, options, correct_answer_index, category, explanation = self.current_question_data
        # Ensure we use the canonical question text for history
        original_question_text = self.game_logic.questions[self.current_question_index][0]
        is_correct = (user_answer_index == correct_answer_index)

        # --- Update History (Common to both modes) ---
        self.game_logic.update_history(original_question_text, category, is_correct)
        self.game_logic.total_questions_session += 1 # Increment logic counter
        self.questions_answered_in_session_gui += 1 # Increment GUI counter
        # Saving history now happens at end of session or explicit actions

        # --- Mode-Specific Actions ---
        if self.current_quiz_mode == QUIZ_MODE_STANDARD:
            # Show immediate feedback
            if is_correct:
                self.feedback_label.config(text="Correct! \U0001F389", style="Correct.Feedback.TLabel")
                self.game_logic.score += 1 # Update score only in standard mode display
            else:
                correct_option_text = options[correct_answer_index]
                feedback_text = f"Incorrect. \U0001F61E Correct was: {correct_answer_index + 1}. {correct_option_text}"
                self.feedback_label.config(text=feedback_text, style="Incorrect.Feedback.TLabel")

                # Show explanation if incorrect and available
                if explanation:
                     self.explanation_text.config(state=tk.NORMAL)
                     self.explanation_text.delete(1.0, tk.END)
                     self.explanation_text.insert(tk.END, f"Explanation:\n{explanation}")
                     self.explanation_text.config(state=tk.DISABLED)
                     self.explanation_text.grid() # Show explanation widget
                else:
                     self.explanation_text.grid_remove() # Hide if no explanation

            # Update UI state for standard mode
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
            self.show_results_button.pack_forget() # Ensure hidden
            for widget in self.options_frame.winfo_children():
                if isinstance(widget, ttk.Radiobutton):
                    widget.config(state=tk.DISABLED) # Disable options after answering
            # Update status with score
            score_percent = (self.game_logic.score / self.game_logic.total_questions_session * 100) if self.game_logic.total_questions_session else 0
            self._update_status(f"Answer submitted. Score: {self.game_logic.score}/{self.game_logic.total_questions_session} ({score_percent:.0f}%)")
            self.next_button.focus_set()

        elif self.current_quiz_mode == QUIZ_MODE_VERIFY:
            # Store result, don't show feedback yet
            self.gui_verify_session_answers.append((self.current_question_data, user_answer_index, is_correct))

            # Update UI state for verify mode (just move to next question)
            self.feedback_label.config(text="Answer recorded.", style="Info.Feedback.TLabel") # Subtle feedback
            self.explanation_text.grid_remove() # Ensure explanation is hidden
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL) # Enable next button immediately
            self.show_results_button.pack_forget() # Ensure hidden
            for widget in self.options_frame.winfo_children():
                 if isinstance(widget, ttk.Radiobutton):
                     widget.config(state=tk.DISABLED) # Disable options temporarily
            self._update_status(f"Answer {self.questions_answered_in_session_gui} recorded.")
            # Automatically trigger next question after a short delay? Or require click? Let's require click.
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

        # Use ScrolledText for the stats display
        stats_text_widget = scrolledtext.ScrolledText(stats_frame, wrap=tk.WORD, font=self.fonts["stats"],
                             relief="solid", bd=1, borderwidth=1,
                             bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                             padx=15, pady=15,
                             selectbackground=self.colors["accent"],
                             selectforeground=self.colors["bg"])
        stats_text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        try:
            stats_text_widget.vbar.configure(style="Vertical.TScrollbar")
        except tk.TclError:
             print("Note: Could not apply custom style to ScrolledText scrollbar in stats.")


        # --- Define tags for coloring/styling in the Text widget ---
        stats_text_widget.tag_configure("header", font=self.fonts["subheader"], foreground=self.colors["fg_header"], spacing1=10, spacing3=10)
        stats_text_widget.tag_configure("subheader", font=self.fonts["bold"], foreground=self.colors["accent"], spacing1=8, spacing3=5)
        stats_text_widget.tag_configure("label", foreground=self.colors["status_fg"])
        stats_text_widget.tag_configure("value", foreground=self.colors["fg"])
        stats_text_widget.tag_configure("correct", foreground=self.colors["correct"])
        stats_text_widget.tag_configure("incorrect", foreground=self.colors["incorrect"])
        stats_text_widget.tag_configure("neutral", foreground=self.colors["accent_dark"])
        stats_text_widget.tag_configure("dim", foreground=self.colors["dim"])
        stats_text_widget.tag_configure("q_text", foreground=self.colors["fg"], spacing1=5)
        stats_text_widget.tag_configure("q_details", foreground=self.colors["dim"], spacing3=10) # Details tag

        # --- Populate Stats Text ---
        stats_text_widget.insert(tk.END, "--- Study Statistics ---\n", "header")

        # Overall Performance
        history = self.game_logic.study_history
        total_attempts = history.get("total_attempts", 0)
        total_correct = history.get("total_correct", 0)
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        acc_tag = "correct" if overall_accuracy >= 75 else ("neutral" if overall_accuracy >= 50 else "incorrect")

        stats_text_widget.insert(tk.END, "Overall Performance (All Time):\n", "subheader")
        stats_text_widget.insert(tk.END, "  Total Questions Answered: ", "label")
        stats_text_widget.insert(tk.END, f"{total_attempts}\n", "value")
        stats_text_widget.insert(tk.END, "  Total Correct:            ", "label")
        stats_text_widget.insert(tk.END, f"{total_correct}\n", "value")
        stats_text_widget.insert(tk.END, "  Overall Accuracy:         ", "label")
        stats_text_widget.insert(tk.END, f"{overall_accuracy:.2f}%\n\n", acc_tag)

        # Performance by Category
        stats_text_widget.insert(tk.END, "Performance by Category:\n", "subheader")
        categories_data = history.get("categories", {})
        # Filter out categories with 0 attempts before sorting
        sorted_categories = sorted(
            [(cat, stats) for cat, stats in categories_data.items() if stats.get("attempts", 0) > 0],
            key=lambda item: item[0] # Sort by category name
        )

        if not sorted_categories:
            stats_text_widget.insert(tk.END, "  No category data recorded yet (or no attempts made).\n", "dim")
        else:
            max_len = max((len(cat) for cat, stats in sorted_categories), default=10)
            header_line = f"  {'Category'.ljust(max_len)} | {'Correct'.rjust(7)} | {'Attempts'.rjust(8)} | {'Accuracy'.rjust(9)}\n"
            stats_text_widget.insert(tk.END, header_line, "label")
            stats_text_widget.insert(tk.END, f"  {'-' * max_len}-+---------+----------+----------\n", "dim")
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0) # Should be > 0
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) # No zero check needed
                acc_tag = "correct" if cat_accuracy >= 75 else ("neutral" if cat_accuracy >= 50 else "incorrect")

                stats_text_widget.insert(tk.END, f"  {category.ljust(max_len)} | ")
                stats_text_widget.insert(tk.END, f"{str(cat_correct).rjust(7)}", "value")
                stats_text_widget.insert(tk.END, " | ")
                stats_text_widget.insert(tk.END, f"{str(cat_attempts).rjust(8)}", "value")
                stats_text_widget.insert(tk.END, " | ")
                stats_text_widget.insert(tk.END, f"{f'{cat_accuracy:.1f}%'.rjust(9)}\n", acc_tag)
        stats_text_widget.insert(tk.END, "\n")

        # Performance on Specific Questions
        stats_text_widget.insert(tk.END, "Performance on Specific Questions (All History):\n", "subheader")
        question_stats = history.get("questions", {})
        # Filter out questions with 0 attempts before sorting
        attempted_questions = {q: stats for q, stats in question_stats.items() if stats.get("attempts", 0) > 0}

        if not attempted_questions:
            stats_text_widget.insert(tk.END, "  No specific question data recorded yet (or no attempts made).\n", "dim")
        else:
            # Sort questions by accuracy (lowest first) then attempts (highest first)
            def sort_key(item):
                q_text, stats = item
                attempts = stats.get("attempts", 0) # Should be > 0
                correct = stats.get("correct", 0)
                accuracy = correct / attempts # No zero check needed
                return (accuracy, -attempts)

            sorted_questions = sorted(attempted_questions.items(), key=sort_key)
            stats_text_widget.insert(tk.END, "  (Sorted by lowest accuracy first)\n", "dim")

            for i, (q_text, stats) in enumerate(sorted_questions):
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                accuracy = (correct / attempts * 100) # No zero check needed
                acc_tag = "correct" if accuracy >= 75 else ("neutral" if accuracy >= 50 else "incorrect")

                last_result = "N/A"
                last_tag = "dim"
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_tag = "correct" if last_correct else "incorrect"

                display_text = (q_text[:100] + '...') if len(q_text) > 100 else q_text
                stats_text_widget.insert(tk.END, f"{i+1}. \"{display_text}\"\n", "q_text")
                # Use the q_details tag
                stats_text_widget.insert(tk.END, f"      ({attempts} attempts, ", "q_details")
                stats_text_widget.insert(tk.END, f"{accuracy:.1f}%", acc_tag)
                stats_text_widget.insert(tk.END, " acc.) Last: ", "q_details")
                stats_text_widget.insert(tk.END, f"{last_result}\n\n", last_tag)
        # --- End Populate ---

        stats_text_widget.config(state=tk.DISABLED) # Make text read-only

        # Close button frame
        button_frame = ttk.Frame(stats_win, style="TFrame")
        button_frame.pack(pady=(10, 15))
        close_button = ttk.Button(button_frame, text="Close", command=stats_win.destroy, style="TButton", width=12)
        close_button.pack()

        self.root.wait_window(stats_win)

    def _show_verify_results_gui(self):
        """Displays the results after a 'Verify Knowledge' session in a Toplevel window."""
        results_win = tk.Toplevel(self.root)
        results_win.title("Verification Results")
        results_win.geometry("900x700") # Make it a bit taller for results
        results_win.transient(self.root)
        results_win.grab_set()
        results_win.configure(bg=self.colors["bg"])
        results_win.minsize(700, 550)

        try:
            results_win.tk_setPalette(background=self.colors["bg"], foreground=self.colors["fg"])
        except tk.TclError:
            print("Warning: Could not set Toplevel palette for results window.")

        results_frame = ttk.Frame(results_win, padding="15")
        results_frame.pack(fill=tk.BOTH, expand=True)

        results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=self.fonts["base"], # Use base font
                                                 relief="solid", bd=1, borderwidth=1,
                                                 bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                                                 padx=15, pady=15,
                                                 selectbackground=self.colors["accent"],
                                                 selectforeground=self.colors["bg"])
        results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        try:
             results_text.vbar.configure(style="Vertical.TScrollbar")
        except tk.TclError:
             print("Note: Could not apply custom style to ScrolledText scrollbar in results.")

        # --- Define tags ---
        results_text.tag_configure("header", font=self.fonts["subheader"], foreground=self.colors["fg_header"], spacing1=10, spacing3=10)
        results_text.tag_configure("subheader", font=self.fonts["bold"], foreground=self.colors["accent"], spacing1=8, spacing3=5)
        results_text.tag_configure("label", foreground=self.colors["status_fg"])
        results_text.tag_configure("value", foreground=self.colors["fg"])
        results_text.tag_configure("correct", foreground=self.colors["correct"])
        results_text.tag_configure("incorrect", foreground=self.colors["incorrect"])
        results_text.tag_configure("neutral", foreground=self.colors["accent_dark"])
        results_text.tag_configure("dim", foreground=self.colors["dim"])
        results_text.tag_configure("q_text", font=self.fonts["question"], foreground=self.colors["fg"], spacing1=8, spacing3=5)
        results_text.tag_configure("option", font=self.fonts["option"], foreground=self.colors["fg"], lmargin1=20, lmargin2=20)
        results_text.tag_configure("explanation", font=self.fonts["explanation"], foreground=self.colors["dim"], lmargin1=20, lmargin2=20, spacing1=5, spacing3=10)
        results_text.tag_configure("separator", foreground=self.colors["border"], justify='center', spacing1=10, spacing3=10)


        # --- Populate Results ---
        results_text.insert(tk.END, "--- Verification Results ---\n", "header")

        if not self.gui_verify_session_answers:
            results_text.insert(tk.END, "No questions were answered in this verification session.\n", "dim")
        else:
            num_correct = sum(1 for _, _, is_correct in self.gui_verify_session_answers if is_correct)
            total_answered = len(self.gui_verify_session_answers)
            accuracy = (num_correct / total_answered * 100) if total_answered > 0 else 0
            acc_tag = "correct" if accuracy >= 75 else ("neutral" if accuracy >= 50 else "incorrect")

            results_text.insert(tk.END, "Session Summary:\n", "subheader")
            results_text.insert(tk.END, f"  Total Questions Answered: ", "label")
            results_text.insert(tk.END, f"{total_answered}\n", "value")
            results_text.insert(tk.END, f"  Correct Answers:         ", "label")
            results_text.insert(tk.END, f"{num_correct}\n", "value")
            results_text.insert(tk.END, f"  Accuracy:                ", "label")
            results_text.insert(tk.END, f"{accuracy:.2f}%\n\n", acc_tag)
            results_text.insert(tk.END, f"{'-'*50}\n", "separator")

            results_text.insert(tk.END, "Detailed Review:\n", "subheader")
            for i, (q_data, user_answer_idx, is_correct) in enumerate(self.gui_verify_session_answers):
                q_text, options, correct_idx, _, explanation = q_data
                results_text.insert(tk.END, f"{i+1}. {q_text}\n", "q_text")
                user_choice_text = options[user_answer_idx]
                correct_choice_text = options[correct_idx]

                # Display user's answer with feedback
                user_tag = "correct" if is_correct else "incorrect"
                feedback_icon = "\U0001F389" if is_correct else "\U0001F61E"
                results_text.insert(tk.END, f"Your answer: {user_answer_idx+1}. {user_choice_text} ({feedback_icon})\n", ("option", user_tag))

                # Display correct answer only if incorrect
                if not is_correct:
                    results_text.insert(tk.END, f"Correct answer: {correct_idx+1}. {correct_choice_text}\n", ("option", "correct"))

                # Display explanation if available
                if explanation:
                    results_text.insert(tk.END, f"Explanation: {explanation}\n", "explanation")

                results_text.insert(tk.END, f"{'.'*50}\n", "separator") # Separator after each question


        results_text.config(state=tk.DISABLED) # Make read-only

        # Close button
        button_frame = ttk.Frame(results_win, style="TFrame")
        button_frame.pack(pady=(10, 15))
        close_button = ttk.Button(button_frame, text="Close", style="TButton", width=12)
        close_button.pack()

        # Reset main window state after closing results
        def on_close():
            results_win.destroy()
            self._load_initial_state() # Go back to welcome screen

        results_win.protocol("WM_DELETE_WINDOW", on_close) # Handle window close button
        close_button.config(command=on_close) # Also handle button click

        self.root.wait_window(results_win)


    def _clear_stats_gui(self):
        """Ask for confirmation and clear stats via game logic."""
        if messagebox.askyesno("Confirm Clear",
                               "Are you sure you want to delete ALL study history?\n"
                               "This includes all performance statistics and the list of incorrect answers.\n\n"
                               "This action cannot be undone.",
                               parent=self.root, icon='warning'):
            self.game_logic.study_history = self.game_logic._default_history()
            # Re-populate categories with 0 stats
            for category in self.game_logic.categories:
                 self.game_logic.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.game_logic.save_history()
            messagebox.showinfo("Stats Cleared", "Study history has been cleared.", parent=self.root)
            self._update_status("Study history cleared.")
            # Disable review button if list is now empty
            self.review_button.config(state=tk.DISABLED)


    def _review_incorrect_gui(self):
        """Allows reviewing incorrect answers in the GUI (Basic View)."""
        incorrect_list = self.game_logic.study_history.get("incorrect_review", [])

        if not incorrect_list:
            messagebox.showinfo("Review Incorrect", "No incorrect answers recorded in history.", parent=self.root)
            return

        # Find the full question data
        questions_to_review = []
        not_found_questions = []
        # Create a temporary copy to iterate over, allowing removal from original
        incorrect_list_copy = list(incorrect_list)
        for incorrect_text in incorrect_list_copy:
             found = False
             for q_data in self.game_logic.questions:
                 if q_data[0] == incorrect_text:
                     questions_to_review.append(q_data)
                     found = True
                     break
             if not found:
                 not_found_questions.append(incorrect_text)
                 # Remove from the actual history list if not found in current questions
                 if incorrect_text in self.game_logic.study_history["incorrect_review"]:
                     self.game_logic.study_history["incorrect_review"].remove(incorrect_text)


        if not questions_to_review:
             messagebox.showerror("Review Error", "Could not load data for any incorrect questions.", parent=self.root)
             self.game_logic.save_history() # Save history if items were removed
             # Update main button if list is now empty
             if not self.game_logic.study_history.get("incorrect_review", []):
                  self.review_button.config(state=tk.DISABLED)
             return

        # --- Create Review Window ---
        review_win = tk.Toplevel(self.root)
        review_win.title("Review Incorrect Answers")
        review_win.geometry("900x700")
        review_win.transient(self.root)
        review_win.grab_set()
        review_win.configure(bg=self.colors["bg"])
        review_win.minsize(700, 550)

        try:
            review_win.tk_setPalette(background=self.colors["bg"], foreground=self.colors["fg"])
        except tk.TclError:
            print("Warning: Could not set Toplevel palette for review window.")

        review_frame = ttk.Frame(review_win, padding="15")
        review_frame.pack(fill=tk.BOTH, expand=True)
        review_frame.rowconfigure(1, weight=1) # Make text area expand
        review_frame.columnconfigure(0, weight=1)

        # Header
        ttk.Label(review_frame, text="Incorrectly Answered Questions", style="Header.TLabel").grid(row=0, column=0, pady=(0,15), sticky="w")

        # Display Area (ScrolledText)
        review_text = scrolledtext.ScrolledText(review_frame, wrap=tk.WORD, font=self.fonts["base"],
                                                 relief="solid", bd=1, borderwidth=1,
                                                 bg=self.colors["explanation_bg"], fg=self.colors["fg"],
                                                 padx=15, pady=15,
                                                 selectbackground=self.colors["accent"],
                                                 selectforeground=self.colors["bg"])
        review_text.grid(row=1, column=0, sticky="nsew", pady=5)
        try:
             review_text.vbar.configure(style="Vertical.TScrollbar")
        except tk.TclError:
             print("Note: Could not apply custom style to ScrolledText scrollbar in review.")

        # --- Define tags ---
        review_text.tag_configure("q_text", font=self.fonts["question"], foreground=self.colors["fg"], spacing1=8, spacing3=5)
        review_text.tag_configure("option", font=self.fonts["option"], foreground=self.colors["fg"], lmargin1=20, lmargin2=20)
        review_text.tag_configure("correct_option", font=self.fonts["option"], foreground=self.colors["correct"], lmargin1=20, lmargin2=20)
        review_text.tag_configure("explanation", font=self.fonts["explanation"], foreground=self.colors["dim"], lmargin1=20, lmargin2=20, spacing1=5, spacing3=10)
        review_text.tag_configure("category", font=self.fonts["italic"], foreground=self.colors["category_fg"], spacing1=5)
        review_text.tag_configure("separator", foreground=self.colors["border"], justify='center', spacing1=10, spacing3=10)
        review_text.tag_configure("warning", foreground=self.colors["incorrect"], font=self.fonts["italic"])


        # --- Populate Review Text ---
        def populate_review_text():
            review_text.config(state=tk.NORMAL)
            review_text.delete(1.0, tk.END)
            for i, q_data in enumerate(questions_to_review):
                q_text, options, correct_idx, category, explanation = q_data
                review_text.insert(tk.END, f"{i+1}. {q_text}\n", "q_text")
                review_text.insert(tk.END, f"Category: {category}\n", "category")

                for j, option in enumerate(options):
                     if j == correct_idx:
                         review_text.insert(tk.END, f"   \u2714 {option} (Correct Answer)\n", "correct_option") # Checkmark
                     else:
                         review_text.insert(tk.END, f"   \u2022 {option}\n", "option") # Bullet

                if explanation:
                    review_text.insert(tk.END, f"Explanation: {explanation}\n", "explanation")

                review_text.insert(tk.END, f"{'-'*50}\n", "separator")

            if not_found_questions:
                 review_text.insert(tk.END, "\nWarning: Some questions previously marked incorrect could not be found (they might have been removed from the source data and were removed from this list):\n", "warning")
                 for nf_text in not_found_questions:
                     review_text.insert(tk.END, f"- {nf_text[:80]}...\n", "warning")
            review_text.config(state=tk.DISABLED) # Make read-only

        populate_review_text() # Initial population

        # --- Action Buttons ---
        button_frame = ttk.Frame(review_win, style="TFrame")
        button_frame.grid(row=2, column=0, pady=(10, 15), sticky="ew") # Place below text area
        button_frame.columnconfigure(1, weight=1) # Spacer

        def clear_item_from_review_list():
             # Simple approach: Ask user which number to clear
             num_str = simpledialog.askstring("Clear Item", "Enter the number of the question to remove from this review list:", parent=review_win)
             if num_str:
                 try:
                     num_to_clear = int(num_str) - 1 # Convert to 0-based index
                     if 0 <= num_to_clear < len(questions_to_review):
                         question_to_clear_text = questions_to_review[num_to_clear][0]
                         if messagebox.askyesno("Confirm Clear", f"Remove question {num_to_clear+1} from the review list?", parent=review_win):
                              if question_to_clear_text in self.game_logic.study_history["incorrect_review"]:
                                  self.game_logic.study_history["incorrect_review"].remove(question_to_clear_text)
                                  self.game_logic.save_history()
                                  messagebox.showinfo("Cleared", "Question removed from review list.", parent=review_win)
                                  # Remove from the list used by this window and refresh display
                                  del questions_to_review[num_to_clear]
                                  populate_review_text() # Refresh the text widget
                                  # Update main window button state if list becomes empty
                                  if not self.game_logic.study_history["incorrect_review"]:
                                       self.review_button.config(state=tk.DISABLED)
                                       # Disable clear button if list is now empty
                                       clear_button.config(state=tk.DISABLED)
                              else:
                                   messagebox.showerror("Error", "Question not found in history list.", parent=review_win)
                     else:
                         messagebox.showwarning("Invalid Number", f"Please enter a number between 1 and {len(questions_to_review)}.", parent=review_win)
                 except ValueError:
                     messagebox.showerror("Invalid Input", "Please enter a valid number.", parent=review_win)

        clear_button_state = tk.NORMAL if questions_to_review else tk.DISABLED
        clear_button = ttk.Button(button_frame, text="Clear Item from List", command=clear_item_from_review_list, style="TButton", width=20, state=clear_button_state)
        clear_button.grid(row=0, column=0, padx=10, sticky="w")

        close_button = ttk.Button(button_frame, text="Close", command=review_win.destroy, style="TButton", width=12)
        close_button.grid(row=0, column=2, padx=10, sticky="e")

        # Save history when closing the window (in case items were removed due to not being found)
        def on_close():
             self.game_logic.save_history()
             review_win.destroy()
        review_win.protocol("WM_DELETE_WINDOW", on_close)


        self.root.wait_window(review_win)


    def _export_data_gui(self):
        """Exports study data via GUI using asksaveasfilename."""
        from tkinter import filedialog # Import here to avoid top-level dependency if GUI not used

        initial_filename = f"linux_plus_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Study Data",
            initialfile=initial_filename,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not export_filename:
            self._update_status("Export cancelled.")
            return # User cancelled

        try:
            export_path = os.path.abspath(export_filename)
            self._update_status(f"Exporting to {os.path.basename(export_path)}...")
            self.root.update_idletasks() # Update status label before potential delay

            with open(export_filename, 'w') as f:
                json.dump(self.game_logic.study_history, f, indent=2)

            messagebox.showinfo("Export Successful", f"Study data successfully exported to:\n{export_path}", parent=self.root)
            self._update_status("Export successful.")

        except IOError as e:
            messagebox.showerror("Export Error", f"Error exporting data: {e}\nPlease check permissions and filename.", parent=self.root)
            self._update_status("Export failed.")
        except Exception as e:
             messagebox.showerror("Export Error", f"An unexpected error occurred during export: {e}", parent=self.root)
             self._update_status("Export failed.")


    def _quit_app(self):
        """Save history before quitting, with confirmation if quiz active."""
        quit_confirmed = True # Assume yes unless quiz is active
        if self.quiz_active:
             # Ask for confirmation if a quiz is in progress
             quit_confirmed = messagebox.askyesno("Quit Confirmation",
                                                  "A quiz session is currently active. Are you sure you want to quit?\n"
                                                  "(Progress for this session might not be fully saved)",
                                                  parent=self.root, icon='warning')

        if quit_confirmed:
             self.game_logic.save_history()
             self.root.quit()
             self.root.destroy() # Ensure window closes fully


# --- Main Execution Block ---
if __name__ == "__main__":
    # Initialize colorama (if available) for CLI
    if 'colorama' in sys.modules:
        colorama.init(autoreset=True)

    # Create instance of the game logic class
    game_engine = LinuxPlusStudyGame()

    # Ask user for interface preference
    interface_choice = ""
    # Check if running interactively (no args, attached to tty)
    is_interactive = sys.stdin.isatty() and len(sys.argv) == 1

    if not is_interactive:
        print("Non-interactive environment detected or arguments provided. Defaulting to CLI.")
        interface_choice = 'cli'
    else:
        # Loop until valid choice or EOF
        while interface_choice not in ['cli', 'gui']:
            # Use colorama colors if available for the prompt
            prompt_text = f"{COLOR_PROMPT}Choose interface ({COLOR_OPTIONS}CLI{COLOR_PROMPT} or {COLOR_OPTIONS}GUI{COLOR_PROMPT}): {COLOR_INPUT}"
            reset_text = COLOR_RESET
            try:
                print(prompt_text, end='')
                sys.stdout.flush() # Ensure prompt appears before input
                interface_choice = input().lower().strip()
                print(reset_text, end='') # Reset color after input
            except EOFError:
                 print(f"\n{COLOR_ERROR} Input interrupted. Exiting. {reset_text}")
                 sys.exit(1)
            except KeyboardInterrupt:
                 print(f"\n{COLOR_WARNING} Operation cancelled by user. Exiting. {reset_text}")
                 sys.exit(0)

            if interface_choice not in ['cli', 'gui']:
                 print(f"{COLOR_INFO} Invalid choice. Please type 'cli' or 'gui'. {reset_text}")

    # --- Launch Selected Interface ---
    if interface_choice == 'gui':
        root = tk.Tk()
        # Apply a base theme attempt (may vary by OS/Tk version)
        # Removed custom theme loading as it's often problematic cross-platform
        # try:
        #     root.tk.call("source", os.path.join(os.path.dirname(__file__), "azure_dark.tcl")) # Example theme file
        #     root.tk.call("set_theme", "dark")
        # except tk.TclError:
        #      print("Note: Could not apply custom Azure dark theme. Using default.")
        # except FileNotFoundError:
        #      print("Note: Theme file 'azure_dark.tcl' not found. Using default.")


        app = LinuxPlusStudyGUI(root, game_engine)
        # Set protocol handler for window close to ensure saving/confirmation
        root.protocol("WM_DELETE_WINDOW", app._quit_app)
        root.mainloop()
    else: # Default to CLI if 'gui' wasn't chosen or in non-interactive mode
        try:
            game_engine.display_welcome_message() # Show welcome message first
            game_engine.main_menu()
        except KeyboardInterrupt:
            print(f"\n{COLOR_WARNING} Keyboard interrupt detected during CLI operation. Saving history and exiting. {COLOR_RESET}")
            game_engine.save_history()
            sys.exit(0)
        except Exception as e:
            # Generic error catcher for CLI mode
            print(f"\n{COLOR_ERROR} An unexpected error occurred in CLI mode: {e} {COLOR_RESET}")
            print(f"{COLOR_INFO} Attempting to save history before exiting... {COLOR_RESET}")
            game_engine.save_history()
            # Optionally print traceback for debugging
            import traceback
            traceback.print_exc()
            sys.exit(1)


