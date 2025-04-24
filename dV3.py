import random
import os
import sys
import time
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Attempt to import colorama for cross-platform colored output
try:
    import colorama
    colorama.init(autoreset=True) # Automatically reset style after each print
    # Define colors using colorama
    COLOR_QUESTION = colorama.Fore.CYAN
    COLOR_OPTIONS = colorama.Fore.WHITE
    COLOR_CATEGORY = colorama.Fore.YELLOW
    COLOR_CORRECT = colorama.Fore.GREEN + colorama.Style.BRIGHT
    COLOR_INCORRECT = colorama.Fore.RED + colorama.Style.BRIGHT
    COLOR_EXPLANATION = colorama.Fore.LIGHTBLACK_EX # Grey
    COLOR_PROMPT = colorama.Fore.MAGENTA
    COLOR_HEADER = colorama.Fore.BLUE + colorama.Style.BRIGHT
    COLOR_STATS_LABEL = colorama.Fore.WHITE + colorama.Style.BRIGHT
    COLOR_STATS_VALUE = colorama.Fore.YELLOW
    COLOR_YELLOW = colorama.Fore.YELLOW # Added missing color
    COLOR_RESET = colorama.Style.RESET_ALL
except ImportError:
    print("Colorama not found. Colored output will be disabled in CLI.")
    # Define empty strings if colorama is not available
    COLOR_QUESTION = ""
    COLOR_OPTIONS = ""
    COLOR_CATEGORY = ""
    COLOR_CORRECT = ""
    COLOR_INCORRECT = ""
    COLOR_EXPLANATION = ""
    COLOR_PROMPT = ""
    COLOR_HEADER = ""
    COLOR_STATS_LABEL = ""
    COLOR_STATS_VALUE = ""
    COLOR_YELLOW = "" # Added missing color
    COLOR_RESET = ""

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
            "sessions": [], # Could store session summaries later
            "questions": {},  # Track performance per question text
            "categories": {},  # Track performance per category name
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
                # Ensure all default keys exist for compatibility
                default = self._default_history()
                for key in default:
                    history.setdefault(key, default[key])
                # Ensure sub-dictionaries have expected structure
                if not isinstance(history.get("questions"), dict): history["questions"] = {}
                if not isinstance(history.get("categories"), dict): history["categories"] = {}
                if not isinstance(history.get("sessions"), list): history["sessions"] = []
                return history
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default history structure if file doesn't exist or is invalid
            print(f"{COLOR_INCORRECT}History file not found or invalid. Starting fresh.{COLOR_RESET}")
            return self._default_history()

    def save_history(self):
        """Save study history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.study_history, f, indent=2)
        except IOError as e:
            print(f"{COLOR_INCORRECT}Error saving history: {e}{COLOR_RESET}")

    def load_questions(self):
        """Load sample Linux+ questions, commands, and definitions."""
        # --- Existing Questions ---
        existing_questions = [
            # Troubleshooting questions (truncated for brevity)
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
            # ... (other existing questions would go here) ...
        ]

        # --- Command Questions ---
        command_questions = [
            # 1.0 System Management Commands
            ("What is the primary function of the `mkinitrd` command?",
             ["Create an initial RAM disk image used during boot", "Install the GRUB bootloader", "Configure network interfaces", "Manage kernel modules"],
             0, "Commands (System Management)",
             "`mkinitrd` creates an initial RAM disk (initrd) image, which contains necessary drivers and utilities needed early in the Linux boot process before the root filesystem is mounted. Example: `mkinitrd /boot/initrd-$(uname -r).img $(uname -r)`"),
            ("Which command installs the GRUB2 bootloader to a specified device?",
             ["grub2-mkconfig", "grub2-install", "update-grub", "dracut"],
             1, "Commands (System Management)",
             "`grub2-install` installs the GRUB2 bootloader files to the appropriate location and typically installs the boot code to the MBR or EFI partition. Example: `grub2-install /dev/sda` (for BIOS systems) or `grub2-install --target=x86_64-efi --efi-directory=/boot/efi` (for UEFI systems)."),
            ("What is the purpose of the `grub2-mkconfig` command?",
             ["Install the GRUB2 bootloader", "Update kernel parameters", "Generate a GRUB2 configuration file", "Create an initial RAM disk"],
             2, "Commands (System Management)",
             "`grub2-mkconfig` scans the system for kernels and operating systems and generates a new GRUB2 configuration file (`grub.cfg`). Example: `grub2-mkconfig -o /boot/grub2/grub.cfg`"),
            ("Which command is typically used on Debian-based systems to update the GRUB2 configuration file?",
             ["grub2-mkconfig", "grub2-install", "update-grub", "dracut"],
             2, "Commands (System Management)",
             "`update-grub` is a script commonly found on Debian-based systems (like Ubuntu) that acts as a wrapper for `grub-mkconfig -o /boot/grub/grub.cfg`. Example: `sudo update-grub`"),
            ("What is the function of the `dracut` command?",
             ["Install the GRUB bootloader", "Manage disk partitions", "Create an initial RAM filesystem (initramfs) image", "Configure network settings"],
             2, "Commands (System Management)",
             "`dracut` is a tool used to create an initramfs image, which is loaded by the bootloader to initialize the hardware and mount the root filesystem during boot. Example: `dracut --force /boot/initramfs-$(uname -r).img $(uname -r)`"),
            ("In the context of compiling software from source, what does the `./configure` script typically do?",
             ["Compiles the source code", "Installs the compiled program", "Checks the system for dependencies and sets up the build environment", "Downloads the source code"],
             2, "Commands (System Management)",
             "The `./configure` script (generated by autotools) checks the system for necessary libraries, tools, and features, and creates a `Makefile` tailored to the system's environment. Example: `./configure --prefix=/usr/local`"),
            ("After running `./configure`, what is the typical next step when compiling software from source?",
             ["make install", "make clean", "make", "./install"],
             2, "Commands (System Management)",
             "The `make` command reads the `Makefile` (generated by `./configure`) and compiles the source code into executable binaries and libraries. Example: `make`"),
            ("What is the final step, usually requiring root privileges, when installing software compiled from source?",
             ["make", "./configure", "make install", "make check"],
             2, "Commands (System Management)",
             "`make install` copies the compiled binaries, libraries, documentation, and other necessary files from the build directory to the system-wide locations specified during configuration (often `/usr/local/bin`, `/usr/local/lib`, etc.). Example: `sudo make install`"),
            ("Which command is used to list PCI devices connected to the system?",
             ["lsusb", "lspci", "lshw", "dmidecode"],
             1, "Commands (System Management)",
             "`lspci` lists all PCI buses and devices in the system, providing information about hardware like network cards, graphics cards, and controllers. Example: `lspci -v` (verbose output)."),
            ("What command lists USB devices connected to the system?",
             ["lspci", "lsblk", "lsusb", "lsof"],
             2, "Commands (System Management)",
             "`lsusb` displays information about USB buses in the system and the devices connected to them. Example: `lsusb -t` (tree view)."),
            ("Which command retrieves detailed hardware information by reading data from the system's DMI/SMBIOS tables?",
             ["lshw", "lspci", "dmidecode", "lsblk"],
             2, "Commands (System Management)",
             "`dmidecode` parses the Desktop Management Interface (DMI) or System Management BIOS (SMBIOS) data tables to display detailed information about the system's hardware components, including BIOS, processor, memory, and chassis. Example: `sudo dmidecode -t memory`"),
            ("What is the primary function of the `sed` command?",
             ["Search for patterns in files (like grep)", "Perform text transformations on an input stream (a stream editor)", "Edit files interactively (like nano or vim)", "Display disk usage"],
             1, "Commands (System Management)",
             "`sed` (Stream Editor) is used for filtering and transforming text. It's commonly used for search-and-replace operations, deletions, insertions, and other text manipulations. Example: `sed 's/old/new/g' input.txt > output.txt`"),
            ("Which command is a powerful text-processing tool often used for pattern scanning and processing language?",
             ["grep", "sed", "awk", "cut"],
             2, "Commands (System Management)",
             "`awk` is a versatile programming language designed for text processing, typically used for data extraction and reporting. It processes files line by line based on specified patterns and actions. Example: `awk -F':' '{print $1}' /etc/passwd` (prints first field of passwd file)."),
            ("What command is used to format and print text according to specified formats?",
             ["echo", "cat", "printf", "fmt"],
             2, "Commands (System Management)",
             "`printf` formats and prints data according to a specified format string, similar to the C printf function. It offers more control over output formatting than `echo`. Example: `printf \"User: %s\\nID: %d\\n\" \"alice\" 1001`"),
            ("Which command launches a simple, modeless text editor popular for beginners?",
             ["vim", "emacs", "nano", "ed"],
             2, "Commands (System Management)",
             "`nano` is a user-friendly, straightforward text editor often recommended for beginners due to its simplicity and on-screen help. Example: `nano /etc/hosts`"),
            ("What is `vi` or `vim`?",
             ["A file compression utility", "A command to display system processes", "A powerful, modal text editor common on Unix-like systems", "A tool for managing disk partitions"],
             2, "Commands (System Management)",
             "`vi` (Visual Editor) and its improved version `vim` are highly configurable, powerful text editors known for their modal editing interface (insert mode, command mode, etc.). Example: `vim my_script.sh`"),
             # ... (other command questions) ...
        ]

        # --- Definition Questions ---
        definition_questions = [
            # A
             ("What does ACL stand for in Linux security?",
              ["Access Configuration Layer", "Advanced Control List", "Access Control List", "Allowed Command List"],
              2, "Concepts & Terms (Security)",
              "ACL (Access Control List) provides a more flexible permission mechanism than traditional Unix permissions, allowing specific permissions for individual users or groups on a file or directory."),
             ("In Kubernetes, what is an Ambassador container?",
              ["A container that monitors network traffic", "A container acting as an outbound proxy for external services", "A primary application container", "A container managing storage volumes"],
              1, "Concepts & Terms (Containers)",
              "An Ambassador container acts as a proxy within a Pod, simplifying communication between the application container(s) and external services by handling tasks like discovery, routing, or authentication."),
             ("What is Ansible primarily used for?",
              ["Container orchestration", "Version control", "Automation (configuration management, deployment)", "Network monitoring"],
              2, "Concepts & Terms (Automation)",
              "Ansible is an open-source automation tool for tasks like configuration management, application deployment, task execution, and orchestration."),
             ("What is AppArmor?",
              ["A firewall utility", "A Linux kernel security module for mandatory access control based on program profiles", "A package manager", "A type of filesystem"],
              1, "Concepts & Terms (Security)",
              "AppArmor confines individual programs to a limited set of resources using per-program profiles, enhancing system security."),
             ("What is an AppImage?",
              ["A kernel module", "A format for distributing portable Linux applications without installation", "A type of container image", "A systemd unit file"],
              1, "Concepts & Terms (System Management)",
              "AppImage allows developers to package applications with all dependencies into a single file that can run on various Linux distributions without needing installation or root privileges."),
             ("What does API stand for?",
              ["Advanced Programming Interface", "Application Protocol Interchange", "Application Program Interface", "Automated Process Invocation"],
              2, "Concepts & Terms (General)",
              "An API (Application Program Interface) is a set of rules and specifications that software programs can follow to communicate with each other."),
             ("What is the function of the Address Resolution Protocol (ARP)?",
              ["Map IP addresses to domain names", "Map IP addresses to MAC addresses on a local network", "Route packets between networks", "Assign IP addresses dynamically"],
              1, "Concepts & Terms (Networking)",
              "ARP is used by network devices to discover the link layer address (MAC address) associated with a given Internet layer address (IP address) on the same local network."),
             ("In SELinux, what does 'Autorelabel' mean?",
              ["Automatically assigning labels based on file type", "The process of relabeling the entire filesystem according to the current policy", "A type of SELinux policy", "A command to change a single file's context"],
              1, "Concepts & Terms (Security)",
              "Autorelabel is the process, often initiated by creating a file named `.autorelabel` at the root and rebooting, where SELinux relabels all files on the filesystem to match the contexts defined in the loaded policy."),
            # ... (other definition questions) ...
        ]

        # Combine all question types
        self.questions = existing_questions + command_questions + definition_questions
        random.shuffle(self.questions) # Shuffle questions initially

        # Populate categories and ensure they exist in history
        self.categories = set(q[3] for q in self.questions) # Category is the 4th element (index 3)
        for category in self.categories:
            self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        # Save history in case new categories were added
        self.save_history()

    def update_history(self, question_text, category, is_correct):
        """Update study history with the result of the answered question."""
        timestamp = datetime.now().isoformat()

        # Update overall stats
        self.study_history["total_attempts"] = self.study_history.get("total_attempts", 0) + 1
        if is_correct:
            self.study_history["total_correct"] = self.study_history.get("total_correct", 0) + 1

        # Update question-specific stats (using question text as key)
        q_stats = self.study_history["questions"].setdefault(question_text, {"correct": 0, "attempts": 0, "history": []})
        q_stats["attempts"] += 1
        if is_correct:
            q_stats["correct"] += 1
        q_stats["history"].append({"timestamp": timestamp, "correct": is_correct})
        # Optional: Limit history per question
        # q_stats["history"] = q_stats["history"][-10:]

        # Update category-specific stats
        cat_stats = self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        cat_stats["attempts"] += 1
        if is_correct:
            cat_stats["correct"] += 1

        # Note: Session tracking could be added here if needed

    def select_question(self, category_filter=None):
        """Select a question, optionally filtered, avoiding recent repeats and using weighting."""
        possible_indices = [
            idx for idx, q in enumerate(self.questions)
            if (category_filter is None or q[3] == category_filter)
        ]

        if not possible_indices:
            print(f"{COLOR_INCORRECT}No questions found for filter: {category_filter}{COLOR_RESET}")
            return None, -1

        # Filter out questions already answered in this session
        available_indices = [idx for idx in possible_indices if idx not in self.answered_indices_session]

        # If all questions in the filter have been answered this session, reset session list for this filter
        if not available_indices:
            print(f"{COLOR_YELLOW}All questions in this category answered this session. Resetting session list for this category.{COLOR_RESET}")
            # More sophisticated reset: only remove indices matching the filter
            self.answered_indices_session = [idx for idx in self.answered_indices_session if self.questions[idx][3] != category_filter]
            available_indices = possible_indices # Try again with all possible indices for this filter

            if not available_indices: # Should not happen if possible_indices was populated
                 print(f"{COLOR_INCORRECT}Error: Still no available questions after reset.{COLOR_RESET}")
                 return None, -1

        # --- Weighted Selection Logic ---
        weights = []
        indices_for_weighting = []

        for q_idx in available_indices:
            q_text = self.questions[q_idx][0]
            # Use .get for safety if history structure is somehow corrupted
            q_stats = self.study_history.get("questions", {}).get(q_text, {"correct": 0, "attempts": 0})
            attempts = q_stats.get("attempts", 0)
            correct = q_stats.get("correct", 0)

            # Calculate weight: higher weight for fewer attempts or lower accuracy
            accuracy = (correct / attempts) if attempts > 0 else 0.5 # Default to 50% if never seen
            # Weight increases significantly for incorrect answers and questions seen fewer times
            weight = (1.0 - accuracy) * 5 + (1.0 / (attempts + 1)) * 2
            weights.append(max(0.1, weight)) # Ensure weight is positive
            indices_for_weighting.append(q_idx)

        if not indices_for_weighting or not weights or len(weights) != len(indices_for_weighting):
            print(f"{COLOR_INCORRECT}Weighting error. Falling back to random choice.{COLOR_RESET}")
            # Fallback to simple random choice among available indices
            chosen_original_index = random.choice(available_indices)
        else:
            # Perform weighted random choice
            try:
                chosen_original_index = random.choices(indices_for_weighting, weights=weights, k=1)[0]
            except (IndexError, ValueError) as e:
                 print(f"{COLOR_INCORRECT}Weighted choice error: {e}. Falling back to random choice.{COLOR_RESET}")
                 chosen_original_index = random.choice(available_indices)

        # Add the chosen question's *original index* to the answered list for this session
        self.answered_indices_session.append(chosen_original_index)
        chosen_question = self.questions[chosen_original_index]

        return chosen_question, chosen_original_index # Return question data and its original index

    def display_question(self, question_data):
        """Display the question and options with colors."""
        question_text, options, _, category, _ = question_data
        print(f"\n--- {COLOR_CATEGORY}Category: {category}{COLOR_RESET} ---")
        print(f"\n{COLOR_QUESTION}Q: {question_text}{COLOR_RESET}\n")
        for i, option in enumerate(options):
            print(f"  {COLOR_OPTIONS}{i + 1}. {option}{COLOR_RESET}")
        print(f"{COLOR_HEADER}{'-' * (len(category) + 16)}{COLOR_RESET}") # Adjust line length

    def get_user_answer(self, num_options):
        """Get and validate user input for CLI."""
        while True:
            try:
                prompt = f"{COLOR_PROMPT}Your choice (1-{num_options}), 's' to skip, 'q' to quit session: {COLOR_RESET}"
                answer = input(prompt).lower().strip()
                if answer == 'q':
                    return 'q'
                if answer == 's':
                    return 's'
                choice = int(answer)
                if 1 <= choice <= num_options:
                    return choice - 1  # Return 0-based index
                else:
                    print(f"{COLOR_INCORRECT}Invalid choice. Please enter a number between 1 and {num_options}.{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_INCORRECT}Invalid input. Please enter a number, 's', or 'q'.{COLOR_RESET}")

    def show_feedback(self, question_data, user_answer_index, original_index):
        """Show feedback based on the user's answer with colors."""
        question_text, options, correct_answer_index, category, explanation = question_data
        # Ensure we use the exact question text from the loaded list for history update
        original_question_text = self.questions[original_index][0]

        is_correct = (user_answer_index == correct_answer_index)

        if is_correct:
            print(f"\n{COLOR_CORRECT}Correct! \U0001F389{COLOR_RESET}")
            self.score += 1
        else:
            correct_option_text = options[correct_answer_index]
            print(f"\n{COLOR_INCORRECT}Incorrect. \U0001F61E The correct answer was: {correct_answer_index + 1}. {correct_option_text}{COLOR_RESET}")
            if explanation: # Show explanation only if incorrect and available
                 print(f"{COLOR_EXPLANATION}Explanation: {explanation}{COLOR_RESET}")

        # Update history using the original question text
        self.update_history(original_question_text, category, is_correct)
        self.total_questions_session += 1
        input(f"\n{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")

    def show_stats(self):
        """Display overall and category-specific statistics with colors."""
        self.clear_screen()
        print(f"{COLOR_HEADER}--- Study Statistics ---{COLOR_RESET}")

        total_attempts = self.study_history.get("total_attempts", 0)
        total_correct = self.study_history.get("total_correct", 0)
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        print(f"\n{COLOR_HEADER}Overall Performance:{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Total Questions Answered (All Time):{COLOR_RESET} {COLOR_STATS_VALUE}{total_attempts}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Total Correct (All Time):{COLOR_RESET} {COLOR_STATS_VALUE}{total_correct}{COLOR_RESET}")
        print(f"  {COLOR_STATS_LABEL}Overall Accuracy (All Time):{COLOR_RESET} {COLOR_STATS_VALUE}{overall_accuracy:.2f}%{COLOR_RESET}")

        print(f"\n{COLOR_HEADER}Performance by Category:{COLOR_RESET}")
        categories_data = self.study_history.get("categories", {})
        sorted_categories = sorted(categories_data.items())

        if not sorted_categories:
            print(f"  {COLOR_EXPLANATION}No category data yet.{COLOR_RESET}")
        else:
            max_len = max((len(cat) for cat in categories_data.keys()), default=10) if categories_data else 10
            header = f"  {COLOR_STATS_LABEL}{'Category'.ljust(max_len)} | Correct | Attempts | Accuracy{COLOR_RESET}"
            print(header)
            print(f"  {COLOR_HEADER}{'-' * max_len}-+---------+----------+----------{COLOR_RESET}")
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0)
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) if cat_attempts > 0 else 0
                acc_color = COLOR_CORRECT if cat_accuracy >= 75 else (COLOR_YELLOW if cat_accuracy >= 50 else COLOR_INCORRECT)
                print(f"  {category.ljust(max_len)} | {COLOR_STATS_VALUE}{str(cat_correct).rjust(7)}{COLOR_RESET} | {COLOR_STATS_VALUE}{str(cat_attempts).rjust(8)}{COLOR_RESET} | {acc_color}{f'{cat_accuracy:.1f}%'.rjust(8)}{COLOR_RESET}")

        # --- Updated Section: Show ALL question history ---
        print(f"\n{COLOR_HEADER}Performance on Specific Questions (All History):{COLOR_RESET}")
        question_stats = self.study_history.get("questions", {})
        if not question_stats:
            print(f"  {COLOR_EXPLANATION}No specific question data yet.{COLOR_RESET}")
        else:
            # Sort questions alphabetically by question text
            sorted_questions = sorted(question_stats.items())

            print(f"  {COLOR_STATS_LABEL}Showing all questions with recorded history:{COLOR_RESET}")
            for q_text, stats in sorted_questions:
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                # Ensure attempts is not zero before calculating accuracy
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                # Determine color based on accuracy
                acc_color = COLOR_CORRECT if accuracy >= 75 else (COLOR_YELLOW if accuracy >= 50 else COLOR_INCORRECT)

                # Get last result if history exists
                last_result = "N/A"
                last_color = COLOR_EXPLANATION
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_color = COLOR_CORRECT if last_correct else COLOR_INCORRECT

                # Truncate long question text
                display_text = (q_text[:70] + '...') if len(q_text) > 70 else q_text
                print(f"    - \"{display_text}\"")
                print(f"      ({COLOR_STATS_VALUE}{attempts}{COLOR_RESET} attempts, {acc_color}{accuracy:.1f}%{COLOR_RESET} acc.) Last: {last_color}{last_result}{COLOR_RESET}")
        # --- End Updated Section ---

        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def select_category(self):
        """Allow the user to select a category to focus on, using colors."""
        self.clear_screen()
        print(f"{COLOR_HEADER}--- Select a Category ---{COLOR_RESET}")
        sorted_categories = sorted(list(self.categories))
        if not sorted_categories:
            print(f"{COLOR_INCORRECT}No categories found!{COLOR_RESET}")
            time.sleep(2)
            return None # Indicate no selection possible

        print(f"{COLOR_OPTIONS}0. All Categories{COLOR_RESET}")
        for i, category in enumerate(sorted_categories):
            print(f"{COLOR_OPTIONS}{i + 1}. {category}{COLOR_RESET}")

        while True:
            try:
                prompt = f"{COLOR_PROMPT}Enter category number (0-{len(sorted_categories)}), or 'b' to go back: {COLOR_RESET}"
                choice = input(prompt).lower().strip()
                if choice == 'b':
                    return 'b' # Indicate going back
                num_choice = int(choice)
                if num_choice == 0:
                    return None # None signifies All Categories
                elif 1 <= num_choice <= len(sorted_categories):
                    return sorted_categories[num_choice - 1]
                else:
                    print(f"{COLOR_INCORRECT}Invalid choice.{COLOR_RESET}")
            except ValueError:
                print(f"{COLOR_INCORRECT}Invalid input. Please enter a number or 'b'.{COLOR_RESET}")

    def clear_stats(self):
        """Clear all stored statistics after confirmation."""
        self.clear_screen()
        print(f"{COLOR_INCORRECT}--- Clear Statistics ---{COLOR_RESET}")
        confirm = input(f"{COLOR_PROMPT}Are you sure you want to delete ALL study history? This cannot be undone. (yes/no): {COLOR_RESET}").lower().strip()
        if confirm == 'yes':
            self.study_history = self._default_history()
            # Re-populate categories from loaded questions, but reset counts
            for category in self.categories:
                 self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.save_history()
            print(f"\n{COLOR_CORRECT}Study history has been cleared.{COLOR_RESET}")
        else:
            print(f"\n{COLOR_YELLOW}Operation cancelled. History not cleared.{COLOR_RESET}")
        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def run_quiz(self, category_filter=None):
        """Run the main quiz loop for the CLI."""
        self.score = 0
        self.total_questions_session = 0
        self.answered_indices_session = [] # Reset session history

        while True:
            self.clear_screen()
            if category_filter:
                 print(f"{COLOR_HEADER}Current Category: {category_filter}{COLOR_RESET}")
            else:
                 print(f"{COLOR_HEADER}Current Category: All{COLOR_RESET}")
            print(f"{COLOR_STATS_LABEL}Session Score: {COLOR_STATS_VALUE}{self.score}/{self.total_questions_session}{COLOR_RESET}")

            question_data, original_index = self.select_question(category_filter)

            if question_data is None:
                 print(f"{COLOR_INCORRECT}Could not select a question (possibly none left?). Returning to menu.{COLOR_RESET}")
                 time.sleep(3)
                 break # Exit loop if no question can be selected

            self.display_question(question_data)
            user_answer = self.get_user_answer(len(question_data[1])) # Pass number of options

            if user_answer == 'q':
                break # Quit the quiz session
            elif user_answer == 's':
                # Fixed NameError here by ensuring COLOR_YELLOW is defined
                print(f"\n{COLOR_YELLOW}Skipping question...{COLOR_RESET}")
                # Optionally mark skip as incorrect in history
                # self.update_history(question_data[0], question_data[3], is_correct=False)
                self.total_questions_session += 1 # Count skipped question in session total
                input(f"{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
                continue # Go to the next question

            # If a valid answer number was given
            self.show_feedback(question_data, user_answer, original_index)

        print(f"\n{COLOR_HEADER}Quiz session finished.{COLOR_RESET}")
        print(f"{COLOR_STATS_LABEL}Your score for this session: {COLOR_STATS_VALUE}{self.score} / {self.total_questions_session}{COLOR_RESET}")
        self.save_history() # Save history at the end of a session
        input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")

    def main_menu(self):
        """Display the main menu and handle user choices for CLI."""
        while True:
            self.clear_screen()
            print(f"{COLOR_HEADER}--- Linux+ Study Game ---{COLOR_RESET}")
            print(f"{COLOR_OPTIONS}1. Start Quiz (All Categories){COLOR_RESET}")
            print(f"{COLOR_OPTIONS}2. Start Quiz (Select Category){COLOR_RESET}")
            print(f"{COLOR_OPTIONS}3. View Statistics{COLOR_RESET}")
            print(f"{COLOR_OPTIONS}4. Clear Statistics{COLOR_RESET}")
            print(f"{COLOR_OPTIONS}5. Quit{COLOR_RESET}")
            print(f"{COLOR_HEADER}-------------------------{COLOR_RESET}")
            choice = input(f"{COLOR_PROMPT}Enter your choice: {COLOR_RESET}")

            if choice == '1':
                self.run_quiz(category_filter=None)
            elif choice == '2':
                selected_category = self.select_category()
                if selected_category == 'b':
                    continue # Go back to main menu
                # If selected_category is None (All) or a specific category string
                self.run_quiz(category_filter=selected_category)
            elif choice == '3':
                self.show_stats()
            elif choice == '4':
                self.clear_stats()
            elif choice == '5':
                print(f"{COLOR_YELLOW}Saving history and quitting. Goodbye!{COLOR_RESET}")
                self.save_history()
                sys.exit()
            else:
                print(f"{COLOR_INCORRECT}Invalid choice. Please try again.{COLOR_RESET}")
                time.sleep(1)

# --- GUI Game Class ---
class LinuxPlusStudyGUI:
    """Handles the Tkinter Graphical User Interface for the study game."""
    def __init__(self, root, game_logic):
        self.root = root
        self.game_logic = game_logic # Use the CLI class instance for logic

        self.current_question_index = -1 # Start before the first question
        self.current_question_data = None
        self.selected_answer_var = tk.IntVar(value=-1) # Variable for radio buttons
        self.quiz_active = False
        self.current_category_filter = None

        self._setup_styles()
        self._setup_ui()
        self._load_initial_state()

    def _setup_styles(self):
        """Configure ttk styles for a nicer look."""
        self.style = ttk.Style()
        # Try different themes if available, fallback to 'clam' or default
        available_themes = self.style.theme_names()
        if 'vista' in available_themes:
            self.style.theme_use('vista')
        elif 'aqua' in available_themes: # macOS
             self.style.theme_use('aqua')
        elif 'clam' in available_themes:
            self.style.theme_use('clam')
        # else: use default theme

        # Define colors (adapt if needed based on theme)
        BG_COLOR = "#f0f0f0" # Light grey background
        TEXT_COLOR = "#333333"
        HEADER_COLOR = "#003366" # Dark blue
        BUTTON_BG = "#d0d0d0"
        BUTTON_FG = "#000000"
        CORRECT_COLOR = "#008000" # Green
        INCORRECT_COLOR = "#cc0000" # Red
        EXPLANATION_BG = "#ffffff" # White background for explanation

        # Configure styles
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10)) # Changed font
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=HEADER_COLOR)
        self.style.configure("Category.TLabel", font=("Segoe UI", 10, "italic"), foreground="#555555")
        self.style.configure("Status.TLabel", font=("Segoe UI", 9), foreground="#333333")
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5, background=BUTTON_BG, foreground=BUTTON_FG)
        self.style.map("TButton", background=[('active', '#b0b0b0')]) # Slightly darker on hover/press
        self.style.configure("Big.TButton", font=("Segoe UI", 12, "bold"), padding=8)
        self.style.configure("TRadiobutton", background=BG_COLOR, font=("Segoe UI", 10), indicatorrelief=tk.FLAT)
        self.style.map("TRadiobutton", indicatorbackground=[('selected', HEADER_COLOR)]) # Color the radio indicator
        self.style.configure("Feedback.TLabel", font=("Segoe UI", 11, "bold"), padding=5)
        self.style.configure("Correct.Feedback.TLabel", foreground=CORRECT_COLOR, background=BG_COLOR)
        self.style.configure("Incorrect.Feedback.TLabel", foreground=INCORRECT_COLOR, background=BG_COLOR)
        # Explanation Label Style (using standard tk Label for better background control)
        self.explanation_style = {
            "bg": EXPLANATION_BG,
            "fg": TEXT_COLOR,
            "relief": "solid",
            "borderwidth": 1,
            "padx": 5,
            "pady": 5,
            "font": ("Consolas", 9) # Monospace font for explanation
        }


    def _setup_ui(self):
        """Create the main UI elements."""
        self.root.title("Linux+ Study Game")
        self.root.geometry("850x700") # Slightly wider/taller
        self.root.configure(bg="#f0f0f0") # Use BG_COLOR

        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="15") # Increased padding
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Header ---
        header_frame = ttk.Frame(main_frame, padding=(0, 0, 0, 15)) # More bottom padding
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Linux+ Study Game", style="Header.TLabel").pack(side=tk.LEFT)
        self.status_label = ttk.Label(header_frame, text="Status: Idle", style="Status.TLabel")
        self.status_label.pack(side=tk.RIGHT, padx=5)

        # --- Quiz Area Frame ---
        # Using a standard tk.Frame for better border control if needed
        quiz_frame_outer = tk.Frame(main_frame, bd=1, relief="sunken", bg="#cccccc")
        quiz_frame_outer.pack(fill=tk.BOTH, expand=True, pady=10)
        quiz_frame = ttk.Frame(quiz_frame_outer, padding="15") # Inner padding
        quiz_frame.pack(fill=tk.BOTH, expand=True)


        # Category Label
        self.category_label = ttk.Label(quiz_frame, text="Category: N/A", style="Category.TLabel")
        self.category_label.pack(anchor=tk.W, pady=(0, 10)) # More space below category

        # Question Text (Scrollable) - Using tk.Text for better control
        q_frame = tk.Frame(quiz_frame, height=120, bd=1, relief="solid", bg="#ffffff") # White background
        q_frame.pack(fill=tk.X, pady=5)
        q_frame.pack_propagate(False) # Prevent resizing based on content

        q_scroll = ttk.Scrollbar(q_frame, orient=tk.VERTICAL)
        self.question_text = tk.Text(q_frame, wrap=tk.WORD, height=4,
                                     yscrollcommand=q_scroll.set,
                                     font=("Segoe UI", 11), relief="flat", # Changed font
                                     bg="#ffffff", fg="#333333", bd=0, state=tk.DISABLED,
                                     padx=5, pady=5) # Padding inside text area
        q_scroll.config(command=self.question_text.yview)
        q_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.question_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Options Frame (Radio Buttons)
        self.options_frame = ttk.Frame(quiz_frame, padding=(0, 10, 0, 5)) # More padding
        self.options_frame.pack(fill=tk.X, pady=10)
        # Options label removed, implied by radio buttons

        # Feedback Area
        self.feedback_label = ttk.Label(quiz_frame, text="", style="Feedback.TLabel", anchor=tk.W) # Align left
        self.feedback_label.pack(fill=tk.X, pady=(10, 5))
        # Using standard tk.Label for explanation styling
        self.explanation_label = tk.Label(quiz_frame, text="", wraplength=750, anchor=tk.W, justify=tk.LEFT, **self.explanation_style)
        self.explanation_label.pack(fill=tk.X, pady=5)
        self.explanation_label.pack_forget() # Hide initially

        # --- Control Frame ---
        control_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0)) # More top padding
        control_frame.pack(fill=tk.X)

        # Left side (Quiz Controls)
        quiz_controls = ttk.Frame(control_frame)
        quiz_controls.pack(side=tk.LEFT)
        self.submit_button = ttk.Button(quiz_controls, text="Submit Answer", command=self._submit_answer_gui, state=tk.DISABLED, style="Big.TButton") # Bigger button
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.next_button = ttk.Button(quiz_controls, text="Next Question", command=self._next_question_gui, state=tk.DISABLED, style="Big.TButton") # Bigger button
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Right side (Main Actions)
        main_actions = ttk.Frame(control_frame)
        main_actions.pack(side=tk.RIGHT)
        ttk.Button(main_actions, text="Start Quiz", command=self._start_quiz_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="View Stats", command=self._show_stats_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Clear Stats", command=self._clear_stats_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(main_actions, text="Quit", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def _load_initial_state(self):
        """Set the initial welcome message."""
        self._update_status("Ready. Click 'Start Quiz' to begin.")
        self._clear_quiz_area()
        self.question_text.config(state=tk.NORMAL)
        self.question_text.insert(tk.END, "Welcome to the Linux+ Study Game!\n\n"
                                          "Select 'Start Quiz' to choose a category and begin.")
        self.question_text.config(state=tk.DISABLED)

    def _clear_quiz_area(self):
        """Clear question, options, and feedback."""
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete(1.0, tk.END)
        self.question_text.config(state=tk.DISABLED)
        # Destroy only radiobuttons in options_frame
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.destroy()
        self.feedback_label.config(text="", style="Feedback.TLabel") # Reset style too
        self.explanation_label.pack_forget() # Hide explanation
        self.selected_answer_var.set(-1) # Reset selection

    def _update_status(self, message):
        """Update the status bar label."""
        self.status_label.config(text=f"Status: {message}")

    def _start_quiz_dialog(self):
        """Show dialog to select category and start quiz."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Start Quiz")
        dialog.geometry("400x200") # Adjusted size
        dialog.transient(self.root) # Stay on top of main window
        dialog.grab_set() # Modal
        dialog.resizable(False, False)
        dialog.configure(bg="#e1e1e1") # Match theme

        ttk.Label(dialog, text="Select Category:", font=("Segoe UI", 12, "bold"), background="#e1e1e1").pack(pady=(15, 5))

        categories = ["All Categories"] + sorted(list(self.game_logic.categories))
        category_var = tk.StringVar(value=categories[0])

        # Use OptionMenu for a dropdown feel
        option_menu = ttk.OptionMenu(dialog, category_var, categories[0], *categories)
        option_menu.config(width=30)
        option_menu.pack(pady=10, padx=20)


        def on_start():
            selected = category_var.get()
            self.current_category_filter = None if selected == "All Categories" else selected
            dialog.destroy()
            self._start_quiz_session()

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Start", command=on_start, style="Big.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)


        self.root.wait_window(dialog) # Wait for dialog to close

    def _start_quiz_session(self):
        """Begin a new quiz session."""
        self.quiz_active = True
        self.game_logic.score = 0
        self.game_logic.total_questions_session = 0
        self.game_logic.answered_indices_session = [] # Reset session answers
        self.current_question_index = -1 # Reset index
        cat_display = self.current_category_filter or 'All'
        self._update_status(f"Quiz started (Category: {cat_display}).")
        self._next_question_gui() # Load the first question

    def _display_question_gui(self):
        """Update the GUI with the current question data."""
        if not self.current_question_data:
            self._clear_quiz_area()
            self.question_text.config(state=tk.NORMAL)
            self.question_text.insert(tk.END, "No more questions in this category/session.")
            self.question_text.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.quiz_active = False
            self._update_status("Quiz finished or no questions found.")
            return

        self._clear_quiz_area() # Clear previous stuff

        q_text, options, _, category, _ = self.current_question_data

        # Display Category
        self.category_label.config(text=f"Category: {category}")

        # Display Question
        self.question_text.config(state=tk.NORMAL)
        self.question_text.insert(tk.END, q_text)
        self.question_text.config(state=tk.DISABLED)

        # Display Options (Radio Buttons)
        self.selected_answer_var.set(-1) # Deselect previous answer
        for i, option in enumerate(options):
            # FIX: Removed justify=tk.LEFT from ttk.Radiobutton
            rb = ttk.Radiobutton(self.options_frame, text=option, variable=self.selected_answer_var,
                                 value=i, style="TRadiobutton")
            rb.pack(anchor=tk.W, padx=10, pady=3) # Less vertical padding

        # Enable Submit, disable Next
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def _next_question_gui(self):
        """Select and display the next question."""
        if not self.quiz_active:
             messagebox.showinfo("Quiz Over", "The quiz session is not active. Please start a new quiz.")
             return

        # Select next question using game logic
        question_data, original_index = self.game_logic.select_question(self.current_category_filter)

        if question_data is None:
            # Handle end of quiz or no questions found
            self.current_question_data = None
            self.current_question_index = -1
            self._display_question_gui() # Show end message
            messagebox.showinfo("Quiz Complete", "You've answered all available questions in this category for this session!")
        else:
            self.current_question_data = question_data
            self.current_question_index = original_index # Store the original index
            self._display_question_gui() # Display the new question

    def _submit_answer_gui(self):
        """Process the user's submitted answer."""
        user_answer_index = self.selected_answer_var.get()

        if user_answer_index == -1:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        if not self.current_question_data:
            messagebox.showerror("Error", "No current question data available.")
            return

        q_text, options, correct_answer_index, category, explanation = self.current_question_data
        # Use the original question text from the full list for history
        original_question_text = self.game_logic.questions[self.current_question_index][0]

        is_correct = (user_answer_index == correct_answer_index)

        # Update feedback label and style
        if is_correct:
            self.feedback_label.config(text="Correct! \U0001F389", style="Correct.Feedback.TLabel")
            self.game_logic.score += 1
        else:
            correct_option_text = options[correct_answer_index]
            # Ensure feedback text wraps if too long
            feedback_text = f"Incorrect. \U0001F61E Correct was: {correct_answer_index + 1}. {correct_option_text}"
            self.feedback_label.config(text=feedback_text, style="Incorrect.Feedback.TLabel")
            # Show explanation if incorrect and available
            if explanation:
                 self.explanation_label.config(text=f"Explanation: {explanation}")
                 # Make sure explanation label is visible
                 self.explanation_label.pack(fill=tk.X, pady=5, before=self.feedback_label)
            else:
                 self.explanation_label.pack_forget()


        # Update history via game logic
        self.game_logic.update_history(original_question_text, category, is_correct)
        self.game_logic.total_questions_session += 1
        self.game_logic.save_history() # Save after each answer

        # Update UI state
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
        # Disable radio buttons after submitting
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ttk.Radiobutton):
                widget.config(state=tk.DISABLED)

        self._update_status(f"Answer submitted. Score: {self.game_logic.score}/{self.game_logic.total_questions_session}")


    def _show_stats_gui(self):
        """Display statistics in a Toplevel window."""
        stats_win = tk.Toplevel(self.root)
        stats_win.title("Study Statistics")
        stats_win.geometry("800x600") # Wider for full stats
        stats_win.transient(self.root)
        stats_win.grab_set()
        stats_win.configure(bg="#f0f0f0")

        # Use a Text widget for scrollable stats display
        stats_text = tk.Text(stats_win, wrap=tk.WORD, font=("Consolas", 10), relief="flat", bg="#ffffff", bd=1, padx=10, pady=10) # White background
        stats_scroll = ttk.Scrollbar(stats_win, orient=tk.VERTICAL, command=stats_text.yview)
        stats_text.config(yscrollcommand=stats_scroll.set)

        stats_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Define tags for coloring ---
        stats_text.tag_configure("header", font=("Segoe UI", 12, "bold"), foreground="#003366")
        stats_text.tag_configure("subheader", font=("Segoe UI", 10, "bold"))
        stats_text.tag_configure("label", foreground="#555555")
        stats_text.tag_configure("value", foreground="#000000")
        stats_text.tag_configure("correct", foreground="#008000")
        stats_text.tag_configure("incorrect", foreground="#cc0000")
        stats_text.tag_configure("neutral", foreground="#555555") # For N/A or 50%

        # --- Populate Stats Text ---
        stats_text.insert(tk.END, "--- Study Statistics ---\n\n", "header")

        # Overall Performance
        history = self.game_logic.study_history
        total_attempts = history.get("total_attempts", 0)
        total_correct = history.get("total_correct", 0)
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        stats_text.insert(tk.END, "Overall Performance (All Time):\n", "subheader")
        stats_text.insert(tk.END, "  Total Questions Answered: ", "label")
        stats_text.insert(tk.END, f"{total_attempts}\n", "value")
        stats_text.insert(tk.END, "  Total Correct:            ", "label")
        stats_text.insert(tk.END, f"{total_correct}\n", "value")
        stats_text.insert(tk.END, "  Overall Accuracy:         ", "label")
        stats_text.insert(tk.END, f"{overall_accuracy:.2f}%\n\n", "value")

        # Performance by Category
        stats_text.insert(tk.END, "Performance by Category:\n", "subheader")
        categories_data = history.get("categories", {})
        sorted_categories = sorted(categories_data.items())

        if not sorted_categories:
            stats_text.insert(tk.END, "  No category data yet.\n", "label")
        else:
            max_len = max((len(cat) for cat in categories_data.keys()), default=10) if categories_data else 10
            header = f"  {'Category'.ljust(max_len)} | {'Correct'.rjust(7)} | {'Attempts'.rjust(8)} | {'Accuracy'.rjust(8)}\n"
            stats_text.insert(tk.END, header, "label")
            stats_text.insert(tk.END, f"  {'-' * max_len}-+---------+----------+----------\n", "label")
            for category, stats in sorted_categories:
                cat_attempts = stats.get("attempts", 0)
                cat_correct = stats.get("correct", 0)
                cat_accuracy = (cat_correct / cat_attempts * 100) if cat_attempts > 0 else 0
                # Determine accuracy color tag
                acc_tag = "correct" if cat_accuracy >= 75 else ("neutral" if cat_accuracy >= 50 else "incorrect")

                stats_text.insert(tk.END, f"  {category.ljust(max_len)} | ")
                stats_text.insert(tk.END, f"{str(cat_correct).rjust(7)}", "value")
                stats_text.insert(tk.END, " | ")
                stats_text.insert(tk.END, f"{str(cat_attempts).rjust(8)}", "value")
                stats_text.insert(tk.END, " | ")
                stats_text.insert(tk.END, f"{f'{cat_accuracy:.1f}%'.rjust(8)}\n", acc_tag) # Apply tag here
        stats_text.insert(tk.END, "\n")

        # --- Updated Section: Show ALL question history ---
        stats_text.insert(tk.END, "Performance on Specific Questions (All History):\n", "subheader")
        question_stats = history.get("questions", {})
        if not question_stats:
            stats_text.insert(tk.END, "  No specific question data yet.\n", "label")
        else:
            # Sort questions alphabetically
            sorted_questions = sorted(question_stats.items())

            for q_text, stats in sorted_questions:
                attempts = stats.get("attempts", 0)
                correct = stats.get("correct", 0)
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                acc_tag = "correct" if accuracy >= 75 else ("neutral" if accuracy >= 50 else "incorrect")

                # Get last result if history exists
                last_result = "N/A"
                last_tag = "neutral"
                if stats.get("history"):
                    last_correct = stats["history"][-1].get("correct")
                    last_result = "Correct" if last_correct else "Incorrect"
                    last_tag = "correct" if last_correct else "incorrect"

                # Use insert with tags
                display_text = (q_text[:90] + '...') if len(q_text) > 90 else q_text # Adjusted length
                stats_text.insert(tk.END, f"  - \"{display_text}\"\n")
                stats_text.insert(tk.END, "      (")
                stats_text.insert(tk.END, f"{attempts}", "value")
                stats_text.insert(tk.END, " attempts, ")
                stats_text.insert(tk.END, f"{accuracy:.1f}%", acc_tag)
                stats_text.insert(tk.END, " acc.) Last: ")
                stats_text.insert(tk.END, f"{last_result}\n\n", last_tag)
        # --- End Updated Section ---

        # --- End Populate ---

        stats_text.config(state=tk.DISABLED) # Make text read-only

        # Close button
        close_button = ttk.Button(stats_win, text="Close", command=stats_win.destroy)
        close_button.pack(pady=10)

        self.root.wait_window(stats_win)


    def _clear_stats_gui(self):
        """Ask for confirmation and clear stats via game logic."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete ALL study history? This cannot be undone.", parent=self.root):
            self.game_logic.study_history = self.game_logic._default_history()
             # Re-populate categories from loaded questions, but reset counts
            for category in self.game_logic.categories:
                 self.game_logic.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.game_logic.save_history()
            messagebox.showinfo("Stats Cleared", "Study history has been cleared.", parent=self.root)
            self._update_status("Study history cleared.")


# --- Main Execution Block ---
if __name__ == "__main__":
    # Initialize colorama (if available) for CLI
    if 'colorama' in sys.modules:
        colorama.init(autoreset=True)

    # Create instance of the game logic class
    # This instance will be used by both CLI and GUI
    game_engine = LinuxPlusStudyGame()

    # Ask user for interface preference
    interface_choice = ""
    # Check if running in a non-interactive environment (e.g., Git Bash without interactive TTY)
    # or if arguments are passed (might indicate automated execution)
    is_interactive = sys.stdin.isatty() and len(sys.argv) == 1

    if not is_interactive:
        print("Non-interactive environment detected or arguments provided. Defaulting to CLI.")
        interface_choice = 'cli'
    else:
        while interface_choice not in ['cli', 'gui']:
            # Use print directly for initial prompt to ensure colors work if available
            print(f"{COLOR_PROMPT}Choose interface ({COLOR_OPTIONS}CLI{COLOR_PROMPT} or {COLOR_OPTIONS}GUI{COLOR_PROMPT}): {COLOR_RESET}", end='')
            # Flush output to ensure prompt appears before input is read
            sys.stdout.flush()
            try:
                interface_choice = input().lower().strip()
            except EOFError: # Handle case where input stream is closed unexpectedly
                 print("\nEOF received. Exiting.")
                 sys.exit(1)

            if interface_choice not in ['cli', 'gui']:
                 print(f"{COLOR_INCORRECT}Invalid choice. Please type 'cli' or 'gui'.{COLOR_RESET}")


    if interface_choice == 'gui':
        # Run the GUI version
        root = tk.Tk()
        app = LinuxPlusStudyGUI(root, game_engine)
        # Attempt to set a modern icon (optional, requires icon file)
        # try:
        #     # You might need to provide the full path to the icon file
        #     # Example for Windows: root.iconbitmap('path/to/icon.ico')
        #     # Example for Linux/macOS (using PhotoImage for PNG/GIF):
        #     # img = tk.PhotoImage(file='path/to/icon.png')
        #     # root.tk.call('wm', 'iconphoto', root._w, img)
        #     pass # Add icon setting code here if you have an icon file
        # except Exception as e:
        #     print(f"Could not set window icon: {e}")

        root.mainloop()
    else:
        # Run the CLI version
        game_engine.main_menu()

