import random
import os
import sys
import time
import json
from datetime import datetime

class LinuxPlusStudyGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.total_questions = 0
        self.categories = set()
        self.answered_questions = []  # Track answered questions
        self.history_file = "linux_plus_history.json"
        self.study_history = self.load_history()
        self.load_questions() # Load questions after initializing history

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_history(self):
        """Load study history from file if it exists."""
        try:
            with open(self.history_file, 'r') as f:
                # Ensure default keys exist if loading an older format
                history = json.load(f)
                history.setdefault("sessions", [])
                history.setdefault("questions", {})
                history.setdefault("categories", {})
                history.setdefault("total_correct", 0)
                history.setdefault("total_attempts", 0)
                return history
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default history structure if file doesn't exist or is invalid
            return {
                "sessions": [],
                "questions": {},  # Track performance per question
                "categories": {},  # Track performance per category
                "total_correct": 0,
                "total_attempts": 0
            }

    def save_history(self):
        """Save study history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.study_history, f, indent=2)

    def load_questions(self):
        """Load sample Linux+ questions, commands, and definitions."""
        # Question format: (question_text, [options], correct_answer_index, category, explanation)
        # --- Existing Questions ---
        existing_questions = [
            # Troubleshooting questions from the provided file (truncated for brevity)
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
             "`update-grub` is a script commonly found on Debian-based systems (like Ubuntu) that acts as a wrapper for `grub-mkconfig -o /boot/grub/grub.cfg`. Example: `sudo update-grub`"), # Note: Objectives list grub2-update, which is less common. update-grub is more standard for this action.

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
              # ... (other existing command questions would go here) ...
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
                # --- The rest of the Definition Questions go here ---

        ]


        # Combine all question types
        self.questions.extend(existing_questions)
        self.questions.extend(command_questions)
        self.questions.extend(definition_questions)

        # Populate categories
        for q in self.questions:
            self.categories.add(q[3]) # Category is the 4th element (index 3)

        # Update history with categories from questions if not already present
        for category in self.categories:
            self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        self.save_history() # Save potentially updated categories


    def update_history(self, question_text, category, is_correct):
        """Update study history with the result of the answered question."""
        timestamp = datetime.now().isoformat()

        # Update overall stats
        self.study_history["total_attempts"] += 1
        if is_correct:
            self.study_history["total_correct"] += 1

        # Update question-specific stats
        q_stats = self.study_history["questions"].setdefault(question_text, {"correct": 0, "attempts": 0, "history": []})
        q_stats["attempts"] += 1
        if is_correct:
            q_stats["correct"] += 1
        q_stats["history"].append({"timestamp": timestamp, "correct": is_correct})
        # Keep only the last N attempts per question if desired (e.g., last 10)
        # q_stats["history"] = q_stats["history"][-10:]

        # Update category-specific stats
        cat_stats = self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        cat_stats["attempts"] += 1
        if is_correct:
            cat_stats["correct"] += 1

        # Optionally, record session info (can be enhanced)
        # self.study_history["sessions"].append({"timestamp": timestamp, "question": question_text, "category": category, "correct": is_correct})


    def select_question(self, category_filter=None):
        """Select a question, optionally filtered by category, avoiding recent repeats."""
        available_questions = [q for q_idx, q in enumerate(self.questions)
                               if q_idx not in self.answered_questions and
                               (category_filter is None or q[3] == category_filter)]

        if not available_questions:
            print("No more questions available in this category or session. Resetting answered list.")
            self.answered_questions = [] # Reset if all questions in filter/set were answered
            available_questions = [q for q_idx, q in enumerate(self.questions)
                                   if category_filter is None or q[3] == category_filter]
            if not available_questions: # Still no questions means category filter is invalid or no questions exist
                 print(f"Error: No questions found at all, even after reset. Filter: {category_filter}")
                 return None, -1


        # --- Weighted Selection Logic ---
        # Prioritize questions answered incorrectly or less frequently
        weights = []
        question_indices = [] # Store original indices

        # Gather original indices for available questions
        available_indices = [q_idx for q_idx, q in enumerate(self.questions)
                               if q_idx not in self.answered_questions and
                               (category_filter is None or q[3] == category_filter)]

        if not available_indices: # Should be handled above, but double-check
             print("Error: Could not find indices for available questions.")
             return None, -1


        for q_idx in available_indices:
             q_text = self.questions[q_idx][0]
             q_stats = self.study_history["questions"].get(q_text, {"correct": 0, "attempts": 0})
             attempts = q_stats["attempts"]
             correct = q_stats["correct"]

             # Basic weighting: higher weight for fewer attempts or lower accuracy
             # Avoid division by zero
             accuracy = (correct / attempts) if attempts > 0 else 0.5 # Assume 50% if never attempted
             weight = (1.0 - accuracy) + (1.0 / (attempts + 1)) # Prioritize low accuracy and low attempts
             weights.append(weight * 10) # Scale weight for better random.choices behavior
             question_indices.append(q_idx)


        if not question_indices or not weights:
             print("Error: Could not calculate weights or indices for question selection.")
             # Fallback to simple random choice if weighting fails
             fallback_idx = random.choice(available_indices)
             return self.questions[fallback_idx], fallback_idx


        # Perform weighted random choice using original indices
        try:
            # Use random.choices which handles weights directly
             chosen_original_index = random.choices(question_indices, weights=weights, k=1)[0]
             chosen_question = self.questions[chosen_original_index]

        except IndexError:
             print("Error during weighted selection. Falling back to random choice.")
             # Fallback if something goes wrong with weighted choice
             chosen_original_index = random.choice(available_indices)
             chosen_question = self.questions[chosen_original_index]

        # Add the chosen question's *original index* to the answered list for this session
        self.answered_questions.append(chosen_original_index)

        return chosen_question, chosen_original_index # Return question and its original index


    def display_question(self, question_data):
        """Display the question and options."""
        question_text, options, _, category, _ = question_data
        print(f"\n--- Category: {category} ---")
        print(f"\nQ: {question_text}\n")
        for i, option in enumerate(options):
            print(f"  {i + 1}. {option}")
        print("-" * (len(category) + 16)) # Adjust line length

    def get_user_answer(self, num_options):
        """Get and validate user input."""
        while True:
            try:
                answer = input(f"Your choice (1-{num_options}), 's' to skip, 'q' to quit: ").lower()
                if answer == 'q':
                    return 'q'
                if answer == 's':
                    return 's'
                choice = int(answer)
                if 1 <= choice <= num_options:
                    return choice - 1  # Return 0-based index
                else:
                    print("Invalid choice. Please enter a number within the options.")
            except ValueError:
                print("Invalid input. Please enter a number, 's', or 'q'.")

    def show_feedback(self, question_data, user_answer_index, original_index):
        """Show feedback based on the user's answer."""
        _, _, correct_answer_index, category, explanation = question_data
        question_text = self.questions[original_index][0] # Get text using original index

        is_correct = (user_answer_index == correct_answer_index)

        if is_correct:
            print("\nCorrect! \U0001F389") # Party Popper
            self.score += 1
        else:
            print(f"\nIncorrect. \U0001F61E The correct answer was: {correct_answer_index + 1}") # Disappointed Face
            print(f"Explanation: {explanation}")

        self.update_history(question_text, category, is_correct)
        self.total_questions += 1
        input("\nPress Enter to continue...")


    def show_stats(self):
        """Display overall and category-specific statistics."""
        self.clear_screen()
        print("--- Study Statistics ---")

        total_attempts = self.study_history["total_attempts"]
        total_correct = self.study_history["total_correct"]
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        print("\nOverall Performance:")
        print(f"  Total Questions Answered: {total_attempts}")
        print(f"  Total Correct: {total_correct}")
        print(f"  Overall Accuracy: {overall_accuracy:.2f}%")

        print("\nPerformance by Category:")
        sorted_categories = sorted(self.study_history["categories"].items())
        if not sorted_categories:
             print("  No category data yet.")
        else:
             # Calculate max category name length for alignment
             max_len = 0
             if self.study_history["categories"]:
                  max_len = max(len(cat) for cat in self.study_history["categories"].keys())

             print(f"  {'Category'.ljust(max_len)} | Correct | Attempts | Accuracy")
             print(f"  {'-' * max_len}-+---------+----------+----------")
             for category, stats in sorted_categories:
                 cat_attempts = stats.get("attempts", 0)
                 cat_correct = stats.get("correct", 0)
                 cat_accuracy = (cat_correct / cat_attempts * 100) if cat_attempts > 0 else 0
                 print(f"  {category.ljust(max_len)} | {str(cat_correct).rjust(7)} | {str(cat_attempts).rjust(8)} | {f'{cat_accuracy:.1f}%'.rjust(8)}")


        print("\nPerformance on Specific Questions (Top/Bottom 5 by Attempts):")
        # Sort questions by attempts to show most/least practiced
        # Filter out questions with 0 attempts before sorting
        attempted_questions = {q: s for q, s in self.study_history["questions"].items() if s.get("attempts", 0) > 0}

        if not attempted_questions:
             print("  No specific question data yet.")

        else:
            sorted_by_attempts = sorted(attempted_questions.items(), key=lambda item: item[1].get("attempts", 0), reverse=True)

            print("  Most Attempted:")
            for q_text, stats in sorted_by_attempts[:5]:
                 attempts = stats.get("attempts", 0)
                 correct = stats.get("correct", 0)
                 accuracy = (correct / attempts * 100) if attempts > 0 else 0
                 # Truncate long question text
                 display_text = (q_text[:70] + '...') if len(q_text) > 70 else q_text
                 print(f"    - \"{display_text}\" ({attempts} attempts, {accuracy:.1f}%)")


            if len(sorted_by_attempts) > 5:
                 print("\n  Least Attempted (but attempted at least once):")
                 for q_text, stats in sorted_by_attempts[-5:]:
                     attempts = stats.get("attempts", 0)
                     correct = stats.get("correct", 0)
                     accuracy = (correct / attempts * 100) if attempts > 0 else 0
                     display_text = (q_text[:70] + '...') if len(q_text) > 70 else q_text
                     print(f"    - \"{display_text}\" ({attempts} attempts, {accuracy:.1f}%)")


        input("\nPress Enter to return to the main menu...")


    def select_category(self):
        """Allow the user to select a category to focus on."""
        self.clear_screen()
        print("--- Select a Category ---")
        sorted_categories = sorted(list(self.categories))
        if not sorted_categories:
            print("No categories found!")
            time.sleep(2)
            return None

        print("0. All Categories")
        for i, category in enumerate(sorted_categories):
            print(f"{i + 1}. {category}")

        while True:
            try:
                choice = input(f"Enter category number (0-{len(sorted_categories)}), or 'b' to go back: ").lower()
                if choice == 'b':
                    return None # Indicate going back
                num_choice = int(choice)
                if num_choice == 0:
                    return None # None signifies All Categories
                elif 1 <= num_choice <= len(sorted_categories):
                    return sorted_categories[num_choice - 1]
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a number or 'b'.")


    def run_quiz(self, category_filter=None):
        """Run the main quiz loop, optionally filtered by category."""
        self.score = 0
        self.total_questions = 0
        self.answered_questions = [] # Reset session history

        while True:
            self.clear_screen()
            question_data, original_index = self.select_question(category_filter)

            if question_data is None:
                 print("Could not select a question. Returning to menu.")
                 time.sleep(2)
                 break # Exit loop if no question can be selected


            self.display_question(question_data)
            user_answer = self.get_user_answer(len(question_data[1])) # Pass number of options

            if user_answer == 'q':
                break # Quit the quiz session
            elif user_answer == 's':
                print("\nSkipping question...")
                 # Update history as skipped/incorrect? Optional. For now, just move on.
                 # self.update_history(question_data[0], question_data[3], is_correct=False) # Example: Treat skip as incorrect
                input("Press Enter to continue...")
                continue # Go to the next question

            self.show_feedback(question_data, user_answer, original_index)

        print("\nQuiz session finished.")
        print(f"Your score for this session: {self.score} / {self.total_questions}")
        self.save_history() # Save history at the end of a session
        input("Press Enter to return to the main menu...")


    def main_menu(self):
        """Display the main menu and handle user choices."""
        while True:
            self.clear_screen()
            print("--- Linux+ Study Game ---")
            print("1. Start Quiz (All Categories)")
            print("2. Start Quiz (Select Category)")
            print("3. View Statistics")
            print("4. Quit")
            print("-------------------------")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.run_quiz(category_filter=None)
            elif choice == '2':
                selected_category = self.select_category()
                if selected_category is not None: # Check if user didn't choose 'b' (back)
                    self.run_quiz(category_filter=selected_category)
                # If selected_category is None, loop back to main menu (handles 'All' or 'Back')
            elif choice == '3':
                self.show_stats()
            elif choice == '4':
                print("Saving history and quitting. Goodbye!")
                self.save_history()
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)

if __name__ == "__main__":
    game = LinuxPlusStudyGame()
    game.main_menu()
