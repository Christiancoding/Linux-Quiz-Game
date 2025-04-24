import random
import os
import sys
import time
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font as tkFont, scrolledtext # Import scrolledtext
from tkinter import filedialog # Import filedialog for GUI export

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
    # Ensure text is a string
    text_str = str(text)
    padding = (length - len(text_str) - 2) // 2
    if padding < 0: padding = 0 # Prevent negative padding
    print(f"{color}{char * padding} {text_str} {char * (length - len(text_str) - 2 - padding)}{COLOR_RESET}")


def cli_print_box(lines, title="", width=60, border_color=COLOR_BORDER, title_color=COLOR_HEADER, text_color=COLOR_WELCOME_TEXT):
    """Prints text within a colored box."""
    border = f"{border_color}{'=' * width}{COLOR_RESET}"
    print(border)
    if title:
        padding = (width - len(title) - 4) // 2
        if padding < 0: padding = 0
        print(f"{border_color}* { ' ' * padding }{title_color}{title}{border_color}{ ' ' * (width - len(title) - 4 - padding)} *{COLOR_RESET}")
        print(border)

    for line in lines:
        # Basic way to estimate length without color codes (might be inaccurate with complex chars)
        line_len_no_color = 0
        in_escape = False
        for char in line:
            if char == '\x1b':
                in_escape = True
            elif in_escape and char.isalpha():
                in_escape = False
            elif not in_escape:
                line_len_no_color += 1

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
            with open(self.history_file, 'r', encoding='utf-8') as f: # Specify encoding
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
        except Exception as e: # Catch other potential errors like permissions
            print(f"{COLOR_ERROR} Error loading history file '{self.history_file}': {e} {COLOR_RESET}")
            print(f"{COLOR_WARNING} Starting with empty history. {COLOR_RESET}")
            return self._default_history()

    def save_history(self):
        """Save study history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f: # Specify encoding
                json.dump(self.study_history, f, indent=2)
        except IOError as e:
            print(f"{COLOR_ERROR} Error saving history: {e} {COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ERROR} An unexpected error occurred during history save: {e} {COLOR_RESET}")


    def load_questions(self):
        """Load sample Linux+ questions, commands, and definitions."""
        # --- (Question data remains the same - truncated for brevity) ---
        # Note: Add your actual questions here
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
            ),
  
    # Troubleshooting questions from the provided file
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
    
    (
        "A Linux system administrator has found that a web server service is failing to start automatically at system boot, which necessitates a manual start each time. After booting, systemctl status of the service reports a failed state, yet no errors are recorded in the standard service logs. What is the most likely cause of this issue?",
        [
            "The server's network Time Protocol (NTP) configuration is incorrect, leading to time-related service start failures.",
            "There is an error with the ExecStart command that only manifests during the automated start sequence.",
            "The primary configuration file for the service contains syntax errors that are only checked during automated starts.",
            "The web server service is missing a dependency on network-online.target in the unit file, causing it to start before the network stack is ready."
        ],
        3,
        "Troubleshooting",
        "The correct answer is that the service unit does not correctly specify a dependency on the network being fully ready, which is needed for it to start properly. Since the web server starts without errors manually post-boot, this suggests that the service itself is configured correctly, but requires the network to be operational, something network-online.target would ensure. Checking with systemctl is-enabled network-online.target would verify if the network-online.target is considered in the boot process, thereby affecting dependent services. Incorrect ExecStart paths or name resolution failures would generate identifiable error messages, and time-zone configurations typically do not affect service start processes in this manner."
    ),
    
    (
        "A Linux server cannot establish connections to devices located on another segment of the network. Upon inspection, you discover that the server has been assigned an address of 192.168.1.126 with a mask indicating it can host up to 126 devices. A noted detail is that the segment's gateway resides at 192.168.1.129. What is the BEST explanation for this connectivity issue?",
        [
            "The server is assigned the special address of its subnet that denotes the beginning of the IP range",
            "The subnet does not provide an adequate number of host addresses for the network's needs",
            "The gateway's address falls outside the server's subnet range",
            "The server is utilizing the address typically reserved for broadcasting within its subnet"
        ],
        2,
        "Troubleshooting",
        "Given the server's assignment allowing for 126 devices, the subnet mask is inferred to be 255.255.255.128, which points to a /25 CIDR notation. This division places the server within the range of 192.168.1.0 to 192.168.1.127. The gateway's address of 192.168.1.129 falls outside of this range, meaning they are not on the same subnet; hence, the server cannot communicate through this gateway to other segments. The server is not assigned a special address such as a network or broadcast address, and the network's host capacity appears correctly configured for its subnet, dismissing the other provided options."
    ),
    
    (
        "A system administrator notices that a Linux server is performing poorly and, upon investigation, discovers that the I/O wait time is consistently high, even under normal workload. The server hosts a database service that is critical for the company's operations. Which of the following actions should the administrator take FIRST to address the high I/O wait issue?",
        [
            "Add additional RAM to the server to improve overall performance",
            "Check for network issues that may be affecting storage access",
            "Upgrade to faster storage hardware, such as NVMe drives",
            "Analyze disk I/O activity using utilities like iotop or iostat"
        ],
        3,
        "Troubleshooting",
        "The correct answer is 'Analyze disk I/O activity using utilities like iotop or iostat'. High I/O wait indicates that the CPU is spending significant time waiting for I/O operations to complete. Investigating disk I/O activity can help identify a potential bottleneck or excessive read/write operations that may be causing the high wait times. Upgrading the storage hardware may eventually be necessary, but initially, the administrator needs to pinpoint the problem. Adding RAM may reduce I/O by increasing the buffer cache, but it does not directly address I/O problems. Checking for network issues is unrelated to local I/O wait and does not help in this instance."
    ),
    
    (
        "When configuring a systemd service unit file, selecting which 'Type' setting will only consider the service started once the process finishes initializing and is ready to accept connections or tasks?",
        [
            "dbus",
            "forking",
            "oneshot",
            "simple",
            "notify",
            "idle"
        ],
        4,
        "Troubleshooting",
        "The 'Type=notify' setting is used when the service sends a notification message via the sd_notify() function to inform systemd that it has finished its initialization and is ready to handle requests. Other types such as 'simple' assume the service is ready as soon as the binary is executed, while 'forking' assumes readiness when the initial process exits."
    ),
    
    (
        "A process that has terminated but still appears in the process table with a status code 'Z' can be interacted with using the kill command to release its consumed resources.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "A process with a 'Z' status code is known as a zombie process. Zombie processes cannot be interacted with or killed using the kill command because they are already terminated and are only awaiting the parent process to read their exit status. The resources are held by the OS to allow the parent process to check the child's exit status. Only the parent process finishing or reading the exit status can remove the zombie from the process table."
    ),
    
    (
        "A Linux server is having intermittent problems resolving domain names, which is affecting the ability to access external websites. None of the remote services has reported downtime, and other devices on the same network are not experiencing any issues. What is the BEST step to take to diagnose the issue on the Linux server?",
        [
            "Ping the domain name in question to verify if domain name resolution works intermittently.",
            "Immediately modify the /etc/resolv.conf file to use different nameservers without doing further investigation.",
            "Check for a high number of outgoing DNS queries that might indicate a misconfigured service or DNS flood attack.",
            "Run dig +trace example.com or nslookup example.com to trace the path of the query from the root name servers downward."
        ],
        3,
        "Troubleshooting",
        "To diagnose domain name resolution issues, running dig +trace example.com or nslookup example.com can provide detailed information about the entire process of resolving a domain name, from the root servers down to the authoritative name servers. Comparing this output with known good output can reveal any discrepancies or failures in the resolution process. If dig +trace or nslookup provides the correct information, this indicates that the issue is intermittent or specific to the server's resolver configuration rather than a problem with the DNS server itself. Modifying /etc/resolv.conf would not fully diagnose the problem, as it could be a configuration issue, and checking for a high number of outgoing DNS queries or pinging the domain would not yield detailed resolution process information. Therefore, using dig (with the +trace option) or nslookup is the best initial step for diagnosis."
    ),
    
    (
        "A system administrator notices that an important server is experiencing intermittent problems with data integrity, and suspects filesystem corruption on one of its disks. After running fsck on the unmounted filesystem and fixing several errors, the administrator needs to ensure that the filesystem will be checked and repaired if necessary during the next system boot. Which of the following commands should the administrator use to schedule a filesystem check on boot?",
        [
            "tune2fs -c 1 /dev/sda1",
            "e2fsck -p /dev/sda1",
            "tune2fs -i 0 /dev/sda1",
            "tune2fs -C 0 /dev/sda1"
        ],
        0,
        "Troubleshooting",
        "The correct answer is tune2fs -c 1 /dev/sda1 because the command sets the maximum mount count (-c) to 1 for the filesystem on /dev/sda1, ensuring that fsck will be run the next time the filesystem is mounted. This is typically during the boot process. The option -C 0 sets the current mount count to 0, which is incorrect in this context because it does not schedule a check on the next boot. The -i flag is used for setting the interval between checks based on time, not on the number of mounts. The e2fsck -p /dev/sda1 executes a filesystem check, but does not schedule it for the next boot."
    ),
    
    (
        "An administrator notices that a recently mounted ext4 filesystem is not correctly recording the access times of files when they are read. The administrator suspects that a mount option may be causing this behavior. Which of the following mount options did the administrator most likely use when mounting the filesystem?",
        [
            "sync",
            "dirsync",
            "noatime",
            "relatime"
        ],
        2,
        "Troubleshooting",
        "The correct answer is 'noatime'. This mount option disables the updating of access times on files when they are read, which can improve performance, especially on frequently accessed filesystems. The 'relatime' option updates access times only if the previous access time was earlier than the current modify or change time. 'sync' and 'dirsync' are not directly related to file access time updates; 'sync' makes all writes synchronous, and 'dirsync' ensures directory changes are written synchronously, but neither disables the update of access times."
    ),
    
    (
        "The systemd service will fail to start if the time zone is incorrectly configured.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "The systemd service can start regardless of the time zone configuration. Time-zone misconfiguration could lead to problems with timed events or logging but it does not prevent systemd services from starting. This fact helps to ensure that even if there are configuration issues with the time zone, it will not impede the crucial system services from running."
    ),
    
    (
        "A user reports that they cannot write to a file named 'report.txt' which should be writable by members of the group 'staff'. As a sysadmin, you check the permissions with ls -l report.txt and the output shows -rw-r--r-- 1 root staff 1048576 Jan 01 12:34 report.txt. What is the most likely reason for the user being unable to write to the file?",
        [
            "The file is owned by the 'root' user, so only root can modify it",
            "The file only has write permissions for the owner",
            "The group 'staff' does not exist on the system",
            "The file is too large to be written to by group members"
        ],
        1,
        "Troubleshooting",
        "The correct answer is The file only has write permissions for the owner. The permission string -rw-r--r-- indicates that the owner of the file (in this case, 'root') has read and write permissions, the group 'staff' members and others have only read permissions. Therefore, although the user is in the correct group, they won't be able to write to the file unless the write permission is added for the group."
    ),
    
    (
        "A system administrator has noticed that over time, a Linux server's available memory decreases, even when the workload on the server remains consistent. The 'top' command shows a particular process gradually increasing its memory usage without releasing it back to the system. Which of the following tools should the administrator use to further investigate this suspected memory leak in the problematic process?",
        [
            "mpstat",
            "vmstat",
            "valgrind",
            "free"
        ],
        2,
        "Troubleshooting",
        "The valgrind tool is used to detect memory leaks and memory management problems in programs. When a process is suspected of having a memory leak because it progressively consumes more memory without freeing it, valgrind can be employed to analyze the process and identify where memory is not being appropriately released. free is a command that displays the amount of free and used memory in the system but does not detect memory leaks in processes. vmstat reports information about processes, memory, paging, block IO, traps, disks, and cpu activity, but does not specifically analyze memory leaks in individual processes. mpstat is used to monitor CPU utilization but does not analyze memory leaks in a process."
    ),
    
    (
        "A Linux administrator needs to ensure that a web-based application service does not start until after the graphical interface has been loaded. Which directive should the administrator use within the service's unit file to enforce this dependency?",
        [
            "BindsTo=graphical.target",
            "Wants=graphical.target",
            "After=graphical.target",
            "Requires=graphical.target"
        ],
        2,
        "Troubleshooting",
        "The After=graphical.target directive is used within a systemd unit file to specify that the service should start after the specified target, in this case, the graphical interface, has been reached during the boot process. The Requires=graphical.target establishes a strong dependency, but doesn't specify order. The BindsTo=graphical.target establishes an even stronger binding dependency, but also doesn't specify order. Wants=graphical.target creates a weaker dependency and doesn't guarantee the service will start after the graphical interface."
    ),
    
    (
        "The /proc/meminfo file provides information on the total amount of available memory, but it does not include details about memory committed to buffers and cached data.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "The /proc/meminfo file in Linux provides extensive information about the system's memory usage, including total memory, free memory, and memory used for buffers and cache. The statement is false because /proc/meminfo does include 'Buffers' and 'Cached' labels, which indicate the amount of memory used for buffer space and cache respectively. Not understanding what is represented in /proc/meminfo could lead to incorrect assessments of memory issues."
    ),
    
    (
        "A system administrator receives complaints from users that they cannot write to their home directories on a Linux server despite appearing to have available disk space. The administrator suspects a quota limitation. Which command should the administrator use to verify the user quotas and determine which users have reached their disk space limit?",
        [
            "repquota -a",
            "edquota -u username",
            "quotacheck -avug",
            "quotaon -avug",
            "quotaoff -avug",
            "du -sh /home/*"
        ],
        0,
        "Troubleshooting",
        "The repquota command is used to generate a report of disk usage and limits for user quotas, making it the appropriate choice to check which users have reached their disk space limit. quotacheck scans one or more filesystems for disk usage, it initializes, checks, and repairs quotas. However, it does not provide a readable report for administrators. edquota is used to edit user quotas, not to display them. quotaon and quotaoff are used to enable and disable quota enforcement, respectively, and do not display the quota usage. du displays disk usage statistics but does not show the quota limits or which users have reached their limits."
    ),
    
    (
        "A Linux system administrator notices that despite clearing a substantial amount of data, the 'df' and 'du' commands show significant differences in disk usage reports, and users are unable to create new files. What is the MOST likely cause of this problem?",
        [
            "Rogue processes are continuously consuming disk space",
            "The '/tmp' directory is full",
            "The file system is corrupted",
            "The file system has reached its maximum number of available inodes"
        ],
        3,
        "Troubleshooting",
        "The discrepancy between 'df' and 'du' along with the inability to create new files, despite apparent available disk space, points to inode exhaustion. 'df' reports total disk space including used inodes, while 'du' reports actual file data usage. Inode exhaustion occurs when all the available inodes are in use; new files cannot be created even if physical space is available. A corrupted filesystem would also prevent new files from being created, but wouldn't normally cause the discrepancies between 'df' and 'du' focused on inodes. A full '/tmp' directory would cause issues with file creation but is more likely to be related to space, not inodes, and rogue processes consuming disk space would not directly prevent new file creation if inodes were still available."
    ),
    
    (
        "An administrator is diagnosing an issue where a filesystem on their Linux server appears to be mounted read-only, preventing users from writing data. Which mount option should have been specified during the mounting process to allow both read and write operations on the filesystem?",
        [
            "user",
            "sync",
            "rw",
            "ro"
        ],
        2,
        "Troubleshooting",
        "The 'rw' option is used to mount a filesystem with both read and write permissions. If a filesystem is unintentionally mounted as read-only, ensuring that the 'rw' option is set during the mount process will resolve the issue, allowing users to perform write operations once more. Other options, such as 'ro', 'sync', and 'user', have specific uses: 'ro' mounts the filesystem as read-only, 'sync' ensures that input/output operations are done synchronously, and 'user' allows an ordinary user to mount the filesystem without requiring superuser privileges. However, these do not address the problem described."
    ),
    
    (
        "Which command should be used to verify that the rules currently loaded into the kernel's packet filter are allowing inbound SSH traffic on port 22?",
        [
            "ifconfig",
            "netstat -tuln",
            "nmap -p 22 localhost",
            "iptables -L"
        ],
        3,
        "Troubleshooting",
        "The correct answer is iptables -L, which lists all current firewall rules set by iptables, including those that pertain to the default port for SSH traffic (port 22). It's important to inspect these rules when SSH traffic is being blocked, as a misconfigured or overly restrictive rule might prevent inbound connections. ifconfig is used for configuring network interfaces, not for checking firewall rules. The netstat command is used to display network connections, listening ports, and routing tables, but it doesn't provide information about firewall rules. nmap is a network scanner and while it can show which ports are open, it does not display actual firewall rules."
    ),
    
    (
        "A user reports that they are unable to write to a file named 'report.txt' located in their home directory. However, they have confirmed that they can read the file. Which of the following is the BEST action to take in order to grant the user write access to the file?",
        [
            "Change the ownership of the file using the chown command",
            "Change the file permissions to allow write access for the user",
            "Edit the /etc/fstab file to alter mounting options for the user's home directory",
            "Restart the file service to refresh user permissions"
        ],
        1,
        "Troubleshooting",
        "The correct answer is 'Change the file permissions to allow write access for the user'. Since the user already has read access and only needs write access, modifying the file permissions using the chmod command is the most straightforward approach. The other options do not directly address the specific issue at hand. Changing the file ownership with chown is unnecessary and potentially risky if the user already owns the file. Editing the /etc/fstab file would typically configure file system mount options, not individual file permissions. Restarting the file service is unrelated to file permissions, and would not remedy the user's inability to write to the file."
    ),
    
    (
        "What operation should be periodically performed on a solid-state storage device to indicate which sectors are no longer in use?",
        [
            "Increasing the partition size",
            "Performing a surface scan",
            "Executing a trim command",
            "Conducting a sector-by-sector backup",
            "Running a defragmentation program"
        ],
        2,
        "Troubleshooting",
        "The operation, known as 'trim,' is crucial for solid-state storage devices. It marks sectors as no longer in use, which allows the device's controller to manage flash memory cells efficiently. This process avoids unnecessary write and erase cycles, thus maintaining optimal performance and extending the lifespan of the storage device. It is important to note that traditional defragmentation is not only unnecessary for these devices but also potentially harmful, as it increases write operations without any performance gain."
    ),
    
    (
        "What information does the command 'lsmem' provide when troubleshooting memory issues on a Linux system?",
        [
            "Allows configuration and management of memory usage",
            "Shows memory usage statistics for network devices",
            "Provides complete details of swap usage by the system",
            "Displays the range of memory available along with the online and offline status"
        ],
        3,
        "Troubleshooting",
        "The correct answer is 'Displays the range of memory available along with the online and offline status' because the 'lsmem' command is mainly used to list the ranges of available memory and their attributes, such as online and offline status. The other options are incorrect because 'lsmem' does not directly display swap usage details, network memory statistics, or manage memory usage; instead, it provides an overview of memory range statuses that are critical for system memory analysis."
    ),
    
    (
        "A Linux server with sufficient swap space will never encounter an Out of Memory condition.",
        [
            "False",
            "True"
        ],
        0,
        "Troubleshooting",
        "The statement is false because even if a server has sufficient swap space, it can still encounter Out of Memory conditions. Swap space acts as an overflow for when the physical memory (RAM) is fully utilized, and it allows the system to continue running by temporarily moving some memory pages to disk. However, swap space is significantly slower than RAM, and if the system is under heavy memory pressure, where even the swap space is entirely used, it may still trigger the OOM killer to terminate processes to free up memory. Additionally, certain situations, such as kernel memory allocation requests that cannot be swapped out, may also lead to OOM conditions regardless of the available swap."
    ),
    
    (
        "What command is used to reconfigure the time zone on a Linux system?",
        [
            "tzconfig",
            "date --set-timezone",
            "timezone",
            "timedatectl set-timezone"
        ],
        3,
        "Troubleshooting",
        "The correct answer is timedatectl set-timezone. This command is used to set the time zone of the system to the specified value. It's part of the timedatectl utility, which lets you view and change the current date, time, and timezone settings. The reason the other options are incorrect is that tzconfig is deprecated, date is used for setting the system's date and time but not the timezone, and timezone is not a valid command for setting the system time zone."
    ),
    
    (
        "A system administrator notices that a Linux server is experiencing slow performance, specifically in disk operations. Upon investigating, the administrator discovered that the I/O wait time is considerably high. Which of the following actions is the BEST course of action to reduce the high latency affecting the system?",
        [
            "Deploy additional network interfaces to balance the I/O load.",
            "Increase the CPU clock speed to process I/O operations faster.",
            "Decrease the amount of RAM in the system to reduce the memory available for disk caching.",
            "Replace the current I/O scheduler with one that is better optimized for the system's workload."
        ],
        3,
        "Troubleshooting",
        "In this scenario, the best course of action is to replace the current I/O scheduler with one that is optimized for the particular workload characteristics (e.g. CFQ, Deadline, NOOP). The I/O scheduler is responsible for ordering disk access to improve performance. Some schedulers are better suited for certain workloads than others, and so choosing the correct one can potentially reduce I/O wait times and thus lower latency."
    ),
    
    (
        "An administrator wants to conduct an aggressive scan to retrieve version information, run default scripts, and to detect the operating system of the target device. Which Nmap command option should be used?",
        [
            "-A",
            "-o",
            "-sn",
            "-p-"
        ],
        0,
        "Troubleshooting",
        "The '-A' option in Nmap enables aggressive scanning, which combines OS detection, version detection, script scanning, and traceroute. This thorough scanning option is informative for deep network analysis. The '-sn' option is for ping scanning (host discovery), '-p-' scans all 65535 ports, and '-o' is an invalid option as it lacks the specifics for output files like '-oN' or '-oX'."
    ),
    
    (
        "A system administrator needs to mount a USB drive in Linux and ensure that users other than the owner cannot write to it. What option needs to be added to the mount command to achieve this?",
        [
            "sync",
            "noexec",
            "ro",
            "rw"
        ],
        2,
        "Troubleshooting",
        "To prevent users other than the owner from writing to the USB drive, the 'ro' (read-only) option can be used. This option mounts the filesystem in a read-only mode, allowing only the owner to write to it, thus addressing the administrator's requirement. Other options such as 'rw' (read-write), 'sync', and 'noexec' would not achieve the desired behavior: 'rw' would allow writing by all users, 'sync' would just affect the synchronization timing but not permissions, and 'noexec' would prevent execution of binaries but not affect write permissions."
    ),
    
    (
        "A Linux system administrator notices that a custom service is supposed to start after the local MySQL database server is up and running. However, the custom service sometimes fails because it starts too quickly and does not detect the MySQL service being ready. Which directive should the administrator add to the [Unit] section of the custom service's systemd unit file to ensure it starts after the MySQL service?",
        [
            "Wants=mysqld.service",
            "After=mysqld.service",
            "BindsTo=mysqld.service",
            "BindTo=mysqld.service"
        ],
        1,
        "Troubleshooting",
        "The correct answer is After=mysqld.service because the After= directive ensures that the custom service starts only after the MySQL service (mysqld.service) is active. The Wants= directive is used to start units together but does not dictate order, and BindTo= and BindsTo= are incorrect because there is no systemd directive called BindTo=, and BindsTo= creates a stronger dependency than required for start-up order – it's used to bind the start/stop of units together."
    ),
    
    (
        "A systems administrator notices that a user who was recently added as a member of the 'data-analysts' group cannot modify files in the 'analytics_reports' directory. The directory permissions are set to drwxrwx---. The user and group ownerships are 'datamgr' and 'data-analysts' respectively. The administrator has verified that the user is indeed a member of the 'data-analysts' group. What should the administrator investigate as the most likely cause of this issue?",
        [
            "There are file-specific ACLs that override group permissions and prevent modifications",
            "The filesystem for the 'analytics_reports' directory is mounted as read-only",
            "There is full disk space, preventing any changes to files",
            "The user has not logged out and back in since being added to the group"
        ],
        3,
        "Troubleshooting",
        "The correct answer is 'The user has not logged out and back in since being added to the group'. In Linux, when a user is added to a new group, the group membership is not applied to the user's current sessions. They need to log out and log back in for the system to recognize their new group memberships. 'Full disk space' is incorrect because disk space issues would not affect permissions, 'Filesystem mounted as read-only' is not the likely cause as that would affect all users and not just one, and 'File-specific ACLs' might seem plausible but the question implies group permission is the problem, not specific file permissions."
    ),
    
    (
        "A systems administrator notices a high number of collisions on a Linux-based server's Ethernet interface which is connected to an office's local area network (LAN). The collisions are resulting in noticeable performance degradation. While investigating the cause, what should the administrator check first in order to resolve the issue?",
        [
            "Router's access control lists",
            "Switch port duplex settings",
            "Update the network interface card drivers",
            "Increase the server's RAM"
        ],
        1,
        "Troubleshooting",
        "Collisions occur in networks using a shared medium like Ethernet when two devices attempt to transmit at the same time. They are common in older networks with hubs or in misconfigured networks. The correct answer is 'Switch port duplex settings' because duplex mismatches are a primary cause of network collisions. If one side of the connection is set to full duplex and the other to half duplex, it can lead to a collision domain where each side of the connection expects different behavior regarding data transmission."
    ),
    
    (
        "Using single-threaded I/O operations on a Solid State Drive (SSD) will always result in optimal throughput.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "This statement is false because SSDs are designed to perform optimally with multi-threaded I/O operations that can leverage the drive's capabilities for parallel data access and processing. Single-threaded operations do not fully utilize the SSD's performance potential, which can lead to suboptimal throughput. Additionally, the I/O scheduler and alignment of the file system and partitions can play significant roles in achieving optimal SSD performance. Other false answers may seem plausible but are inaccurate in suggesting a single-threaded approach is always optimal."
    ),
    
    (
        "What command would be used to perform a basic scan of a target system's open ports using Nmap?",
        [
            "nmap -A",
            "nmap",
            "nmap -sV",
            "nmap --top-ports 10"
        ],
        1,
        "Troubleshooting",
        "The correct answer is nmap <target> because Nmap is a network scanning tool, and the most basic usage involves executing nmap followed by the specification of the target, which can be an IP address or hostname. This command will initiate a simple scan to find open ports on the target. Other options like -A and -sV add extra functionality, such as OS detection and service version detection, which is not required for a basic port scan. The --top-ports option specifies that only a certain number of the most common ports should be scanned, not all ports, which would be the default for a basic scan without additional arguments."
    ),
    
    (
        "A Linux administrator is troubleshooting a file system mounted as /dev/sdb1 at /data that seems to be causing issues when users attempt to execute scripts stored there. The device is known to only store data files and should not contain any executable code. To enhance security, the administrator had previously set specific mount options for this file system. Which mount option might the administrator have set to cause this behavior, and should now be reviewed or removed to allow script execution?",
        [
            "defaults",
            "nosuid",
            "sync",
            "noexec",
            "nodev"
        ],
        3,
        "Troubleshooting",
        "The correct answer is noexec. This mount option prevents execution of any binaries on the mounted filesystem to increase security. If scripts need to be executed from this mount point, the noexec option should not be used. The nosuid option prevents the setuid bit from taking effect, which is not directly related to the ability to execute scripts, but rather affects whether users can gain elevated privileges via setuid binaries. The options nodev and sync are related to device node handling and write synchronization respectively, and do not impact script execution. Therefore, noexec is the specific mount option that should be reviewed to resolve the given issue."
    ),
    
    (
        "A Linux system administrator notices that the journal logs on a production server are not persistent across reboots, which is necessary for troubleshooting ongoing issues that occur after system restarts. What's the BEST step the administrator should take to ensure journal logs are retained after a reboot?",
        [
            "Implement logrotate on /run/log/journal to ensure the logs are preserved after reboots.",
            "Modify the 'Storage=' setting in '/etc/systemd/journald.conf' to 'persistent' and reboot the server.",
            "Reboot the server to trigger a new instance of systemd-journald, which will then keep the logs.",
            "Create the /var/log/journal directory and restart the systemd-journald service."
        ],
        3,
        "Troubleshooting",
        "The correct answer is to create the /var/log/journal directory. The systemd journal will store its logs persistently if this directory exists. Without it, logs are stored in /run/log/journal and are volatile. Changing the storage setting in 'journald.conf' without creating the directory, or just rebooting the server, will not have the desired effect of making logs persistent. Implementing log rotation is good practice for managing log size but does not affect whether logs are retained across reboots."
    ),
    
    (
        "A system administrator has been alerted to slow performance on a virtualized Linux server. After checking various system metrics, the administrator finds that a significant amount of processor time is categorized under 'st' when inspecting resource usage with monitoring tools. What does this category represent?",
        [
            "The period during which the system is idle and waiting for user interaction",
            "Duration dedicated to running the kernel and its associated processes",
            "Time spent processing input/output operations waiting for external devices",
            "This is the time spent performing calculations for user-initiated processes",
            "Time reserved for low-priority background tasks within the system",
            "Time allocated by the hypervisor to other virtual processors"
        ],
        5,
        "Troubleshooting",
        "'st', or 'steal' time, is an important metric particularly in virtualized environments. It indicates the amount of time that the virtual processor wanted to execute, but the hypervisor allocated that time to another virtual processor. A high 'steal' time can be a sign of the virtualized server not getting enough processing power because the physical host's resources are heavily used by other virtual machines."
    ),
    
    (
        "A system administrator is configuring a systemd timer unit to start a backup service exactly 10 minutes after the system has finished booting. Which line should be included in the [Timer] section of the timer unit file?",
        [
            "OnCalendar=*:0/10",
            "StartupSec=10min",
            "OnBootSec=10min",
            "OnUnitActiveSec=10min",
            "OnUnitInactiveSec=10min",
            "OnActiveSec=10min"
        ],
        2,
        "Troubleshooting",
        "The 'OnBootSec=10min' directive is the correct answer. It specifies the timer should wait for 10 minutes after the system has booted before activating the associated unit. The directive is part of the timer specification in systemd and is used to delay the start of a service relative to system boot time. Other directives like 'OnUnitActiveSec' and 'OnUnitInactiveSec' are related to the activation times based on when the unit was last activated or became inactive and are not related to the boot process, making them incorrect in this context."
    ),
    
    (
        "An administrator notices that a web service that was running properly until recently has suddenly become unreachable from the network. The server is up and running with no recent changes to the firewall. Running systemctl status shows that the service is active (running). What should be the administrator's NEXT step in troubleshooting this issue?",
        [
            "Use netstat or ss to check if the server is listening on the correct port.",
            "Restart the entire server to ensure that all services are loaded properly.",
            "Check the /etc/hosts file for any incorrect entries that might be causing name resolution issues for the service.",
            "Inspect the /etc/passwd file for any user account discrepancies that might be impacting the web service."
        ],
        0,
        "Troubleshooting",
        "Checking the server's listening ports using netstat or ss is the correct next step because it will help to confirm if the web service is correctly bound to the appropriate port and is listening for incoming connections. If the service is not listening on the expected port, it could be due to misconfiguration, which needs to be investigated further. The other options, checking the /etc/hosts file or restarting the server, may not immediately contribute to solving the issue, where the primary concern is the service's ability to accept connections. Looking into /etc/passwd would be irrelevant as it is used for user account information and not service networking issues."
    ),
    
    (
        "After expanding an existing disk array on a Linux file server, a systems administrator observes reduced performance during write operations. The original configuration consisted of four disks managed by the server's hardware controller, and a fifth disk was introduced to enhance storage capacity. What is the most probable cause of the observed decrease in write operation speed following the expansion?",
        [
            "Suboptimal cable quality is causing a bottleneck in data transfer between the controller and the disks.",
            "The overhead of parity calculations is higher now with the additional disk, slowing down the overall write performance.",
            "The block size of the array is not properly configured for the number of disks, leading to inefficient write operations.",
            "The recent disk added to the server is defective, causing a delay in the array's ability to write data effectively."
        ],
        1,
        "Troubleshooting",
        "The addition of an extra disk into a RAID 5 array increases the complexity of the parity computation for every write operation. Since RAID 5 needs to update the parity information across the drives for data protection, it inherently suffers from write penalties. This can become more pronounced as the array extends, due to the added overhead of handling the parity calculations across an additional disk. The SATA protocol for connecting disks to the controller is not specified in the question, and while degraded cables or faulty hardware could cause slowdowns, they don't directly relate to the expansion of the array, thus are less likely the primary cause of the issue."
    ),
    
    (
        "What symptom would you likely observe on a Linux server if it is experiencing high latency in its storage subsystem?",
        [
            "Decreased number of context switches",
            "Expansion of file cache size",
            "Increased Input/Output (I/O) wait times",
            "Overutilization of swap space"
        ],
        2,
        "Troubleshooting",
        "High latency in the storage subsystem typically leads to increased Input/Output (I/O) wait times. This happens because the CPU needs to wait longer than usual for data to be read from or written to the storage, causing delays and a potential bottleneck in overall system performance."
    ),
    
    (
        "The nice value of a process can be negative for regular users in order to increase the process priority and grant it more CPU time.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "Only the root user or processes with the necessary privileges can set a negative nice value to increase a process's priority. Regular users are not permitted to assign a negative nice value as this would potentially disrupt the system's stability by giving non-privileged processes higher priority over critical system tasks."
    ),
    
    (
        "Enabling the iowait time statistic to be frequently high indicates that the CPU is overutilized due to processing too many operations simultaneously.",
        [
            "True",
            "False"
        ],
        1,
        "Troubleshooting",
        "The iowait time statistic actually represents the time the CPU is waiting for I/O operations to complete. It is not an indicator that the CPU is processing too many operations but rather that it is idle and waiting, which can imply I/O subsystem issues rather than CPU overutilization. High CPU utilization is better indicated by statistics like user and system time ratios."
    ),
    
    (
        "The security policy of your company requires a stealthy scan to minimize the chances of detection by the target system's intrusion detection system (IDS). Which Nmap command would perform a SYN scan, while also spoofing the source port to appear as 53 (DNS) and avoiding port 22 on the target 10.0.0.12?",
        [
            "nmap -sS --source-port 53 --excludefile no-scan-22.txt 10.0.0.12",
            "nmap -sS -g 53 --exclude-ports 22 10.0.0.12",
            "nmap -sS -D RND:10 -g 53 10.0.0.12",
            "nmap -sU -g 53 -p !22 10.0.0.12",
            "nmap -sT --spoof-port 53 -p-22 10.0.0.12",
            "nmap -sS -Pn -g 53 --skip-port 22 10.0.0.12"
        ],
        1,
        "Troubleshooting",
        "The correct answer is nmap -sS -g 53 --exclude-ports 22 10.0.0.12. The -sS flag specifies a SYN scan, which is considered stealthier than a connect scan. The -g 53 option sets the source port to 53, which may help in evading certain IDS configurations as it makes the scan look like DNS traffic. The --exclude-ports 22 option ensures that port 22 is not scanned. The other answers either do not correctly form the combination or are not the proper usage of Nmap flags, making them incorrect for the required stealthy scan excluding port 22."
    ),
    
    (
        "What is typically the primary consequence of unchecked memory leaks over time on a Linux system?",
        [
            "Network bandwidth limitations",
            "Memory exhaustion",
            "Increase in disk capacity",
            "Increased CPU utilization"
        ],
        1,
        "Troubleshooting",
        "Memory leaks occur when a program mismanages memory allocations, by not releasing memory that is no longer needed, causing a progressive loss of available memory. Over time, this can lead to memory exhaustion, where no additional memory is available for use, potentially causing system slowdowns or crashes. While leaks may increase CPU or disk usage indirectly due to increased swapping or garbage collection, memory exhaustion is a direct consequence."
    ),
    
    (
        "Your server has a web application that should be accessible from the internet, but users report they are unable to connect. You have confirmed that the web server is running and that network connectivity is established. What should you check next to ensure that the firewall is not blocking the web application's traffic?",
        [
            "Use a network scanner to detect open ports on the server.",
            "Restart the web server service to ensure it is not a service issue.",
            "Verify that the firewall rules allow traffic on ports 80 (HTTP) and 443 (HTTPS).",
            "Check the listening ports to ensure the server is listening on the correct interface."
        ],
        2,
        "Troubleshooting",
        "When users report that they cannot connect to a web-facing application despite the service running and network connectivity being established, the next step is to check the firewall rules to ensure that traffic on the port used by the web application is not being blocked. In the case of a typical web application, you would check for rules that allow traffic on ports 80 and 443 for HTTP and HTTPS, respectively. If these rules are not present or are misconfigured, the firewall would prevent external users from connecting to the application. Checking the status of a service or the ports being listened on, while potentially useful in other scenarios, would not address a firewall configuration issue."
    ),
    
    (
        "A Linux user is unable to write to a file named 'report.txt' located in a directory they own. Which of the following commands should the system administrator use to BEST resolve this issue?",
        [
            "chmod 777 report.txt",
            "chmod u+w report.txt",
            "chmod a+wx report.txt",
            "chown :usergroup report.txt"
        ],
        1,
        "Troubleshooting",
        "The correct answer is 'chmod u+w report.txt', as the use of the 'chmod' command with the 'u+w' option grants the user (owner) of the file write permissions. This aligns most closely with the presented scenario, where a user is unable to write to their own file. The other options either set overly permissive rights, change group ownership which may not be needed, or use an invalid option."
    ),
    
    (
        "After installing a new network adapter in a Linux server, users report sporadic and sluggish connections to hosted services. Upon inspecting the interface statistics, you notice an abnormally high count of discarded packets. Identifying the probable root cause of this issue is your next step. Which of the following should you investigate first?",
        [
            "Check for duplex mismatch between the network adapter and the corresponding switch configuration",
            "Investigate a possible speed mismatch between the server's network adapter and the clients' adapters",
            "Verify that the network configurations on the server are correctly assigned",
            "Examine the physical cables for signs of damage or wear"
        ],
        0,
        "Troubleshooting",
        "A high count of discarded packets is typically indicative of a duplex mismatch issue, where there is a configuration inconsistency between how the installed network adapter and the corresponding switch port manage data transmission. This would result in data collision and packet loss. A speed mismatch can also cause performance problems, but it doesn't typically increase the rate of discarded packets. Damaged cables may lead to packet loss, but this is less likely in a new installation where the adapter settings are a common concern. Incorrectly assigned network configurations could interfere with connectivity but generally do not lead directly to increased packet loss."
    ),
    
    (
        "A Linux administrator needs to verify if a newly installed web server is listening on the default port and is reachable from a remote system. Which command should the administrator use?",
        [
            "openssl s_client -connect remote_server_ip:80",
            "nmap -p 80 remote_server_ip",
            "dig remote_server_ip -p 80",
            "netstat -tuln | grep ':80'"
        ],
        1,
        "Troubleshooting",
        "The nmap command is a versatile tool for network exploration and security auditing. It can scan network entities for open ports and services. When provided with an IP address and port number, it can verify if a given service is running and reachable on that port, which is exactly what is needed to check if a web server is listening on its default port. openssl s_client is typically used to troubleshoot SSL/TLS connections, not to confirm if a service is listening on a specific port. netstat is useful for displaying network connections on the local machine, but it is not designed for testing remote system ports. dig is a tool for querying DNS name servers, which is unrelated to checking for open ports on a remote system."
    ),
    
    (
        "A system administrator has noticed that applications are having trouble accessing configuration files stored on a mounted filesystem. Upon inspection, the system logs indicate read errors on the filesystem in question. The administrator suspects filesystem corruption. Which command should be executed to check and repair the filesystem while it's unmounted, preventing further damage or potential data loss?",
        [
            "e2fsck /dev/sda2",
            "fdisk /dev/sda2",
            "fsck /dev/sda2",
            "mkfs -t ext4 /dev/sda2"
        ],
        2,
        "Troubleshooting",
        "The correct command for checking and repairing a corrupted filesystem is fsck. It checks the integrity of the filesystem and repairs any errors found when the filesystem is not mounted, which prevents additional corruption or data loss during the repair process. The command e2fsck allows checks only for ext2/ext3/ext4 filesystem types, which might not apply to all filesystems. The mkfs command is used to create a filesystem, not repair it. Using it in this scenario would result in data loss. fdisk is used for disk partitioning, which is not applicable to filesystem checks or repairs."
    ),
    
    (
        "A system administrator needs to verify the SSL certificate information of a web server at the domain 'example.com' running on the default HTTPS port. Which command should be used to retrieve and display the certificate details?",
        [
            "openssl s_client -host example.com -port 443",
            "openssl s_client -tls1_2 -connect example.com:443",
            "openssl s_client -connect example.com:443 -showcerts",
            "openssl s_server -connect example.com:443",
            "openssl s_client -verify example.com",
            "openssl s_client -connect example.com:443 -cert"
        ],
        2,
        "Troubleshooting",
        "The command openssl s_client -connect example.com:443 -showcerts establishes a connection to the specified domain on the default HTTPS port and retrieves the full certificate chain as provided by the server. This information is valuable when verifying the authenticity and trustworthiness of the SSL certificates in use."
    ),
    
    (
        "Which command would you use to display detailed information about the CPU architecture on a Linux system?",
        [
            "lsmod",
            "lshw",
            "lsblk",
            "lscpu"
        ],
        3,
        "Troubleshooting",
        "The command lscpu stands for 'list CPU' and is used to display information about the CPU architecture. It shows detailed and specific information including the number of CPUs, cores, threads, CPU family, and architecture. This is crucial information when diagnosing systems for CPU-related performance issues. The other options, while they may relate to system information, do not provide the detailed CPU architecture information that lscpu does."
    ),
    (
        "A directory named 'data_backup' contains multiple files and subdirectories. How would an administrator remove the entire directory and its contents without being prompted for each file or directory?",
        [
            "rm -i data_backup",
            "rm -rf data_backup",
            "rmdir data_backup",
            "rm data_backup"
        ],
        1,
        "System Management",
        "The correct answer is rm -rf data_backup. The -r option stands for 'recursive' and is necessary to delete directories and their contents. The -f option stands for 'force', which prevents the command from prompting for confirmation. This combination is powerful and should be used with caution to avoid accidental data loss. rm data_backup is not correct because it will only work on individual files and will fail on directories. rmdir data_backup only removes empty directories, and rm -i data_backup will prompt for confirmation, which we want to avoid based on the question."
    ),
    (
        "What does the 'dig' tool primarily query and display information from?",
        [
            "Dynamic Host Configuration Protocol (DHCP) servers",
            "Domain Name System (DNS) servers",
            "Simple Mail Transfer Protocol (SMTP) servers",
            "Network Information Service (NIS) servers"
        ],
        1,
        "System Management",
        "The 'dig' command is used to query Domain Name System (DNS) servers. When you run 'dig', followed by a domain name, it sends a DNS lookup request to a DNS server and then shows the response it gets from the server. This is useful for troubleshooting DNS issues and for confirming the correct operation of DNS servers."
    ),
    (
        "A system administrator needs to run a file system check on user directories but wants to ensure user data is not affected during system uptime. Which of the following strategies would BEST achieve this?",
        [
            "Running a file system check during boot time on the partition mounted as /home.",
            "Mounting the /home partition as read-only while users are logged in.",
            "Using the usermod command to lock user accounts and then performing a file system check.",
            "Scheduling a cron job to run a file system check on /home at midnight."
        ],
        0,
        "System Management",
        "The correct answer is 'Running a file system check during a boot time on the partition mounted as /home'. This is because running file system checks can potentially disrupt user access to files. Performing these checks during boot time ensures user directories are not in use, preventing potential data loss or corruption. Mounting the partition as read-only won't accomplish a file system check but will prevent changes. Scheduling a cron job for file system check will still affect users if they are logged in and using their directories. Although usermod can manipulate user accounts, it doesn't facilitate a file system check on the /home directories."
    ),
    (
        "A system administrator wants to ensure that a specific Ethernet interface does not start automatically upon system boot, while still retaining the configuration for manual activation later. Which NetworkManager command should the administrator use?",
        [
            "nmcli con up IFNAME",
            "nmcli con delete IFNAME",
            "nmcli con mod IFNAME connection.autoconnect no",
            "nmcli dev disconnect IFNAME"
        ],
        2,
        "System Management",
        "The correct answer is A. The nmcli con mod IFNAME connection.autoconnect no command is used to modify an existing network connection to not automatically connect at system boot, where IFNAME needs to be replaced with the actual connection name or UUID. Remember to use 'con mod' for modifying an existing connection, which retains the interface configuration for future use. Answer B, using 'nmcli dev disconnect IFNAME', is incorrect, as it only disconnects an active connection but does not change the autoconnect property of the connection. Answer C, 'nmcli con up IFNAME', is the opposite of what is needed as it activates a connection. Answer D, 'nmcli con delete IFNAME', permanently removes the connection profile, which is not suitable when the goal is to keep the profile for later manual activation."
    ),
    (
        "A system administrator needs to monitor resource usage and performance in real time to identify a process that is consuming an unusually high percentage of CPU resources. Which of the following commands provides the BEST solution for this requirement?",
        [
            "ps aux --sort -%cpu",
            "cat /proc/cpuinfo",
            "pscat",
            "top"
        ],
        3,
        "System Management",
        "The 'top' command is the correct answer because it displays a real-time view of system processes, including CPU usage, memory consumption, and other important metrics. By using 'top', the administrator can easily identify processes that are using a high percentage of CPU resources. Other commands listed either do not provide real-time monitoring, or they address different aspects of system management."
    ),
    (
        "After installing a new version of a service, you notice that some of your custom configurations are no longer in effect. The service in question utilizes .rpmsave and .rpmnew files during upgrades. Which of the following actions should you take to BEST ensure that your previous configurations are incorporated into the new service version?",
        [
            "Manually compare the .rpmsave file with the .rpmnew file and integrate custom configurations as needed, then remove the .rpmnew suffix.",
            "Replace the new configuration file with the file that has the .rpmsave extension.",
            "Rename the .rpmnew file to overwrite the current configuration file without manual checks.",
            "Ignore the .rpmnew and .rpmsave files as the service will automatically merge the configurations."
        ],
        0,
        "System Management",
        "When an RPM package upgrade process detects that a configuration file has been changed by the system administrator, it preserves the original file with an .rpmsave extension and installs the new default configuration file with an .rpmnew extension. To incorporate previous custom configurations into the new version, you should compare the .rpmsave file with the .rpmnew file and manually integrate any necessary customizations. Simply replacing the .rpmnew file with the .rpmsave file may not be ideal because the new version of the service might require new configuration parameters that are present in the .rpmnew file."
    ),
    (
        "If a system administrator wants to update the GRUB2 boot loader on a system that uses BIOS, which command should be used to ensure GRUB2 is properly installed onto the Master Boot Record (MBR)?",
        [
            "grub2-install /dev/sda",
            "update-grub",
            "grub2-update",
            "grub2-mkconfig -o /boot/grub2/grub.cfg"
        ],
        0,
        "System Management",
        "The grub2-install command is used to install the GRUB2 bootloader to the MBR when a system is using BIOS firmware. This command is critical when repairing or reconfiguring the GRUB2 installation. The grub2-mkconfig command generates a new GRUB2 configuration file based on the current system settings, but does not install GRUB to the MBR. There is no such command as grub2-update, and while update-grub is a wrapper script commonly found in Debian-based Linux distributions that calls grub2-mkconfig, it is not the correct command for installing GRUB2 to the MBR."
    ),
    (
        "A system administrator needs to ensure a specific service starts automatically on system boot. Which of the following systemctl subcommands would allow the administrator to achieve this?",
        [
            "status",
            "enable",
            "start",
            "reload"
        ],
        1,
        "System Management",
        "The correct answer is enable. The systemctl enable command is used to create a set of symlinks, so the specified unit is started automatically during the boot process. start only initiates the service immediately but does not configure it to start on boot. status provides the current status of the unit and does not modify its startup behavior. reload is used to re-read the configuration of a service without interrupting its operation."
    ),
    (
        "What is the primary purpose of the 'cat' command in a Linux environment?",
        [
            "To compare the contents of files line by line",
            "To read and display the content of files on standard output",
            "To display the first few lines of a file",
            "To edit the contents of a text file interactively"
        ],
        1,
        "System Management",
        "The 'cat' command is used to read and display the content of files on standard output. By mastering its usage, users can view the contents of a file or concatenate multiple files easily. The incorrect options relate to file editing, file comparison, and reading the beginning of files, which are tasks associated with other commands ('nano', 'diff', and 'head', respectively)."
    ),
    (
        "A system administrator suspects that a newly installed network card is not being recognized by the Linux kernel. Which command should be used to verify if the card is detected by the system at the hardware level?",
        [
            "lsmod",
            "lspci",
            "dmesg | grep -i network",
            "lsusb"
        ],
        1,
        "System Management",
        "The 'lspci' command lists all PCI devices on the system, including network cards, regardless of whether the kernel has appropriate drivers for them. This makes it the correct tool to check if the hardware is recognized at the PCI level. 'lsusb' is incorrect because it lists USB devices, not PCI devices. 'dmesg | grep -i network' could show kernel messages about network cards, but it would not necessarily list all PCI devices. 'lsmod' is used to display the kernel modules currently loaded, which is useful for driver information but not for listing hardware."
    ),
    (
        "What is the state of a Linux process that has completed execution but still has an entry in the process table?",
        [
            "Stopped",
            "Sleeping",
            "Zombie",
            "Running"
        ],
        2,
        "System Management",
        "A process that has completed execution but still has an entry in the process table is in the 'zombie' state. This occurs when a process has finished running, but its parent has not yet called wait() to read the child's exit status, leaving an entry in the process table as a 'zombie' that needs to be reaped. This is why the 'zombie' state is also sometimes referred to as a 'defunct' process. The other options are incorrect: 'running' is when a process is actively being executed; 'sleeping' is when a process is waiting for a resource or event; 'stopped' is when a process has been paused, typically by a signal, not when it has finished execution."
    ),
    (
        "Which command would you use to download a file from the internet using the command line while ensuring that the output is saved with a specific filename?",
        [
            "wget --save-as desired_filename http://example.com/file",
            "wget --download-as desired_filename http://example.com/file",
            "wget --output-file desired_filename http://example.com/file",
            "wget -O desired_filename http://example.com/file"
        ],
        3,
        "System Management",
        "The wget -O command allows you to specify a filename for the saved content when downloading from the internet. This is useful when you want to control the naming of downloaded files, especially when the default name is not descriptive or conflicts with existing files in your directory. The -O option specifically designates the output filename."
    ),
    (
        "Pressing Ctrl+Z in a shell sends the SIGSTOP signal to the current foreground process, thus immediately and permanently stopping the process.",
        [
            "False",
            "True"
        ],
        0,
        "System Management",
        "Pressing Ctrl+Z does send the SIGSTOP signal to the foreground process, but it does not stop the process permanently; instead, it suspends the process, allowing it to be resumed later. A suspended process can be continued in the background with the bg command or brought back to the foreground with fg."
    ),
    (
        "A system administrator is writing a shell script that periodically checks the disk space usage on a Linux server. To ensure that the output of the disk check does not flood the terminal or logs when running the script via a cron job, the administrator wants to discard the standard output. Which command redirection to /dev/null achieves this purpose?",
        [
            "df -h > /dev/null",
            "df -h 2> /dev/null",
            "df -h &> /dev/null",
            "df -h | /dev/null"
        ],
        0,
        "System Management",
        "The correct answer is df -h > /dev/null. The > operator redirects the standard output (STDOUT) to the specified file, in this case, /dev/null. The /dev/null device is a special file that discards all data written to it, effectively silencing any output that would normally be sent to the terminal. Incorrect answers involve the use of 2> /dev/null which would only redirect standard error (STDERR) and &> /dev/null which is not as commonly used or may not be the intended operation since it redirects both STDOUT and STDERR."
    ),
    (
        "Which signal is commonly sent by command-line utilities to request a graceful termination of a process?",
        [
            "SIGKILL",
            "SIGTERM",
            "SIGSTOP",
            "SIGQUIT"
        ],
        1,
        "System Management",
        "The SIGTERM signal is used by system administrators to request a graceful termination of a process. When a process receives a SIGTERM, it has the opportunity to perform clean-up actions such as closing files, releasing resources, and saving state before actually terminating. This is in contrast to SIGKILL, which forcibly terminates the process without any clean-up. SIGQUIT is designed to terminate processes and generate a core dump for debugging purposes, which is not typically used for graceful terminations. SIGSTOP is used to pause a process, not terminate it."
    ),
    (
        "During resource-intensive operations, a Linux system administrator needs to ensure that a new statistical analysis application doesn't consume excessive CPU resources, potentially impacting the performance of other critical services. Which of the following commands will start the new application with a reduced CPU priority?",
        [
            "nice -n 10 /path/to/stat_analysis_app",
            "adjust -n 10 /path/to/stat_analysis_app",
            "priority -10 /path/to/stat_analysis_app",
            "renice -n 10 -p /path/to/stat_analysis_app"
        ],
        0,
        "System Management",
        "The correct command to start a new process with a reduced CPU priority is nice -n 10 /path/to/stat_analysis_app, where -n 10 adjusts the niceness level, thereby decreasing the process's priority. The usage of priority and adjust commands is incorrect because they are not standard Linux commands used for managing process priorities. The renice command, although related to priority management, is used for changing the priority of an already running process, not for starting a new one with a specific priority."
    ),
    (
        "Which command will permanently mount a filesystem at boot by adding an entry to a specific configuration file?",
        [
            "Use fstab --add-entry",
            "Use mount --permanent",
            "Edit /etc/fstab",
            "Execute systemctl enable mount"
        ],
        2,
        "System Management",
        "To permanently mount a filesystem at boot in Linux, an entry must be added to the /etc/fstab file. The mount command only mounts filesystems temporarily until the next reboot."
    ),
    (
        "When administering a system, which command would you use to load a kernel module for immediate use without reflecting on module dependencies or its configuration?",
        [
            "modprobe",
            "lsmod",
            "insmod",
            "modinfo"
        ],
        2,
        "System Management",
        "'insmod' is the correct command for directly inserting a module into the Linux kernel without checking module dependencies. 'modprobe', in contrast, inserts a module considering its dependencies. 'lsmod' lists the currently loaded modules, and 'modinfo' provides detailed information about a specific module. Hence, the correct choice involves using 'insmod' when you do not want to account for dependencies."
    ),
    (
        "When working in the terminal, you need to display the absolute path of your current working directory. Which command will provide you with the most accurate and detailed result?",
        [
            "cd -",
            "dirname $(pwd)",
            "ls -a",
            "pwd"
        ],
        3,
        "System Management",
        "The command pwd (print working directory) is used to display the absolute pathname of the current working directory. This is the most direct and explicit command for this purpose, hence it is the correct answer. Understanding the current directory's absolute path is essential for numerous tasks, like referencing files or changing directories. The other options, ls for listing directory contents, cd - for moving to the previous directory, and dirname for extracting a path's directory part, do not serve the purpose of displaying the current directory's path."
    ),
    (
        "A system administrator needs to check the attributes of all volume groups on a Linux server to ensure they have enough free space to allocate to a new logical volume. Which command should the administrator execute?",
        [
            "vgdisplay",
            "lvdisplay",
            "lvs",
            "vgs"
        ],
        0,
        "System Management",
        "The vgs command provides a concise and formatted output showing various attributes of all volume groups on a system, including their size, the amount of space allocated, and free space. By using this command, the administrator can quickly ascertain if there is sufficient free space in any of the existing volume groups to accommodate a new logical volume. The other commands listed either do not provide the necessary information or apply to logical volumes (lvs) rather than volume groups."
    ),
    (
        "The command 'at' can be used to schedule a job for a specific time without the requirement for that to recur at regular intervals.",
        [
            "The statement is inaccurate",
            "The statement is accurate"
        ],
        1,
        "System Management",
        "The 'at' command is indeed used for one-time task scheduling on Linux systems. It does not provide a way to schedule recurring jobs; that functionality is handled by 'cron'. Therefore, 'at' is suitable for tasks that need to be run once at a certain point in time in the future."
    ),
    (
        "A system administrator has noticed that a server's time is not in sync with its designated time source. They need to verify the current synchronization status and performance of the server's timekeeping. Which command should they use?",
        [
            "chronyc sources",
            "chronyc add server",
            "chronyc tracking",
            "chronyc sourcestats"
        ],
        2,
        "System Management",
        "To check the current time synchronization status and performance metrics such as system time, frequency, and estimated error, the chronyc tracking command should be used. This command provides detailed information about the performance of the timekeeping system, making it invaluable for diagnosing issues related to time synchronization. Other commands like chronyc sources, chronyc add server, and chronyc sourcestats serve different purposes: sources displays information about the time sources that are currently being used, add server is not a valid command, and sourcestats reports on the drift and dispersion of the sources being tracked. However, when it comes to verifying the synchronization status and performance of the server, chronyc tracking is the correct command to use."
    ),
    (
        "Alice is working on a Linux server and has navigated through several directories. She wants to confirm the absolute path of the directory she is currently working in before deploying a new application. Which command should she use to display her current directory path?",
        [
            "ls -d .",
            "echo $PWD",
            "cd",
            "pwd"
        ],
        3,
        "System Management",
        "The correct answer is pwd, which stands for 'print working directory'. This command is used to output the full pathname of the current working directory, providing users with their exact location in the filesystem hierarchy. This information is especially important when performing operations that are sensitive to the current directory context, such as deploying applications, running scripts, or managing files."
    ),
    (
        "Which command would you use to display the full command line of a running process?",
        [
            "ps aux",
            "kill",
            "pidof",
            "lsof"
        ],
        0,
        "System Management",
        "The ps aux command provides a detailed list of all running processes, including the full command line used to start each process. The a flag tells ps to list the processes of all users, u includes user/owner information, and x includes processes that are not attached to a terminal. The pidof command only retrieves the process ID (PID) of a named process, whereas kill is used to send signals to processes (often to terminate them), and lsof lists open files and the processes that opened them."
    ),
    (
        "To create a new archive with cpio, which of the following commands would you use, given that you have a list of files to archive from a file called 'filelist.txt'?",
        [
            "cpio -iv < filelist.txt > archive.cpio",
            "cpio -o < filelist.txt",
            "cpio -ov < filelist.txt > archive.cpio",
            "tar -cf filelist.txt archive.cpio"
        ],
        2,
        "System Management",
        "The command cpio -ov < filelist.txt > archive.cpio is correct for creating a new archive named archive.cpio using the list of files contained in filelist.txt. The -o option is used with cpio to specify that files are being copied out into an archive, and the -v option is for verbose output, listing files as they are archived."
    ),
    (
        "What is the primary purpose of using the mv command in a Linux environment?",
        [
            "Moving and renaming files and directories",
            "Changing file permissions",
            "Copying files to a new directory",
            "Creating a duplicate of a file"
        ],
        0,
        "System Management",
        "The mv command is used primarily to move files and directories from one location to another or to rename them. It's an essential command for managing the filesystem structure. It does not actually copy the file content to a new location but rather changes the file's index node (inode) information in the filesystem's table to reflect the new location or name. This is why the correct answer is 'Moving and renaming files and directories', as it accurately describes the action performed by the mv command. The options 'Copying files to a new directory' and 'Creating a duplicate of a file' suggest replicating the file's content, which is not the behavior of mv; for those purposes, the cp command would be used. Lastly, 'Changing file permissions' is an operation performed by the chmod command, not mv."
    ),
    (
        "A system administrator needs to check the maximum amount of RAM supported by the server's motherboard. Which command would provide this information?",
        [
            "dmidecode --type memory",
            "lscpu",
            "lsblk",
            "dmidecode -s system-product-name"
        ],
        0,
        "System Management",
        "The command dmidecode --type memory is used to retrieve detailed information about the server's memory, including the maximum capacity supported by the motherboard. This is critical when planning upgrades or diagnosing memory-related issues. The other commands listed either provide information about the overall system (dmidecode -s system-product-name), display usage by current components (lsblk), or provide specific processor information (lscpu), but do not offer details about maximum RAM capacity."
    ),
    (
        "An administrator has just completed the installation of a new kernel on a Linux system. After installing the kernel and related modules, they wish to update the GRUB2 bootloader configuration to ensure that the system will boot using this new kernel. Which of the following commands should the administrator run to correctly generate a new configuration and ensure the new kernel is bootable?",
        [
            "grub2-update",
            "grub2-mkconfig -o /boot/grub2/grub.cfg",
            "grub2-install",
            "mkinitrd /boot/initrd.img"
        ],
        1,
        "System Management",
        "The command 'grub2-mkconfig -o /boot/grub2/grub.cfg' generates a new GRUB2 configuration file and writes it to the default location for GRUB2's configuration. The '-o' option is used to specify the output file and is critical for actual application of changes. Other options shown might seem plausible, but they do not perform the task of updating the configuration."
    ),
    (
        "What is the primary purpose of the directory located at '/home' in a Linux file system?",
        [
            "To hold temporary files that are deleted upon reboot",
            "To store personal user files and directories",
            "To store executables necessary for booting the system",
            "To maintain system-wide configuration files"
        ],
        1,
        "System Management",
        "The '/home' directory is designed to contain the personal files and subdirectories for each user on a Linux system. It is the default directory for user-specific data and configurations, and each user is typically granted exclusive access to their respective '/home/username' directory. Other options are either incorrect or based on misconceptions about the purpose of system directories."
    ),
    (
        "After receiving alerts of potential hardware issues, a system administrator needs to check the status of the software RAID arrays on a Linux server. Which is the BEST command to use in order to display the current status of all active RAID arrays managed by mdadm?",
        [
            "fdisk -l",
            "lsblk",
            "cat /proc/mdstat",
            "mdadm --detail"
        ],
        2,
        "System Management",
        "The cat /proc/mdstat command is the correct option because it provides the current status of all active software RAID arrays, including information on individual disks and their state within each array. The mdadm --detail command also gives detailed information, but it needs to be followed by a specific device name (e.g., mdadm --detail /dev/md0), and therefore it is not as comprehensive for displaying all active arrays at once. The fdisk -l command lists all partition tables, which is not specific to active RAID arrays. The lsblk command lists block devices, which includes RAID arrays, but does not provide detailed RAID status."
    ),
    (
        "A Linux administrator needs to configure a Linux server to send its system logs to a remote log server at the IP address 192.168.150.50. Which configuration line should the administrator add to the rsyslog configuration file to accomplish this task?",
        [
            ". @@192.168.150.50",
            ". >192.168.150.50",
            ". #192.168.150.50",
            ". @192.168.150.50"
        ],
        3,
        "System Management",
        "The correct answer is *.* @192.168.150.50 because the syntax specifies that logs of all facilities and all severities (*.*) should be forwarded to the remote server at the specified IP address using the UDP protocol (denoted by a single @ sign). Other answers are incorrect because > does not indicate remote logging, multiple @ signs or using # are not valid for specifying a remote log server in rsyslog configuration, and the > is reminiscent of shell redirection which has no context here."
    ),
    (
        "You are configuring a Linux server and need to prioritize LDAP for user and group lookups but want to fall back to the local /etc/passwd and /etc/group files if the LDAP lookup fails. Which of the following configurations would you implement in /etc/nsswitch.conf to achieve this requirement?",
        [
            "passwd: files nis ldap group: files nis ldap",
            "passwd: nis files ldap group: nis files ldap",
            "passwd: ldap files group: ldap files",
            "passwd: files ldap group: files ldap"
        ],
        2,
        "System Management",
        "The /etc/nsswitch.conf file determines the order of lookups performed when a certain type of information is requested, with the services listed from left to right in order of preference. The correct configuration is passwd: ldap files and group: ldap files, which first attempts to resolve password and group information using LDAP and then falls back to local files if LDAP is not available. The wrong answers suggest looking up files before LDAP, which would not meet the requirement, or including services not mentioned in the scenario, such as NIS."
    ),
    (
        "What command from the net-tools suite is traditionally used to configure network interfaces on Linux systems?",
        [
            "ifconfig",
            "hostname",
            "netstat",
            "iwconfig"
        ],
        0,
        "System Management",
        "The correct answer is ifconfig. The ifconfig command is one of the most commonly used programs from the net-tools suite for network interface configuration. In its basic form, it allows users to configure, manage, and query the settings of network interfaces. It's important to note that while ifconfig is still used on many systems, it is considered deprecated in favor of the more modern ip command from the iproute2 suite. The other answers are not correct because netstat is mainly used for displaying network connections, routing tables, interface statistics, masquerade connections, and multicast memberships. iwconfig is used to configure wireless network interfaces, and hostname is used to show or set the system's host name, not to manage network interfaces."
    ),
    (
        "A system administrator needs to permanently change the hostname on a Linux server to 'server-prod'. They decide to directly edit the necessary file to apply the hostname change across reboots. Which file should the administrator edit to achieve this?",
        [
            "/etc/hosts",
            "/etc/hostname",
            "/etc/hostname.conf",
            "/etc/sysconfig/hostname"
        ],
        1,
        "System Management",
        "The correct file to edit in order to permanently change the hostname on a Linux system is /etc/hostname. This file contains the system's hostname, which is read at boot time and sets the system's hostname for the duration of the session. Other options provided are close, but they serve different purposes: /etc/hosts is used for static IP to hostname mappings, and while /etc/hostname.conf and /etc/sysconfig/hostname look like they might be related to hostname configuration, they are not standard files for setting the hostname on most Linux distributions."
    ),
    (
        "An administrator has started a lengthy data analysis script in the foreground of their terminal. They now need to start another task but realize the script will take several more hours to complete. Which of the following commands should the administrator use to move the currently running script into the background so they can continue using the current terminal session?",
        [
            "Stop the script with Ctrl+Z and then move it to the background with the bg command.",
            "Press Ctrl+C to move the running script to the background.",
            "Press Ctrl+D to send the script to the background and free up the terminal.",
            "Use the jobs command to automatically move the script to the background."
        ],
        0,
        "System Management",
        "The bg command is used for placing a job that was stopped (e.g., with Ctrl+Z) into the background. However, simply using bg won't move a foreground process to the background unless it has been stopped first. Therefore, the correct sequence for moving a currently running foreground process to the background involves stopping the process with Ctrl+Z and then using bg to continue it in the background. The incorrect answers involve commands that either do not affect running jobs (jobs lists the jobs), or are related to stopping (Ctrl+C) or logging out of the shell (Ctrl+D), which will not help to achieve the desired outcome."
    ),
    (
        "A system administrator needs to create a compressed backup of the /var/log directory. Which command should they use to create a gzip-compressed archive file named log_backup.tar.gz?",
        [
            "tar -czvf log_backup.tar.gz /var/log",
            "tar -tzvf log_backup.tar.gz /var/log",
            "tar -xvf log_backup.tar.gz /var/log",
            "tar -cvf log_backup.tar.gz /var/log"
        ],
        0,
        "System Management",
        "The correct answer is tar -czvf log_backup.tar.gz /var/log because the options -c create a new archive, -z filter the archive through gzip for compression, -v produce verbose output, showing all processed files, and -f specify the filename of the archive. The incorrect options either do not specify gzip compression, which is required to produce a .gz file, or use options that perform actions other than creating an archive, such as extracting files or listing the contents of an archive."
    ),
    (
        "Which lvchange option is used to prevent allocation of physical extents to a logical volume?",
        [
            "-a n or --alloc none",
            "-an or --activate no",
            "-r or --resizefs",
            "-l +100%FREE"
        ],
        0,
        "System Management",
        "The lvchange option '-a n' or '--alloc none' is used to change the allocation policy for a logical volume to 'none', preventing further extents from being allocated to the volume. This option would be used in advanced scenarios such as maintenance or to prevent changes to a volume while taking a snapshot. The other listed options do not relate to the allocation policy and serve different purposes within the lvchange command."
    ),
    (
        "After successfully compiling a program from source code using 'make', which command should be used to install the compiled software into the system-wide directories so that it becomes executable from any location?",
        [
            "install make",
            "make setup",
            "make config",
            "make install"
        ],
        3,
        "System Management",
        "The 'make install' command is used after compiling software to copy the binaries, libraries, and any associated files to the appropriate system directories, allowing the software to be run from anywhere on the system. This step often requires administrative privileges because it modifies system-level directories."
    ),
    (
        "During your routine system maintenance, you need to create an archive of the /var/log directory to preserve the system logs before clearing them for the new fiscal year. You decide to use the tar command to create a compressed archive. Which of the following commands correctly creates a gzip compressed archive of the /var/log directory named system_logs.tar.gz?",
        [
            "tar -czvf system_logs.tar.gz /var/log",
            "tar -rvf system_logs.tar.gz /var/log",
            "tar -cv system_logs.tar.gz /var/log",
            "tar cvzf /var/log > system_logs.tar.gz"
        ],
        0,
        "System Management",
        "The correct answer is tar -czvf system_logs.tar.gz /var/log. The -c option tells tar to create a new archive, -z instructs tar to compress the archive with gzip, -v enables verbose output, displaying files added to the archive, and -f specifies the filename of the archive. The incorrect options either omit compression with gzip by not using -z, use the r option inappropriately (which is used for appending files to an already existing archive), or incorrectly specify the output archive name without the -f option which is necessary for naming the archive file."
    ),
    (
        "A system administrator wants to perform a directory synchronization from a local folder to a remote backup server. The requirement is to ensure that only the differences since the last sync are transferred to minimize network usage. The sync needs to be recursive to include all subdirectories and also preserve file permissions. Which command accomplishes this goal most efficiently?",
        [
            "rsync -a /local/directory user@remote:/backup/directory",
            "rsync --update /local/directory user@remote:/backup/directory",
            "rsync --dry-run /local/directory user@remote:/backup/directory",
            "rsync --in-place /local/directory user@remote:/backup/directory"
        ],
        0,
        "System Management",
        "The correct answer is rsync -a /local/directory user@remote:/backup/directory because the -a (archive) flag is used to preserve permissions, timestamps, ownership, and to ensure recursive copying — while also optimizing by transferring only the differences from the last sync. The --dry-run flag would only simulate the transfer without actually copying files, --update will skip files newer on the receiver without considering other changes, and --in-place could potentially reduce transfer efficiency as it updates destination files in place - useful for large, single files but not necessarily for directory syncs with minimal changes."
    ),
    (
        "During system troubleshooting, you notice that user authentication seems to bypass the local /etc/passwd file and is directly querying an LDAP server, leading to delays. Which configuration entry should you examine to ensure that local files are checked before LDAP in the name service resolution process?",
        [
            "passwd: ldap files in /etc/nsswitch.conf",
            "authentication: files ldap in /etc/nsswitch.conf",
            "passwd: nis files in /etc/nsswitch.conf",
            "passwd: files ldap in /etc/nsswitch.conf"
        ],
        3,
        "System Management",
        "The entry passwd: files ldap in the /etc/nsswitch.conf file ensures that the local authentication lookups consult the local /etc/passwd file (files) before attempting to use LDAP. This correct configuration optimizes user authentication by reducing reliance on network services when local credentials are available. Alternative configurations like passwd: ldap files or passwd: nis files suggest that LDAP or NIS (Network Information Service) would be queried before local files respectively, which is not the desired behavior based on the scenario provided. There is no authentication: files ldap directive in /etc/nsswitch.conf, making it an incorrect and misleading answer."
    ),
    (
        "An administrator notices that a backup process, which has a process ID (PID) of 2635, is consuming more resources than it should during peak hours, impacting the performance of other critical services on the server. The administrator decides to lower the priority of this backup process to minimize its impact on system performance. Which of the following commands should be used to change the niceness (priority) of the running process to a higher nice value, thereby giving it a lower scheduling priority, without stopping the process?",
        [
            "nice -5 -p 2635",
            "renice -5 2635",
            "renice +5 2635",
            "nice --adjustment=+5 --pid=2635"
        ],
        2,
        "System Management",
        "The correct answer is renice +5 2635 because renice is used to change the scheduling priority of a running process. The +5 argument increases the nice value for the specified PID, which is 2635 in this case, making it less favorable for scheduling and therefore less competitive for CPU time compared to other processes with a lower nice value. A lower priority is implied by a higher nice value. The incorrect answers involve commands that either do not change process priority, are syntactically incorrect, or specify a decrease in the nice value, which would mistakenly increase the process's competition for CPU resources."
    ),
    (
        "Which of the following commands is used to check and repair filesystem errors on a Linux system?",
        [
            "chmod",
            "mkfs",
            "fdisk",
            "chown",
            "dd",
            "fsck"
        ],
        5,
        "System Management",
        "The fsck command is used to check and repair Linux filesystem errors. This command can be applied to filesystems that are currently unmounted or in an unclean state to inspect them or rectify inconsistencies that are found during the scan. It is often used during system boot time or maintenance mode. Other tools like mkfs are used to create filesystems, not check or repair them, and dd is a command used for copying and converting data."
    ),
    (
        "An administrator wants to check the health and status of the RAID arrays on a Linux system. Which file should be examined to find the most comprehensive information about the RAID devices?",
        [
            "/proc/partitions",
            "/proc/mdstat",
            "/dev/md0",
            "/etc/mdadm.conf"
        ],
        1,
        "System Management",
        "The correct answer is '/proc/mdstat' because this virtual file provides detailed information about the status of RAID arrays. It includes the status of each RAID device, details about individual disks, and the progress of any ongoing RAID recovery or resynchronization. Other options mentioned do not serve the purpose of RAID monitoring. '/etc/mdadm.conf' is used for RAID configuration, not status monitoring. '/dev/md0' is a device file for a specific RAID array, not a status file. '/proc/partitions' provides partition information, but not detailed RAID array status."
    ),
    (
        "The command make install is used before the command ./configure when compiling a package from source.",
        [
            "True",
            "False"
        ],
        1,
        "System Management",
        "When compiling software from source in Linux, the correct sequence of commands starts with ./configure to set up the environment and options for the compilation. Afterward, make is used to compile the source code into executable binaries, and finally, make install is executed to install the binaries into the system. Therefore, make install comes after and not before ./configure."
    ),
    (
        "An organization requires a data storage solution using multiple disks. The solution must ensure continuous data availability even if two disks fail concurrently. Which configuration should be utilized to fulfill this requirement?",
        [
            "Dual parity configuration (capable of handling two simultaneous disk failures)",
            "Striped set without redundancy",
            "Mirrored set across two or more disks without parity",
            "Striped mirrors with single-level parity"
        ],
        0,
        "System Management",
        "The appropriate configuration for this scenario is RAID 6, which uses dual parity, allowing the array to operate even if two disks fail at the same time. RAID 5 uses single parity and can only survive the loss of one disk, which does not meet the criteria of the scenario. RAID 0 has no redundancy and therefore provides no fault tolerance. RAID 10 can sustain multiple drive losses but only if they are not part of the same mirrored set, thus there's a risk if two specific disks fail."
    ),
    (
        "An administrator needs to extend the storage capacity of a Linux server. They have added a new physical disk and created a physical volume (PV) on it. Now, the administrator wants to check the existing volume groups (VGs) to decide into which volume group the new physical volume should be extended. Which command should be used to display the current volume groups and their associated information?",
        [
            "lvdisplay",
            "pvscan",
            "vgs",
            "fdisk -l"
        ],
        2,
        "System Management",
        "The correct answer is 'vgs', as it stands for 'volume groups' and is used to display information about the volume groups managed by LVM. It would give an overview of the volume groups available on the system, including details like VG name, the total size, available free space, and the number of physical volumes (PVs) it contains, helping the administrator in making a decision where to extend the storage. The answer 'lvdisplay' is incorrect because it shows information about logical volumes, not volume groups. 'pvscan' only scans all disks for physical volumes, it doesn't provide detailed information about volume groups. 'fdisk -l' displays partition and disk information, which does not directly relate to LVM's volume group configuration."
    ),
    (
        "A system administrator needs to ensure that a recently installed kernel appears in the boot menu. The GRUB2 bootloader is used, and the administrator has copied the new kernel image to /boot. Which of the following commands should be executed to regenerate the GRUB2 configuration so that the new kernel will be listed at boot time?",
        [
            "grub2-mkconfig -o /boot/grub/grub.cfg",
            "update-grub",
            "mkinitrd",
            "grub2-mkconfig --refresh"
        ],
        0,
        "System Management",
        "The correct answer is grub2-mkconfig -o /boot/grub/grub.cfg. When the grub2-mkconfig command is followed by -o (output) option, it directs the command to write the generated configuration to a specified file, which is typically /boot/grub/grub.cfg or /boot/grub2/grub.cfg depending on the distribution. Writing to any other location, as suggested in the incorrect answers, will not influence the boot process, and the command update-grub is a convenience script present in some systems, which essentially calls grub-mkconfig with the appropriate arguments."
    ),
    (
        "Writing any data to /dev/null saves it in a special buffer that can be retrieved later.",
        [
            "True",
            "False"
        ],
        1,
        "System Management",
        "/dev/null is known as the null device in UNIX-like operating systems, which discards any data written to it. Anything redirected to /dev/null is effectively gone, as this device does not save any data and does not allow for the retrieval of any data written to it."
    ),
    (
        "What is the primary function of the 'resolvectl' command in a Linux system?",
        [
            "Establish a VPN connection",
            "Monitor network traffic in real time",
            "Enable or disable network interfaces",
            "Manage DNS resolution on the system"
        ],
        3,
        "System Management",
        "The 'resolvectl' command is used to query and change the system resolver settings, typically provided by the systemd-resolved service. It effectively allows users to manage DNS settings, such as querying DNS records or changing the DNS server used by the system. Answer A is correct because it directly pertains to managing DNS resolution on the system, which is the primary role of 'resolvectl'. Answer B is incorrect because 'resolvectl' does not manage the enabling or disabling of network interfaces; 'ip' or 'ifconfig' would be used for that. Answer C is incorrect because 'resolvectl' does not provide the functionality to monitor network traffic, which would be accomplished with tools like 'tcpdump' or 'wireshark'. Answer D is incorrect as it describes a function of 'networkmanager' or 'nmcli', not 'resolvectl'."
    ),
    (
        "An administrator needs to modify the file context type for a custom directory, /data/webapp, to match the type used by web content in an SELinux environment. Which command should they use to achieve this, ensuring the default policy is maintained for consistency?",
        [
            "semanage boolean -m --on httpd_sys_content_t '/data/webapp'",
            "semanage fcontext -a -t httpd_sys_content_t '/data/webapp(/.*)?'",
            "restorecon -v /data/webapp",
            "chcon -t httpd_sys_content_t /data/webapp"
        ],
        1,
        "Security",
        "The command semanage fcontext -a -t httpd_sys_content_t '/data/webapp(/.*)?' is correct because it uses the semanage fcontext command, which is responsible for managing file context types within SELinux policy. The -a flag is used to add a file specification, -t specifies the type, and the file path given indicates that the policy change should apply to the /data/webapp directory and all files within. This command ensures that the custom directory has the correct context for serving web content securely according to SELinux policies."
    ),
    (
        "An administrator wants to prevent users from creating hard links to a certain sensitive file on a Linux system. Which command should the administrator use to achieve this security measure?",
        [
            "chattr +i /path/to/file",
            "chmod 700 /path/to/file",
            "chattr +a /path/to/file",
            "setfacl -m u:user:--- /path/to/file"
        ],
        0,
        "Security",
        "The correct answer is chattr +i /path/to/file. The chattr command changes the file attributes on a Linux file system. The +i attribute makes a file immutable, which means that the file can neither be modified nor deleted, and new links cannot be created to it. This is an advanced method for securing files that are not commonly modified but are critical to system security. The incorrect options either do not directly apply to the prevention of hard link creation, use an incorrect attribute, or are unrelated to file attributes."
    ),
    (
        "What is the role of a private key in a public key infrastructure (PKI)?",
        [
            "It is distributed to the public for encrypting data intended for the key's owner.",
            "It is used to decrypt data that has been encrypted with the corresponding public key and to create digital signatures.",
            "It acts as a universally recognized identifier for the key's owner in all encrypted communications.",
            "It verifies the authenticity of digital certificates issued by the certificate authority."
        ],
        1,
        "Security",
        "The private key is used to decrypt data encrypted with the corresponding public key and to create digital signatures. It must be kept secure and confidential to ensure the integrity of the encryption and the authenticity of the data being signed. Sharing the private key compromises the security of the PKI system."
    ),
    (
        "An administrator wishes to grant a user, john, the ability to restart the httpd service without providing a password. Which line should be added to the /etc/sudoers file to accomplish this?",
        [
            "john ALL=(ALL) NOPASSWD: ALL",
            "john ALL=(ALL) /bin/systemctl restart httpd",
            "john ALL=(ALL) NOPASSWD: systemctl restart httpd",
            "john ALL=(ALL) NOPASSWD: /bin/systemctl restart httpd"
        ],
        3,
        "Security",
        "The correct line to add is john ALL=(ALL) NOPASSWD: /bin/systemctl restart httpd. This allows the user john on all hosts (ALL) to execute the specific command /bin/systemctl restart httpd without being prompted for a password (NOPASSWD:). The ALL=(ALL) allows execution as all users and groups, although in this case, the specific command does not require changing to a different user or group. It's important to use full paths for commands in sudoers for security. The other options are incorrect because they either omit NOPASSWD: which would still prompt for a password, use ALL which would undesirably allow all commands, or specify an incorrect command path."
    ),
    (
        "A Linux system administrator wants to enforce strong password policies on the system. They plan to implement password complexity requirements that include a minimum length of 10 characters, at least one uppercase and one lowercase letter, and at least one digit or special character. Which of the following tools should the administrator configure to meet these requirements?",
        [
            "Edit the /etc/login.defs file to include the minimum length password requirement without parameters for complexity.",
            "Use the passwd command to enforce stronger passwords when users change their passwords next time.",
            "Configure the PAM module pam_pwquality.so to include password strength requirements in /etc/security/pwquality.conf or similar.",
            "Use the chage command to set password expiration and enforce the new strong password policy."
        ],
        2,
        "Security",
        "PAM, or Pluggable Authentication Modules, are used in Linux environments to integrate multiple low-level authentication schemes into a high-level API that allows for programs that rely on authentication to be written independently of the underlying authentication mechanism. By configuring the PAM module responsible for password quality control, typically pam_pwquality.so, the administrator can enforce password strength policies. The configurations can include requirements for different character classes, minimum length, and other password policies. The other options, such as chage, passwd, and faillock, do not directly allow an administrator to enforce password strength requirements, as they serve different purposes in user account and password management."
    ),
    (
        "A system administrator is tasked with granting a user named 'techuser' the ability to run all commands as any user on a specific Linux server. To accomplish this securely while employing syntax validation, which of the following configurations should the administrator add to the sudoers file using an appropriate command?",
        [
            "techuser ANY=(ALL) /usr/local/bin/backup.sh",
            "ALL techuser=(ALL) NOPASSWD: /usr/local/bin/backup.sh",
            "techuser ALL=(ALL:ALL) NOPASSWD: /usr/local/bin/backup.sh",
            "techuser /usr/local/bin/backup.sh",
            "techuser ALL=(ALL) ALL",
            "techuser ALL=(ALL:ALL) ALL"
        ],
        5,
        "Security",
        "The correct entry is 'techuser ALL=(ALL:ALL) ALL' which grants the user 'techuser' the ability to run any command as any user on all hosts. The 'ALL=(ALL:ALL)' portion indicates that from any host (the first 'ALL'), 'techuser' can execute commands as any user (the second 'ALL') and as any group (after the colon). The final 'ALL' specifies that any command can be executed. This entry provides the specific privileges required without providing unnecessary access, adhering to the principle of least privilege. The incorrect answers either do not provide the required privileges, have syntax errors, or grant privileges that are too broad, which could pose a security risk."
    ),
    (
        "What are System booleans in the context of Security-enhanced Linux (SELinux)?",
        [
            "Background processes ensuring SELinux states are maintained",
            "Policy types defining the level of confinement in SELinux",
            "Commands used to relabel files with new security contexts",
            "Toggle switches that can adjust SELinux policies at runtime"
        ],
        3,
        "Security",
        "SELinux System booleans are toggle switches that can enable or disable certain security features within SELinux. They are used to adjust the security policy without requiring policy recompilation or relabeling, which makes them a powerful tool for system administrators when customizing the behavior of SELinux. The correct answer explains this concept accurately, whereas the other options relate to different aspects of SELinux or Linux security and do not describe System booleans."
    ),
    (
        "In an effort to secure communication for an internal-facing web service, a system administrator has been tasked with implementing an encrypted connection protocol. External validation of the server's identity by outside entities is not a requirement due to the service being exclusively accessed within the organization. What is the most appropriate action for the administrator to undertake?",
        [
            "Activate encrypted connections without a certificate, as internal services do not require authentication.",
            "Obtain and install a certificate from a recognized certificate authority.",
            "Create and configure a self-signed certificate.",
            "Rely on secure shell protocols for encrypted web traffic, circumventing the need for certificates.",
            "Operate the web service without encryption since it is internally accessed and does not need protection.",
            "Procure a domain-validated certificate and apply it to the web service."
        ],
        2,
        "Security",
        "The correct action is to generate a self-signed certificate because it allows the administrator to implement encryption for the web service without involving an external certificate authority (CA). This method is suitable for environments where trust is established by other means, such as within an organization where all clients accessing the service are controlled and can be configured to trust the self-signed certificate. The use of a self-signed certificate enables encrypted connections and ensures data privacy on the internal network."
    ),
    (
        "In the scenario where a Linux system has multiple services running, which of the following actions is the BEST practice to secure the corresponding service accounts?",
        [
            "Configuring PAM modules to limit the access times for service accounts.",
            "Setting a strong, unique password for each service account.",
            "Changing the default shell of the service accounts to /bin/nologin.",
            "Changing the home directory permissions of service accounts to 700."
        ],
        2,
        "Security",
        "Setting a strong, unique password for service accounts is essential as it ensures that each service has its distinct access credentials, which can prevent unauthorized access if one service is compromised. Locking service accounts with shell access adds an additional layer of security. Disabling login capabilities entirely for service accounts is the most secure practice because it mitigates the risk of these accounts being used to gain unauthorized system access. While changing the default shell to /bin/false or nologin reduces the functionality of the account for interactive use, it does not prevent the account from executing its service-related tasks. The reason this is the best practice is that it does not rely on password strength or the potential for a password to be compromised, as it altogether disables the ability for the service account to be used for direct logins. Service accounts should not be used for interactive logins, and their purpose is to run the corresponding service. Changing the home directory permissions and using PAM modules are also good security practices, but they do not restrict login capabilities as effectively as setting the shell to nologin."
    ),
    (
        "As a systems administrator, you have noticed SELinux Access Vector Cache (AVC) denial messages in your system's audit logs, indicating that a legitimate application is being blocked from performing necessary actions. You want to create a custom SELinux module to adjust the policy and allow the application to function as intended. Which command should you use to generate a custom SELinux policy module based on the recorded AVC denials?",
        [
            "audit2why -M mymodule < /var/log/audit/audit.log",
            "semanage module -i mymodule.pp",
            "audit2allow -M mymodule < /var/log/audit/audit.log",
            "getenforce > mymodule.te"
        ],
        2,
        "Security",
        "The correct command is audit2allow -M mymodule < /var/log/audit/audit.log. It reads the AVC denial messages from the specified log file and generates a custom SELinux policy module named 'mymodule'. The -M option specifies the name of the module. This command is designed to interpret AVC messages and create a tentative policy that permits the denied actions, easing the process of troubleshooting and adjusting SELinux policies. The other options, audit2why, semanage module -i, and getenforce, serve different purposes. The audit2why command is used to interpret denial messages and provide explanations, not to generate policy modules. semanage module -i would be used to install a module, not create one. getenforce simply reports the current SELinux enforcement mode and does nothing related to policy creation."
    ),
    (
        "A Linux user checks the permissions of a file with the ls -l command and receives the following output: -rw-r--r-- 1 alice alice 5607 Jan 20 13:30 report.txt. What can the user 'alice' do with 'report.txt' based on the given permissions?",
        [
            "Only read the file",
            "Read and modify the file",
            "Modify but not read the file",
            "Execute the file"
        ],
        1,
        "Security",
        "The permissions -rw-r--r-- indicate that the owner of the file, which is 'alice', has read and write permissions. The owner can open, read, and modify the file. The group members and others have only read permissions, as indicated by r-- after the owner permissions. They can open and read the file, but cannot modify or execute it."
    ),
    (
        "A Linux system administrator needs to allow a user named 'johndoe' to have read and write access to a file called 'report.txt', which currently does not grant him those rights. The administrator does not want to modify the existing group permissions on the file. Which command should the administrator use to achieve this without affecting the rights of other users?",
        [
            "usermod -a -G report.txt johndoe",
            "setfacl -m u:johndoe:rw report.txt",
            "chmod u+rw johndoe report.txt",
            "chown johndoe: report.txt"
        ],
        1,
        "Security",
        "The setfacl -m u:johndoe:rw report.txt command is correct because it explicitly modifies the access control list for the user 'johndoe' granting him read (r) and write (w) permissions on 'report.txt' without altering current group permissions or the permissions of other users."
    ),
    (
        "During the process of enhancing the security of your company's e-commerce platform, you are tasked to obtain a digital certificate for encrypting web traffic. Considering the critical nature of the data being protected, what aspect should be a top priority when choosing an entity to issue and manage the necessary digital certificates?",
        [
            "The overall trust and reliability of the issuing entity",
            "Past security incidents involving the entity",
            "The pricing model of the entity for certificate issuance",
            "Proximity of the entity's operations to your data center"
        ],
        0,
        "Security",
        "The overall trust and reliability of the entity tasked with issuing digital certificates is essential to consider, as it will be a cornerstone for secure transactions on the e-commerce platform. A entity with a positive reputation has proven their ability to securely validate entities before issuing certificates and generally offers greater support. This contributes to increased confidence among users and partners. While factors like proximity for latency and the price of services are pragmatic business concerns, these do not have a direct impact on the security and reliability of the certificates. An entity's past security incidents, although concerning, are less about trust in a general sense and more specific to their operational security, which could indeed inform their current trustworthiness but should be evaluated alongside the entity's corrective actions and current security posture."
    ),
    (
        "A new junior system administrator has been tasked with reviewing user accounts on a vital Linux server. While inspecting the /etc/passwd file, they noticed an account entry that does not have a corresponding /home directory. Which of the following are potential explanations for this situation?",
        [
            "The account has an expired password and, therefore, the home directory was removed automatically.",
            "The account's default shell is set to /usr/sbin/nologin, which implies that no home directory was created when the account was added.",
            "The account is intended for a system service or process and is not designed for regular user login activities.",
            "The user associated with the account has been assigned to an incorrect group, which is why the home directory is missing."
        ],
        2,
        "Security",
        "In the /etc/passwd file, it is common for system accounts to not have a corresponding /home directory because these accounts are not meant for regular user logins and do not require personal storage space. They're typically used for running specific services or tasks. Standard user accounts should normally be configured with a home directory. The presence of nologin as the shell is an additional confirmation that the account is not intended for interactive login, but it is not a direct indicator of the absence of the home directory. Accounts with shells set to /usr/sbin/nologin or /bin/false can still have home directories configured for storing service data, even though they don't provide shell access. The other answers include misconceptions, as an expired password or incorrect group assignments would not cause an account to lack a home directory; these issues would affect the ability to login or permissions, respectively."
    ),
    (
        "A systems administrator needs to verify the current rules on a Linux system's firewall, including the numeric handle and specific details such as packet counts and byte counters. Which iptables command will provide this detailed information?",
        [
            "iptables -L -v",
            "iptables -t nat -L",
            "iptables -S",
            "iptables -n -v -L"
        ],
        3,
        "Security",
        "The command iptables -n -v -L displays the current rule set with packet and byte counters and does not resolve names, which can slow down the output if there are lots of network traffic and active rules. This is commonly used to get a precise and quick overview of the rules that are counting traffic on a Linux server. iptables -L -v also lists the active rules with verbose output, but without the -n option, it may attempt to resolve names, which can be less efficient in some scenarios. iptables -S lists the active rules in a format that can be used as input to restore the table, but it does not include packet and byte counts. The iptables -t nat -L command specifically checks only the rules in the 'nat' table, which is not what the question asked for."
    ),
    (
        "A Linux administrator needs to grant a user named 'jane' write access to a file called 'data.log', which is currently only accessible by its owner 'john'. The file should not have its existing permissions altered for any other user or group. Which of the following commands would correctly grant 'jane' the required access?",
        [
            "chown jane data.log",
            "setfacl -m u:jane:w data.log",
            "setfacl -m u:jane:rwx data.log",
            "chmod u+w data.log",
            "chmod +w data.log",
            "setfacl -m o:w data.log"
        ],
        1,
        "Security",
        "The correct answer is setfacl -m u:jane:w data.log because the setfacl command is used to set Access Control Lists, and -m is used to modify the ACL by adding a new rule. The rule u:jane:w specifies that the user 'jane' is given write (w) access. Using ACLs allows for extending the permission set beyond the traditional owner, group, and others model."
    ),
    (
        "As a security-conscious server administrator, you are configuring SELinux on a server with very limited services and want to ensure that only essential security policies are applied to maintain system performance. Which SELinux policy type is specifically designed for such a minimalistic approach?",
        [
            "Minimum",
            "Targeted",
            "MCS (Multi-Category Security)",
            "Strict"
        ],
        0,
        "Security",
        "The 'Minimum' policy type is the correct answer because it is explicitly designed for environments that run a limited number of services and where administrators want to minimize the number of services and processes under SELinux management to reduce complexity and performance impact. While the 'Targeted' policy type is also a commonly used SELinux policy that focuses on confining specific services, it is not as minimal as the 'Minimum' policy type. The 'Strict' policy type enforces SELinux security controls across all processes, which is not suitable for a minimal approach."
    ),
    (
        "A system administrator needs to secure the configuration file /etc/important.conf to prevent any modifications, including by root, because it contains sensitive system settings. Which command should the administrator execute to achieve this?",
        [
            "chattr +a /etc/important.conf",
            "chattr +d /etc/important.conf",
            "chattr +i /etc/important.conf",
            "chattr +s /etc/important.conf"
        ],
        2,
        "Security",
        "The chattr +i /etc/important.conf command is correct because it sets the immutable attribute on the file, which prevents any modifications to the file, even by the root user, until the attribute is removed. This is useful for protecting critical system files. The +a attribute only allows appending to the file, not preventing modifications. The +s attribute is used to mark a file for secure deletion, and +d is intended to optimize file deletion, none of which prevent modifications."
    ),
    (
        "A company is planning to streamline their employee's access to multiple internal and external web applications to improve productivity and security. They want their employees to only log in once each day and gain access to all authorized resources without the need to sign in multiple times. Which solution should be implemented to achieve this requirement?",
        [
            "Implement an SSO solution",
            "Implement Pluggable Authentication Modules (PAM) on all servers",
            "Establish centralized user management",
            "Distribute SSH keys to all users"
        ],
        0,
        "Security",
        "The correct answer is Implement an SSO solution because SSO is the process that allows network users to provide their credentials just once to gain access to multiple applications and services. Implementing an SSO solution simplifies the user experience by requiring only one set of login credentials, reducing password fatigue and decreasing the chance of a security breach due to weak user credentials. On the other hand, SSH keys are primarily used for secure remote login from one computer to another and not for SSO across multiple web applications. Centralized user management is used to manage user accounts and permissions from a single location, which is not specific to the single authentication process required by SSO. Lastly, implementing PAM does not directly provide SSO capabilities, as PAM is used for implementing flexible authentication mechanisms for local system access."
    ),
    (
        "Your company requires remote system administrators to authenticate using a method more secure than passwords alone when accessing critical Linux servers. Which of the following options provides an additional layer of security that requires something the user has, in addition to something the user knows?",
        [
            "Using a one-time password (OTP) token in conjunction with their user password",
            "Implementing a strict password strength and rotation policy",
            "Employing biometric authentication such as fingerprint or facial recognition",
            "Requiring administrators to connect using SSH keys"
        ],
        0,
        "Security",
        "Using a one-time password (OTP) token alongside the regular password constitutes two-factor authentication (2FA), which is a subset of MFA. The OTP token is a physical device or software application that generates a time-limited code, adding an additional security layer beyond the password, which is 'something the user knows'. The token ensures 'something the user has', thereby satisfying MFA requirements. Biometric authentication, while it also provides an additional security layer, is categorized as 'something the user is', and it is generally not used in conjunction with a password as the sole two factors in remote system administration. Password strength policies improve the security of the password itself but do not add another factor. SSH keys are a secure method of authentication but are considered a single factor: 'something the user has'."
    ),
    (
        "What is the primary function of the groupmod command in a Linux environment?",
        [
            "To create a new user account on the system",
            "To add or remove a user from a group",
            "To modify a group's name or GID (Group ID)",
            "To modify file permissions for a group of files"
        ],
        2,
        "Security",
        "The groupmod command is used to modify a group's details, such as its name or Group ID (GID). Knowledge of this command is crucial for system administrators when they need to manage group information and its related security implications. For example, changing a group's name might be necessary when organizational roles change or to correct errors in naming conventions. The incorrect options provided are related to user and file management, not directly to groups, which may lead to confusion, but understanding groupmod pertains specifically to group modifications."
    ),
    (
        "A system administrator has noticed SELinux is preventing a web application from functioning properly on a production server running the 'targeted' policy. The administrator wants to temporarily relax SELinux enforcement to diagnose the issue without entirely disabling SELinux or making permanent policy changes. Which command should the administrator use to fulfill this requirement?",
        [
            "setenforce Disabled",
            "setsebool -P",
            "enforce 0",
            "setenforce enforcing",
            "setenforce 0"
        ],
        4,
        "Security",
        "The setenforce 0 command sets SELinux to 'Permissive' mode. In 'Permissive' mode, SELinux continues to evaluate rules and log violations but does not enforce the policy, allowing the administrator to see what would be blocked without impacting the application. Once the evaluation is complete, using setenforce 1 would return SELinux to 'Enforcing' mode. 'setsebool -P' is used to make persistent changes to SELinux booleans, enforce 0 is invalid syntax, and setenforce enforcing uses incorrect terminology. The term 'Disabled' does not apply to runtime changes and is only set in SELinux config files which requires a reboot."
    ),
    (
        "A system administrator is tasked with allowing incoming connections to a web server hosted on Linux. The server needs to accept traffic on port 443. How should the administrator configure UFW to achieve this?",
        [
            "ufw allow 443/udp",
            "ufw deny 443/tcp",
            "ufw allow 443/tcp",
            "ufw allow 80/tcp"
        ],
        2,
        "Security",
        "The correct answer is ufw allow 443/tcp because it allows incoming TCP traffic on port 443, which is the standard port for HTTPS traffic. The answer ufw allow 80/tcp is incorrect as it would allow traffic on port 80, which is the standard for HTTP, not HTTPS. The answer ufw deny 443/tcp is incorrect because it explicitly blocks traffic on port 443 rather than allowing it. Lastly, ufw allow 443/udp is incorrect as it allows UDP traffic on port 443, which is not typically used for web traffic as HTTPS uses the TCP protocol."
    ),
    (
        "A security administrator is hardening a Linux server that should only allow encrypted web traffic over HTTPS. Which of the following firewall-cmd commands should the administrator execute to block unencrypted HTTP traffic on the standard port?",
        [
            "sudo firewall-cmd --permanent --add-service=http",
            "sudo firewall-cmd --permanent --remove-service=http",
            "sudo firewall-cmd --permanent --add-port=80/tcp",
            "sudo firewall-cmd --permanent --list-services"
        ],
        1,
        "Security",
        "The command sudo firewall-cmd --permanent --remove-service=http is correct because it permanently removes the rule allowing HTTP service (which operates by default on port 80) from the firewall configuration using firewall-cmd, the tool for managing firewalld, a firewall service daemon that provides a dynamic firewall management tool with support for network/firewall zones. Removing the HTTP service effectively blocks unencrypted web traffic. The --permanent flag ensures that the change persists across system reboots. Other options either open ports, set up rules for a different service, or list services, hence they do not achieve the task of blocking HTTP traffic."
    ),
    (
        "As a systems administrator, you need to grant a user named 'techuser' the ability to run all commands as any user on a specific Linux server. Which of the following entries should you add to the sudoers file using the 'visudo' command to meet this requirement?",
        [
            "techuser ANY=(ALL:ALL) NOPASSWD: ALL",
            "techuser ALL=(ALL:ALL) ALL",
            "ALL techuser=(ALL:ALL) ALL",
            "techuser ALL=(ALL) ALL"
        ],
        1,
        "Security",
        "The correct entry is 'techuser ALL=(ALL:ALL) ALL' which grants the user 'techuser' the ability to run any command as any user on all hosts. The 'ALL=(ALL:ALL)' portion indicates that from any host (the first 'ALL'), 'techuser' can execute commands as any user (the second 'ALL') and as any group (after the colon). The final 'ALL' specifies that any command can be executed. This entry provides the specific privileges required without providing unnecessary access, adhering to the principle of least privilege. The incorrect answers either do not provide the required privileges, have syntax errors, or grant privileges that are too broad, which could pose a security risk."
    ),
    (
        "The command faillock is used to impose restrictions on users after repeated unsuccessful login attempts.",
        [
            "True",
            "False"
        ],
        0,
        "Security",
        "The answer is correct because faillock is indeed a utility that tracks the number of failed login attempts by a user. When a predefined threshold of consecutive unsuccessful attempts is surpassed, faillock can trigger an account lock, preventing further attempts for a specified duration of time. This is a security measure to protect against brute-force attacks. It is important to understand tools like faillock to secure Linux systems effectively against unauthorized access."
    ),
    (
        "A Linux administrator is configuring a system to make sure that any user attempting to access a certain service should present two different forms of identification. Which of the following authentication methods should the administrator configure?",
        [
            "Pluggable authentication modules (PAM)",
            "System Security Services Daemon (SSSD)",
            "Multifactor authentication (MFA)",
            "Tokens"
        ],
        2,
        "Security",
        "Multifactor authentication (MFA) requires users to provide two or more verification factors to gain access to a resource such as applications, online accounts, or VPNs, making it significantly more secure than single-factor authentication methods. Tokens and Pluggable Authentication Modules (PAM) are forms of single-factor authentication methods, whereas System Security Services Daemon (SSSD) is an authentication broker but does not inherently indicate a requirement for multiple forms of identification."
    ),
    (
        "An administrator is attempting to run a graphical network configuration tool with elevated privileges on a desktop Linux system that uses PolicyKit. The administrator needs to ensure that the proper policy rules are respected, and that any authorization prompts are presented graphically. Which command should the administrator use to execute the network configuration tool?",
        [
            "pexec network-configuration-tool",
            "pkexec network-configuration-tool",
            "polkit network-configuration-tool",
            "sudo network-configuration-tool"
        ],
        1,
        "Security",
        "The correct answer is 'pkexec network-configuration-tool', as pkexec allows an authorized user to execute programs with the security privileges of another user (normally the superuser) by respecting policy definitions. Unlike sudo, pkexec will show a graphical authentication dialog if the session indicates it's graphical; sudo does not provide this and is traditionally used in a terminal. polkit is not a command; it's the toolkit to which pkexec belongs. The pexec command does not exist, and sudo will not provide a graphical dialog."
    ),
    (
        "A system administrator has been instructed to update the unique numeric identifier assigned to the 'developers' group to meet the new organizational policy requiring all development teams to have identifiers above 4999. Which of the following commands will BEST accomplish this?",
        [
            "usermod -g 5000 developers",
            "Manually change the numeric identifier in the /etc/group file next to 'developers'",
            "groupmod -n developers 5000",
            "groupmod -g 5000 developers"
        ],
        3,
        "Security",
        "The correct command is groupmod -g 5000 developers because it directly and succinctly satisfies the task of updating the unique numeric identifier for the group. The -g option specifies the new identifier to be assigned to the group. The incorrect commands either target user account management (usermod), incorrectly use options that are not associated with updating the numeric identifier (-n), or suggest a method that is not recommended due to potential risks (edit the /etc/group file)."
    ),
    (
        "When SELinux is configured with the 'minimum' policy, it provides the same level of confinement for all processes as the 'targeted' policy does.",
        [
            "True",
            "False"
        ],
        1,
        "Security",
        "This statement is false. The 'minimum' policy type in SELinux is less restrictive than the 'targeted' policy. While 'targeted' confines many services and daemons on the system, the 'minimum' policy applies mandatory access controls to a lesser extent, providing confinement only to selected high-risk daemons and leaving other parts of the system unconfined. This means that while the 'minimum' policy does offer some level of security, it does not confine processes to the same extent as the 'targeted' policy does."
    ),
    (
        "What characteristic distinguishes a stateful firewall from its stateless counterpart in the context of network traffic?",
        [
            "Monitors and maintains the state of active connections",
            "Operates at a higher performance level",
            "Filters traffic solely based on static rules",
            "Creates dynamic rules for each new connection"
        ],
        0,
        "Security",
        "A stateful firewall has the capability to monitor the entire state of active connections, and thus can make decisions based on the context of the traffic (such as the state of the connection), rather than relying solely on predetermined rules. This allows it to permit or deny traffic based on the history of the connection, which is not something that stateless firewalls can do. Stateless firewalls can only permit or deny traffic based on static rules and do not have the ability to retain connection state information. Dynamic rule creation is not a feature directly associated with being stateful; while a stateful firewall could potentially create rules dynamically, it's the state tracking that defines it. Nor do performance considerations determine whether a firewall is stateful or stateless."
    ),
    (
        "A system administrator is setting up a new web server that requires encrypted data transfer. Which of the following would be the best to implement on the server to enable HTTPS communication?",
        [
            "A self-signed certificate",
            "A wildcard certificate",
            "An SSL/TLS certificate",
            "A digital signature"
        ],
        2,
        "Security",
        "A Secure Sockets Layer (SSL)/Transport Layer Security (TLS) certificate is required to establish a secure connection between a web server and a client using the HTTPS protocol. This certificate ensures that the data transferred is encrypted and the server's authenticity is validated by a Certificate Authority (CA). A self-signed certificate provides encryption but does not offer third-party validation of the server's identity and can cause trust issues with clients' browsers. A digital signature is used to verify that data has not been altered during transfer but does not by itself enable encrypted communications. A wildcard certificate is used to secure multiple subdomains but still requires the SSL/TLS protocol to function for secure communications."
    ),
    (
        "Setting SELinux to 'Enforcing' state guarantees that any action that is not explicitly permitted by the policy will be blocked and logged.",
        [
            "False",
            "True"
        ],
        1,
        "Security",
        "The correct answer is true. When SELinux is set to 'Enforcing' mode, the security policy is enforced and any actions not explicitly allowed by the policy are denied and recorded in the audit log. Setting SELinux to 'Permissive' would only log the actions without denying them, while 'Disabled' turns off SELinux enforcement and logging altogether."
    ),
    (
        "A new key pair has been created to facilitate secure logins without the use of passwords to a server. Which action should be taken next to correctly and securely deploy the key for authentication?",
        [
            "Use ssh-copy-id to upload the user's public key to the server's list of authorized keys.",
            "Transfer the private key to the server to allow direct recognition during login attempts.",
            "Manually insert the public key data within a configuration file on the server.",
            "Reboot the server to automatically detect and authorize the new key pair for use."
        ],
        0,
        "Security",
        "To deploy the key and enable secure logins without passwords, the public key must be added to the ~/.ssh/authorized_keys file on the server. The ssh-copy-id command automates this process, ensuring the correct permissions are set and reducing the risk of manual errors. It only requires the username and hostname of the server, making the process efficient and secure. The other options are incorrect because they either expose the private key, are unnecessary (restarting the SSH service), or do not follow best practices for securely copying the public key to the server."
    ),
    (
        "While reviewing the security configurations of a web server, you need to implement a certificate that will secure multiple subdomains under a single domain name. Which type of certificate will provide the most efficient and secure solution?",
        [
            "Public key",
            "Wildcard certificate",
            "Self-signed certificate",
            "Digital signature"
        ],
        1,
        "Security",
        "A wildcard certificate is used to secure multiple subdomains of a single domain. This certificate will contain an asterisk (*) in the domain name field, indicating that it can be used for various subdomains. This is the best choice as it saves time and effort when managing certificates for a domain with many subdomains. A self-signed certificate is not signed by a Certificate Authority (CA) and may cause trust issues with clients. A digital signature is a method to ensure the integrity and authenticity of a message but is not specifically used for securing subdomains. A public key is used as part of asymmetric encryption, but on its own, it's not a certificate type and doesn't demonstrate the function described in the question."
    ),
    (
        "In the context of Security-Enhanced Linux (SELinux), what term is used to describe the metadata applied to files and processes that defines the security policy aspects such as type, role, user, and level?",
        [
            "Descriptor",
            "Tag",
            "Label",
            "Policy identifier"
        ],
        2,
        "Security",
        "In SELinux, the term label refers to the metadata assigned to files and processes, which is essential for the SELinux policy to make decisions regarding the permissions and access controls. Labels consist of a type, role, user, and level, which SELinux uses to enforce its security policy. Knowing the concept of labels is crucial for system administrators to effectively manage security on a Linux system."
    ),
    (
        "When reviewing file security configurations, a Linux administrator needs to determine if any files in a directory are set with the 'immutable' attribute to prevent alterations. Which command should the administrator use and what flag should they be looking for in the output?",
        [
            "Use the lsattr -l command and look for a detailed list of attributes",
            "Use the lsattr command and look for files with the 'i' flag",
            "Use the lsattr -a command and search for files with the 'a' flag",
            "Use the chattr command to check for the 'i' attribute"
        ],
        1,
        "Security",
        "The lsattr command is used to list the attributes of files. When looking for immutable files, the administrator should scan for the 'i' attribute in the command output. This attribute indicates that a file cannot be modified, deleted, or renamed. No links to it can be created and no data can be written to the file. The -a option is not related to attribute flags and -l does not provide a more detailed output in the context of lsattr. The chattr command is used for changing attributes, not listing them."
    ),
    (
        "Using the groupadd command with the -r option creates a system group.",
        [
            "True",
            "False"
        ],
        0,
        "Security",
        "The -r option with the groupadd command is used for creating a system group. A system group is typically used for running system services and system users; it is not intended for login users. Therefore, it's important for administrators to understand and use this option appropriately in the context of system security and user management."
    ),
    (
        "An administrator needs to enable a fellow technician to access a remote Linux server for system management. Which of the following configurations will BEST ensure that the technician can connect securely without password authentication?",
        [
            "Instruct the technician to use ssh-add followed by the server's IP to access the server.",
            "Use ssh-keygen to create a key pair and ssh-copy-id to copy the public key to the server.",
            "Modify the ~/.ssh/config file on the technician's machine to include the server's information.",
            "Provide the technician with the server password to use with SSH."
        ],
        1,
        "Security",
        "Using ssh-keygen to generate a key pair and then utilizing ssh-copy-id to deploy the public key to the server's ~/.ssh/authorized_keys file for the technician's account provides a secure, passwordless authentication method that utilizes SSH keys. The private key remains with the technician, who will use it for authentication. This is considered a best practice for remote access as it provides strong encryption and avoids the risks associated with password-based logins. Option B is incorrect because using passwords for SSH access is less secure than key-based authentication. Option C is incorrect because ssh-add adds private keys to the SSH agent but doesn't configure passwordless access to remote servers. Option D is incorrect because modifying ~/.ssh/config can define client-side connection parameters but does not facilitate passwordless login by itself."
    ),
    (
        "During a routine security audit, Bob discovers that SSH keys were not added to the SSH agent with an expiration time, potentially leaving them loaded indefinitely. For improved security, he decides that keys should be automatically removed from the agent after a certain period of inactivity. What option should Bob include with ssh-add to ensure that a key expires after 1 hour of inactivity?",
        [
            "ssh-add -X 3600",
            "ssh-add -T 3600",
            "ssh-add -x 3600",
            "ssh-add -t 3600"
        ],
        3,
        "Security",
        "The command ssh-add -t 3600 adds the private key to the SSH agent with an expiration time of 3600 seconds, which is equivalent to 1 hour. After this time, if not used, the key will be automatically removed from the agent, enhancing security by limiting the timeframe the key is available without user interaction. The options -x, -X, and -T do not serve the purpose described, either because they do not exist or -X unlocks the agent and -T is used for testing purposes in ssh itself, not ssh-add."
    ),
    (
        "You have been tasked with deleting a user account on a Linux server, and you must ensure that the user's home directory and mail spool is also removed. Which command should you execute?",
        [
            "userdel --remove-all-files username",
            "usermod --delete username",
            "deluser --remove username",
            "userdel -r username"
        ],
        3,
        "Security",
        "The correct command is userdel -r username. The -r option removes the user's home directory and mail spool along with the user account itself. Without the -r option, the account will be deleted, but the home directory and mail spool would remain on the system. The usermod command is for modifying an existing user account, not deleting it. The deluser command does not exist by default in most Linux distributions, and userdel --remove-all-files is incorrect because the --remove-all-files option is not a valid option for the userdel command."
    ),
    (
        "A system administrator needs to verify the active firewall rules on a Linux server to ensure compliance with the company's security policies. Which of the following commands provides the most comprehensive output of the currently active firewall rules?",
        [
            "iptables -S",
            "iptables --state",
            "iptables -L -v -n",
            "iptables -L"
        ],
        2,
        "Security",
        "The command iptables -L -v -n is the correct answer as it displays all the active rules in all chains with verbose output and does not resolve hostnames (due to the -n flag), which can be helpful in speeding up the process. It is more comprehensive compared to just listing the rules without additional verbosity, the numeric option preserves exact network addresses and port numbers, and the combination of these flags gives the admin a detailed perspective on the rules. iptables -S simply lists the rules in a format that can be reused as input to the firewall, and the --state flag is not a valid iptables option, leading to a command error. firewall-cmd --list-all only works with systems using firewalld and is therefore not guaranteed to work on all Linux distributions."
    ),
    (
        "Which file should be reviewed to understand the historical logins on a Linux system, including the source IP addresses of the connecting clients?",
        [
            "/var/log/btmp",
            "/var/log/wtmp",
            "/var/log/utmp",
            "/var/log/secure"
        ],
        1,
        "Security",
        "The /var/log/wtmp file holds records of logins and logouts. Using the last command can display the contents of this file, providing information about user logins, their source IP addresses, and logout times, which is why it's essential for understanding historical logins. Other files like /var/log/btmp and /var/log/utmp serve different purposes; /var/log/btmp keeps track of failed login attempts, and /var/log/utmp contains information about current logins."
    ),
    (
        "A Linux system administrator needs to modify the firewall settings to allow access to a web server service that has been recently configured to listen on a non-standard port, 8443 for secure traffic. Simultaneously, they must ensure that other services remain unaffected by this firewall change. To apply this change immediately and make it permanent for subsequent system reboots, which of the following commands should the administrator execute?",
        [
            "firewall-cmd --permanent --zone=public --add-port=443/tcp",
            "iptables -I INPUT -p tcp --dport 8443 -j ACCEPT && service iptables save",
            "firewall-cmd --permanent --add-service=https",
            "firewall-cmd --permanent --add-port=8443/tcp && firewall-cmd --reload"
        ],
        3,
        "Security",
        "The correct command is firewall-cmd --permanent --add-port=8443/tcp && firewall-cmd --reload. This command first makes a permanent change to the firewall rules to allow traffic on port 8443, which is where the web server is now listening for secure traffic, and then reloads the firewall to apply the changes immediately without affecting other services or requiring a system reboot. firewall-cmd --permanent --add-service=https is not correct in this context because the web server is using a non-standard port, not the default port for HTTPS (443). Similarly, firewall-cmd --permanent --zone=public --add-port=443/tcp is incorrect as it opens the default HTTPS port, not the non-standard one in use. iptables -I INPUT -p tcp --dport 8443 -j ACCEPT && service iptables save would apply the rule without making it permanent across reboots because the service iptables save command is specific to certain Linux distributions that use the service management utility and not a standard way to persist firewall rules."
    ),
    (
        "What is the primary benefit of configuring port redirection on a server?",
        [
            "It optimizes the network traffic flow to increase the bandwidth availability for the server.",
            "It enhances the DNS resolution speed for the services running on the server.",
            "It increases the server's processing speed by balancing the load across multiple CPUs.",
            "It provides a secure method to access services on a network that the client cannot connect to directly."
        ],
        3,
        "Security",
        "The primary benefit of configuring port redirection, commonly referred to as port forwarding when done through tools like SSH, is to allow secure, encrypted connections to services on networks that are not directly reachable by the client. It creates a tunnel for the network packets to move from one interface to another within the same machine or from one machine to another, enabling access to services behind a firewall or NAT without exposing them directly to the Internet."
    ),
    (
        "A system administrator is tasked with restricting access to a web server running on the default HTTP port to only the IP range 192.168.100.0/24. The server is currently using firewalld for its firewall management. Which of the following commands should the administrator use to accomplish this task?",
        [
            "firewall-cmd --permanent --new-zone=192.168.100.0/24",
            "firewall-cmd --permanent --zone=public --add-source=192.168.100.256/24",
            "firewall-cmd --permanent --zone=public --add-service=http --source=192.168.100.0/24",
            "firewall-cmd --permanent --zone=public --add-rich-rule='rule family=\"ipv4\" source address=\"192.168.100.0/24\" port protocol=\"tcp\" port=\"80\" accept'",
            "firewall-cmd --permanent --zone=public --add-service=http --add-source=192.168.100.0/24",
            "firewall-cmd --permanent --zone=public --add-source=192.168.100.0/24 --add-service=http"
        ],
        3,
        "Security",
        "The correct answer is firewall-cmd --permanent --zone=public --add-rich-rule='rule family=\"ipv4\" source address=\"192.168.100.0/24\" port protocol=\"tcp\" port=\"80\" accept'. This creates a persistent (--permanent) rule for the public zone in firewalld that uses a rich-rule to enable access on TCP port 80 for the source IP range of 192.168.100.0/24. This ensures that only devices with an IP from this range can access the HTTP service. The other options are incorrect for the following reasons: The first incorrect option attempts to add a service by name, which is not how IP-based restrictions are set. The second incorrect option adds an entire zone instead of the specific rule needed for the IP range. The last incorrect option contains an invalid subnet mask for the given IP range."
    ),
    (
        "An administrator in your organization is concerned about performance issues and believes that Security-Enhanced Linux (SELinux) may be impacting the system's performance negatively. The admin has decided to completely disable SELinux to test this theory. After changing the SELinux mode to 'disabled' and rebooting the system, what long-term security implications should the administrator be made aware of?",
        [
            "SELinux can be re-enabled without rebooting, thus no long-term security implications exist.",
            "The system performance will improve without any negative security implications since file permissions and ACLs continue to protect the system.",
            "SELinux will automatically re-enable after an update, minimizing long-term security risks.",
            "The system will rely solely on traditional Unix/Linux permissions, leading to potential security vulnerabilities."
        ],
        3,
        "Security",
        "Disabling SELinux entirely can expose the system to vulnerabilities and security threats that SELinux would ordinarily mitigate. SELinux provides a layer of security by enforcing access control policies that are not managed by traditional Unix/Linux permissions. When disabled, these policies do not apply, leaving the system susceptible to unauthorized access and potential exploits. The administrator should be aware of the increased risk and consider alternative methods for diagnosing performance issues, such as permissive mode, without compromising on security."
    ),
    (
        "As a system administrator, you need to remove a user's account from a Linux system. The user's account, 'johndoe', must be deleted along with the user's home directory and mail spool. Which command should you use to accomplish this task?",
        [
            "userdel johndoe",
            "deluser johndoe",
            "userdel -r johndoe",
            "removeuser --files johndoe"
        ],
        2,
        "Security",
        "The command userdel -r johndoe will remove the user 'johndoe' and delete the user's home directory as well as the mail spool. The -r option stands for 'remove' and is used specifically for this purpose. Simply using userdel johndoe would not remove the home directory or mail spool. deluser and removeuser are not standard Linux commands. It is essential to use the correct options and command to ensure proper cleanup of user accounts."
    ),
    (
        "An administrator has discovered that a newly deployed web application cannot write to the /var/www/html/reports directory on a SELinux-enabled system, despite the directory having write permissions set for the proper user and group. Which of the following commands should the administrator use to diagnose the issue related to SELinux context permissions?",
        [
            "sestatus",
            "ls -Z /var/www/html/reports",
            "getsebool -a",
            "ps auxZ"
        ],
        1,
        "Security",
        "The correct answer is ls -Z /var/www/html/reports. The -Z option displays the SELinux context for files, which includes user, role, type, and level information. This information is crucial in diagnosing why the web application cannot write to the directory despite seemingly appropriate Unix file permissions. If the SELinux context is incorrect, even with the right Unix permissions, access will be denied based on SELinux policy rules. The other options are incorrect because getsebool -a lists all of the SELinux boolean values, which are not specific to file contexts. ps auxZ shows the SELinux context of running processes, not files. sestatus provides an overview of the current SELinux operational state; it does not provide information on specific file contexts."
    ),
    (
        "An administrator is tasked with running a remote session for a graphically-intensive application on a Linux server, where the display output is needed on a local machine. Given security considerations and the necessity for GUI rendering, which SSH command should the administrator use to initiate this remote session securely?",
        [
            "ssh -C user@hostname",
            "ssh -X user@hostname",
            "ssh -x user@hostname",
            "ssh -Y user@hostname"
        ],
        1,
        "Security",
        "The correct answer is ssh -X user@hostname as it enables X11 forwarding securely, allowing the graphical output of the remote application to be displayed on the local machine. The -Y option is less secure than -X and should be used with caution as it provides trusted X11 forwarding, which can expose the local system to possible X11 security risks. The -x option disables X11 forwarding and is incorrect. Lastly, the -C option compresses data during the session, which might be useful in low-bandwidth scenarios but does not address the requirement for X11 forwarding and GUI display. Therefore, while -C combined with -X could be used together, -C alone is not correct for the scenario described."
    ),
    (
        "A system administrator has been tasked with writing a shell script that reads a list of usernames from a text file named 'users.txt' and then checks whether each user exists on the system. The admin decides to use a loop along with a built-in command to verify this. Which command should be used within the loop to check the presence of a user account in the system environment?",
        [
            "id",
            "whoami",
            "hostname",
            "date",
            "pwd"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The 'id' command is used to obtain user and group identity information, which makes it an appropriate tool for checking whether a user account exists. Specifically, the id command returns the user and group information for the specified username, and if the user does not exist, it will produce an error message. The other commands listed do not serve the purpose of checking for the existence of a user account. For instance, 'pwd' displays the current directory, 'whoami' shows the current user, 'date' outputs the current date and time, and 'hostname' reveals the system's host name."
    ),
    (
        "A system administrator needs to write a shell script that will output 'Large file detected' if a specified file size exceeds 1024 kilobytes. Which of the following shell script code blocks is the BEST to accomplish this?",
        [
            "if [ $(stat -c%s \"file.txt\") -gt 1048576 ]; then echo 'Large file detected'; fi",
            "if [ $(stat -c%s \"file.txt\") / 1024 -gt 1024 ]; then echo 'Large file detected'; fi",
            "if [ $(stat -c%s \"file.txt\") -gt 1024 ]; then echo 'Large file detected'; fi",
            "if [[ $(stat -c%s \"file.txt\") -gt 1024 ]]; then echo 'Large file detected'; fi"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct code block uses the -gt operator to check if the file size is greater than 1024 kilobytes. Remember that stat -c%s filename retrieves the file size in bytes, so you must divide by 1024 to convert bytes to kilobytes. The if statement then evaluates this condition and prints 'Large file detected' if the condition is true. Other comparisons or the lack of size conversion can result in incorrect behavior or syntax errors."
    ),
    (
        "A colleague informs you that a new feature has been added to a project, and it's available on the 'feature-login' branch for preview before it's merged into the main codebase. You are currently on the 'main' branch and have made some local modifications that you don't want to commit yet. How would you switch to the 'feature-login' branch to review the new additions without losing your uncommitted changes?",
        [
            "git merge feature-login into your main branch",
            "git commit -m 'Temp commit' and then use git checkout feature-login",
            "git stash your changes and then use git checkout feature-login",
            "git checkout feature-login --force"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The correct answer is git stash your changes and then use git checkout feature-login. This is because you can save your uncommitted changes with git stash, which acts like a stack where you can push changes to be temporarily stored, and later you can pop them off. After stashing your changes, you can safely change branches using git checkout. Using the other commands might either lead to a loss of local changes or are not correct commands for handling a change in branches."
    ),
    (
        "Is it possible to create a never-ending loop using the 'while' construct in a shell script without explicitly including a terminating condition within the loop?",
        [
            "True",
            "False"
        ],
        0,
        "Scripting, Containers, and Automation",
        "Using the 'while' loop construct, one can create an infinite loop by providing a condition that always evaluates to true. A common practice to create such a loop is to use while true; do ...; done. This loop will continue indefinitely because 'true' is a command that always exits with a status of 0, which the 'while' construct interprets as a success or 'true' condition."
    ),
    (
        "You have been working on a new feature in a separate branch called 'feature-xyz' of your project's repository. After completing the work on your feature, you want to integrate it into the main codebase. What is the next step to request the integration of your changes into the 'main' branch, ensuring that your peers can review it before it is merged?",
        [
            "Commit the changes in your 'feature-xyz' branch and notify your team that the feature is complete.",
            "Push the changes from your 'feature-xyz' branch directly to the 'main' branch without a pull request.",
            "Tag the latest commit in your 'feature-xyz' branch and ask your team to review the tag.",
            "Create a pull request in the repository, comparing your 'feature-xyz' branch to the 'main' branch."
        ],
        3,
        "Scripting, Containers, and Automation",
        "The correct answer is to create a pull request. A pull request is initiated by the contributor to propose the changes made in their branch to be pulled into another branch, typically the main repository branch. It provides an opportunity for peer review and discussion before the changes are merged. Pushing changes directly without a pull request bypasses the review process, while committing changes only affects the local repository and does not notify team members of the proposed changes. Tagging the latest commit creates a reference to a specific point in the repository history, but it does not facilitate the merging and review process like a pull request does."
    ),
    (
        "Which command utility can be used to search for and replace patterns within a file, and it requires no additional scripting or programming?",
        [
            "grep",
            "sed",
            "awk",
            "tail"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The sed utility, short for stream editor, is designed to filter and transform text. It is used on the command line and within scripts for pattern matching and substitution, making it an ideal tool for search and replace operations within files without the need for writing complex scripts or programs. The other choices do not match the specific utility that directly performs search and replace operations on a file."
    ),
    (
        "What would be the result of the following command: echo 'The quick brown fox' | sed 's/quick/slow/'?",
        [
            "The quick brown fox",
            "Theslowbrownfox",
            "The slow brown fox",
            "The quick slow brown fox"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The sed command is used to perform basic text transformations. In the example provided, 's/quick/slow/' is a substitute command that tells sed to replace the first occurrence of the pattern 'quick' with the replacement 'slow'. The result is the output of the initial string with the word 'quick' replaced by 'slow'."
    ),
    (
        "When a container is set to use the host networking mode, it will share the networking namespace with the host machine allowing the container to listen on the host's IP address.",
        [
            "True",
            "False"
        ],
        0,
        "Scripting, Containers, and Automation",
        "Using the host networking mode means that the container shares the host's networking namespace. This allows the container to bind ports directly to the host's IP address. It's crucial for certain applications that require direct visibility from external networks without network address translation (NAT). Other answers might seem correct, but they do not accurately describe the behavior of containers in host network mode."
    ),
    (
        "What command would you use to display all the currently running container instances in the system?",
        [
            "docker ps",
            "docker inspect",
            "docker list",
            "docker running"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The docker ps command is used to list all running containers. The option -a or --all can be added to show all containers, not just those that are running. The commands docker list and docker running are not valid Docker commands. While docker inspect provides detailed information about one or more containers, it does not list all running containers."
    ),
    (
        "A system administrator needs to find all lines within '/var/log/syslog' that contain either 'error' or 'failed'. The administrator decides to use a command that supports regular expressions to accomplish this task. Which command will correctly output the desired lines?",
        [
            "egrep \"'error'|'failed'\" /var/log/syslog",
            "egrep \"error&&failed\" /var/log/syslog",
            "egrep \"error|failed\" /var/log/syslog",
            "egrep \"/error|failed/\" /var/log/syslog"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The command 'egrep \"error|failed\" /var/log/syslog' uses regular expressions to search for lines that match either 'error' or 'failed'. Here, the pipe '|' character serves as a logical OR operator in the regular expression. The use of double quotes allows the pipe character to be interpreted correctly by the shell as part of the egrep command's pattern argument."
    ),
    (
        "What is the primary function of an Ansible playbook?",
        [
            "To compile and execute Ansible modules on remote nodes",
            "To create a visual dashboard and reporting tool for Ansible",
            "To store sensitive variables and data for Ansible roles",
            "To define and run a series of tasks to configure managed nodes"
        ],
        3,
        "Scripting, Containers, and Automation",
        "An Ansible playbook is a YAML file that defines work for a configuration management system and is used for defining and running multi-machine deployment sequences. It provides a series of tasks to automate the configuration of managed nodes. The correct answer is 'To define and run a series of tasks to configure managed nodes' because playbooks are Ansible's primary method for automation execution. The incorrect answers are closely related terms or Ansible components but do not correctly describe the function of an Ansible playbook."
    ),
    (
        "An organization is looking to improve its software development lifecycle by automatically building, testing, and deploying applications following code commits. Which of the following would BEST implement this requirement?",
        [
            "Configuring a Git hook to trigger deployment scripts",
            "Automating deployments using custom shell scripts",
            "Setting up a Jenkins pipeline",
            "Using cron jobs for scheduled deployments"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The correct answer is 'Setting up a Jenkins pipeline.' Jenkins is a popular automation server that is widely used for implementing continuous integration and continuous deployment pipelines. By setting up a Jenkins pipeline, developers can automate the process of building, testing, and deploying their code whenever a commit is made. While 'Configuring a Git hook' can trigger actions upon code changes, it lacks the robust pipeline features Jenkins offers. 'Using cron jobs for scheduled deployments' is not the best solution as it doesn't provide immediate deployments following code commits. 'Automating with shell scripts' can be part of a CI/CD pipeline but on its own is not sufficient for establishing a full pipeline that encompasses building, testing, and deploying."
    ),
    (
        "What is the role of the pipe character in a Linux command line operation?",
        [
            "To append the output of a command to the end of a file",
            "To redirect the output of one command to the input of another command",
            "To execute a command in the background",
            "To overwrite the content of a file with the output of a command"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The pipe character (|) is used to take the standard output of the command on the left, and feeds it as standard input to the command on the right. It is a crucial tool in shell scripting and command line operations to chain commands and construct more complex procedures by handling the flow of data from one utility to another."
    ),
    (
        "Using the command echo Number_{1..5} in a shell script will output Number_1 Number_2 Number_3 Number_4 Number_5.",
        [
            "This statement is inaccurate",
            "This statement is accurate"
        ],
        1,
        "Scripting, Containers, and Automation",
        "Brace expansions are used to generate sets of strings or sequences. The command echo Number_{1..5} correctly uses brace expansion to generate a sequence from 1 to 5, each prefixed with 'Number_'. The spaces in the output are due to the echo command, which outputs its arguments separated by spaces by default."
    ),
    (
        "A system administrator is deploying a multi-container application on a single Docker host. The application includes a web server container that needs to communicate with a database container. Both containers should be isolated from other network traffic on the Docker host. Which Docker network driver should the administrator use to fulfill these requirements?",
        [
            "Host",
            "Overlay",
            "Bridge",
            "Default bridge"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The correct answer is 'Bridge' because the bridge network driver provides a private network internal to the host machine, allowing containers connected to the same bridge network to communicate with each other while isolating them from other containers not connected to the bridge. The default bridge network does not provide isolation between containers, which is why it is necessary to create a user-defined bridge network for this scenario. The 'Overlay' network driver is used for networking between multiple Docker hosts, which is not the requirement here. The 'Host' mode removes network isolation and uses the host's networking directly, which does not meet the requirement for network isolation. 'Host' mode also would not use NAT because the containers would share the network with the host. Therefore, the 'Host' network driver is not suitable for this scenario."
    ),
    (
        "During script execution, an administrator needs to ensure a command is executed only when a certain variable holds the exact word 'config'. Which syntax will correctly verify this within an if statement?",
        [
            "[[ $VARNAME != 'config' ]]",
            "[[ $VARNAME -eq 'config' ]]",
            "[[ $VARNAME == 'config' ]]",
            "[ $VARNAME == 'config' ]"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The conditional test using == is the correct answer because in shell scripting, this operator is used to compare two strings for equality. The single [ and double [[ are both used for the test construct, but the double bracket [[ is a newer Bash construct that offers additional functionality, such as regex matching and doesn't require quotes around the variable. The other answers are incorrect because -eq is used for arithmetic comparison, and using != would check for inequality, which is not the desired operation."
    ),
    (
        "A system administrator is creating a shell script that will automate the configuration of a new service on a Linux server. The script needs to append a multi-line configuration block to a file named /etc/service.conf. The administrator decides to use a here document within the script to achieve this. Which of the following snippets will correctly append the configuration block to the end of the file using a here document?",
        [
            "cat > /etc/service.conf <<EOF\nSetting1=Value\nSetting2=Value\nEOF",
            "cat <<EOF > /etc/service.conf\nSetting1=Value\nSetting2=Value\nEOF",
            "echo <<EOF >> /etc/service.conf\nSetting1=Value\nSetting2=Value\nEOF",
            "cat <<EOF >> /etc/service.conf\nSetting1=Value\nSetting2=Value\nEOF"
        ],
        3,
        "Scripting, Containers, and Automation",
        "A here document allows the input of multi-line text strings in shell scripts. It starts with the << operator followed by a delimiter that indicates the end of the here document. The correct answer provides the correct syntax with <<EOF as the starting delimiter and EOF on a line by itself to signify the end. The >> operator is used to append to /etc/service.conf file without overwriting its current contents. The incorrect answers either use wrong syntax, which will not work as expected, or will not append the text correctly."
    ),
    (
        "In a Kubernetes environment, you are tasked with configuring a container to manage authentication and monitoring of traffic between your cluster's microservices and a third-party API. This container should intercept all outbound requests to the API. Which container pattern would you implement to BEST fulfill this requirement?",
        [
            "Adapter container",
            "Proxy container",
            "Ambassador container",
            "Network bridge container"
        ],
        2,
        "Scripting, Containers, and Automation",
        "To manage outbound communication with a third-party API, the Ambassador container pattern is the most suitable choice. It acts as an outbound proxy that enables microservices to use an external service as if it was part of the local network, handling tasks such as authentication, monitoring, and circuit breaking. The Adapter container modifies or adapts the output of a container to a standardized format, but it is not primarily focused on outbound traffic management. The Proxy container is an oversimplified term that does not capture the specificity of the Ambassador's responsibilities. Lastly, while a Network bridge container is related to networking, it mainly refers to a container that builds network bridges, rather than managing external API communication."
    ),
    (
        "An administrator wants to monitor disk usage by individual users on a shared system and has decided to utilize the output from the 'du' command. The command 'du -s /home/*' produces a list of directories and their sizes within the /home directory, which is then redirected to 'awk' for further processing. The administrator is interested in directories that consume more than 1GB of disk space. Which 'awk' command should the administrator use to extract and print the usernames (the directory names within /home) and their corresponding disk space usage in gigabytes, but only for those users utilizing more than 1GB?",
        [
            "du -s /home/* | awk '$1 > 1048576 { print substr($2,7) \":\" $1/1048576 \"GB\" }'",
            "du -s /home/* | awk '{ print $3 \":\" $1/1048576 \"GB\" }'",
            "du -s /home/* | awk '{ print substr($2,7) \":\" $1 \"KB\" }'",
            "du -s /home/* | awk '{ if $1 > 1048576 print substr($2,7) \":\" $1/1048576 \"GB\" }'"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct 'awk' command filters the output of 'du' by dividing the first column (size in kilobytes) by 1048576 to convert it to gigabytes and prints the size along with the username, which is inferred from the directory name after the last slash in the second column. The 'substr($2,7)' function is utilized to remove '/home/' (the first 6 characters), leaving the username. Only records with a size greater than 1GB are output.\nAs for the incorrect answers:\n    • The second answer overlooks the requirement to convert kilobytes to gigabytes before comparing to 1GB.\n    • The third answer uses incorrect syntax, merging the 'if' construct improperly.\n    • The fourth answer is incorrect because it prints all records, and it attempts to use a field '$3' that does not exist in the 'du' output."
    ),
    (
        "A systems administrator needs to investigate an issue in a Docker container that is failing to start correctly. The administrator wishes to view the output logs to diagnose the problem. Which command should the administrator run to display the last 50 lines of logs from the container named 'web-app'?",
        [
            "docker logs --tail 50 web-app",
            "docker inspect --format='{{.LogPath}}' web-app",
            "docker logs -f web-app | tail -50",
            "docker container logs web-app --last 50"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct answer is docker logs --tail 50 web-app. The --tail option with the docker logs command allows the user to view the specified number of most recent lines from the container's logs, making it an appropriate choice for checking recent activity or errors that could lead to understanding the issue with the container."
    ),
    (
        "A developer wants to deploy a web application and an accompanying database on their local development machine using Docker. Both should be deployed as separate containers but configured to communicate with each other. Which Docker feature allows the definition of this multi-container setup?",
        [
            "Cloud-init",
            "Docker Compose",
            "Docker Swarm",
            "Kubernetes Pods"
        ],
        1,
        "Scripting, Containers, and Automation",
        "Docker Compose is a tool for defining and running multi-container Docker applications. With a Compose file (usually docker-compose.yml), you can define the services, networks, and volumes that need to be created and run together. Compose setups help in maintaining consistency in environments and streamlining the deployment process. The other options, such as Kubernetes and Cloud-init, are not as applicable for single-node, local development scenarios. Compose fits perfectly here since it is designed to deal with multi-container Docker applications on a single node, as opposed to orchestrating clusters of nodes."
    ),
    (
        "A system administrator is automating the backup process for a set of user directories. They have decided to write a shell script that compresses each user's home directory into an individual archive file. Assuming all user directories are located in /home, which snippet of code will successfully create a gzip-compressed archive of each user's home directory with the filename format 'username.tar.gz'?",
        [
            "for dir in /home/*/; do tar -cf \"\\(dir\" | gzip > \"\\).tar.gz\"; done",
            "for dir in /home/; do gzip \"/home/${dir##/}\"; done",
            "for dir in /home/; do tar -czf \"/home/\\({dir}.tar.gz\" \"/home/\\)\"; done",
            "for dir in /home/; do tar -czf \"/home/${dir##/}.tar.gz\" \"$dir\"; done"
        ],
        3,
        "Scripting, Containers, and Automation",
        "The correct script uses a 'for' loop to iterate over every item in the /home directory and then applies the 'tar' command with the correct options to compress each directory into an individual gzip archive file. The '${dir##*/}' expression is used to strip the path and leave just the user's name for the archive file. Incorrect answers may have syntax errors, use incorrect commands, or incorrectly handle the directory names, resulting in failure to achieve the desired task."
    ),
    (
        "What is a Pod in the context of a Kubernetes environment?",
        [
            "A tool used to manage the lifecycle of Kubernetes containers, including their deployment and scaling operations",
            "A collection of nodes designed to host the containers within a Kubernetes cluster",
            "The smallest deployable unit in Kubernetes, which may consist of one or more containers that share storage and network, as well as specifications on how to run the containers",
            "The networking layer within Kubernetes that handles outbound traffic from containers"
        ],
        2,
        "Scripting, Containers, and Automation",
        "In Kubernetes, a Pod is the smallest deployable unit that can be created and managed. It represents a single instance of an application or process. A Pod encapsulates one or more containers, storage resources, a unique network IP, and options that govern how the container(s) should run. Pods can contain multiple containers, but they are typically co-located and co-scheduled on the same node and in the same execution environment, which allows them to share context and resources. This differentiates Pods from standalone containers, services, or deployments, which serve different roles in the Kubernetes ecosystem."
    ),
    (
        "Which command is used to display detailed information about a specific container, including its configuration and current state?",
        [
            "docker info",
            "docker status",
            "docker list",
            "docker inspect"
        ],
        3,
        "Scripting, Containers, and Automation",
        "The docker inspect command is designed to return low-level information on Docker objects. Providing a container ID or name as an argument will give a detailed report about the container, which includes its configuration and state among other data. This information is crucial for both troubleshooting and understanding the operational aspects of a Docker container. The docker status command does not exist, and while docker list and docker info are similar commands, they do not provide the level of detail that docker inspect does."
    ),
    (
        "What type of network allows containers hosted on separate physical servers to communicate with each other as if they are on the same local network?",
        [
            "NAT network",
            "Overlay network",
            "Host network",
            "Bridging network"
        ],
        1,
        "Scripting, Containers, and Automation",
        "Overlay networks provide a virtual network that sits on top of the physical network, allowing containers on different hosts to communicate with each other seamlessly. This abstraction is vital for container orchestration and scalability, as it decouples the container network from the underlying physical network infrastructure."
    ),
    (
        "The || operator in a shell script will execute the command that follows it if the command preceding it was successful.",
        [
            "This statement is false: the command following || is executed only if the preceding command fails.",
            "This statement is true: the command following || is executed only if the preceding command succeeds."
        ],
        0,
        "Scripting, Containers, and Automation",
        "The || operator in shell scripting is used as a logical OR. When used between two commands, it executes the second command only if the first command fails (exits with a non-zero status). It does not execute the second command if the first command is successful. Therefore, the correct statement is the opposite of what || actually does."
    ),
    (
        "A system administrator needs to write a shell script that prompts the user for a file name and then reads a single line from that file. The goal is to store this line in a variable for further processing. Which of the following options achieves this while making sure the script asks for the file name and reads only the first line of the provided file?",
        [
            "read -p \"Enter the file name: \" file; IFS= read -r line <<< \"$file\"",
            "read -p \"Enter the file name: \" file; IFS= read -r line <<< $(cat $file)",
            "read -p \"Enter the file name: \" file; IFS= read -r line < \"$file\"",
            "read -p \"Enter the file name: \" file; line=$(cat $file | head -n 1)"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The correct answer is 'read -p \"Enter the file name: \" file; IFS= read -r line < \"$file\"' because the '-p' option allows the script to prompt the user with a message and read input into the 'file' variable. Then, 'IFS= read -r line < \"$file\"' is used to read the first line from the file specified by the user into the variable 'line'; 'IFS=' prevents leading/trailing whitespace from being trimmed, and '-r' prevents backslashes from being interpreted as escape characters. The '< \"$file\"' syntax redirects the contents of the file into the read command. Options B and C are incorrect because they attempt to use 'cat', which is unnecessary and will not properly assign the first line to the variable 'line'. Option D is incorrect because '<<<' is not the correct way to redirect file content to 'read'."
    ),
    (
        "The command xargs can be used to apply a single command to each line of input it receives.",
        [
            "True",
            "False"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The xargs command is typically used to take output from a command that generates a list of items, one per line, and then applies another command to each item. This turns the multi-line input into arguments for the given command, effectively allowing that command to be run for each input item. For example, cat list.txt | xargs rm would attempt to run the rm command on each line listed in list.txt. Other answers are incorrect because they misinterpret the functionality of xargs or describe capabilities it does not possess."
    ),
    (
        "An administrator needs to download the latest version of an Ubuntu image for container deployment. Which of the following commands will perform this operation?",
        [
            "docker push ubuntu",
            "pull ubuntu",
            "docker pull ubuntu",
            "docker rmi ubuntu"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The command docker pull ubuntu retrieves the latest version of the Ubuntu image from the default Docker hub registry. docker pull ubuntu is the correct command because it specifies only the image name, which defaults to pulling the 'latest' tag if no other version is specified. pull ubuntu is incorrect because it is missing the docker command. docker push ubuntu is incorrect because it is using push which is for uploading images, not downloading them. docker rmi ubuntu is incorrect because rmi is used to remove images, not to pull them."
    ),
    (
        "A Linux administrator needs to read user input during the execution of a shell script to capture a username that will be used later in the script. Which built-in command should be used to fulfill this requirement most effectively?",
        [
            "Use source to read the username from a separate file.",
            "Apply grep on the /etc/passwd file to extract a list of usernames.",
            "Use echo to display a prompt and then capture the user input.",
            "Use read to prompt the user and store the input."
        ],
        3,
        "Scripting, Containers, and Automation",
        "The read command is specifically designed to accept user input during shell script execution. Using read is the most direct and efficient way to capture user input and store it in a variable for later use. Even though commands like echo and source are useful for outputting messages and evaluating files in the current shell context, they do not fulfill the purpose of reading user input."
    ),
    (
        "When configuring a Docker container's network, which option allows you to create a dedicated subnet where containers can be attached, providing isolation from other containers on the same host?",
        [
            "Host mode networking",
            "Overlay network",
            "None (network disabled)",
            "User-defined bridge network",
            "Default bridge network",
            "MACVLAN network"
        ],
        3,
        "Scripting, Containers, and Automation",
        "A user-defined bridge network is correct because it enables users to create isolated networking environments. Containers attached to a user-defined bridge network can communicate via their internal IPs, and this network is isolated from other containers unless explicitly connected. The default bridge is less secure since all containers are able to communicate by default. A MACVLAN network allows containers to have their own MAC address providing the appearance of physical devices which is different from the network isolation described. An Overlay network is used for communication between containers on different Docker daemons, which was not the scenario described. Host mode directly attaches the container to the host's network, with no isolation. None disables all networking for a container, however, it doesn't allow communication within a subnet."
    ),
    (
        "What type of loop would be most appropriate for reading lines from a text file until reaching the end of the file in a shell script?",
        [
            "while",
            "for",
            "until",
            "switch/case"
        ],
        0,
        "Scripting, Containers, and Automation",
        "A while loop is appropriate for reading lines from a text file until the end because it allows for continuous looping as long as the specified condition is true. In the context of reading from a file, the loop will continue until it reaches the end of the file, which is a common task in shell scripting when processing or analyzing text files line by line."
    ),
    (
        "A system administrator is tasked with setting up several virtual machines to join an existing cloud infrastructure. They need to ensure that each virtual machine is configured automatically upon boot with a specific hostname pattern, user credentials, and custom network configuration without manual intervention. Which technology would be the MOST effective for achieving this goal during the initial boot process?",
        [
            "Systemd service units",
            "Cloud-init",
            "Ansible",
            "Puppet"
        ],
        1,
        "Scripting, Containers, and Automation",
        "Cloud-init is a widely used tool for the early initialization of cloud instances. It supports various cloud platforms and allows for the automatic configuration of the environment based on user-provided initialization metadata, such as setting hostnames, usernames, and network configurations through user-data scripts or configuration files. This makes it excellent for quickly bootstrapping new virtual machines with the necessary custom settings. Other tools like Puppet and Ansible are also used for automation and configuration management, but they are typically used post-boot for ongoing management, rather than during the initial boot process."
    ),
    (
        "A system administrator is working on a container deployment and requires connectivity from the containers to the external network without allocating a public IP address for each container. Which of the following solutions will BEST facilitate this requirement?",
        [
            "Use layer 2 bridging in conjunction with network address translation.",
            "Implement network address translation at the host level.",
            "Apply VLAN tagging to the container network interfaces.",
            "Configure direct bridge networking for each container."
        ],
        1,
        "Scripting, Containers, and Automation",
        "Applying NAT at the host level will allow containers to share the host's IP address to access the external network. The traffic from the containers will appear to originate from the host's IP, thus not requiring a public IP for each container. Direct bridge networking would not solve the problem of public IP allocation for each container, Layer 2 bridging with NAT is not a standard approach for container networking, and VLAN tagging is typically used to separate LAN segments and is not directly related to the NAT process."
    ),
    (
        "Which command would you use to create a new container from an existing image and start it immediately?",
        [
            "docker create",
            "docker run",
            "docker build",
            "docker commit"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The command docker run is used to create a new container instance from a specified image and start the container immediately. If the image is not available locally, it will be pulled from the container registry. docker create only creates the container without starting it, which requires a separate docker start command to run the container. docker build is used to create an image from a Dockerfile, not to start a container. docker commit creates a new image from a container's changes."
    ),
    (
        "A Linux administrator is deploying an application on Kubernetes and needs to ensure that two containers (a web server and a caching service) share the same network and storage resources. Which of the following is the BEST option to achieve this requirement?",
        [
            "Create a new Kubernetes service to facilitate communication between two standalone pods",
            "Launch separate pods for each container and use a service to link them",
            "Use a DaemonSet to ensure that both containers run on each node in the cluster",
            "Deploy both containers within a single pod"
        ],
        3,
        "Scripting, Containers, and Automation",
        "The correct answer is 'Deploy both containers within a single pod'. In Kubernetes, a Pod represents one or more containers that should be run together. Containers within the same pod share the same IP address, network, and storage resources, which means they can communicate with each other using 'localhost' and can access shared volumes. This is the exact scenario described, making it the ideal solution. The other options do not correctly represent how containers are co-located to share resources in the Kubernetes context. Creating separate pods for each container would not allow them to share network and storage resources directly. Configuring a service or deploying a DaemonSet would not target the issue at hand, which is the shared network and storage for closely related containers."
    ),
    (
        "You are maintaining a script that updates system packages and restarts a critical service afterward, but only if the update succeeds. Which line of code correctly implements this behavior?",
        [
            "yum update -y ; service httpd restart",
            "yum update -y && service httpd restart",
            "yum update -y || service httpd restart",
            "yum update -y & service httpd restart"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The use of && ensures that the subsequent command (service httpd restart) is executed only if the preceding command (yum update -y) completes successfully with an exit status of 0. Using ; does not check the success of the previous command. Using || only executes the subsequent command if the preceding one fails. Using & will put the first command in the background and immediately run the second one regardless of the first one's result."
    ),
    (
        "A system administrator wants to generate a report of disk usage by each user in the home directory and store the output to a file called disk_report.txt, overwriting any existing data in the file. Which command should they use to accomplish this task?",
        [
            "du -h /home/* >> disk_report.txt",
            "du -h /home/* > disk_report.txt",
            "du -h /home/* < disk_report.txt",
            "du -h /home/* &> disk_report.txt"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The correct answer is 'du -h /home/* > disk_report.txt' because the '>' operator will redirect the output of the 'du' command to 'disk_report.txt', overwriting its contents every time the command is run, thus only saving the latest disk usage report in the file.\nThe 'du -h /home/* >> disk_report.txt' is incorrect because using the '>>' operator would append to the file rather than overwriting it, leading to accumulation of data over time rather than maintaining a single report.\nThe 'du -h /home/* < disk_report.txt' is incorrect because the '<' operator is used for input redirection, which is not what is needed when intending to write to a file.\nLastly, 'du -h /home/* &> disk_report.txt' is incorrect as '&>' redirects both standard output and standard error to a file, which could include error messages in the report unnecessarily."
    ),
    (
        "An organization is transitioning to a microservices architecture for their cloud-based application, requiring smooth scaling, high availability, and a unified method of configuration. Which Kubernetes feature allows the organization to manage a group of identically configured containers, ensuring they can be scaled easily in response to demand?",
        [
            "StatefulSet",
            "Pod",
            "Service",
            "Deployment"
        ],
        3,
        "Scripting, Containers, and Automation",
        "In Kubernetes, a Deployment manages a group of identically configured containers, providing declarative updates to the application. Deployments allow for easy scaling, self-healing, and rolling updates to the containerized applications, which is ideal for scenarios needing smooth scaling and high availability. While Pods are the smallest deployable units and can hold one or more containers, they do not by themselves provide scaling or self-healing capabilities. That is orchestrated by a Deployment. Services are used to expose an application running on a set of Pods as a network service, and while they help in communication aspects and remain constant despite changes in Pods, they aren't the mechanism for managing container scaling. StatefulSets are similar to Deployments but are intended to manage stateful applications and provide unique identity to each pod they manage, which is not the focus of this scenario."
    ),
    (
        "What is the purpose of the Git command that is used to update your local repository with commits from a remote repository?",
        [
            "Retrieve updates from a remote repository",
            "Merge a remote branch into the current branch",
            "Revert a local commit",
            "Push changes to a remote repository"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct answer is 'Retrieve updates from a remote repository.' This answer is correct because the Git command in question is designed specifically to fetch and merge changes from a remote repository into the current branch in a local repository. 'Push changes to a remote repository' is incorrect as this is the purpose of the git push command, which transmits local branch updates to the corresponding remote branch. 'Merge a remote branch into the current branch' doesn't necessarily involve remote communication and could be done with local branches, thus it is also incorrect. 'Revert a local commit' pertains to commands such as git revert or git reset, which are used to undo local changes."
    ),
    (
        "The command docker logs can only retrieve logs from currently running containers.",
        [
            "True",
            "False"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The statement is incorrect. The docker logs command can retrieve logs from both running and stopped containers, provided that the container's logging driver and configuration support log retrieval after the container has stopped."
    ),
    (
        "As a system administrator, you have received a file named 'logins.txt' containing a list of usernames. However, the usernames are separated by commas and you need them to be separated by newlines to process them in a script. Using the 'tr' command, how would you translate the commas into newline characters in a shell script?",
        [
            "tr -d ',' '\\n' logins.txt",
            "tr ',' '\\n' < logins.txt",
            "tr '\\n' ',' < logins.txt",
            "tr -s ',' '\\n' logins.txt"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The command 'tr ',' '\\n' < logins.txt' is used for replacing all commas in the file 'logins.txt' with newline characters. This is the correct use of the 'tr' command where the first argument is the set of characters to be replaced (commas) and the second argument is the set of characters to replace with (newline characters). The '<' operator is used to pass the contents of 'logins.txt' to the 'tr' command."
    ),
    (
        "A system administrator needs to create a shell script that iterates over user-specified file names and checks if each file exists in the current directory. If the file exists, the script should display the name of the file along with a message stating that it exists. Which of the following script snippets would BEST accomplish this task?",
        [
            "for file; do if [ -e \"$file exists\" ]; then echo \"The file was found\"; fi; done",
            "for file in \"$@\"; do if [ -e \"$file\" ]; then echo \"File $file exists\"; fi; done",
            "for file in \"$@\"; do if [ -e $file_name ]; then echo \"File $file found\"; fi; done",
            "for file in \"$@\"; do echo \"Checking $file\" << if [ -e $file ]; then echo \"$file detected\"; fi; done"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The correct answer is Option A. The for file in \"$@\"; do ...; done loop correctly iterates over the list of arguments passed to the script. For each iteration, if [ -e \"$file\" ]; then checks if the current file exists with -e (file exists test operator) and the following echo \"File $file exists\" statement prints the appropriate message. Double-quoted $file prevents issues with filenames containing spaces or special characters.\nOption B is incorrect because it checks if a string literal '$file exists' rather than checking if each file exists. Option C is incorrect as it checks for the variable $file_name which is not defined in the context and also uses incorrect syntax for testing file existence. Option D is incorrect because it uses << redirection operator, which is used to redirect input from a here document and is not a proper way to check for the existence of files."
    ),
    (
        "A system administrator needs to find occurrences of the word 'refused' in the 'auth.log' file, which indicates failed SSH login attempts, and then count how many times this occurs. Which command will provide the accurate count?",
        [
            "grep -c 'refused' /var/log/auth.log",
            "grep 'refused' /var/log/auth.log | wc -l",
            "grep 'refused' /var/log/auth.log -c",
            "grep -v 'refused' /var/log/auth.log | wc -l"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct answer is grep -c 'refused' /var/log/auth.log because the -c option in the grep command provides a count of matching lines that contain the pattern specified. In this scenario, it counts the number of lines that have the word 'refused', giving an indication of the number of failed SSH login attempts logged in the 'auth.log' file. The options that include piping with the wc -l command are incorrect because when used with grep's -c option, they are redundant and unnecessarily complicate the command. The option that includes -v is incorrect because this inverts the match and would count all lines that do not contain the word 'refused'."
    ),
    (
        "An administrator is writing a shell script where the output of a command needs to be both displayed on the screen and written to a file for logging purposes. Which command and operator should the administrator use to achieve this?",
        [
            "Redirecting output using the > operator",
            "Appending the output to a file using the >> operator",
            "Piping the output to another command with the | operator",
            "Using the tee command with the | operator"
        ],
        3,
        "Scripting, Containers, and Automation",
        "The 'tee' command is the right choice for this task because it reads from standard input and writes to both standard output (allowing the user to see the output on the screen) and one or more files, essentially duplicating the output stream. The operator > is used to redirect output to a file but does not display it on the screen. The operator | is used to pipe the output of one command to another but on its own does not write to a file. The operator >> is used to append output to a file but again, it does not display the output on the screen."
    ),
    (
        "What command is used in a shell script to perform actions based on whether a particular condition is met or not?",
        [
            "case",
            "if",
            "while",
            "for"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The if command is used to execute conditional statements in a shell script, allowing the script to branch and perform different actions based on whether specified conditions are true or not. The while command is used for loops that continue as long as the condition is true. for is also a looping command but iterates over a list of values. case is used for matching a variable against a series of patterns, not specifically for a conditional statement."
    ),
    (
        "A team member has made several updates to files in a local Git repository. To prepare for the next commit, the team member wants to stage a specific file called update.txt that has been modified along with various other files. Which command should the team member use to stage only the changes in update.txt?",
        [
            "git add update.txt",
            "git commit update.txt",
            "git add .",
            "git push update.txt"
        ],
        0,
        "Scripting, Containers, and Automation",
        "The correct answer is git add update.txt because it stages the specific changes made to update.txt, making it ready for the next commit. The git add . command would stage all changes in the current directory and subdirectories, which is not desired in this scenario if the intention is to only stage update.txt. Using git commit update.txt without the add command would not work because commit attempts to create a new commit from currently staged changes, and it does not accept a file path as an argument. git push update.txt is incorrect because push is used for updating remote refs along with associated objects, not for staging changes."
    ),
    (
        "A systems administrator needs to create a Docker image from a Dockerfile located in the current directory. The image should include the tag 'webserver:v1'. Which of the following commands will successfully create the required Docker image?",
        [
            "docker create -t webserver:v1 .",
            "docker image build --name webserver:v1",
            "docker compile -t webserver:v1",
            "docker build -t webserver:v1 ."
        ],
        3,
        "Scripting, Containers, and Automation",
        "The docker build command is used to build a Docker image from a Dockerfile. The -t option allows the user to specify a repository and tag in the 'name:tag' format for the image. Hence, docker build -t webserver:v1 . is the correct command, where '.' specifies the build context - in this case, the current directory containing the Dockerfile."
    ),
    (
        "Which command demonstrates the correct use of the '||' operator in a shell script to execute a backup script only if the primary backup command fails?",
        [
            "tar czf /backup/primary.tar.gz /data | /usr/local/bin/backup-fallback.sh",
            "tar czf /backup/primary.tar.gz /data || /usr/local/bin/backup-fallback.sh",
            "/usr/local/bin/backup-fallback.sh || tar czf /backup/primary.tar.gz /data",
            "tar czf /backup/primary.tar.gz /data && /usr/local/bin/backup-fallback.sh"
        ],
        1,
        "Scripting, Containers, and Automation",
        "The '||' operator is used in shell scripts to execute the right-hand command only if the left-hand command returns a non-zero exit status, indicating failure. In the context of the provided answers, 'tar czf /backup/primary.tar.gz /data || /usr/local/bin/backup-fallback.sh' correctly represents the usage of '||', as it will only attempt to run the backup-fallback.sh script if the initial tar command fails."
    ),
    (
        "Which command will efficiently allow a monitoring script to display the last five entries of a log file and continue to output any new entries as they are appended, while also ensuring that file rotations are handled correctly by tracking the file descriptor?",
        [
            "tail -n 5 /var/log/webserver.log",
            "tail -F /var/log/webserver.log",
            "tail -F -n 5 /var/log/webserver.log",
            "tail -f -n 5 /var/log/webserver.log"
        ],
        2,
        "Scripting, Containers, and Automation",
        "The command tail -F -n 5 /var/log/webserver.log addresses the question's requirements by using -F (capital F), which not only outputs the last five lines of the file with -n 5 but also monitors the file descriptor in case the log file is rotated, as is common with log management. This is useful for system administrators who want to ensure that the monitoring script continues to function even if the original log file is archived and a new one is created. The wrong answers either don't follow the file descriptor changes (tail -f -n 5), don't provide real-time monitoring (tail -n 5), or lack specificity in tracking the correct number of lines (tail -F)."
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

            ("Which command is used to compress files using the Gzip algorithm, typically adding a `.gz` extension?",
             ["zip", "tar", "gzip", "bzip2"],
             2, "Commands (System Management)",
             "`gzip` compresses files using Lempel-Ziv coding (LZ77). It replaces the original file with a compressed version ending in `.gz`. Example: `gzip large_log_file.log`"),

            ("What command compresses files using the Burrows-Wheeler block sorting algorithm, often achieving higher compression than gzip?",
             ["gzip", "xz", "zip", "bzip2"],
             3, "Commands (System Management)",
             "`bzip2` is a compression utility that generally offers better compression ratios than `gzip` but can be slower. It typically adds a `.bz2` extension. Example: `bzip2 data_archive.tar`"),

            ("Which command creates archives compatible with MS-DOS/Windows systems, often using the `.zip` extension?",
             ["tar", "gzip", "zip", "rar"],
             2, "Commands (System Management)",
             "`zip` creates compressed archive files commonly used on Windows and other operating systems. It can store multiple files and directories. Example: `zip my_archive.zip file1.txt dir1/`"),

            ("What is the primary purpose of the `tar` command?",
             ["Compress files individually", "Manipulate tape archives and create/extract `.tar` archive files", "Manage disk partitions", "Display text files"],
             1, "Commands (System Management)",
             "`tar` (Tape Archive) is used to bundle multiple files and directories into a single archive file (`.tar`). It's often used in combination with compression tools like `gzip` or `bzip2`. Example: `tar -czvf backup.tar.gz /home/user/data` (create gzipped archive)."),

            ("Which command uses the LZMA2 compression algorithm, often providing very high compression ratios?",
             ["gzip", "bzip2", "zip", "xz"],
             3, "Commands (System Management)",
             "`xz` is a compression utility using the LZMA/LZMA2 algorithms, known for achieving high compression ratios, often better than `bzip2`, though potentially slower. Example: `xz -k data_file` (-k keeps original file)."),

            ("What is the `cpio` command used for?",
             ["Copying files between systems securely", "Managing process priorities", "Copying files to and from archives (cpio or tar format)", "Checking filesystem integrity"],
             2, "Commands (System Management)",
             "`cpio` (copy in and out) is an archive utility used to copy files into or out of a cpio or tar archive. It reads file lists from standard input. Example (copy-out): `find . -depth -print | cpio -ov > /path/to/archive.cpio`"),

            ("Which command is used for low-level copying and conversion of data, often used for disk cloning or creating image files?",
             ["cp", "rsync", "dd", "cat"],
             2, "Commands (System Management)",
             "`dd` copies data block by block, allowing for fine-grained control over the process. It's powerful but potentially dangerous if used incorrectly. Example: `sudo dd if=/dev/sda of=/dev/sdb bs=4M status=progress` (disk clone)."),

            ("What command displays detailed file status information, including permissions, owner, size, and timestamps?",
             ["ls", "file", "stat", "du"],
             2, "Commands (System Management)",
             "`stat` provides detailed information about files and filesystems, going beyond the basic listing provided by `ls`. Example: `stat /etc/passwd`"),

            ("Which command attempts to determine the type of a file based on its content?",
             ["stat", "ls", "file", "type"],
             2, "Commands (System Management)",
             "`file` examines a file's magic numbers and content patterns to determine its type (e.g., text, executable, image). Example: `file my_document.pdf`"),

            ("What is the primary function of the `rsync` command?",
             ["Remotely execute commands via SSH", "Efficiently synchronize files and directories between systems or locally", "Manage running services", "Compress archive files"],
             1, "Commands (System Management)",
             "`rsync` is a fast, versatile utility for synchronizing files and directories. It minimizes data transfer by only copying changed portions of files. Example: `rsync -avz /local/data/ user@remote:/remote/data/`"),

            ("Which command securely copies files between hosts using the SSH protocol?",
             ["ftp", "rcp", "scp", "sftp"],
             2, "Commands (System Management)",
             "`scp` (Secure Copy) uses SSH for data transfer, providing secure authentication and encrypted copying of files over a network. Example: `scp local_file.txt user@remote:/path/`"),

            ("What is the `nc` (netcat) command often used for?",
             ["Configuring network interfaces", "Anything involving TCP or UDP: port scanning, file transfer, chat, network debugging", "Managing DNS records", "Tracing network routes"],
             1, "Commands (System Management)",
             "`nc` (netcat) is a versatile networking utility that reads and writes data across network connections using TCP or UDP. It's a 'Swiss army knife' for networking tasks. Example (listen): `nc -l -p 1234` Example (connect): `nc remote.host 1234`"),

            ("Which command is used to move or rename files and directories?",
             ["cp", "mv", "rm", "mkdir"],
             1, "Commands (System Management)",
             "`mv` (move) renames a file or directory, or moves it to a different location within the same filesystem (fast) or across filesystems (slower, involves copy+delete). Example (rename): `mv oldname.txt newname.txt` Example (move): `mv file.txt /path/to/destination/`"),

            ("What command copies files and directories?",
             ["mv", "cp", "ln", "dd"],
             1, "Commands (System Management)",
             "`cp` (copy) creates duplicates of files or directories. Example: `cp source_file.txt destination_file.txt` Example (copy dir): `cp -r source_dir/ destination_dir/`"),

            ("Which command creates new directories?",
             ["touch", "rmdir", "mkdir", "mkfile"],
             2, "Commands (System Management)",
             "`mkdir` (make directory) creates one or more new directories. Example: `mkdir new_folder` Example (create parent dirs): `mkdir -p path/to/deep/folder`"),

            ("What command removes *empty* directories?",
             ["rm", "del", "rmdir", "unlink"],
             2, "Commands (System Management)",
             "`rmdir` (remove directory) deletes directories, but only if they are empty. Example: `rmdir empty_folder`"),

            ("Which command lists directory contents?",
             ["dir", "ls", "list", "show"],
             1, "Commands (System Management)",
             "`ls` (list) displays information about files and directories within the specified directory (or the current directory if none is specified). Example: `ls -al` (list all files including hidden, long format)."),

            ("What command prints the full path of the current working directory?",
             ["cwd", "path", "pwd", "whereami"],
             2, "Commands (System Management)",
             "`pwd` (print working directory) displays the absolute path of the directory you are currently in. Example: `pwd`"),

            ("Which command removes (deletes) files or directories?",
             ["del", "erase", "rm", "unlink"],
             2, "Commands (System Management)",
             "`rm` (remove) deletes files. With the `-r` (recursive) option, it can delete directories and their contents (use with caution!). Example (file): `rm old_file.txt` Example (directory): `rm -r old_folder/`"),

            ("What command changes the current working directory?",
             ["chd", "cd", "chdir", "goto"],
             1, "Commands (System Management)",
             "`cd` (change directory) moves your shell session to a different directory in the filesystem. Example: `cd /var/log` Example (home dir): `cd ~` or `cd`"),

            ("Which command displays the contents of a directory in a tree-like format?",
             ["ls -R", "find", "tree", "du"],
             2, "Commands (System Management)",
             "`tree` lists the contents of directories in a depth-indented, tree-like structure. Example: `tree /etc`"),

            ("What command displays the contents of one or more files to standard output?",
             ["more", "less", "cat", "head"],
             2, "Commands (System Management)",
             "`cat` (concatenate) reads files sequentially and writes their content to standard output. Often used to display short files or combine files. Example: `cat file1.txt file2.txt > combined.txt`"),

            ("Which command creates an empty file or updates the access/modification timestamps of an existing file?",
             ["mkfile", "create", "touch", "new"],
             2, "Commands (System Management)",
             "`touch` is primarily used to change file timestamps, but if the file doesn't exist, it creates an empty file with that name. Example: `touch new_empty_file.txt`"),

            ("What command is used to create and modify partition tables on disk drives (older, MBR-focused)?",
             ["parted", "gparted", "fdisk", "mkfs"],
             2, "Commands (System Management)",
             "`fdisk` is a classic, menu-driven utility for creating and manipulating disk partition tables, primarily associated with MBR partitioning schemes. Example: `sudo fdisk /dev/sda`"),

            ("Which command is a more modern utility for managing disk partitions, supporting both MBR and GPT?",
             ["fdisk", "cfdisk", "parted", "gdisk"],
             2, "Commands (System Management)",
             "`parted` is a powerful partition editor that supports multiple partition table types (including GPT) and can perform actions non-interactively. Example: `sudo parted /dev/sdb mklabel gpt`"),

            ("What command informs the kernel of partition table changes without requiring a reboot?",
             ["reboot", "partprobe", "udevadm trigger", "sync"],
             1, "Commands (System Management)",
             "`partprobe` requests the operating system kernel to re-read the partition table of specified devices, making changes visible without a reboot. Example: `sudo partprobe /dev/sdc`"),

            ("Which command attaches a filesystem located on a device to a specific directory (mount point) in the filesystem hierarchy?",
             ["fstab", "umount", "mount", "attach"],
             2, "Commands (System Management)",
             "`mount` connects a filesystem on a storage device (like a partition or network share) to the main filesystem tree at a specified mount point directory. Example: `sudo mount /dev/sdb1 /mnt/data`"),

            ("What command reports filesystem disk space usage?",
             ["du", "ls", "df", "stat"],
             2, "Commands (System Management)",
             "`df` (disk free) displays the amount of available and used disk space on mounted filesystems. Example: `df -h` (human-readable sizes)."),

            ("Which command estimates file and directory space usage?",
             ["df", "stat", "ls -s", "du"],
             3, "Commands (System Management)",
             "`du` (disk usage) summarizes the disk space occupied by files and directories, recursively by default. Example: `du -sh /var/log` (summary, human-readable)."),

            ("What command displays information about LVM Physical Volumes (PVs)?",
             ["vgs", "lvs", "pvs", "pvdisplay"],
             2, "Commands (System Management)",
             "`pvs` provides a concise overview list of Physical Volumes configured for use with the Logical Volume Manager (LVM). Example: `pvs`"),

            ("Which command displays information about LVM Volume Groups (VGs)?",
             ["lvs", "pvs", "vgs", "vgdisplay"],
             2, "Commands (System Management)",
             "`vgs` provides a concise overview list of Volume Groups defined within LVM. Example: `vgs`"),

            ("What command displays information about LVM Logical Volumes (LVs)?",
             ["pvs", "vgs", "lvs", "lvdisplay"],
             2, "Commands (System Management)",
             "`lvs` provides a concise overview list of Logical Volumes created within LVM Volume Groups. Example: `lvs`"),

            ("Which command is used to change the attributes of an LVM Logical Volume?",
             ["lvcreate", "lvresize", "lvchange", "lvremove"],
             2, "Commands (System Management)",
             "`lvchange` modifies various attributes of a Logical Volume, such as its permissions or activation state. Example: `lvchange -a n /dev/vg01/lv_data` (deactivate)."),

            ("What command creates a new LVM Logical Volume within a Volume Group?",
             ["vgcreate", "pvcreate", "lvcreate", "mkfs"],
             2, "Commands (System Management)",
             "`lvcreate` allocates space from a Volume Group to create a new Logical Volume. Example: `lvcreate -L 10G -n lv_web vg01`"),

            ("Which command creates a new LVM Volume Group from one or more Physical Volumes?",
             ["pvcreate", "lvcreate", "vgcreate", "mkfs"],
             2, "Commands (System Management)",
             "`vgcreate` combines one or more initialized Physical Volumes into a new Volume Group. Example: `vgcreate vg_database /dev/sdc1 /dev/sdd1`"),

            ("What command increases or decreases the size of an LVM Logical Volume?",
             ["lvchange", "lvextend", "lvreduce", "lvresize"],
             3, "Commands (System Management)",
             "`lvresize` can both increase and decrease the size of a Logical Volume (though decreasing requires caution). Often used with filesystem resizing tools. Example: `lvresize -L +5G /dev/vg01/lv_data`"),

            ("Which command initializes a disk or partition for use as an LVM Physical Volume?",
             ["vgcreate", "lvcreate", "pvcreate", "fdisk"],
             2, "Commands (System Management)",
             "`pvcreate` writes LVM metadata onto a disk or partition, marking it as a Physical Volume ready to be added to a Volume Group. Example: `pvcreate /dev/sdb1`"),

            ("What command adds Physical Volumes to an existing LVM Volume Group, increasing its total capacity?",
             ["vgchange", "vgmerge", "vgextend", "vgresize"],
             2, "Commands (System Management)",
             "`vgextend` incorporates additional Physical Volumes into an existing Volume Group. Example: `vgextend vg_data /dev/sde1`"),

            ("Which command is used to manage Linux software RAID arrays?",
             ["lvm", "raidutils", "mdadm", "fdisk"],
             2, "Commands (System Management)",
             "`mdadm` (multiple device admin) is the primary tool for creating, managing, and monitoring software RAID devices (MD devices) in Linux. Example: `mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sda1 /dev/sdb1`"),

            ("What command lists SCSI devices recognized by the system?",
             ["lsusb", "lspci", "lsscsi", "lsblk"],
             2, "Commands (System Management)",
             "`lsscsi` lists information about SCSI devices (including devices using SCSI protocols like SATA and USB storage). Example: `lsscsi`"),

            ("Which command lists block devices (like disks and partitions)?",
             ["lsdev", "lsblk", "lspci", "lsscsi"],
             1, "Commands (System Management)",
             "`lsblk` displays information about block devices in a tree-like format, showing disks and their partitions. Example: `lsblk -f` (show filesystem info)."),

            ("What command displays block device attributes, such as UUIDs and filesystem types?",
             ["lsblk", "blkid", "fdisk -l", "stat"],
             1, "Commands (System Management)",
             "`blkid` locates and prints block device attributes (UUID, LABEL, TYPE) by reading metadata directly from the device. Example: `sudo blkid`"),

            ("Which command displays statistics for Fibre Channel (FC) host bus adapters (HBAs)?",
             ["lspci", "lsscsi", "fcstat", "hba_info"],
             2, "Commands (System Management)",
             "`fcstat` retrieves and displays statistics and information about Fibre Channel host adapters connected to the system. Example: `fcstat fcs0`"),

            ("What command is the primary tool for controlling the systemd system and service manager?",
             ["service", "initctl", "systemctl", "chkconfig"],
             2, "Commands (System Management)",
             "`systemctl` is used to introspect and control the state of the systemd system and service manager, including starting, stopping, enabling, disabling, and checking the status of services (units). Example: `systemctl status sshd`"),

            ("Which command is used to manage scheduled jobs for the `cron` daemon?",
             ["at", "schedule", "crontab", "cronjob"],
             2, "Commands (System Management)",
             "`crontab` is used to maintain crontab files for individual users, which specify commands to be run periodically by the `cron` daemon. Example: `crontab -e` (edit user's crontab)."),

            ("What command schedules a command to be run once at a specific time in the future?",
             ["cron", "at", "schedule", "timer"],
             1, "Commands (System Management)",
             "`at` reads commands from standard input or a file and schedules them to be executed later by the `atd` daemon. Example: `echo \"/path/to/script.sh\" | at now + 1 hour`"),

            ("Which command provides a dynamic, real-time view of running system processes?",
             ["ps", "htop", "top", "pstree"],
             2, "Commands (System Management)",
             "`top` displays a continuously updated list of system processes, ordered by resource usage (CPU by default), along with summary information about system load, memory usage, etc. Example: `top`"),

            ("What command displays a snapshot of the currently running processes?",
             ["top", "htop", "ps", "jobs"],
             2, "Commands (System Management)",
             "`ps` (process status) reports information about active processes based on options provided. Example: `ps aux` (show all processes with user and detailed info)."),

            ("Which command lists files opened by processes?",
             ["fuser", "lsof", "openfiles", "netstat"],
             1, "Commands (System Management)",
             "`lsof` (list open files) displays information about files opened by processes, including regular files, directories, network sockets, devices, etc. Example: `sudo lsof -i :80` (list processes using TCP port 80)."),

            ("What command provides an interactive, enhanced process viewer (often considered more user-friendly than `top`)?",
             ["ps", "top", "htop", "atop"],
             2, "Commands (System Management)",
             "`htop` is an ncurses-based interactive process viewer offering features like color, scrolling, tree view, and easier process manipulation compared to `top`. Example: `htop`"),

            ("Which command starts a process with a modified scheduling priority (niceness value)?",
             ["renice", "chpriority", "nice", "setpri"],
             2, "Commands (System Management)",
             "`nice` executes a command with a specified niceness adjustment. Higher niceness values mean lower priority. Example: `nice -n 10 backup_script.sh`"),

            ("What command changes the scheduling priority (niceness value) of already running processes?",
             ["nice", "chpriority", "setpri", "renice"],
             3, "Commands (System Management)",
             "`renice` alters the niceness value (priority) of one or more running processes, specified by PID, user, or group. Example: `sudo renice -n 5 -p 12345`"),

            ("Which job control command resumes a stopped job and runs it in the background?",
             ["fg", "jobs", "bg", "stop"],
             2, "Commands (System Management)",
             "`bg` (background) resumes a job that was suspended (e.g., with Ctrl+Z) and continues its execution in the background. Example: `bg %1`"),

            ("What job control command brings a background or stopped job into the foreground?",
             ["bg", "jobs", "fg", "resume"],
             2, "Commands (System Management)",
             "`fg` (foreground) brings the specified job (or the most recently suspended/backgrounded one) to the foreground, giving it terminal control. Example: `fg %1`"),

            ("Which job control command lists the active jobs running in the current shell session?",
             ["ps", "top", "jobs", "listjobs"],
             2, "Commands (System Management)",
             "`jobs` displays the status of jobs (processes started from the current shell) that are running in the background or stopped. Example: `jobs -l` (list with PIDs)."),

            ("What command finds processes based on their name or other attributes?",
             ["ps", "findproc", "pgrep", "pidof"],
             2, "Commands (System Management)",
             "`pgrep` looks through the currently running processes and lists the process IDs (PIDs) that match the selection criteria (e.g., name). Example: `pgrep -u username sshd`"),

            ("Which command sends signals to processes based on their name or other attributes?",
             ["kill", "pkill", "killall", "sigsend"],
             1, "Commands (System Management)",
             "`pkill` signals processes based on matching criteria (like name), similar to how `pgrep` finds them. Example: `pkill -USR1 nginx` (send USR1 signal to nginx processes)."),

            ("What command finds the process ID (PID) of a running program by name?",
             ["pgrep", "ps", "pidof", "getpid"],
             2, "Commands (System Management)",
             "`pidof` finds the PIDs of named running programs. It's often simpler than `pgrep` for just finding PIDs by exact name. Example: `pidof apache2`"),

            ("Which command from the iproute2 suite is used to show and manipulate routing, network devices, interfaces, and tunnels?",
             ["ifconfig", "route", "ip", "netstat"],
             2, "Commands (System Management)",
             "`ip` is the modern, primary tool in Linux for viewing and configuring network interfaces, routing tables, ARP tables, tunnels, and more, replacing older tools like `ifconfig` and `route`. Example: `ip addr show`"),

            ("What command from the iproute2 suite displays socket statistics and network connections?",
             ["netstat", "ss", "lsof", "ip sockets"],
             1, "Commands (System Management)",
             "`ss` (socket statistics) is used to dump socket statistics. It can display information similar to `netstat` but is generally considered faster and more modern. Example: `ss -tuln` (show TCP/UDP listening sockets, numeric)."),

            ("Which command-line utility controls the NetworkManager service?",
             ["networkctl", "nmcli", "systemctl network-manager", "ifconfig"],
             1, "Commands (System Management)",
             "`nmcli` (NetworkManager command-line interface) is the tool for controlling NetworkManager and reporting network status from the command line. Example: `nmcli device status`"),

            ("What older command (from net-tools) is used to configure network interfaces?",
             ["ip", "ifconfig", "ifcfg", "netconf"],
             1, "Commands (System Management)",
             "`ifconfig` (interface configuration) was the traditional command for configuring and displaying network interface parameters. It's largely superseded by `ip`. Example: `ifconfig eth0`"),

            ("Which command displays or sets the system's hostname?",
             ["hostnamectl", "sethostname", "hostname", "uname -n"],
             2, "Commands (System Management)",
             "`hostname` shows or sets the system's current hostname. Example: `hostname` (display) or `sudo hostname new-name` (set temporarily)."),

            ("What command manipulates the kernel's ARP cache?",
             ["ip neigh", "route", "arp", "ip arp"],
             2, "Commands (System Management)",
             "`arp` (from net-tools) is used to display and modify the Address Resolution Protocol (ARP) cache, which maps IP addresses to MAC addresses on the local network. Example: `arp -n`"),

            ("Which older command (from net-tools) shows or manipulates the IP routing table?",
             ["ip route", "route", "netstat -r", "traceroute"],
             1, "Commands (System Management)",
             "`route` was the traditional command for viewing and modifying the kernel's IP routing table. It's largely superseded by `ip route`. Example: `route -n`"),

            ("What command controls the system hostname and related settings via systemd?",
             ["hostname", "systemd-hostnamed", "hostnamectl", "localectl"],
             2, "Commands (System Management)",
             "`hostnamectl` queries and changes the system hostname and related settings managed by the `systemd-hostnamed` service. Example: `hostnamectl set-hostname server.example.com`"),

            ("Which command controls network name resolution settings via systemd-resolved?",
             ["nsswitch", "resolvconf", "resolvectl", "systemd-resolved"],
             2, "Commands (System Management)",
             "`resolvectl` queries and controls the `systemd-resolved` service, managing DNS settings, cache, and status. Example: `resolvectl status`"),

            ("What command is used for DNS lookups and querying name servers?",
             ["nslookup", "host", "ping", "dig"],
             3, "Commands (System Management)",
             "`dig` (Domain Information Groper) is a flexible tool for interrogating DNS name servers. It's often preferred over `nslookup` and `host` for detailed DNS troubleshooting. Example: `dig example.com MX`"),

            ("Which command is a simple utility for performing DNS lookups?",
             ["dig", "nslookup", "host", "dnsquery"],
             1, "Commands (System Management)",
             "`nslookup` is an older program for querying DNS servers, available in interactive and non-interactive modes. Example: `nslookup google.com`"),

            ("What command performs DNS lookups, often providing simpler output than `dig`?",
             ["nslookup", "dig", "host", "resolve"],
             2, "Commands (System Management)",
             "`host` is another utility for DNS lookups, generally providing concise output suitable for quick checks or scripting. Example: `host www.example.com`"),

            ("Which command looks up domain name registration information (owner, contacts, name servers)?",
             ["dig", "nslookup", "whois", "domaininfo"],
             2, "Commands (System Management)",
             "`whois` queries databases to retrieve information about domain names, IP addresses, and autonomous system numbers. Example: `whois comptia.org`"),

            ("What command captures and analyzes network packets?",
             ["netstat", "ss", "tcpdump", "wireshark"],
             2, "Commands (System Management)",
             "`tcpdump` is a powerful command-line packet analyzer that allows capturing and displaying TCP/IP and other packets being transmitted or received over a network. Example: `sudo tcpdump -i eth0 port 80`"),

            ("Which graphical tool (or its command-line counterpart `tshark`) is widely used for network protocol analysis?",
             ["tcpdump", "ethereal", "wireshark/tshark", "netmon"],
             2, "Commands (System Management)",
             "`Wireshark` (graphical) and `tshark` (command-line) are extremely popular and powerful network protocol analyzers used for troubleshooting, analysis, development, and education. Example: `tshark -i eth0 -f \"tcp port 443\"`"),

            ("What older command (from net-tools) displays network connections, routing tables, interface statistics, etc.?",
             ["ss", "ip", "netstat", "ifconfig"],
             2, "Commands (System Management)",
             "`netstat` provides various network-related information. It's largely superseded by `ss` and `ip`. Example: `netstat -tulnp` (show listening TCP/UDP sockets with PIDs)."),

            ("Which command traces the network path (route) packets take to a destination host?",
             ["ping", "mtr", "traceroute", "tracepath"],
             2, "Commands (System Management)",
             "`traceroute` sends packets with increasing TTL (Time To Live) values to discover the intermediate routers along the path to a network host. Example: `traceroute google.com`"),

            ("What command sends ICMP ECHO_REQUEST packets to network hosts to test reachability?",
             ["traceroute", "ping", "echo", "netcat"],
             1, "Commands (System Management)",
             "`ping` is a fundamental utility for testing network connectivity by sending ICMP echo requests and measuring response times. Example: `ping 8.8.8.8`"),

            ("Which command combines the functionality of `ping` and `traceroute` into a single network diagnostic tool?",
             ["tracepath", "pingroute", "mtr", "nettrace"],
             2, "Commands (System Management)",
             "`mtr` (My Traceroute) continuously sends packets like `traceroute` but also displays statistics about latency and packet loss for each hop along the path. Example: `mtr example.com`"),

            ("What command initiates a Secure Shell (SSH) connection to a remote host?",
             ["telnet", "rlogin", "ssh", "connect"],
             2, "Commands (System Management)",
             "`ssh` is the client program for logging into and executing commands on a remote machine securely using the SSH protocol. Example: `ssh user@remote.server.com`"),

            ("Which command-line tool transfers data from or to a server using various protocols like HTTP, HTTPS, FTP, etc.?",
             ["wget", "ftp", "curl", "scp"],
             2, "Commands (System Management)",
             "`curl` is a versatile tool for transferring data specified with URL syntax. It supports numerous protocols and options. Example: `curl -O https://example.com/file.zip`"),

            ("What command is a non-interactive network downloader, primarily used for retrieving files using HTTP, HTTPS, and FTP?",
             ["curl", "wget", "ftp", "get"],
             1, "Commands (System Management)",
             "`wget` is designed for robustly downloading files from the web, supporting recursive downloads, resuming interrupted downloads, etc. Example: `wget https://www.gnu.org/software/wget/wget.latest.tar.gz`"),

            ("Which command is used on Red Hat-based systems (like Fedora, CentOS, RHEL 8+) for package management?",
             ["apt", "yum", "dnf", "rpm"],
             2, "Commands (System Management)",
             "`dnf` (Dandified YUM) is the successor to YUM, used for installing, updating, and removing packages on RPM-based systems like Fedora and RHEL 8+. Example: `sudo dnf install httpd`"),

            ("What command was the predecessor to DNF on older Red Hat-based systems (like CentOS 7, RHEL 7)?",
             ["apt", "yum", "dnf", "rpm"],
             1, "Commands (System Management)",
             "`yum` (Yellowdog Updater, Modified) was the primary package manager for earlier RPM-based distributions. Example: `sudo yum update`"),

            ("Which command is the primary package management tool for Debian-based systems (like Debian, Ubuntu)?",
             ["yum", "dnf", "apt", "dpkg"],
             2, "Commands (System Management)",
             "`apt` (Advanced Package Tool) is the high-level command-line interface for managing packages (installing, removing, updating, searching) on Debian-based systems. Example: `sudo apt install nginx`"),

            ("What is the low-level tool for installing, querying, and managing individual `.rpm` package files?",
             ["yum", "dnf", "apt", "rpm"],
             3, "Commands (System Management)",
             "`rpm` is the underlying package manager for RPM-based systems. While `dnf` or `yum` are typically used for repository management, `rpm` can directly manipulate `.rpm` files. Example: `rpm -q httpd` (query installed httpd package)."),

            ("Which low-level tool installs, removes, and provides information about `.deb` package files on Debian-based systems?",
             ["apt", "apt-get", "dpkg", "debconf"],
             2, "Commands (System Management)",
             "`dpkg` is the base package management system for Debian-based distributions. `apt` provides a higher-level interface to it. Example: `sudo dpkg -i package_file.deb`"),

            ("What is the package management command used primarily by openSUSE and SUSE Linux Enterprise?",
             ["dnf", "apt", "zypper", "yast"],
             2, "Commands (System Management)",
             "`zypper` is the command-line package manager using the libzypp library, common on SUSE-based distributions. Example: `sudo zypper refresh`"),

            ("Which command manages Snap applications (sandboxed packages)?",
             ["flatpak", "appimage", "snap", "apt"],
             2, "Commands (System Management)",
             "`snap` is the command-line tool for interacting with the `snapd` daemon to install, manage, and remove Snap packages. Example: `sudo snap install vlc`"),

            ("What command is used to adjust kernel parameters at runtime and configure them persistently?",
             ["kconfig", "modprobe", "sysctl", "kernelcfg"],
             2, "Commands (System Management)",
             "`sysctl` modifies kernel parameters dynamically. Changes can be made persistent by editing `/etc/sysctl.conf` or files in `/etc/sysctl.d/`. Example: `sudo sysctl -w net.ipv4.ip_forward=1`"),

            ("Which command lists the currently loaded kernel modules?",
             ["insmod", "modprobe", "lsmod", "modinfo"],
             2, "Commands (System Management)",
             "`lsmod` formats the information from `/proc/modules` to show the kernel modules currently loaded into memory. Example: `lsmod`"),

            ("What command removes a kernel module from memory?",
             ["insmod", "modprobe", "rmmod", "unloadmod"],
             2, "Commands (System Management)",
             "`rmmod` unloads specified kernel modules. It generally requires that the module is not currently in use. Example: `sudo rmmod pcspkr`"),

            ("Which command loads a kernel module directly, without handling dependencies?",
             ["modprobe", "insmod", "loadmod", "lsmod"],
             1, "Commands (System Management)",
             "`insmod` loads a specified kernel module file directly into the kernel. It does not resolve dependencies like `modprobe` does. Example: `sudo insmod /path/to/module.ko`"),

            ("What command intelligently loads kernel modules, handling dependencies automatically?",
             ["insmod", "loadmod", "modprobe", "depmod"],
             2, "Commands (System Management)",
             "`modprobe` loads kernel modules and automatically loads any prerequisite modules (dependencies). It's the preferred way to load modules. Example: `sudo modprobe vboxdrv`"),

            ("Which command displays information about a specific kernel module file?",
             ["lsmod", "modinfo", "modstat", "modprobe -i"],
             1, "Commands (System Management)",
             "`modinfo` shows details about a kernel module, such as its filename, license, description, parameters, and dependencies. Example: `modinfo i915`"),

            ("What command controls the system time, date, and timezone settings via systemd?",
             ["date", "hwclock", "timedatectl", "localectl"],
             2, "Commands (System Management)",
             "`timedatectl` queries and changes the system clock and its settings, including time, date, timezone, and NTP synchronization status. Example: `timedatectl status`"),

            ("Which command controls the system locale and keyboard layout settings via systemd?",
             ["locale", "keyboardctl", "localectl", "timedatectl"],
             2, "Commands (System Management)",
             "`localectl` queries and changes the system locale and keyboard layout settings managed by `systemd-localed`. Example: `localectl set-locale LANG=en_US.UTF-8`"),

            # 2.0 Security Commands
            ("What command adds a new user account to the system?",
             ["adduser", "useradd", "newuser", "mkuser"],
             1, "Commands (Security)",
             "`useradd` is the low-level utility for creating a new user account or updating default new user information. Example: `sudo useradd -m -s /bin/bash newuser` (-m creates home dir, -s sets shell)."),

            ("Which command creates a new group on the system?",
             ["groupadd", "addgroup", "newgroup", "mkgroup"],
             0, "Commands (Security)",
             "`groupadd` creates a new group account using the values specified on the command line plus the default values from the system. Example: `sudo groupadd developers`"),

            ("What command deletes a user account from the system?",
             ["rmuser", "userdel", "deluser", "eraseuser"],
             1, "Commands (Security)",
             "`userdel` modifies the system account files, deleting all entries that refer to the username. Example: `sudo userdel olduser` (use `-r` to also remove home dir)."),

            ("Which command removes a group from the system?",
             ["groupdel", "delgroup", "rmgroup", "erasegroup"],
             0, "Commands (Security)",
             "`groupdel` deletes a group account from the system files. Example: `sudo groupdel oldgroup`"),

            ("What command modifies an existing user account's properties (e.g., shell, home directory, group membership)?",
             ["usermod", "chuser", "moduser", "useredit"],
             0, "Commands (Security)",
             "`usermod` changes various attributes of an existing user account. Example: `sudo usermod -aG sudo alice` (add alice to sudo group)."),

            ("Which command modifies the properties of an existing group (e.g., name, GID)?",
             ["groupmod", "chgroup", "modgroup", "groupedit"],
             0, "Commands (Security)",
             "`groupmod` modifies the definition of the specified group. Example: `sudo groupmod -n newname oldname` (rename group)."),

            ("What command changes a user's password?",
             ["chpasswd", "passwd", "password", "setpass"],
             1, "Commands (Security)",
             "`passwd` updates a user's authentication tokens (passwords). Used by users to change their own password or by root to change any user's password. Example: `passwd` (for current user) or `sudo passwd username`."),

            ("Which command modifies password aging information for a user account?",
             ["passwd -e", "chage", "agepass", "usermod -e"],
             1, "Commands (Security)",
             "`chage` (change aging) changes the number of days between password changes and the date of the last password change. Example: `sudo chage -l username` (list aging info)."),

            ("What older command displays or resets failed login attempt counts (often related to PAM)?",
             ["faillock", "pam_tally2", "logcheck", "lastb"],
             1, "Commands (Security)",
             "`pam_tally2` was used with the `pam_tally2.so` module to display and manipulate the failed login counter. It's largely replaced by `faillock`. Example: `pam_tally2 --user username`."),

            ("Which command is the modern replacement for `pam_tally2`, used to display and reset failed authentication attempt records?",
             ["pam_tally2", "faillock", "fail2ban-client", "authlog"],
             1, "Commands (Security)",
             "`faillock` is used with the `pam_faillock.so` module to maintain and display failed authentication attempt records and can lock accounts after too many failures. Example: `faillock --user username --reset`."),

            ("What command displays user identity information (UID, GID, groups)?",
             ["whoami", "groups", "id", "finger"],
             2, "Commands (Security)",
             "`id` prints real and effective user and group IDs for the specified user (or the current user if none specified). Example: `id alice`"),

            ("Which command shows who is currently logged into the system?",
             ["users", "who", "w", "last"],
             1, "Commands (Security)",
             "`who` displays a list of users currently logged in, along with their terminal, login time, and originating host. Example: `who`"),

            ("What command provides a more detailed view of logged-in users and their current activities compared to `who`?",
             ["who", "last", "w", "users"],
             2, "Commands (Security)",
             "`w` displays information about the users currently on the machine and their processes, including login time, idle time, JCPU, PCPU, and command line. Example: `w`"),

            ("Which command manages the `firewalld` service (common on RHEL-based systems)?",
             ["iptables", "ufw", "firewall-cmd", "systemctl firewalld"],
             2, "Commands (Security)",
             "`firewall-cmd` is the command-line client for managing `firewalld`, allowing configuration of zones, services, ports, and rules. Example: `sudo firewall-cmd --list-all`."),

            ("What command is used to configure the kernel's netfilter packet filtering rules (older, static ruleset)?",
             ["firewall-cmd", "nft", "iptables", "ufw"],
             2, "Commands (Security)",
             "`iptables` is the traditional tool for setting up, maintaining, and inspecting the tables of IP packet filter rules in the Linux kernel. Example: `sudo iptables -L -v -n`."),

            ("Which command interacts with the `nftables` packet filtering framework (newer replacement for iptables)?",
             ["iptables", "nft", "firewall-cmd", "ufw"],
             1, "Commands (Security)",
             "`nft` is the command-line utility for setting up, maintaining and inspecting packet filtering and classification rules using the `nftables` framework. Example: `sudo nft list ruleset`."),

            ("What command provides a user-friendly interface for managing netfilter firewall rules (common on Debian-based systems)?",
             ["firewall-cmd", "iptables", "gufw", "ufw"],
             3, "Commands (Security)",
             "`ufw` (Uncomplicated Firewall) provides a simplified command-line interface for managing `iptables` or `nftables`, aiming for ease of use. Example: `sudo ufw status`."),

            ("Which command generates SSH public and private key pairs?",
             ["ssh-copy-id", "ssh-agent", "ssh-keygen", "ssh-add"],
             2, "Commands (Security)",
             "`ssh-keygen` creates and manages authentication keys for SSH. Example: `ssh-keygen -t rsa -b 4096`"),

            ("What command installs an SSH public key onto a remote server's `authorized_keys` file?",
             ["ssh-add", "ssh-keygen", "scp", "ssh-copy-id"],
             3, "Commands (Security)",
             "`ssh-copy-id` securely copies a public key to a remote host, appending it to the user's `~/.ssh/authorized_keys` file for passwordless login. Example: `ssh-copy-id user@remote.host`"),

            ("Which command adds SSH private keys to the SSH authentication agent?",
             ["ssh-keygen", "ssh-copy-id", "ssh-add", "ssh-agent"],
             2, "Commands (Security)",
             "`ssh-add` adds private key identities to the authentication agent (`ssh-agent`), so you don't have to enter passphrases repeatedly. Example: `ssh-add ~/.ssh/id_rsa`"),

            ("What command allows a permitted user to execute a command as the superuser or another user?",
             ["su", "runas", "sudo", "pkexec"],
             2, "Commands (Security)",
             "`sudo` (superuser do) enables authorized users to run specific commands as root or another user, as defined in the `/etc/sudoers` file. Example: `sudo apt update`"),

            ("Which command should *always* be used to safely edit the `/etc/sudoers` file?",
             ["nano /etc/sudoers", "vim /etc/sudoers", "visudo", "sudoedit /etc/sudoers"],
             2, "Commands (Security)",
             "`visudo` locks the sudoers file, edits it with the default editor (like vi or nano), and performs syntax checking before saving to prevent errors. Direct editing is risky. Example: `sudo visudo`"),

            ("What command allows switching to another user account, including the superuser (root)?",
             ["sudo", "login", "su", "runuser"],
             2, "Commands (Security)",
             "`su` (substitute user) starts a new shell session as a different user. Without a username, it defaults to root (requires root password). Example: `su - username` (login shell for user)."),

            ("Which command executes a command as another user based on PolicyKit authorization?",
             ["sudo", "su", "runuser", "pkexec"],
             3, "Commands (Security)",
             "`pkexec` (PolicyKit execute) allows authorized users to run commands as another user (typically root) according to PolicyKit rules, often prompting graphically. Example: `pkexec synaptic`"),

            ("What command changes the owner (user) and optionally the group of a file or directory?",
             ["chmod", "chgrp", "chown", "chattr"],
             2, "Commands (Security)",
             "`chown` (change owner) modifies the user and/or group ownership of files and directories. Example: `sudo chown alice:developers report.txt`"),

            ("Which command sets the default file mode creation mask?",
             ["chmod", "chmask", "umask", "setmask"],
             2, "Commands (Security)",
             "`umask` sets or displays the file mode creation mask, which determines the default permissions for newly created files and directories. Example: `umask 022`"),

            ("What command changes the permission mode (read, write, execute) of files and directories?",
             ["chown", "chgrp", "chmod", "setperm"],
             2, "Commands (Security)",
             "`chmod` (change mode) modifies the access permissions of files and directories using symbolic (u+w) or octal (755) notation. Example: `chmod 755 script.sh` or `chmod u+x script.sh`"),

            ("Which command retrieves file Access Control Lists (ACLs)?",
             ["setfacl", "lsacl", "getfacl", "chacl"],
             2, "Commands (Security)",
             "`getfacl` displays the file Access Control Lists (ACLs), which provide more fine-grained permissions than standard Unix permissions. Example: `getfacl /path/to/file`"),

            ("What command sets or modifies file Access Control Lists (ACLs)?",
             ["getfacl", "setfacl", "chacl", "modacl"],
             1, "Commands (Security)",
             "`setfacl` modifies the ACLs of files and directories. Example: `setfacl -m u:bob:rw shared_file.txt`"),

            ("Which command sets the SELinux mode (Enforcing, Permissive) temporarily?",
             ["semanage", "getenforce", "setenforce", "sestatus"],
             2, "Commands (Security)",
             "`setenforce` modifies the current SELinux mode. `setenforce 1` sets Enforcing, `setenforce 0` sets Permissive. This change does not persist across reboots. Example: `sudo setenforce 0`"),

            ("What command displays the current SELinux mode (Enforcing, Permissive, or Disabled)?",
             ["setenforce", "sestatus", "getenforce", "selinuxctl"],
             2, "Commands (Security)",
             "`getenforce` prints the current SELinux operating mode to standard output. Example: `getenforce`"),

            ("Which command changes special file attributes on Linux ext2/ext3/ext4 filesystems (e.g., immutable)?",
             ["chmod", "setattr", "chattr", "lsattr"],
             2, "Commands (Security)",
             "`chattr` modifies file attributes on certain Linux filesystems, providing features beyond standard permissions. Example: `sudo chattr +i /etc/resolv.conf` (make immutable)."),

            ("What command lists the special file attributes set by `chattr`?",
             ["chattr", "getattr", "lsattr", "stat"],
             2, "Commands (Security)",
             "`lsattr` displays the extended attributes of files on Linux filesystems. Example: `lsattr /etc/passwd`"),

            ("Which command changes the group ownership of a file or directory?",
             ["chown", "chmod", "chgrp", "groupmod"],
             2, "Commands (Security)",
             "`chgrp` (change group) modifies only the group ownership of files and directories. Example: `chgrp users shared_document.txt`"),

            ("What command modifies SELinux boolean values (tunable policy settings)?",
             ["semanage bool", "setenforce", "getsebool", "setsebool"],
             3, "Commands (Security)",
             "`setsebool` changes the current value of SELinux booleans. Use `-P` to make the change persistent across reboots. Example: `sudo setsebool -P httpd_can_network_connect on`"),

            ("Which command displays the current values of SELinux booleans?",
             ["semanage bool", "getsebool", "setsebool", "sestatus"],
             1, "Commands (Security)",
             "`getsebool` lists SELinux boolean names and their current state (on or off). Example: `getsebool -a` (list all booleans)."),

            ("What command changes the SELinux security context (type, role, user) of a file?",
             ["restorecon", "semanage fcontext", "chcon", "setfattr"],
             2, "Commands (Security)",
             "`chcon` (change context) modifies the SELinux security context of files. Changes made with `chcon` may not persist across filesystem relabels. Example: `chcon -t httpd_sys_content_t /var/www/html/index.html`"),

            ("Which command restores the default SELinux security contexts for files based on policy rules?",
             ["chcon", "restorecon", "semanage fcontext", "fixfiles"],
             1, "Commands (Security)",
             "`restorecon` sets the security context of files to match the specifications defined in the active SELinux policy. Example: `sudo restorecon -Rv /var/www/html`"),

            ("What command manages persistent SELinux policy elements like contexts, booleans, ports, users, etc.?",
             ["sepolicy", "semodule", "semanage", "setsebool"],
             2, "Commands (Security)",
             "`semanage` is the SELinux policy management tool used to configure persistent local policy modifications, including file contexts, port types, booleans, and user mappings. Example: `sudo semanage fcontext -l` (list file contexts)."),

            ("Which command helps generate SELinux policy modules from audit log denial messages?",
             ["audit2why", "semodule", "audit2allow", "semanage module"],
             2, "Commands (Security)",
             "`audit2allow` reads SELinux denial messages from the audit log and generates suggested policy rules (Type Enforcement rules) to allow the denied actions, often packaged into a loadable module. Example: `audit2allow -a -M my_policy_module`"),

            # 3.0 Scripting, Containers, and Automation Commands
            ("What command searches for files in a directory hierarchy based on various criteria (name, type, size, time)?",
             ["grep", "locate", "find", "search"],
             2, "Commands (Scripting)",
             "`find` recursively searches directories for files matching specified criteria. It's extremely powerful and flexible. Example: `find /home -name \"*.log\" -type f`"),

            ("Which command searches for patterns within text files using regular expressions?",
             ["sed", "awk", "find", "grep"],
             3, "Commands (Scripting)",
             "`grep` (Global Regular Expression Print) searches input files (or standard input) for lines matching a given pattern (often a regular expression) and prints the matching lines. Example: `grep 'error' /var/log/syslog`"),

            ("What is `egrep` typically an alias for?",
             ["grep -E", "grep -F", "grep -i", "sed"],
             0, "Commands (Scripting)",
             "`egrep` is equivalent to `grep -E`, which enables Extended Regular Expressions (ERE) syntax, offering more features than Basic Regular Expressions (BRE). Example: `egrep 'warn|error' logfile.txt`"),

            ("Which command reads from standard input and writes to both standard output and one or more files?",
             ["cat", "tee", "split", "log"],
             1, "Commands (Scripting)",
             "`tee` duplicates its input, sending one copy to standard output and another to the specified file(s). Useful for viewing output while also logging it. Example: `ls -l | tee file_list.txt`"),

            ("What command counts lines, words, and bytes in files or standard input?",
             ["count", "stat", "wc", "size"],
             2, "Commands (Scripting)",
             "`wc` (word count) counts newlines, words, and bytes. Options like `-l` (lines), `-w` (words), `-c` (bytes) provide specific counts. Example: `cat report.txt | wc -l`"),

            ("Which command removes sections (columns/fields) from each line of a file?",
             ["sed", "awk", "cut", "paste"],
             2, "Commands (Scripting)",
             "`cut` extracts specified sections from each line, based on byte position, character, or field delimiter. Example: `cut -d':' -f1 /etc/passwd` (extract usernames)."),

            ("What command translates or deletes characters from standard input?",
             ["sed", "awk", "tr", "translate"],
             2, "Commands (Scripting)",
             "`tr` (translate) substitutes or deletes characters. Useful for case conversion or changing delimiters. Example: `echo \"Hello World\" | tr 'A-Z' 'a-z'` (convert to lowercase)."),

            ("Which command outputs the first part (default 10 lines) of files?",
             ["cat", "tail", "head", "first"],
             2, "Commands (Scripting)",
             "`head` displays the beginning portion of files. The `-n` option specifies the number of lines. Example: `head -n 5 /var/log/messages`"),

            ("What command outputs the last part (default 10 lines) of files?",
             ["cat", "head", "tail", "last"],
             2, "Commands (Scripting)",
             "`tail` displays the ending portion of files. The `-f` option allows following appended data in real-time. Example: `tail -f /var/log/syslog`"),

            ("Which shell built-in command reads a line from standard input into variables?",
             ["echo", "input", "read", "getline"],
             2, "Commands (Scripting)",
             "`read` is used in shell scripts to get input from the user (or a file via redirection) and assign it to one or more variables. Example: `read -p \"Enter your name: \" user_name`"),

            ("What shell built-in command displays lines of text or variable values?",
             ["print", "printf", "echo", "display"],
             2, "Commands (Scripting)",
             "`echo` outputs its arguments, followed by a newline, to standard output. Example: `echo \"Processing file: $filename\"`"),

            ("Which shell built-in command executes commands from a file in the current shell environment?",
             ["exec", "run", "source", "include"],
             2, "Commands (Scripting)",
             "`source` (or its shorthand `.`) reads and executes commands from the specified file within the current shell session, allowing scripts to modify the current environment. Example: `source ~/.bashrc`"),

            ("What command reads items from standard input and builds/executes command lines?",
             ["buildcmd", "execargs", "xargs", "apply"],
             2, "Commands (Scripting)",
             "`xargs` constructs command lines by taking items from standard input (often delimited by newlines or null characters) and using them as arguments to a specified command. Example: `find . -name \"*.tmp\" -print0 | xargs -0 rm`"),

            ("Which Git command downloads a repository from a remote source to a local directory?",
             ["git pull", "git fetch", "git clone", "git init"],
             2, "Commands (Version Control)",
             "`git clone` creates a copy of an existing Git repository, including its history, branches, and files, from a remote URL. Example: `git clone https://github.com/user/repo.git`"),

            ("What Git command uploads local repository content and refs to a remote repository?",
             ["git fetch", "git pull", "git commit", "git push"],
             3, "Commands (Version Control)",
             "`git push` updates remote refs (like branches) using local refs, sending the necessary commit objects. Example: `git push origin main`"),

            ("Which Git command fetches commits from and integrates with another repository or a local branch?",
             ["git fetch", "git merge", "git pull", "git rebase"],
             2, "Commands (Version Control)",
             "`git pull` is essentially a combination of `git fetch` (downloading changes from the remote) followed by `git merge` (integrating the fetched changes into the current local branch). Example: `git pull origin main`"),

            ("What Git command records changes staged in the index to the repository history?",
             ["git add", "git stage", "git commit", "git save"],
             2, "Commands (Version Control)",
             "`git commit` creates a new commit object containing the changes currently staged in the index, along with a log message describing the changes. Example: `git commit -m \"Implement new login feature\"`"),

            ("Which Git command adds file contents to the staging area (index) for the next commit?",
             ["git stage", "git add", "git commit -a", "git track"],
             1, "Commands (Version Control)",
             "`git add` updates the index using the current content found in the working tree, preparing content for the next commit. Example: `git add modified_file.py` or `git add .` (add all changes)."),

            ("What Git command switches branches or restores working tree files?",
             ["git switch", "git restore", "git checkout", "git branch -m"],
             2, "Commands (Version Control)",
             "`git checkout` is used to switch to a different branch or restore files in the working directory to a state from a specific commit or the index. Example (switch branch): `git checkout develop` Example (restore file): `git checkout -- old_file.txt`"),

            ("Which Git command lists, creates, or deletes branches?",
             ["git checkout -b", "git switch", "git branch", "git ref"],
             2, "Commands (Version Control)",
             "`git branch` manages branches. Without arguments, it lists local branches. With a name, it creates a new branch. With `-d`, it deletes a branch. Example (list): `git branch` Example (create): `git branch new-feature`"),

            ("What Git command creates, lists, deletes, or verifies a tag object signed with GPG?",
             ["git label", "git mark", "git tag", "git sign"],
             2, "Commands (Version Control)",
             "`git tag` is used to mark specific points in history as important, typically used for releases. Example (create lightweight): `git tag v1.0.0` Example (list): `git tag`"),

            ("Which Git command joins two or more development histories (branches) together?",
             ["git rebase", "git combine", "git merge", "git join"],
             2, "Commands (Version Control)",
             "`git merge` incorporates changes from named commits (since their histories diverged from the current branch) into the current branch. Example: `git merge feature-branch`"),

            ("What Git command reapplies commits from one branch onto another base branch?",
             ["git merge", "git cherry-pick", "git rebase", "git apply"],
             2, "Commands (Version Control)",
             "`git rebase` rewrites commit history by taking commits from one branch and applying them sequentially onto the tip of another branch, often used to maintain a linear history. Example: `git rebase main` (while on feature branch)."),

            # 4.0 Troubleshooting Commands
            ("Which command is a versatile network scanner used for port scanning, service detection, and OS detection?",
             ["netstat", "ss", "nmap", "ping"],
             2, "Commands (Troubleshooting)",
             "`nmap` (Network Mapper) is a powerful open-source tool for network discovery and security auditing. Example: `nmap -sV target.example.com` (scan for open ports and service versions)."),

            ("What command connects to an SSL/TLS enabled service and displays certificate information?",
             ["curl -k", "wget --no-check-certificate", "openssl s_client", "gnutls-cli"],
             2, "Commands (Troubleshooting)",
             "`openssl s_client` is part of the OpenSSL toolkit and acts as a generic SSL/TLS client, often used to connect to servers and examine certificate details. Example: `openssl s_client -connect google.com:443`"),

            ("Which command displays detailed CPU architecture information?",
             ["lshw -class processor", "cat /proc/cpuinfo", "lscpu", "dmidecode -t processor"],
             2, "Commands (Troubleshooting)",
             "`lscpu` gathers CPU architecture information from sysfs and /proc/cpuinfo and presents it in a readable format. Example: `lscpu`"),

            ("What command displays information about memory configuration and usage?",
             ["free", "vmstat", "lsmem", "cat /proc/meminfo"],
             2, "Commands (Troubleshooting)",
             "`lsmem` lists the ranges of available memory along with their online status. Example: `lsmem`"),
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

             # B
             ("What does high network 'Latency' typically mean?",
              ["High data transfer rate", "Low data transfer rate", "Delay in data transfer", "Frequent packet loss"],
              2, "Concepts & Terms (Networking)",
              "Latency refers to the time delay experienced in a system, often the time it takes for a data packet to travel from its source to its destination across a network."),

             ("What is the BIOS?",
              ["A type of hard drive", "Firmware used to initialize hardware during boot", "The Linux kernel", "A networking protocol"],
              1, "Concepts & Terms (System Management)",
              "BIOS (Basic Input/Output System) is firmware stored on a chip on the motherboard that initializes hardware and starts the boot process when a computer is turned on. It's largely superseded by UEFI."),

             ("What does the term 'Block Storage' refer to?",
              ["Storing data in files and folders", "Storing data as discrete objects with metadata", "Storing data in fixed-size blocks, often used by SANs", "Storing data temporarily in RAM"],
              2, "Concepts & Terms (System Management)",
              "Block storage breaks data into fixed-size blocks, each with a unique address but no additional metadata. It's common in Storage Area Networks (SANs) and is used for structured data like databases or as volumes for virtual machines."),

             ("What is the 'Boot Process' in Linux?",
              ["Compiling the kernel", "Installing software packages", "The sequence of steps from power-on to a usable operating system", "Managing user logins"],
              2, "Concepts & Terms (System Management)",
              "The boot process involves loading firmware (BIOS/UEFI), running the bootloader (GRUB), loading the kernel and initramfs, initializing hardware, mounting the root filesystem, and starting the init system (systemd)."),

             ("In cloud computing, what does 'Bootstrapping' often refer to?",
              ["Installing the operating system", "Configuring the network manually", "The initial automated configuration of a server instance upon first boot", "Updating the system firmware"],
              2, "Concepts & Terms (Automation)",
              "Bootstrapping is the process of performing initial setup and configuration automatically when a new cloud instance or virtual machine starts for the first time, often using tools like cloud-init."),

             ("What is Bash?",
              ["A text editor", "A popular command-line interpreter (shell)", "A filesystem type", "A version control system"],
              1, "Concepts & Terms (Scripting)",
              "Bash (Bourne Again SHell) is the default shell on many Linux distributions, providing a command-line interface for interacting with the operating system and executing scripts."),

             ("What is 'Brace Expansion' in shell scripting?",
              ["Expanding wildcard characters like *", "A mechanism to generate arbitrary strings based on patterns", "Substituting variable values", "Redirecting command output"],
              1, "Concepts & Terms (Scripting)",
              "Brace expansion allows generating lists of strings based on a pattern containing braces `{}`. Example: `echo file{A,B,C}.txt` expands to `fileA.txt fileB.txt fileC.txt`."),

             ("What is 'Bridging' in container networking?",
              ["Connecting containers across multiple hosts", "Sharing the host's network namespace directly", "Connecting a container to a virtual network managed by the host, often using NAT", "Isolating a container completely from the network"],
              2, "Concepts & Terms (Containers)",
              "A bridge network creates a software bridge on the host, connecting containers attached to it into their own network. The host acts as a router, often using NAT for external connectivity."),

             ("What is Btrfs?",
              ["A block device driver", "A modern copy-on-write (CoW) filesystem for Linux with advanced features", "A backup utility", "A network protocol"],
              1, "Concepts & Terms (System Management)",
              "Btrfs is a filesystem known for features like snapshots, built-in RAID support, checksums, compression, and efficient space usage, designed for fault tolerance and easy administration."),

            # C
             ("What is a Certificate Authority (CA)?",
              ["A type of encryption algorithm", "An entity that issues and verifies digital certificates", "A server that stores private keys", "A network firewall component"],
              1, "Concepts & Terms (Security)",
              "A CA is a trusted third party that validates the identity of entities (like websites or individuals) and issues digital certificates containing their public key, vouching for their authenticity."),

             ("What is 'Certificate Authentication'?",
              ["Encrypting data using a certificate", "Using digital certificates to verify the identity of a user or system", "Signing a document digitally", "Generating a new key pair"],
              1, "Concepts & Terms (Security)",
              "Certificate authentication uses the public/private key pair within a digital certificate to prove identity, commonly used in TLS/SSL for server/client authentication or for user authentication (e.g., smart cards)."),

             ("What does CPU stand for?",
              ["Central Processing Unit", "Core Programming Utility", "Computer Power Unit", "Control Program Unit"],
              0, "Concepts & Terms (System Management)",
              "The CPU (Central Processing Unit) is the primary component of a computer that performs most of the processing and executes instructions."),

             ("In Linux device files (`/dev`), what is a 'Character Device'?",
              ["A device representing a disk drive", "A device that transfers data character by character (e.g., terminal, serial port)", "A special device like /dev/null", "A network interface"],
              1, "Concepts & Terms (System Management)",
              "Character devices handle data sequentially, one character (or byte) at a time. Examples include terminals (`/dev/tty`), serial ports (`/dev/ttyS0`), and pseudo-terminals."),

             ("What is Chef?",
              ["A version control system", "A container orchestration platform", "An automation platform for configuration management", "A text editor"],
              2, "Concepts & Terms (Automation)",
              "Chef is a configuration management tool that uses 'recipes' and 'cookbooks' (written in Ruby) to automate the setup and maintenance of infrastructure."),

             ("What is `chrony` used for in Linux?",
              ["Managing cron jobs", "Network time synchronization (NTP client/server)", "Checking filesystem integrity", "Managing user accounts"],
              1, "Concepts & Terms (System Management)",
              "`chrony` is an implementation of the Network Time Protocol (NTP) used to keep the system clock accurate by synchronizing it with NTP servers."),

             ("What is Cloud-init?",
              ["A cloud storage service", "A tool for initializing and customizing cloud instances during first boot", "A container runtime", "A web server"],
              1, "Concepts & Terms (Automation)",
              "Cloud-init is the industry standard multi-distribution method for cross-platform cloud instance initialization. It allows automatic configuration on first boot using metadata provided by the cloud platform."),

             ("In networking, what are 'Collisions'?",
              ["Intentional interference to disrupt traffic", "Occur when two devices transmit simultaneously on a shared network medium (common with hubs or half-duplex)", "A type of network routing protocol", "Successful data packet deliveries"],
              1, "Concepts & Terms (Networking)",
              "Collisions happen in shared-medium Ethernet networks (like those using hubs or operating in half-duplex mode) when multiple devices try to send data at the exact same time, corrupting the transmissions."),

             ("What does 'Compilation from source' mean?",
              ["Downloading pre-built software packages", "Running a script", "Translating human-readable source code into machine-executable code", "Installing a kernel module"],
              2, "Concepts & Terms (System Management)",
              "Compiling from source involves taking the original programming code written by developers and using a compiler (like GCC) to translate it into binary code that the computer's processor can execute."),

             ("What is Docker Compose used for?",
              ["Orchestrating containers across multiple hosts", "Building Docker images", "Defining and running multi-container Docker applications on a single host", "Managing Docker storage volumes"],
              2, "Concepts & Terms (Containers)",
              "Docker Compose uses a YAML file (typically `docker-compose.yml`) to configure and start multiple related Docker containers as a single service or application stack."),

             ("What are 'Conditionals' in scripting?",
              ["Loops that repeat code", "Variables storing boolean values", "Statements (like `if`, `case`) that execute code blocks based on whether a condition is true or false", "Functions that return true or false"],
              2, "Concepts & Terms (Scripting)",
              "Conditionals allow scripts to make decisions and execute different paths based on the outcome of tests or comparisons."),

             ("What is a 'Container' in computing?",
              ["A physical server", "A type of virtual machine", "A standardized unit of software packaging code and dependencies together", "A network storage device"],
              2, "Concepts & Terms (Containers)",
              "Containers provide OS-level virtualization, packaging an application and its dependencies to run reliably in isolation across different computing environments."),

             ("What is a 'Container Image'?",
              ["A running instance of a container", "A template containing the application code, runtime, libraries, and settings needed to run a container", "A storage volume used by containers", "A network configuration for containers"],
              1, "Concepts & Terms (Containers)",
              "A container image is a lightweight, standalone, executable package that serves as the blueprint for creating running container instances."),

             ("What is a 'Container Network'?",
              ["The physical network connecting container hosts", "Virtual networks created for containers to communicate", "A tool for monitoring container traffic", "A container that manages network routing"],
              1, "Concepts & Terms (Containers)",
              "Container networks (like bridge, overlay, host) define how containers connect to each other, the host machine, and external networks."),

             ("What is a 'Container Registry'?",
              ["A running container instance", "A tool for building container images", "A storage and distribution system for container images (e.g., Docker Hub)", "A container monitoring dashboard"],
              2, "Concepts & Terms (Containers)",
              "A container registry is a repository where container images are stored, managed, and can be pulled from to run containers."),

             ("In SELinux, what is a 'Context'?",
              ["The current working directory", "A security label applied to processes and files used for access control decisions", "A user's login shell", "A type of firewall rule"],
              1, "Concepts & Terms (Security)",
              "An SELinux context (or security context) is metadata (user:role:type:level) attached to every process and object (file, socket, etc.) that SELinux uses to enforce its security policy."),

             ("What does CI/CD stand for?",
              ["Continuous Integration / Continuous Deployment (or Delivery)", "Code Integration / Code Deployment", "Centralized Infrastructure / Centralized Deployment", "Configuration Integrity / Configuration Delivery"],
              0, "Concepts & Terms (Automation)",
              "CI/CD is a set of practices and tools that automate the process of building, testing, and deploying software changes, enabling faster and more reliable releases."),

             ("What does 'Filesystem Corruption' mean?",
              ["Running out of disk space", "Damage to the filesystem's structure or data, potentially leading to errors or data loss", "Incorrect file permissions", "A virus infection"],
              1, "Concepts & Terms (Troubleshooting)",
              "Filesystem corruption indicates that the metadata or data on a storage volume is inconsistent or damaged, often requiring tools like `fsck` to repair."),

             ("What is 'cron'?",
              ["A text editor", "A time-based job scheduler daemon in Unix-like systems", "A command to change file ownership", "A version control system"],
              1, "Concepts & Terms (System Management)",
              "`cron` is the background daemon that executes scheduled commands (cron jobs) specified in crontab files."),

            # D
             ("What is a 'Daemon' in Linux?",
              ["A user account with root privileges", "A program that runs in the background to provide a service", "A hardware device driver", "A graphical user interface element"],
              1, "Concepts & Terms (System Management)",
              "A daemon is a long-running background process that typically starts at boot time and waits to handle service requests (e.g., `sshd`, `httpd`, `crond`)."),

             ("What is a 'Digital Signature'?",
              ["An electronic signature image", "A cryptographic method to verify the authenticity and integrity of a message or document", "A type of SSL/TLS certificate", "A user's password hash"],
              1, "Concepts & Terms (Security)",
              "A digital signature uses the sender's private key to create a unique code attached to a message. The recipient can use the sender's public key to verify that the message hasn't been tampered with and truly came from the sender."),

             ("What is 'Disk Partitioning'?",
              ["Formatting a disk", "Dividing a physical disk drive into one or more logical sections", "Encrypting a disk drive", "Checking a disk for errors"],
              1, "Concepts & Terms (System Management)",
              "Partitioning divides a disk into separate areas (partitions), each of which can contain a filesystem or be used for other purposes (like swap space)."),

             ("What is the 'Domain Name System' (DNS)?",
              ["A file sharing protocol", "A system for translating human-readable domain names into IP addresses", "A network security protocol", "A directory service for user accounts"],
              1, "Concepts & Terms (Networking)",
              "DNS acts like the phonebook of the Internet, translating domain names (like `www.google.com`) that humans use into the IP addresses (like `172.217.160.142`) that computers use to locate each other."),

            # E
             ("What is 'Encryption'?",
              ["Compressing data", "Converting data into a code to prevent unauthorized access", "Checking data for errors", "Deleting data securely"],
              1, "Concepts & Terms (Security)",
              "Encryption uses algorithms to scramble data so that it can only be read by authorized parties who possess the correct key to unscramble (decrypt) it."),

             ("What are 'Environment Variables'?",
              ["Variables used only inside the kernel", "Settings related to the graphical environment", "Dynamic named values that affect how processes behave (e.g., PATH, HOME)", "Variables stored in configuration files"],
              2, "Concepts & Terms (Scripting)",
              "Environment variables are part of the operating system environment where processes run, providing configuration settings, paths, and other information."),

             ("What are 'Exit Codes' in shell scripting?",
              ["Codes indicating script errors only", "A numerical value returned by a command indicating its success or failure status", "Codes used to exit a loop", "User input codes"],
              1, "Concepts & Terms (Scripting)",
              "When a command finishes, it returns an exit code (status). By convention, 0 indicates success, and any non-zero value indicates some kind of failure or error."),

             ("What is Ext4?",
              ["A text editor", "A widely used journaling filesystem for Linux", "A network protocol", "A package manager"],
              1, "Concepts & Terms (System Management)",
              "Ext4 is a mature and reliable journaling filesystem, the default on many Linux distributions, offering improvements over its predecessors Ext2 and Ext3."),

            # F
             ("What is a 'Filesystem'?",
              ["A physical hard drive", "The way an operating system organizes and stores files on a storage device", "A network connection", "A running process"],
              1, "Concepts & Terms (System Management)",
              "A filesystem defines the structure (directories, files, metadata) used to manage data on a disk partition or other storage medium."),

             ("What is the 'Filesystem Hierarchy Standard' (FHS)?",
              ["A type of filesystem like Ext4", "A standard defining the main directories and their purpose in Linux", "A command to check filesystem integrity", "A tool for creating partitions"],
              1, "Concepts & Terms (System Management)",
              "FHS provides a common layout for Linux filesystems (e.g., `/bin` for essential binaries, `/etc` for configuration, `/var` for variable data like logs) to ensure consistency across distributions."),

             ("What is FUSE (Filesystem in Userspace)?",
              ["A kernel-level filesystem driver", "An interface allowing non-privileged users to create filesystems without kernel code changes", "A tool for formatting disks", "A network file sharing protocol"],
              1, "Concepts & Terms (System Management)",
              "FUSE enables developers to implement fully functional filesystems that run in user space, often used for accessing remote storage or unconventional data sources as if they were local filesystems."),

             ("What is 'File Storage'?",
              ["Storing data in fixed-size blocks", "Storing data as objects with metadata", "A hierarchical method of storing data using files and directories (e.g., NAS)", "Storing data in a database"],
              2, "Concepts & Terms (System Management)",
              "File storage (or file-level storage) presents data to users and applications as files organized within a hierarchy of directories, familiar from desktops and typical NAS devices."),

             ("What is `firewalld`?",
              ["A specific firewall hardware appliance", "A dynamic firewall management daemon common on RHEL-based systems", "The underlying packet filtering engine (like iptables)", "A command to list firewall rules"],
              1, "Concepts & Terms (Security)",
              "`firewalld` provides a dynamically managed firewall with support for network zones, allowing changes without restarting the entire firewall."),

             ("What is Flatpak?",
              ["A Linux distribution", "A system for building, distributing, and running sandboxed desktop applications", "A container runtime", "A filesystem type"],
              1, "Concepts & Terms (System Management)",
              "Flatpak is a framework for distributing desktop applications across various Linux distributions, running them in a sandboxed environment for better security and dependency management."),

            # G
             ("What is Git?",
              ["A text editor", "A distributed version control system", "A package manager", "A web server"],
              1, "Concepts & Terms (Automation)",
              "Git is the most widely used modern version control system, designed for tracking changes in source code and coordinating work among programmers."),

             ("What is a `.gitignore` file used for?",
              ["Storing Git configuration settings", "Specifying intentionally untracked files that Git should ignore", "Listing committed files", "Defining Git hooks"],
              1, "Concepts & Terms (Automation)",
              "A `.gitignore` file lists patterns for files and directories that Git should not track or stage for commits (e.g., build artifacts, log files, temporary files)."),

             ("What does GUID stand for?",
              ["General User Identifier", "Globally Unique Identifier", "Group User ID", "Graphical User Interface Driver"],
              1, "Concepts & Terms (System Management)",
              "A GUID is a 128-bit number used to create unique identifiers for resources. GPT partition tables use GUIDs to identify partition types and individual partitions."),

             ("What is 'Globbing' in the shell?",
              ["Running commands in the background", "Using wildcard characters (*, ?, []) to match filenames", "Redirecting command output", "Executing multiple commands sequentially"],
              1, "Concepts & Terms (Scripting)",
              "Globbing is the process where the shell expands patterns containing wildcards into a list of matching file or directory names before executing a command."),

             ("What is GRUB?",
              ["A filesystem checking tool", "A common bootloader used by many Linux distributions", "A text editor", "A network configuration utility"],
              1, "Concepts & Terms (System Management)",
              "GRUB (GRand Unified Bootloader) is the program that loads the Linux kernel into memory during the boot process, often presenting a menu to choose which OS or kernel to boot."),

             ("What does GPT stand for in disk partitioning?",
              ["General Partition Table", "GUID Partition Table", "Global Partition Type", "Group Partition Table"],
              1, "Concepts & Terms (System Management)",
              "GPT (GUID Partition Table) is a modern standard for the layout of partition tables on a physical storage device, using Globally Unique Identifiers (GUIDs). It overcomes limitations of the older MBR standard."),

            # H
             ("What does 'Linux Hardening' involve?",
              ["Installing more software", "Increasing hardware performance", "Reducing the system's vulnerability surface by applying security best practices", "Encrypting the entire hard drive"],
              2, "Concepts & Terms (Security)",
              "Hardening involves configuring a system securely by disabling unnecessary services, enforcing strong passwords, setting up firewalls, applying access controls, keeping software updated, etc."),

             ("What is 'Hashing' in cryptography?",
              ["Encrypting data with a key", "Transforming data into a fixed-size string of characters (hash value) for integrity checks or lookups", "Compressing data", "Signing data with a private key"],
              1, "Concepts & Terms (Security)",
              "Hashing algorithms produce a unique, fixed-size hash value from input data. It's used to verify data integrity (if the hash changes, the data changed) and securely store passwords (by storing hashes instead of plain text)."),

             ("What are 'Here Documents' in shell scripting?",
              ["Documentation embedded in comments", "Files included using the `source` command", "A way to redirect multiple lines of input to a command within the script", "External configuration files"],
              2, "Concepts & Terms (Scripting)",
              "A here document (using `<<DELIMITER`) allows feeding several lines of text directly from the script as standard input to a command, ending when the `DELIMITER` is encountered on a line by itself."),

             ("What does HTTP stand for?",
              ["HyperText Transfer Protocol", "High Transfer Text Protocol", "HyperText Transmission Protocol", "Hyperlink Text Transfer Protocol"],
              0, "Concepts & Terms (Networking)",
              "HTTP is the underlying protocol used by the World Wide Web for transferring web pages and other resources between clients (browsers) and servers."),

             ("What does HTTPS stand for?",
              ["HyperText Transfer Protocol Secure", "HyperText Transmission Protocol Standard", "Hyperlink Text Transfer Protocol Secure", "High Transfer Text Protocol Secure"],
              0, "Concepts & Terms (Networking)",
              "HTTPS is the secure version of HTTP, using SSL/TLS encryption to protect the communication between the client and the server."),

            # I
             ("What is 'Identity Management'?",
              ["Managing hardware inventory", "Managing digital identities, authentication, and authorization", "Managing software licenses", "Managing network configurations"],
              1, "Concepts & Terms (Security)",
              "Identity Management encompasses the policies and technologies used to control user access to resources, including processes like authentication, authorization, and user lifecycle management."),

             ("What does IaC stand for?",
              ["Infrastructure as Code", "Internet and Computing", "Integrated Access Control", "Internal Application Configuration"],
              0, "Concepts & Terms (Automation)",
              "Infrastructure as Code (IaC) is the practice of managing and provisioning infrastructure (networks, servers, databases, etc.) through machine-readable definition files (code), rather than manual configuration."),

             ("What is an 'initrd' or 'initramfs'?",
              ["The main Linux kernel file", "A temporary filesystem loaded into memory early in the boot process", "The systemd init daemon", "A type of disk partition"],
              1, "Concepts & Terms (System Management)",
              "The Initial RAM Disk (initrd) or Initial RAM Filesystem (initramfs) contains necessary drivers and tools loaded by the bootloader to allow the kernel to mount the real root filesystem."),

             ("What is an 'Inode'?",
              ["A network socket", "A data structure on a filesystem storing metadata about a file (permissions, owner, size, location)", "A running process", "A kernel module"],
              1, "Concepts & Terms (System Management)",
              "Each file and directory on a typical Linux filesystem has an inode that stores its attributes and points to the data blocks. The number of inodes is finite, so running out of them prevents new file creation."),

             ("What does I/O stand for?",
              ["Internet Output", "Input/Output", "Instruction Operation", "Internal Object"],
              1, "Concepts & Terms (Troubleshooting)",
              "I/O refers to the communication between a computer system and its external resources, such as storage devices (disk I/O) or networks (network I/O)."),

             ("What does IOPS stand for?",
              ["Input/Output Processing Speed", "Internet Operations Per Second", "Input/Output Operations Per Second", "Internal Object Processing Speed"],
              2, "Concepts & Terms (Troubleshooting)",
              "IOPS is a performance metric for storage devices, measuring the number of read and write operations it can perform per second."),

             ("What is an 'I/O Scheduler'?",
              ["A cron job for I/O tasks", "A kernel component that manages the order of disk read/write requests", "A hardware controller for disk drives", "A tool for monitoring I/O performance"],
              1, "Concepts & Terms (Troubleshooting)",
              "The I/O scheduler decides the sequence in which block I/O operations are submitted to the storage device, aiming to optimize throughput, latency, or fairness."),

             ("What is 'IP Forwarding'?",
              ["Translating private IP addresses to public ones (NAT)", "Assigning IP addresses automatically (DHCP)", "Enabling a system to act as a router, passing packets between different networks", "Resolving domain names to IP addresses (DNS)"],
              2, "Concepts & Terms (Security)",
              "IP forwarding allows a Linux machine with multiple network interfaces to route traffic between the networks connected to those interfaces."),

            # J
             ("What is 'Job Control' in the shell?",
              ["Managing scheduled cron jobs", "Features allowing users to manage multiple processes (jobs) within a single terminal session (e.g., fg, bg, Ctrl+Z)", "Controlling user permissions for running jobs", "Assigning job priorities"],
              1, "Concepts & Terms (System Management)",
              "Job control allows users to suspend processes (Ctrl+Z), run them in the background (`bg`), bring them to the foreground (`fg`), and list them (`jobs`)."),

             ("What is the 'systemd journal'?",
              ["A type of journaling filesystem", "A component of systemd that collects and stores system log data in a structured, binary format", "A user's command history file", "A configuration file for systemd"],
              1, "Concepts & Terms (Troubleshooting)",
              "The systemd journal centralizes logging from the kernel, initrd, services' stdout/stderr, and syslog, storing it in a queryable binary format managed by `journalctl`."),

             ("What is a 'Journaling Filesystem'?",
              ["A filesystem stored entirely in RAM", "A filesystem that keeps a log (journal) of changes before committing them, improving crash recovery", "A filesystem designed for log files", "A read-only filesystem"],
              1, "Concepts & Terms (System Management)",
              "Journaling filesystems (like Ext4, XFS, Btrfs) maintain a journal to track pending metadata changes, allowing for faster recovery and reduced risk of corruption after a crash."),

            # K
             ("What is the 'Kernel' in Linux?",
              ["The command-line interface", "The core component of the OS managing hardware and processes", "A collection of utility programs", "The graphical user interface"],
              1, "Concepts & Terms (System Management)",
              "The Linux kernel is the central part of the operating system, responsible for resource management (CPU, memory), hardware interaction, and providing fundamental services."),

             ("What are 'Kernel Modules'?",
              ["User-space applications", "Pieces of code that can be dynamically loaded/unloaded to extend kernel functionality (e.g., device drivers)", "Configuration files for the kernel", "The kernel's source code"],
              1, "Concepts & Terms (System Management)",
              "Kernel modules allow the Linux kernel to be extended without recompilation, commonly used for hardware drivers, filesystem support, or network protocols."),

             ("What is a 'Kernel Panic'?",
              ["A user-space application crash", "A security alert", "A fatal error detected by the kernel from which it cannot recover, usually halting the system", "A warning about low memory"],
              2, "Concepts & Terms (System Management)",
              "A kernel panic occurs when the kernel encounters a critical error it cannot handle safely, preventing potential data corruption by stopping the system."),

             ("What are 'Kernel Parameters'?",
              ["Arguments passed to user-space programs", "Settings that control the behavior of the Linux kernel, often tunable via sysctl", "Hardware specifications", "Filesystem options"],
              1, "Concepts & Terms (System Management)",
              "Kernel parameters (or sysctl parameters) allow administrators to adjust various aspects of the kernel's operation, such as network stack behavior, memory management, and filesystem settings."),

             ("What are 'Kill Signals'?",
              ["Network packets used to terminate connections", "Signals sent to processes to request termination or other actions (e.g., SIGTERM, SIGKILL, SIGHUP)", "Hardware interrupts", "Error messages from the kernel"],
              1, "Concepts & Terms (System Management)",
              "Signals are a form of inter-process communication used to notify processes of events or request specific actions, most commonly termination."),

             ("What is Kubernetes?",
              ["A container runtime like Docker", "An open-source container orchestration system", "A configuration management tool like Ansible", "A cloud provider like AWS"],
              1, "Concepts & Terms (Containers)",
              "Kubernetes automates the deployment, scaling, and management of containerized applications across clusters of hosts."),

            # L
             ("In SELinux, what are 'Labels'?",
              ["User-defined tags for files", "Security contexts (user:role:type:level) applied to objects and processes", "Filesystem mount options", "Firewall zone names"],
              1, "Concepts & Terms (Security)",
              "SELinux labels are the core metadata used by the policy to make access control decisions. Every file, process, port, etc., has an associated label."),

             ("What does LDAP stand for?",
              ["Linux Directory Access Protocol", "Lightweight Directory Access Protocol", "Local Data Authentication Protocol", "Layered Data Access Protocol"],
              1, "Concepts & Terms (Security)",
              "LDAP is a standard protocol for accessing and maintaining distributed directory information services (like user directories) over a network."),

             ("What is 'Link Status' in networking?",
              ["The speed of the network connection", "Indication of whether a network interface has an active physical connection", "The IP address assigned to an interface", "The amount of traffic on the link"],
              1, "Concepts & Terms (Troubleshooting)",
              "Link status (often shown by `ip link` or `ethtool`) indicates whether the network interface detects a live connection on the cable (e.g., link detected: yes/no)."),

             ("What is the difference between Soft and Hard Links?",
              ["Soft links point to inodes, Hard links point to paths", "Hard links are shortcuts, Soft links are copies", "Hard links are extra names for the same inode (file data), Soft links are pointers to a path name", "Soft links work across filesystems, Hard links do not"], # This last part is also true, but the core difference is the inode/path distinction.
              2, "Concepts & Terms (System Management)",
              "A hard link creates another directory entry pointing to the exact same inode (and thus the same file data) as the original. A soft link (symbolic link) is a special file that simply contains the path to another file or directory."),

             ("What does LUKS stand for?",
              ["Linux Universal Key System", "Logical User Key Setup", "Linux Unified Key Setup", "Layered Universal Kernel Security"],
              2, "Concepts & Terms (System Management)",
              "LUKS is the standard for block device encryption in Linux, providing a platform-independent way to manage encrypted volumes."),

             ("What is 'Load Average'?",
              ["The current CPU utilization percentage", "A measure of system load based on the number of processes running or waiting for CPU/IO", "The amount of free memory", "Network throughput"],
              1, "Concepts & Terms (Troubleshooting)",
              "Load average (typically shown as 1, 5, and 15-minute averages) reflects the number of processes in the run queue (running or waiting for CPU) plus those waiting for uninterruptible I/O. High values indicate a busy system."),

             ("What does 'Localization' mean in software?",
              ["Running software locally instead of remotely", "Adapting software for a specific language, region, and cultural conventions", "Securing software against local attacks", "Optimizing software for local hardware"],
              1, "Concepts & Terms (System Management)",
              "Localization involves translating text, adjusting date/time/number formats, and adapting other elements of software to suit users in a particular locale."),

             ("What does LVM stand for?",
              ["Linux Virtual Memory", "Logical Volume Manager", "Local Volume Mount", "Large Virtual Machine"],
              1, "Concepts & Terms (System Management)",
              "LVM provides a layer of abstraction over physical storage, allowing flexible management of disk space through physical volumes, volume groups, and logical volumes."),

            # M
             ("What is the MBR?",
              ["Memory Buffer Register", "Master Boot Record", "Main Board ROM", "Managed Backup Resource"],
              1, "Concepts & Terms (System Management)",
              "The MBR is the traditional partitioning scheme and boot sector located at the very beginning of a disk drive, limited in partition size and count compared to GPT."),

             ("What does MTU stand for?",
              ["Maximum Transmission Unit", "Minimum Transfer Utility", "Multiple Tasking Unit", "Main Transaction Unit"],
              0, "Concepts & Terms (Networking)",
              "The MTU is the size (in bytes) of the largest data packet that a network layer protocol (like IP) can transmit over a specific link layer (like Ethernet)."),

             ("What is 'Memory Exhaustion'?",
              ["A CPU error", "Running out of disk space", "A state where the system has insufficient free RAM and swap space", "A network connection failure"],
              2, "Concepts & Terms (Troubleshooting)",
              "Memory exhaustion occurs when processes require more memory than is physically available (RAM + swap), potentially leading to the OOM killer terminating processes."),

             ("What is a 'Memory Leak'?",
              ["Data leaking from RAM onto disk", "Unauthorized access to memory contents", "A programming error where allocated memory is not released when no longer needed, causing gradual memory loss", "Physical damage to RAM modules"],
              2, "Concepts & Terms (Troubleshooting)",
              "Memory leaks cause applications to consume progressively more memory over time, eventually leading to performance degradation or memory exhaustion."),

             ("What is file 'Metadata'?",
              ["The actual content of the file", "Data *about* the file (e.g., permissions, owner, size, timestamps)", "A backup copy of the file", "A compressed version of the file"],
              1, "Concepts & Terms (System Management)",
              "Metadata describes the properties of a file rather than its content, stored typically within the filesystem's inode structure."),

             ("What does 'Mounting' a filesystem mean?",
              ["Formatting the filesystem", "Checking the filesystem for errors", "Making a filesystem on a device accessible at a specific directory location", "Encrypting the filesystem"],
              2, "Concepts & Terms (System Management)",
              "Mounting attaches a filesystem (e.g., from a disk partition or network share) to a directory (the mount point) within the main filesystem tree, making its contents available."),

             ("What does MFA stand for?",
              ["Multiple Factor Authentication", "Main Frame Access", "Managed File Access", "Multifactor Authentication"],
              3, "Concepts & Terms (Security)",
              "MFA requires users to provide two or more different types of verification factors (e.g., something you know, something you have, something you are) to gain access."),

             ("What is `multipathd` used for?",
              ["Managing multiple network interfaces (bonding)", "Managing multiple paths to storage devices (e.g., in a SAN) for redundancy/performance", "Distributing processes across multiple CPUs", "Handling multiple user logins"],
              1, "Concepts & Terms (System Management)",
              "`multipathd` is the daemon that manages device mapper multipathing, detecting and grouping multiple I/O paths to the same storage LUN to provide fault tolerance and potentially improve performance."),

            # N
             ("What is 'Name Resolution' in networking?",
              ["Assigning names to IP addresses", "Translating hostnames/domain names into IP addresses (and vice-versa)", "Configuring network interface names", "Resolving network conflicts"],
              1, "Concepts & Terms (Networking)",
              "Name resolution is the process, typically using DNS, of converting human-friendly names into the numerical IP addresses needed for network communication."),

             ("What does NAS stand for?",
              ["Network Access Server", "Network Attached Storage", "Network Administration System", "Network Allocation Service"],
              1, "Concepts & Terms (System Management)",
              "NAS is dedicated file storage device connected to a network, providing centralized data access and sharing capabilities to multiple clients using file-level protocols (like NFS or SMB/CIFS)."),

             ("What does NAT stand for?",
              ["Network Access Translation", "Network Address Translation", "Network Administration Tool", "Network Allocation Table"],
              1, "Concepts & Terms (Containers)",
              "NAT modifies IP address information in packet headers, commonly used to allow multiple devices on a private network to share a single public IP address for internet access."),

             ("What is NFS?",
              ["Network File System", "New File Standard", "Network Foundation Service", "Network Firewall System"],
              0, "Concepts & Terms (System Management)",
              "NFS is a distributed file system protocol allowing a client computer to access files over a network as if they were on its local storage."),

             ("What is NetworkManager?",
              ["A command to manage network routes", "A system daemon that manages network devices and connections", "A graphical network configuration tool", "A network packet analyzer"],
              1, "Concepts & Terms (System Management)",
              "NetworkManager aims to simplify network configuration and management, automatically handling connections and switching between networks."),

             ("What does NTP stand for?",
              ["Network Time Protocol", "Network Transfer Protocol", "Network Topology Protocol", "Network Testing Protocol"],
              0, "Concepts & Terms (System Management)",
              "NTP is a protocol designed to synchronize the clocks of computers over a network."),

             ("What does NVMe stand for?",
              ["New Virtual Memory extension", "Non-Volatile Memory Express", "Network Volume Management extension", "Native Virtual Machine environment"],
              1, "Concepts & Terms (Troubleshooting)",
              "NVMe is a high-performance interface specification specifically designed for accessing SSDs over a PCI Express bus, offering lower latency and higher IOPS than older interfaces like SATA."),

            # O
             ("What is 'Object Storage'?",
              ["Storing data in files within directories", "Storing data in fixed-size blocks", "Managing data as discrete units called objects, each with metadata and a unique ID", "Storing data in a relational database"],
              2, "Concepts & Terms (System Management)",
              "Object storage systems manage data as objects in a flat address space, accessed typically via HTTP APIs. Often used for large amounts of unstructured data (backups, media, archives) and common in cloud storage."),

             ("What is the 'OOM Killer'?",
              ["A process that kills idle connections", "A Linux kernel mechanism that terminates processes to free up memory under severe memory pressure", "A security tool that kills malicious processes", "A command to manually kill processes"],
              1, "Concepts & Terms (Troubleshooting)",
              "The Out Of Memory (OOM) Killer is invoked by the kernel when the system is critically low on memory and cannot allocate more, sacrificing processes (based on heuristics) to prevent a total system freeze."),

             ("What is an 'Overlay Network' in containerization?",
              ["The physical network infrastructure", "A virtual network spanning multiple hosts, allowing containers on different hosts to communicate directly", "The host machine's network interface", "A network bridge on a single host"],
              1, "Concepts & Terms (Containers)",
              "Overlay networks create a logical network on top of the existing physical network, enabling seamless communication between containers regardless of which host they are running on."),

            # P
             ("What is 'Package Management'?",
              ["Managing physical hardware packages", "The process of installing, upgrading, configuring, and removing software packages consistently", "Managing network data packets", "Organizing files into packages"],
              1, "Concepts & Terms (System Management)",
              "Package managers (like APT, DNF, Yum, Zypper) automate software management using repositories and package files (`.deb`, `.rpm`), handling dependencies and updates."),

             ("What is 'Parity' in RAID?",
              ["Mirroring data across multiple disks", "Striping data across multiple disks", "Redundant information calculated from data blocks, used to reconstruct data from a failed drive", "A measure of disk performance"],
              2, "Concepts & Terms (System Management)",
              "Parity is a form of checksum used in RAID levels like RAID 5 and RAID 6. By calculating parity data across disks, the array can tolerate one (RAID 5) or two (RAID 6) drive failures."),

             ("What does PAM stand for?",
              ["Pluggable Authentication Modules", "Process Authorization Manager", "Password Access Management", "Privileged Access Module"],
              0, "Concepts & Terms (Security)",
              "PAM provides a flexible framework for authentication-related services in Linux, allowing administrators to configure how applications authenticate users without modifying the applications themselves."),

             ("What is a 'Pod' in Kubernetes?",
              ["A physical server node", "A network service endpoint", "The smallest deployable unit, consisting of one or more containers sharing network/storage", "A storage volume"],
              2, "Concepts & Terms (Containers)",
              "A Pod is the basic building block in Kubernetes, representing a group of co-located containers that share resources and are managed as a single unit."),

             ("What is 'PolicyKit'?",
              ["An SELinux policy management tool", "A framework for controlling system-wide privileges for user processes", "A firewall configuration utility", "A password management tool"],
              1, "Concepts & Terms (Security)",
              "PolicyKit (polkit) provides a centralized way to define and grant specific administrative privileges to non-root users for particular tasks, often used by graphical desktop environments."),

             ("What is 'Port Forwarding' via SSH?",
              ["Opening ports on a firewall", "Redirecting traffic from one network port to another on the same machine", "Tunneling network connections for a specific port through an encrypted SSH session", "Assigning static ports to services"],
              2, "Concepts & Terms (Security)",
              "SSH port forwarding (tunneling) allows redirecting TCP connections destined for a local port through the secure SSH channel to a port on the remote server (or vice-versa), useful for accessing services securely or bypassing firewalls."),

             ("What does PKI stand for?",
              ["Private Key Infrastructure", "Public Key Infrastructure", "Password Key Integration", "Protocol Key Interchange"],
              1, "Concepts & Terms (Security)",
              "PKI encompasses the hardware, software, policies, and procedures needed to create, manage, distribute, use, store, and revoke digital certificates and manage public-key encryption."),

             ("What does PXE stand for?",
              ["Preboot Execution Environment", "Primary Execution Engine", "Protocol Extension Ethernet", "Persistent Xen Environment"],
              0, "Concepts & Terms (System Management)",
              "PXE allows a computer to boot using its network card, loading the operating system or installation environment from a network server instead of a local disk."),

             ("What is Puppet?",
              ["A container runtime", "A version control system", "An automation tool for configuration management using a declarative language", "A network monitoring tool"],
              2, "Concepts & Terms (Automation)",
              "Puppet uses a declarative, model-based approach to define the desired state of infrastructure, which the Puppet agent then enforces on managed nodes."),

            # Q
             ("What are 'Quotas' in Linux?",
              ["User permission levels", "Limits on disk space usage or the number of files per user/group", "CPU usage limits", "Network bandwidth limits"],
              1, "Concepts & Terms (Troubleshooting)",
              "Disk quotas allow administrators to restrict the amount of disk space or the number of files that users or groups can consume on a filesystem."),

            # R
             ("What does RAID stand for?",
              ["Redundant Array of Independent Disks", "Rapid Access Integrated Drive", "Random Access Indexed Disk", "Reliable Array of Inexpensive Drives"], # Both Independent and Inexpensive are common expansions
              0, "Concepts & Terms (System Management)",
              "RAID combines multiple physical disks into a logical unit to improve performance, provide data redundancy (fault tolerance), or both."),

             ("What are 'Regular Expressions' (Regex)?",
              ["Shell command aliases", "Sequences of characters defining a search pattern for text matching", "Filesystem path specifications", "Network address formats"],
              1, "Concepts & Terms (Scripting)",
              "Regular expressions provide a powerful and concise way to describe patterns in text, used extensively by tools like `grep`, `sed`, and `awk`."),

             ("What is 'Routing'?",
              ["Connecting two computers directly", "The process of selecting paths across networks for data packets to travel", "Assigning IP addresses", "Encrypting network traffic"],
              1, "Concepts & Terms (Networking)",
              "Routing involves devices (routers) making decisions based on destination IP addresses to forward packets towards their final destination across interconnected networks."),

             ("What does RPM stand for?",
              ["Red Hat Package Manager", "Remote Procedure Module", "Real-time Process Monitor", "Recursive Program Manager"], # Originally stood for Red Hat Package Manager, now sometimes Recursive acronym
              0, "Concepts & Terms (System Management)",
              "RPM is both a package file format (`.rpm`) and the underlying package management system used by distributions like RHEL, Fedora, CentOS, and SUSE."),

            # S
             ("What is SaltStack?",
              ["A cloud storage provider", "A configuration management and remote execution tool based on Python", "A type of solid-state drive", "A network firewall"],
              1, "Concepts & Terms (Automation)",
              "SaltStack (or Salt) uses a master/minion architecture and YAML configuration files (states) for automating infrastructure management and executing commands remotely."),

             ("What are 'Sandboxed Applications'?",
              ["Applications run directly on the host OS", "Applications run inside virtual machines", "Applications run in a restricted environment with limited access to host resources", "Applications compiled from source"],
              2, "Concepts & Terms (System Management)",
              "Sandboxing isolates applications (like Snaps or Flatpaks) from the host system to enhance security and manage dependencies, limiting their potential impact."),

             ("What is 'Scripting'?",
              ["Compiling source code", "Writing sequences of commands in a file to automate tasks", "Managing user accounts", "Configuring network interfaces"],
              1, "Concepts & Terms (Scripting)",
              "Scripting involves writing programs (scripts) in a scripting language (like Bash, Python, Perl) to automate repetitive or complex tasks."),

             ("What is 'Secure Boot'?",
              ["Encrypting the bootloader", "A security standard (often part of UEFI) ensuring only trusted software is loaded during boot", "Password-protecting the BIOS/UEFI setup", "Scanning for viruses during boot"],
              1, "Concepts & Terms (Security)",
              "Secure Boot uses digital signatures to verify the authenticity of the bootloader, kernel, and drivers loaded during the startup process, preventing malware from hijacking the boot sequence."),

             ("What is SCP?",
              ["Secure Channel Protocol", "System Copy Protocol", "Secure Copy Protocol", "Session Control Protocol"],
              2, "Concepts & Terms (System Management)",
              "SCP uses SSH to securely transfer files between hosts over a network."),

             ("What does SELinux stand for?",
              ["Secure Linux", "Security-Enhanced Linux", "System Enforcement Layer for Linux", "Standard Edition Linux"],
              1, "Concepts & Terms (Security)",
              "SELinux is a Linux kernel security module that provides mechanisms for supporting mandatory access control (MAC) security policies."),

             ("What is SFTP?",
              ["Simple File Transfer Protocol", "Secure File Transfer Protocol", "System File Transfer Protocol", "Standard File Transfer Protocol"],
              1, "Concepts & Terms (System Management)",
              "SFTP (SSH File Transfer Protocol) provides secure file access, transfer, and management capabilities over an SSH connection. It's distinct from FTP/FTPS."),

             ("What does SGID (Set Group ID) permission do on a directory?",
              ["Allows only the owner to delete files", "Makes files created in the directory inherit the directory's group ownership", "Allows anyone to execute files in the directory", "Prevents files from being modified"],
              1, "Concepts & Terms (Security)",
              "When the SGID bit is set on a directory, new files and subdirectories created within it inherit the group ID of the directory, rather than the primary group ID of the user who created them."),

             ("What does SMB stand for?",
              ["System Message Block", "Server Message Block", "Secure Management Bus", "Standard Messaging Bus"],
              1, "Concepts & Terms (System Management)",
              "SMB is a network file sharing protocol primarily used by Windows systems. Linux systems use Samba to interact with SMB/CIFS shares."),

             ("What is a 'Service Mesh'?",
              ["The physical network connecting servers", "A dedicated infrastructure layer for managing service-to-service communication in microservices", "A type of firewall", "A load balancer"],
              1, "Concepts & Terms (Containers)",
              "A service mesh provides features like traffic management, observability, security, and reliability for communication between microservices, often implemented using sidecar proxies."),

             ("What does SSSD stand for?",
              ["Simple Security Services Daemon", "System Security Services Daemon", "Secure Socket Service Director", "Single Sign-on Service Daemon"],
              1, "Concepts & Terms (Security)",
              "SSSD acts as an intermediary between local services and remote identity/authentication providers (like LDAP, Kerberos, Active Directory), providing caching and offline capabilities."),

             ("What does SUID (Set User ID) permission do on an executable file?",
              ["Allows the file owner to execute it", "Makes the file executable by anyone", "Causes the file to run with the privileges of the file's owner, not the user running it", "Prevents the file from being executed"],
              2, "Concepts & Terms (Security)",
              "The SUID bit allows users to run an executable with the permissions of the file owner (often root), used carefully for specific tasks requiring elevated privileges."),

             ("What does SSH stand for?",
              ["Secure Shell", "System Shell", "Secure Socket Hub", "Standard Service Host"],
              0, "Concepts & Terms (System Management)",
              "SSH is a cryptographic network protocol used for secure remote login, command execution, and other secure network services between two networked computers."),

             ("What does SSL stand for?",
              ["Secure Socket Layer", "System Security Layer", "Standard Security Link", "Secure Session Link"],
              0, "Concepts & Terms (Security)",
              "SSL was the predecessor to TLS, providing encrypted communication channels between clients and servers. While the term SSL is still common, TLS is the modern standard."),

             ("What does SSO stand for?",
              ["Secure Sign-On", "Single Sign-On", "System Service Object", "Standard Session Object"],
              1, "Concepts & Terms (Security)",
              "SSO allows users to authenticate once and gain access to multiple independent systems or applications without re-entering credentials."),

             ("What is a 'Stateful' firewall?",
              ["A firewall that only uses static rules", "A firewall that tracks the state of active network connections", "A firewall implemented in hardware", "A firewall that blocks all traffic by default"],
              1, "Concepts & Terms (Security)",
              "Stateful firewalls monitor the state of connections (e.g., TCP handshake status) and make filtering decisions based on this context, allowing return traffic for established connections automatically."),

             ("What is a 'Stateless' firewall?",
              ["A firewall that tracks connection states", "A firewall that examines each packet individually based on static rules, without context of traffic flows", "A firewall that allows all traffic", "A user-space firewall"],
              1, "Concepts & Terms (Security)",
              "Stateless firewalls (or packet filters) make decisions based solely on the information in individual packet headers (IP addresses, ports), without considering whether the packet is part of an existing connection."),

             ("What does the 'Sticky Bit' do when set on a directory?",
              ["Makes the directory read-only", "Prevents anyone from deleting the directory", "Allows only the file owner, directory owner, or root to delete or rename files within that directory", "Causes files to inherit the directory's permissions"],
              2, "Concepts & Terms (Security)",
              "The sticky bit (often seen on `/tmp`) restricts deletion/renaming within a world-writable directory, ensuring users can only remove their own files."),

             ("What does SAN stand for?",
              ["Storage Access Network", "System Area Network", "Storage Area Network", "Secure Access Node"],
              2, "Concepts & Terms (System Management)", # <<< NOTE: The fetched content ended here in the previous turn. Assuming it was meant to be completed.
              "SAN is a dedicated high-speed network connecting servers to shared pools of block-level storage devices."), # Added plausible completion

            # T
             ("What is a 'Target' in systemd?",
              ["A specific service file", "A grouping of systemd units, often representing a system state or synchronization point (like runlevels)", "A network destination", "A hardware device"],
              1, "Concepts & Terms (System Management)",
              "systemd targets (like `multi-user.target`, `graphical.target`) are used to bring the system to a certain state by starting a set of associated services and other units."),

             ("What is Terraform?",
              ["A cloud provider", "An open-source infrastructure as code (IaC) tool", "A container orchestration platform", "A monitoring dashboard"],
              1, "Concepts & Terms (Automation)",
              "Terraform allows users to define and provision infrastructure using a declarative configuration language, managing resources across various cloud providers and platforms."),

             ("What does 'Throughput' measure?",
              ["Network delay (latency)", "The actual rate of data transfer achieved over a connection", "The number of CPU cores", "The amount of disk space used"],
              1, "Concepts & Terms (Troubleshooting)",
              "Throughput is the quantity of data successfully transferred per unit of time, often measured in bits per second (bps) or bytes per second (Bps)."),

             ("What are 'Time Expressions' in systemd Timers?",
              ["Specific dates and times", "Syntax used in `OnCalendar=` directives to specify recurring activation times", "Time intervals measured in seconds", "System uptime values"],
              1, "Concepts & Terms (System Management)",
              "systemd timer units use specific calendar time expressions (e.g., `*-*-* 10:00:00`, `Mon..Fri *-*-* 08:00:00`) to define when a corresponding unit should be activated."),

             ("What is a 'Timer' unit in systemd?",
              ["A unit that measures command execution time", "A unit used to schedule the activation of another unit based on time events", "A unit that sets the system clock", "A unit that monitors system time changes"],
              1, "Concepts & Terms (System Management)",
              "Timer units (`.timer`) provide a flexible way to schedule jobs or services within systemd, similar to cron but integrated with other systemd features."),

             ("What are 'Tokens' in authentication?",
              ["User passwords", "Pieces of data (often temporary) used to authenticate or authorize access without repeatedly sending credentials", "Hardware security devices", "Encryption keys"],
              1, "Concepts & Terms (Security)",
              "Authentication tokens (like session cookies, JWTs, API keys) are issued after initial authentication and presented for subsequent requests to prove identity or permission."),

             ("What does TCP stand for?",
              ["Transfer Control Protocol", "Transmission Control Protocol", "Tunneling Connection Protocol", "Transport Communication Protocol"],
              1, "Concepts & Terms (Networking)",
              "TCP is a fundamental, connection-oriented protocol in the Internet Protocol suite, providing reliable, ordered, and error-checked delivery of data streams."),

             ("What does TLS stand for?",
              ["Transport Layer Security", "Transmission Link Standard", "Tunneling Layer Service", "Terminal Login Security"],
              0, "Concepts & Terms (Security)",
              "TLS is the successor to SSL, providing cryptographic protocols for secure communication over networks, widely used in HTTPS, email, VPNs, etc."),

             ("What is TFTP?",
              ["Tested File Transfer Protocol", "Trivial File Transfer Protocol", "Tunneling File Transfer Protocol", "TCP File Transfer Protocol"],
              1, "Concepts & Terms (Networking)",
              "TFTP is a very simple file transfer protocol using UDP, often used for network booting (PXE) or transferring configurations to network devices due to its small footprint."),

             ("What does 'Troubleshooting' involve?",
              ["Installing new software", "Writing documentation", "The systematic process of identifying, analyzing, and resolving problems", "Optimizing system performance"],
              2, "Concepts & Terms (Troubleshooting)",
              "Troubleshooting is a logical approach to diagnose and fix issues within a system or process."),

             ("What is 'Tunneling' in networking?",
              ["Digging physical tunnels for cables", "Encapsulating one network protocol within another (e.g., VPNs, SSH port forwarding)", "Analyzing network traffic", "Blocking specific network ports"],
              1, "Concepts & Terms (Security)",
              "Tunneling creates a secure or logical path through an underlying network by wrapping packets of one protocol inside packets of another."),

            # U
             ("What does UFW stand for?",
              ["User Firewall", "Unix Firewall", "Uncomplicated Firewall", "Universal Firewall"],
              2, "Concepts & Terms (Security)",
              "UFW provides a simplified interface for managing netfilter (iptables/nftables) firewall rules, aiming for ease of use, especially on Debian/Ubuntu systems."),

             ("What does UEFI stand for?",
              ["Unified Extensible Firmware Interface", "Universal External File Interface", "User Environment Foundation Initialization", "Unix Enhanced Firmware Installer"],
              0, "Concepts & Terms (System Management)",
              "UEFI is a modern specification for the firmware interface between the operating system and platform hardware, replacing the legacy BIOS."),

             ("What are 'Unit Files' in systemd?",
              ["Binary executable files", "Configuration files describing resources managed by systemd (services, sockets, devices, mounts, timers, etc.)", "Log files generated by systemd units", "Temporary files used by services"],
              1, "Concepts & Terms (System Management)",
              "Unit files (ending in `.service`, `.socket`, `.mount`, etc.) define how systemd should manage various system resources and services."),

             ("What does USB stand for?",
              ["Universal System Bus", "Universal Serial Bus", "Unified Service Base", "User Session Backup"],
              1, "Concepts & Terms (System Management)",
              "USB is the standard interface for connecting peripherals (keyboards, mice, printers, storage) to computers."),

             ("What does UUID stand for?",
              ["Universal User Identifier", "Universally Unique Identifier", "Unified Unit ID", "User Utility ID"],
              1, "Concepts & Terms (System Management)",
              "A UUID is a 128-bit number guaranteed to be unique across space and time, often used in Linux to reliably identify block devices or filesystems regardless of device name changes."),

             ("What does UDP stand for?",
              ["User Datagram Protocol", "Universal Data Protocol", "Unified Datagram Packet", "User Directed Protocol"],
              0, "Concepts & Terms (Networking)",
              "UDP is a connectionless protocol in the Internet Protocol suite, offering faster but less reliable data transmission compared to TCP as it lacks error checking and ordering guarantees."),

            # V
             ("What are 'Variables' in scripting?",
              ["Fixed constants", "Placeholders used to store and manipulate data within a script", "External command names", "Input/output file names"],
              1, "Concepts & Terms (Scripting)",
              "Variables allow scripts to store values (numbers, strings) that can change or be reused throughout the script's execution."),

             ("What is 'Version Control'?",
              ["Managing software versions for installation", "Systems for tracking and managing changes to files (especially source code) over time", "Controlling access levels for different users", "Monitoring system resource versions"],
              1, "Concepts & Terms (Automation)",
              "Version Control Systems (VCS) like Git allow developers to record changes, revert to previous states, branch out for experiments, and collaborate effectively."),

             ("What does VM stand for?",
              ["Virtual Memory", "Virtual Machine", "Volume Manager", "Verified Module"],
              1, "Concepts & Terms (General)",
              "A VM is a software emulation of a physical computer system, capable of running its own operating system and applications independently on shared physical hardware."),

             ("What does VNC stand for?",
              ["Virtual Network Computing", "Video Network Card", "Verified Network Connection", "Visual Node Controller"],
              0, "Concepts & Terms (General)",
              "VNC is a graphical desktop sharing system that allows remote control of another computer's desktop environment over a network."),

             ("What is `vmlinuz`?",
              ["A systemd unit file", "The compressed Linux kernel executable file", "A virtual machine manager", "A filesystem checking tool"],
              1, "Concepts & Terms (System Management)",
              "`vmlinuz` (or similar names like `vmlinuz-linux`) is the bootable, usually compressed, binary file containing the core Linux kernel."),

            # W
             ("What is a 'Wildcard Certificate'?",
              ["A certificate valid for any domain name", "A certificate that has expired", "An SSL/TLS certificate valid for a domain and all its direct subdomains (*.example.com)", "A self-signed certificate"],
              2, "Concepts & Terms (Security)",
              "A wildcard certificate secures multiple subdomains under a single domain name using a wildcard character (*) in the common name field."),

            # X
             ("What is 'X11 Forwarding' via SSH?",
              ["Forwarding X11 log messages", "Tunneling the X Window System protocol over SSH to display remote graphical applications locally", "Configuring the X display server", "A type of network packet forwarding"],
              1, "Concepts & Terms (Security)",
              "X11 forwarding allows users logged into a remote server via SSH to run graphical applications on the server and have their windows appear on their local desktop."),

             ("What is XFS?",
              ["An X Window System display manager", "A high-performance journaling filesystem", "A network file sharing protocol", "A version control system"],
              1, "Concepts & Terms (System Management)",
              "XFS is a robust, scalable, high-performance filesystem originally developed by SGI, known for its efficiency with large files and filesystems."),

             ("What does XML stand for?",
              ["Extended Markup Language", "Executable Machine Language", "Extensible Markup Language", "Example Markup Language"],
              2, "Concepts & Terms (Automation)",
              "XML is a markup language defining rules for encoding documents in a format that is both human-readable and machine-readable, often used for data exchange and configuration."),

            # Y
             ("What does YAML stand for?",
              ["Yet Another Markup Language", "YAML Ain't Markup Language", "Young Algorithmic Machine Language", "Yotta Application Meta Language"],
              1, "Concepts & Terms (Automation)",
              "YAML is a human-friendly data serialization standard, commonly used for configuration files in tools like Ansible, Kubernetes, and Docker Compose due to its readability."),

            # Z
             ("What is a 'Zombie Process'?",
              ["A process consuming excessive CPU", "A malicious process", "A process that has terminated but whose entry remains in the process table until the parent collects its status", "A process running with root privileges"],
              2, "Concepts & Terms (Troubleshooting)",
              "Zombie processes (marked with 'Z' in `ps` output) are defunct processes that have finished execution but haven't been properly reaped (waited on) by their parent process."),

             ("What are 'Zones' in firewalld?",
              ["Network subnets", "Predefined sets of firewall rules representing levels of trust for network interfaces or sources", "Specific port ranges", "User groups with firewall permissions"],
              1, "Concepts & Terms (Security)",
              "firewalld uses zones (e.g., public, internal, home, dmz) to apply different security rules based on the trustworthiness of the network a connection originates from."),

             ("What is ZYpp (or zypper)?",
              ["A filesystem type", "The package management system used by SUSE/openSUSE", "A compression utility", "A text editor"],
              1, "Concepts & Terms (System Management)",
              "libzypp is the underlying library, and `zypper` is the command-line interface for package management on SUSE Linux Enterprise and openSUSE distributions."),
        ]

        # Combine all question lists
        self.questions = existing_questions + command_questions + definition_questions
        random.shuffle(self.questions) # Shuffle once on load

        self.categories = set(q[3] for q in self.questions if len(q) > 3) # Ensure index 3 exists
        # Ensure all categories from questions exist in history
        for category in self.categories:
            self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
        # Optional: self.save_history() # Save potentially updated history (might slow down startup)

    def update_history(self, question_text, category, is_correct):
        """Update study history with the result of the answered question."""
        timestamp = datetime.now().isoformat()
        history = self.study_history

        # Overall totals
        history["total_attempts"] = history.get("total_attempts", 0) + 1
        if is_correct:
            history["total_correct"] = history.get("total_correct", 0) + 1

        # Question specific stats
        q_stats = history.setdefault("questions", {}).setdefault(question_text, {"correct": 0, "attempts": 0, "history": []})
        q_stats["attempts"] += 1
        if is_correct:
            q_stats["correct"] += 1
             # Remove from review list if answered correctly
            # Ensure 'incorrect_review' list exists and is a list before modifying
            if isinstance(history.get("incorrect_review"), list) and question_text in history["incorrect_review"]:
                 try:
                    history["incorrect_review"].remove(question_text) # Use list remove method
                 except ValueError:
                    pass # Ignore if somehow not present
        else:
            # Add to review list if incorrect and not already there
            # Ensure 'incorrect_review' list exists and is a list before appending
            if not isinstance(history.get("incorrect_review"), list):
                history["incorrect_review"] = [] # Initialize if missing or wrong type
            if question_text not in history["incorrect_review"]:
                 history["incorrect_review"].append(question_text)

        # Ensure history list exists and is a list
        if not isinstance(q_stats.get("history"), list):
            q_stats["history"] = []
        q_stats["history"].append({"timestamp": timestamp, "correct": is_correct})
        # q_stats["history"] = q_stats["history"][-10:] # Optional: limit history length

        # Category specific stats
        cat_stats = history.setdefault("categories", {}).setdefault(category, {"correct": 0, "attempts": 0})
        cat_stats["attempts"] += 1
        if is_correct:
            cat_stats["correct"] += 1
        # Saving happens elsewhere (end of session, quit, explicit actions)

    def select_question(self, category_filter=None):
        """Select a question, optionally filtered, avoiding recent repeats and using weighting. DOES NOT auto-reset session list."""
        possible_indices = [
            idx for idx, q in enumerate(self.questions)
            if (category_filter is None or (len(q) > 3 and q[3] == category_filter)) # Check length for safety
        ]

        if not possible_indices:
            return None, -1

        available_indices = [idx for idx in possible_indices if idx not in self.answered_indices_session]

        # If all questions in the category/filter have been answered this session, STOP.
        if not available_indices:
             return None, -1 # Return None immediately when list is exhausted

        # --- Weighting Logic ---
        weights = []
        indices_for_weighting = []
        for q_idx in available_indices:
            if q_idx < 0 or q_idx >= len(self.questions): continue # Safety check
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
            # Fallback to simple random choice if weighting fails or no items
            if available_indices:
                 chosen_original_index = random.choice(available_indices)
        else:
            try:
                chosen_original_index = random.choices(indices_for_weighting, weights=weights, k=1)[0]
            except (IndexError, ValueError):
                 # Fallback on error during weighted choice
                 if available_indices:
                     chosen_original_index = random.choice(available_indices)

        if chosen_original_index != -1:
            self.answered_indices_session.append(chosen_original_index) # Mark as answered this session
            # Safety check index before accessing
            if 0 <= chosen_original_index < len(self.questions):
                chosen_question = self.questions[chosen_original_index]
                return chosen_question, chosen_original_index
            else:
                 print(f"{COLOR_ERROR} Error: Chosen index {chosen_original_index} out of bounds. {COLOR_RESET}")
                 return None, -1
        else:
            # Should not happen if available_indices check above works, but safety net
            return None, -1

    def display_question(self, question_data, question_num=None, total_questions=None):
        """Display the question and options with enhanced CLI formatting."""
        if len(question_data) < 5: # Basic validation
             print(f"{COLOR_ERROR} Error: Invalid question data format. {COLOR_RESET}")
             return
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
            except KeyboardInterrupt:
                 print(f"\n{COLOR_WARNING} Session interrupted by user. Quitting session. {COLOR_RESET}")
                 return 'q' # Treat Ctrl+C as quit

    def show_feedback(self, question_data, user_answer_index, original_index):
        """Show feedback based on the user's answer with enhanced CLI formatting."""
        if len(question_data) < 5:
             print(f"{COLOR_ERROR} Error: Invalid question data format for feedback. {COLOR_RESET}")
             return
        _, options, correct_answer_index, category, explanation = question_data
        # Use the original question text from the loaded list for history consistency
        if original_index < 0 or original_index >= len(self.questions):
             print(f"{COLOR_ERROR} Error: Invalid original index for feedback. {COLOR_RESET}")
             # Fallback or handle error appropriately
             original_question_text = "Unknown Question"
        else:
            original_question_text = self.questions[original_index][0]

        is_correct = (user_answer_index == correct_answer_index)

        print() # Add spacing before feedback
        if is_correct:
            print(f"{COLOR_CORRECT}>>> Correct! \U0001F389 <<<{COLOR_RESET}")
            self.score += 1
        else:
            # Ensure indices are valid before accessing options
            if 0 <= correct_answer_index < len(options) and 0 <= user_answer_index < len(options):
                correct_option_text = options[correct_answer_index]
                user_option_text = options[user_answer_index]
                print(f"{COLOR_INCORRECT}>>> Incorrect! \U0001F61E <<<")
                print(f"{COLOR_INCORRECT}    Your answer:      {COLOR_OPTION_NUM}{user_answer_index + 1}.{COLOR_RESET} {COLOR_OPTIONS}{user_option_text}{COLOR_RESET}")
                print(f"{COLOR_CORRECT}    Correct answer was: {COLOR_OPTION_NUM}{correct_answer_index + 1}.{COLOR_RESET} {COLOR_OPTIONS}{correct_option_text}{COLOR_RESET}")
                if explanation:
                     print(f"\n{C['bold']}Explanation:{COLOR_RESET}")
                     # Indent explanation for clarity
                     explanation_lines = explanation.split('\n')
                     for line in explanation_lines:
                         print(f"  {COLOR_EXPLANATION}{line}{COLOR_RESET}")
            else:
                print(f"{COLOR_ERROR} Error displaying feedback: Invalid answer index. {COLOR_RESET}")


        # Update history using the original question text key
        self.update_history(original_question_text, category, is_correct)
        self.total_questions_session += 1
        print()
        try:
            input(f"{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
        except EOFError:
            print(f"\n{COLOR_ERROR} Input interrupted. Continuing... {COLOR_RESET}")
        except KeyboardInterrupt:
             print(f"\n{COLOR_WARNING} Interrupted. Continuing... {COLOR_RESET}")


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
            [(cat, stats) for cat, stats in categories_data.items() if isinstance(stats, dict) and stats.get("attempts", 0) > 0],
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
        attempted_questions = {q: stats for q, stats in question_stats.items() if isinstance(stats, dict) and stats.get("attempts", 0) > 0}

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
                # Check 'history' key exists and is a non-empty list
                if isinstance(stats.get("history"), list) and stats["history"]:
                    # Check the last entry exists and has 'correct' key
                    last_entry = stats["history"][-1]
                    if isinstance(last_entry, dict) and "correct" in last_entry:
                        last_correct = last_entry.get("correct")
                        last_result = "Correct" if last_correct else "Incorrect"
                        last_color = COLOR_CORRECT if last_correct else COLOR_INCORRECT

                display_text = (q_text[:75] + '...') if len(q_text) > 75 else q_text
                print(f"\n  {COLOR_QUESTION}{i+1}. \"{display_text}\"{COLOR_RESET}")
                print(f"     {C['dim']}({COLOR_STATS_VALUE}{attempts}{C['dim']} attempts, {acc_color}{accuracy:.1f}%{C['dim']} acc.) Last: {last_color}{last_result}{C['dim']}){COLOR_RESET}")

        print()
        cli_print_separator(color=COLOR_BORDER)
        try:
            input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        except EOFError:
             print(f"\n{COLOR_ERROR} Input interrupted. Returning to menu... {COLOR_RESET}")
        except KeyboardInterrupt:
             print(f"\n{COLOR_WARNING} Interrupted. Returning to menu... {COLOR_RESET}")

    def select_category(self):
        """Allow the user to select a category to focus on, using enhanced CLI."""
        self.clear_screen()
        cli_print_header("Select a Category")
        # Convert set to list for reliable sorting
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
            except KeyboardInterrupt:
                 print(f"\n{COLOR_WARNING} Interrupted. Returning to main menu. {COLOR_RESET}")
                 return 'b' # Treat Ctrl+C as back

    def clear_stats(self):
        """Clear all stored statistics after confirmation with enhanced CLI."""
        self.clear_screen()
        cli_print_header("Clear Statistics", char='!', color=COLOR_ERROR)
        print(f"\n{COLOR_WARNING} This action will permanently delete ALL study history,")
        print(f"{COLOR_WARNING} including question performance and the list of incorrect answers.")
        print(f"{COLOR_WARNING} This cannot be undone. {COLOR_RESET}")
        confirm = ''
        try:
            confirm = input(f"{COLOR_PROMPT}Are you sure you want to proceed? ({COLOR_OPTIONS}yes{COLOR_PROMPT}/{COLOR_OPTIONS}no{COLOR_PROMPT}): {COLOR_INPUT}").lower().strip()
            print(COLOR_RESET, end='') # Reset color
        except (EOFError, KeyboardInterrupt):
             print(f"\n{COLOR_WARNING} Clear operation cancelled. {COLOR_RESET}")
             confirm = 'no' # Treat interrupt as 'no'

        if confirm == 'yes':
            self.study_history = self._default_history()
            # Re-populate categories with 0 stats
            for category in self.categories:
                 self.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.save_history() # Save the cleared history
            print(f"\n{COLOR_CORRECT}>>> Study history has been cleared. <<<{COLOR_RESET}")
        else:
            print(f"\n{COLOR_INFO}Operation cancelled. History not cleared.{COLOR_RESET}")

        print()
        try:
            input(f"{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        except (EOFError, KeyboardInterrupt):
             print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")

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
            try:
                 input(f"{COLOR_PROMPT}Press Enter to start...{COLOR_RESET}")
            except (EOFError, KeyboardInterrupt):
                 print(f"\n{COLOR_WARNING} Quiz cancelled. Returning to menu. {COLOR_RESET}")
                 return # Exit if interrupted before starting


        # --- Calculate total questions for the current filter ---
        if category_filter is None:
            # If no filter, total is all questions
            total_questions_in_filter = len(self.questions)
        else:
            # Count questions matching the filter
            total_questions_in_filter = sum(1 for q in self.questions if len(q) > 3 and q[3] == category_filter) # Check length

        if total_questions_in_filter == 0:
             print(f"{COLOR_WARNING}Warning: No questions found for the selected filter: {category_filter}. Returning to menu.{COLOR_RESET}")
             time.sleep(3)
             # No need to proceed if there are no questions
             self.save_history() # Save history before returning
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
                print(f"\n{COLOR_INFO} Quitting quiz session. {COLOR_RESET}")
                break # Exit the while loop
            elif user_answer == 's':
                print(f"\n{COLOR_INFO}Skipping question...{COLOR_RESET}")
                # Skipping does NOT increment total_questions_session (answered count)
                # It also doesn't update history
                try:
                    input(f"\n{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{COLOR_WARNING} Interrupted. Continuing... {COLOR_RESET}")
                continue # Go to next iteration of the while loop

            # --- Process Answer (Only if not skipped or quit) ---
            if len(question_data) < 5: # Validation
                print(f"{COLOR_ERROR} Error: Invalid question data during processing. Skipping. {COLOR_RESET}")
                continue
            _, _, correct_answer_index, category, _ = question_data
            # Validate original_index before accessing self.questions
            if original_index < 0 or original_index >= len(self.questions):
                 print(f"{COLOR_ERROR} Error: Invalid original index ({original_index}). Skipping history update. {COLOR_RESET}")
                 # Handle this case - maybe skip history update or try a fallback?
                 original_question_text = "Error: Unknown Question Text" # Placeholder
            else:
                 original_question_text = self.questions[original_index][0] # Use the canonical text

            is_correct = (user_answer == correct_answer_index)

            # Update history and session *answered* count (Done inside show_feedback/manually for verify)

            if mode == QUIZ_MODE_STANDARD:
                # show_feedback updates total_questions_session internally and calls update_history
                self.show_feedback(question_data, user_answer, original_index) # Shows feedback immediately
            else: # QUIZ_MODE_VERIFY
                # Store the result, don't show feedback yet
                self.verify_session_answers.append((question_data, user_answer, is_correct))
                # Manually update session answered count for verify mode
                self.total_questions_session += 1
                # Update history for verify mode here
                self.update_history(original_question_text, category, is_correct)
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
        try:
            input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")


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
            if len(q_data) < 5: continue # Safety skip
            q_text, options, correct_idx, _, explanation = q_data
            print(f"\n{COLOR_QUESTION}{i+1}. {q_text}{COLOR_RESET}")

            # Validate indices before accessing options
            if 0 <= user_answer_idx < len(options) and 0 <= correct_idx < len(options):
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
            else:
                print(f"  {COLOR_ERROR} Error displaying details for this question: Invalid index. {COLOR_RESET}")


    def review_incorrect_answers(self):
        """Allows the user to review questions they previously answered incorrectly (CLI - Basic View)."""
        self.clear_screen()
        cli_print_header("Review Incorrect Answers")
        # Ensure incorrect_review exists and is a list
        incorrect_list = self.study_history.get("incorrect_review", [])
        if not isinstance(incorrect_list, list):
            incorrect_list = []
            self.study_history["incorrect_review"] = [] # Fix in history if needed

        if not incorrect_list:
            print(f"\n{COLOR_INFO}You haven't marked any questions as incorrect yet, or your history was cleared.{COLOR_RESET}")
            print(f"{COLOR_INFO}Keep practicing!{COLOR_RESET}")
            try:
                input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
            except (EOFError, KeyboardInterrupt):
                 print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")
            return

        # Find the full question data based on the text stored in incorrect_review
        questions_to_review = []
        not_found_questions = []
        # Create a temporary copy to iterate over, allowing removal from original
        incorrect_list_copy = list(incorrect_list)
        questions_to_remove_from_history = [] # Track questions not found

        for incorrect_text in incorrect_list_copy:
            found = False
            for q_data in self.questions:
                 # Check if q_data is valid and has at least one element (the text)
                 if isinstance(q_data, (list, tuple)) and len(q_data) > 0 and q_data[0] == incorrect_text:
                    questions_to_review.append(q_data)
                    found = True
                    break
            if not found:
                 not_found_questions.append(incorrect_text)
                 print(f"{COLOR_WARNING} Could not find full data for question: {incorrect_text[:50]}... (Maybe removed from source?){COLOR_RESET}")
                 questions_to_remove_from_history.append(incorrect_text)


        # Remove not found questions from the actual history list
        history_changed = False
        if questions_to_remove_from_history:
             # Filter the list directly
             original_len = len(self.study_history.get("incorrect_review", []))
             self.study_history["incorrect_review"] = [
                 q_text for q_text in self.study_history.get("incorrect_review", [])
                 if q_text not in questions_to_remove_from_history
             ]
             if len(self.study_history["incorrect_review"]) != original_len:
                  history_changed = True


        if not questions_to_review:
             print(f"\n{COLOR_ERROR} Could not load data for any incorrect questions. {COLOR_RESET}")
             if history_changed:
                  self.save_history() # Save history if items were removed
             try:
                input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
             except (EOFError, KeyboardInterrupt):
                  print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")
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
                 # Check if q_data has text before accessing
                 if isinstance(q_data, (list, tuple)) and len(q_data) > 0:
                     q_text_short = (q_data[0][:60] + '...') if len(q_data[0]) > 60 else q_data[0]
                     print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_OPTIONS}{q_text_short}{COLOR_RESET}")
                 else:
                      print(f"  {COLOR_OPTION_NUM}{i + 1}.{COLOR_RESET} {COLOR_ERROR} [Invalid Question Data] {COLOR_RESET}")

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
                    # Check if question data is valid before accessing text
                    if isinstance(questions_to_review[item_to_clear], (list, tuple)) and len(questions_to_review[item_to_clear]) > 0:
                        question_to_clear_text = questions_to_review[item_to_clear][0]
                        confirm_clear = input(f"{COLOR_PROMPT}Clear question {item_to_clear+1} from the incorrect review list? ({COLOR_OPTIONS}yes{COLOR_PROMPT}/{COLOR_OPTIONS}no{COLOR_PROMPT}): {COLOR_INPUT}").lower().strip()
                        if confirm_clear == 'yes':
                             # Ensure list exists and is a list before removing
                            if isinstance(self.study_history.get("incorrect_review"), list) and question_to_clear_text in self.study_history["incorrect_review"]:
                                 self.study_history["incorrect_review"].remove(question_to_clear_text)
                                 history_changed = True # Mark history as changed
                                 print(f"{COLOR_CORRECT}Question removed from review list.{COLOR_RESET}")
                                 # Remove from the current display list as well
                                 del questions_to_review[item_to_clear]
                                 time.sleep(1.5)
                            else:
                                 print(f"{COLOR_ERROR}Error: Question text not found in history's incorrect list anymore?{COLOR_RESET}")
                                 # Also remove from display list if it's somehow missing from history
                                 try:
                                      del questions_to_review[item_to_clear]
                                 except IndexError:
                                      pass # Ignore if index already invalid
                                 time.sleep(2)
                        else:
                            print(f"{COLOR_INFO}Clear cancelled.{COLOR_RESET}")
                            time.sleep(1)
                    else:
                         print(f"{COLOR_ERROR} Cannot clear invalid question data. {COLOR_RESET}")
                         time.sleep(2)
                    continue # Go back to list display


                # --- Display selected question ---
                num_choice = int(choice)
                if 1 <= num_choice <= len(questions_to_review):
                    self.clear_screen()
                    cli_print_header("Reviewing Question")
                    selected_q_data = questions_to_review[num_choice-1]
                    if len(selected_q_data) < 5: # Validation
                         print(f"{COLOR_ERROR} Error: Invalid data for selected question. {COLOR_RESET}")
                         time.sleep(2)
                         continue

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
                    try:
                        input(f"\n{COLOR_PROMPT}Press Enter to return to the review list...{COLOR_RESET}")
                    except (EOFError, KeyboardInterrupt):
                         print(f"\n{COLOR_WARNING} Returning to list... {COLOR_RESET}")
                         continue # Continue the loop to re-display list

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
            except KeyboardInterrupt:
                 print(f"\n{COLOR_WARNING} Interrupted. Returning to main menu. {COLOR_RESET}")
                 current_choice = 'b' # Treat Ctrl+C as back
                 break

        # Save history if any items were removed due to not being found or cleared by user
        if history_changed:
             self.save_history()


    def export_study_data(self):
        """Exports study history data (JSON export)."""
        self.clear_screen()
        cli_print_header("Export Study Data (History)")

        default_filename = f"linux_plus_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_filename = default_filename # Default value
        try:
            prompt = f"{COLOR_PROMPT}Enter filename for export ({COLOR_INFO}default: {default_filename}{COLOR_PROMPT}): {COLOR_INPUT}"
            filename_input = input(prompt).strip()
            print(COLOR_RESET, end='')
            export_filename = filename_input if filename_input else default_filename
        except (EOFError, KeyboardInterrupt):
             print(f"\n{COLOR_WARNING} Export cancelled. {COLOR_RESET}")
             try: input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
             except: pass
             return


        # Basic validation
        if not export_filename.lower().endswith(".json"):
             export_filename += ".json"

        try:
            export_path = os.path.abspath(export_filename) # Get full path
            print(f"\n{COLOR_INFO}Attempting to export history data to: {COLOR_STATS_VALUE}{export_path}{COLOR_RESET}")
            with open(export_filename, 'w', encoding='utf-8') as f: # Use encoding
                json.dump(self.study_history, f, indent=2)
            print(f"\n{COLOR_CORRECT}>>> Study history successfully exported to {export_filename} <<<{COLOR_RESET}")
        except IOError as e:
            print(f"\n{COLOR_ERROR}Error exporting history: {e}{COLOR_RESET}")
            print(f"{COLOR_ERROR}Please check permissions and filename.{COLOR_RESET}")
        except Exception as e:
             print(f"\n{COLOR_ERROR}An unexpected error occurred during history export: {e}{COLOR_RESET}")

        try:
             input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")

    # --- NEW METHOD: Export Questions and Answers to MD ---
    def export_questions_answers_md(self):
        """Exports all loaded questions and answers to a Markdown file."""
        self.clear_screen() # Optional: Clear screen in CLI
        cli_print_header("Export Questions & Answers to Markdown")

        # Check if there are questions loaded
        if not self.questions:
             print(f"\n{COLOR_WARNING}No questions are currently loaded to export.{COLOR_RESET}")
             try: input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
             except: pass
             return

        default_filename = f"Linux_plus_QA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        export_filename = default_filename # Default
        try:
            prompt = f"{COLOR_PROMPT}Enter filename for export ({COLOR_INFO}default: {default_filename}{COLOR_PROMPT}): {COLOR_INPUT}"
            filename_input = input(prompt).strip()
            print(COLOR_RESET, end='')
            export_filename = filename_input if filename_input else default_filename
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_WARNING} Export cancelled. {COLOR_RESET}")
            try: input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
            except: pass
            return

        # Ensure it ends with .md
        if not export_filename.lower().endswith(".md"):
             export_filename += ".md"

        try:
            export_path = os.path.abspath(export_filename)
            print(f"\n{COLOR_INFO}Attempting to export Q&A to: {COLOR_STATS_VALUE}{export_path}{COLOR_RESET}")

            with open(export_filename, 'w', encoding='utf-8') as f:
                # --- Write Questions Section ---
                f.write("# Questions\n\n")
                for i, q_data in enumerate(self.questions):
                    if len(q_data) < 5: continue # Safety skip malformed data
                    question_text, options, _, category, _ = q_data
                    f.write(f"**Q{i+1}.** ({category})\n") # Add category like in the example
                    f.write(f"{question_text}\n")
                    # Add options with letters
                    for j, option in enumerate(options):
                        f.write(f"   {chr(ord('A') + j)}. {option}\n")
                    f.write("\n") # Blank line after each question

                f.write("---\n\n") # Separator

                # --- Write Answers Section ---
                f.write("# Answers\n\n")
                for i, q_data in enumerate(self.questions):
                    if len(q_data) < 5: continue # Safety skip malformed data
                    _, options, correct_answer_index, _, explanation = q_data
                    # Validate index before using
                    if 0 <= correct_answer_index < len(options):
                        correct_option_letter = chr(ord('A') + correct_answer_index)
                        correct_option_text = options[correct_answer_index]

                        f.write(f"**A{i+1}.** {correct_option_letter}. {correct_option_text}\n")
                        if explanation:
                            # Indent explanation slightly for readability in Markdown
                            explanation_lines = explanation.split('\n')
                            f.write("   *Explanation:*")
                            first_line = True
                            for line in explanation_lines:
                               if not first_line:
                                    f.write("   ") # Indent subsequent lines
                               f.write(f" {line.strip()}\n") # Add space before each line, strip extra whitespace
                               first_line = False
                        f.write("\n\n") # Blank line after each answer block
                    else:
                         f.write(f"**A{i+1}.** Error: Invalid correct answer index.\n\n")


            print(f"{COLOR_CORRECT}>>> Questions & Answers successfully exported to {export_filename} <<<{COLOR_RESET}")

        except IOError as e:
            print(f"\n{COLOR_ERROR}Error exporting Q&A: {e}{COLOR_RESET}")
            print(f"{COLOR_ERROR}Please check permissions and filename.{COLOR_RESET}")
        except Exception as e:
             print(f"\n{COLOR_ERROR}An unexpected error occurred during Q&A export: {e}{COLOR_RESET}")

        try:
            input(f"\n{COLOR_PROMPT}Press Enter to return to the main menu...{COLOR_RESET}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{COLOR_WARNING} Returning to menu... {COLOR_RESET}")
    # --- END NEW METHOD ---

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
        try:
            input(f"{COLOR_PROMPT}Press Enter to continue...{COLOR_RESET}")
        except (EOFError, KeyboardInterrupt):
             print(f"\n{COLOR_WARNING} Exiting... {COLOR_RESET}")
             self.save_history()
             sys.exit(0)


    # --- MODIFIED main_menu ---
    def main_menu(self):
        """Display the main menu and handle user choices for CLI."""
        while True:
            self.clear_screen()
            cli_print_header("MAIN MENU", char='*', length=60)
            print(f"\n{COLOR_OPTIONS}Please choose an option:{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}1.{COLOR_RESET} {COLOR_OPTIONS}Start Quiz (Standard){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}2.{COLOR_RESET} {COLOR_OPTIONS}Quiz by Category (Standard){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}3.{COLOR_RESET} {COLOR_OPTIONS}Verify Knowledge (Category/All){COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}4.{COLOR_RESET} {COLOR_OPTIONS}Review Incorrect Answers{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}5.{COLOR_RESET} {COLOR_OPTIONS}View Statistics{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}6.{COLOR_RESET} {COLOR_OPTIONS}Export Study Data (History){COLOR_RESET}") # Renamed
            # --- New Option ---
            print(f"  {COLOR_OPTION_NUM}7.{COLOR_RESET} {COLOR_OPTIONS}Export Questions & Answers (MD){COLOR_RESET}")
            # --- Renumber subsequent options ---
            print(f"  {COLOR_OPTION_NUM}8.{COLOR_RESET} {COLOR_OPTIONS}Exit{COLOR_RESET}")
            print(f"  {COLOR_OPTION_NUM}9.{COLOR_RESET} {COLOR_WARNING}Clear All Statistics{COLOR_RESET}")
            cli_print_separator(color=COLOR_BORDER)

            choice = ''
            try:
                choice = input(f"{COLOR_PROMPT}Enter your choice: {COLOR_INPUT}")
                print(COLOR_RESET, end='') # Reset color
            except (EOFError, KeyboardInterrupt):
                print(f"\n{COLOR_WARNING} Exiting... {COLOR_RESET}")
                choice = '8' # Treat interrupt as exit

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
                self.export_study_data() # Call the history export function
            # --- Handle New Option ---
            elif choice == '7':
                self.export_questions_answers_md() # Call the new Q&A export method
            # --- Handle Renumbered Options ---
            elif choice == '8':
                print(f"\n{COLOR_INFO}Saving history and quitting. Goodbye!{COLOR_RESET}")
                self.save_history()
                sys.exit()
            elif choice == '9':
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
        # --- MODIFIED: Renamed History Export Button ---
        self.export_history_button = ttk.Button(main_actions, text="Export History", command=self._export_data_gui, style="TButton")
        self.export_history_button.pack(side=tk.LEFT, padx=5)
        # --- NEW: Q&A Export Button ---
        self.export_qa_button = ttk.Button(main_actions, text="Export Q&A", command=self._export_questions_answers_gui, style="TButton")
        self.export_qa_button.pack(side=tk.LEFT, padx=5)
        # --- End New Button ---
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

        # Enable/Disable Review based on history content
        incorrect_list = self.game_logic.study_history.get("incorrect_review", [])
        self.review_button.config(state=tk.NORMAL if isinstance(incorrect_list, list) and incorrect_list else tk.DISABLED)

        # History export can always be enabled
        self.export_history_button.config(state=tk.NORMAL)
        # Q&A export enabled if questions are loaded
        self.export_qa_button.config(state=tk.NORMAL if self.game_logic.questions else tk.DISABLED)


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
                self.total_questions_in_filter_gui = sum(1 for q in self.game_logic.questions if len(q)>3 and q[3] == self.current_category_filter) # Check length

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
            # self._update_question_count_label() # Clear count label after session ends? No, keep final.
            self.game_logic.save_history() # Save history at the end
            # Update button states for Review/Export if history changed
            incorrect_list = self.game_logic.study_history.get("incorrect_review", [])
            self.review_button.config(state=tk.NORMAL if isinstance(incorrect_list, list) and incorrect_list else tk.DISABLED)
            return

        # --- Display the actual question ---
        self._clear_quiz_area(clear_question=True, clear_options=True, clear_feedback=True, clear_explanation=True)
        if len(self.current_question_data) < 5: # Validation
             self._update_status("Error: Invalid question data.")
             self._load_initial_state() # Go back to welcome
             return
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
        # Focus first radio button? Might be better UX.
        if self.options_frame.winfo_children():
            try:
                self.options_frame.winfo_children()[0].focus_set()
            except tk.TclError: # Handle potential focus issues
                pass


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
            # Silently ignore if no answer selected and button somehow clicked
            return

        if not self.current_question_data or len(self.current_question_data) < 5:
            # Instead of error, maybe just disable button? Or return to idle?
            self._update_status("Error: No valid question data.")
            self._load_initial_state()
            return

        # --- Get question details ---
        q_text, options, correct_answer_index, category, explanation = self.current_question_data
        # Ensure we use the canonical question text for history
        # Validate original index before using it
        if self.current_question_index < 0 or self.current_question_index >= len(self.game_logic.questions):
             self._update_status("Error: Invalid question index.")
             # Fallback: Use displayed text (might be inconsistent if questions change)
             original_question_text = q_text
             # Or better: log error and potentially stop quiz?
             self.quiz_active = False
             messagebox.showerror("Internal Error", "Invalid question index encountered. Stopping quiz.", parent=self.root)
             self._load_initial_state()
             return
        else:
             original_question_text = self.game_logic.questions[self.current_question_index][0]

        is_correct = (user_answer_index == correct_answer_index)

        # --- Update History (Common to both modes) ---
        self.game_logic.update_history(original_question_text, category, is_correct)
        # Update review button state immediately after history update
        incorrect_list = self.game_logic.study_history.get("incorrect_review", [])
        self.review_button.config(state=tk.NORMAL if isinstance(incorrect_list, list) and incorrect_list else tk.DISABLED)
        # Increment counters
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
                # Ensure index is valid before accessing
                if 0 <= correct_answer_index < len(options):
                    correct_option_text = options[correct_answer_index]
                    feedback_text = f"Incorrect. \U0001F61E Correct was: {correct_answer_index + 1}. {correct_option_text}"
                    self.feedback_label.config(text=feedback_text, style="Incorrect.Feedback.TLabel")
                else:
                    self.feedback_label.config(text="Incorrect (Error displaying correct option)", style="Incorrect.Feedback.TLabel")


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
            [(cat, stats) for cat, stats in categories_data.items() if isinstance(stats, dict) and stats.get("attempts", 0) > 0],
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
        attempted_questions = {q: stats for q, stats in question_stats.items() if isinstance(stats, dict) and stats.get("attempts", 0) > 0}

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
                if isinstance(stats.get("history"), list) and stats["history"]:
                    last_entry = stats["history"][-1]
                    if isinstance(last_entry, dict) and "correct" in last_entry:
                        last_correct = last_entry.get("correct")
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
                if len(q_data) < 5: continue # Safety skip
                q_text, options, correct_idx, _, explanation = q_data
                results_text.insert(tk.END, f"{i+1}. {q_text}\n", "q_text")

                 # Validate indices before accessing options
                if 0 <= user_answer_idx < len(options) and 0 <= correct_idx < len(options):
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
                else:
                     results_text.insert(tk.END, f"Error displaying details: Invalid index.\n", "incorrect")
                     results_text.insert(tk.END, f"{'.'*50}\n", "separator")


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
            # Re-populate categories with 0 stats just in case logic changes
            for category in self.game_logic.categories:
                 self.game_logic.study_history["categories"].setdefault(category, {"correct": 0, "attempts": 0})
            self.game_logic.save_history()
            messagebox.showinfo("Stats Cleared", "Study history has been cleared.", parent=self.root)
            self._update_status("Study history cleared.")
            # Disable review button as list is now empty
            self.review_button.config(state=tk.DISABLED)

    # --- MODIFIED _review_incorrect_gui ---
    def _review_incorrect_gui(self):
        """Allows reviewing incorrect answers in the GUI (Basic View)."""
        incorrect_list = self.game_logic.study_history.get("incorrect_review", [])
        # Ensure it's a list
        if not isinstance(incorrect_list, list):
             incorrect_list = []
             self.game_logic.study_history["incorrect_review"] = [] # Fix in history

        if not incorrect_list:
            messagebox.showinfo("Review Incorrect", "No incorrect answers recorded in history.", parent=self.root)
            return

        # Find the full question data
        questions_to_review = []
        not_found_questions = []
        questions_to_remove_from_history = []
        # Create a temporary copy to iterate over
        incorrect_list_copy = list(incorrect_list)

        for incorrect_text in incorrect_list_copy:
             found = False
             for q_data in self.game_logic.questions:
                 if isinstance(q_data, (list, tuple)) and len(q_data) > 0 and q_data[0] == incorrect_text:
                     questions_to_review.append(q_data)
                     found = True
                     break
             if not found:
                 not_found_questions.append(incorrect_text)
                 questions_to_remove_from_history.append(incorrect_text)


        # Remove not found questions from the actual history list
        history_changed = False # Initialize flag here
        if questions_to_remove_from_history:
             original_len = len(self.game_logic.study_history.get("incorrect_review", []))
             self.game_logic.study_history["incorrect_review"] = [
                 q_text for q_text in self.game_logic.study_history.get("incorrect_review", [])
                 if q_text not in questions_to_remove_from_history
             ]
             if len(self.game_logic.study_history["incorrect_review"]) != original_len:
                  history_changed = True
             # Update main button immediately if list is now empty
             if not self.game_logic.study_history.get("incorrect_review", []):
                 self.review_button.config(state=tk.DISABLED)

        if not questions_to_review and not_found_questions:
             # Only show error if questions were expected but not found
             messagebox.showerror("Review Error", "Could not load data for any previously incorrect questions. They may have been removed from the source.", parent=self.root)
             if history_changed:
                  self.game_logic.save_history() # Save history if items were removed
             return
        elif not questions_to_review:
             # This case means the list was initially empty or became empty after removing missing questions
             messagebox.showinfo("Review Incorrect", "No incorrect answers available to review.", parent=self.root)
             if history_changed:
                  self.game_logic.save_history()
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

        # Main content frame using pack
        review_frame = ttk.Frame(review_win, padding="15")
        review_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP) # Pack this first
        review_frame.rowconfigure(1, weight=1) # Make text area expand within grid
        review_frame.columnconfigure(0, weight=1)

        # Header (using grid inside review_frame)
        ttk.Label(review_frame, text="Incorrectly Answered Questions", style="Header.TLabel").grid(row=0, column=0, pady=(0,15), sticky="w")

        # Display Area (ScrolledText using grid inside review_frame)
        review_text = scrolledtext.ScrolledText(review_frame, wrap=tk.WORD, font=self.fonts["base"], # Use base font
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
                 if len(q_data) < 5: continue # Safety skip malformed
                 q_text, options, correct_idx, category, explanation = q_data
                 review_text.insert(tk.END, f"{i+1}. {q_text}\n", "q_text")
                 review_text.insert(tk.END, f"Category: {category}\n", "category")

                 for j, option in enumerate(options):
                     # Validate index
                     if 0 <= correct_idx < len(options):
                         if j == correct_idx:
                             review_text.insert(tk.END, f"   \u2714 {option} (Correct Answer)\n", "correct_option") # Checkmark
                         else:
                             review_text.insert(tk.END, f"   \u2022 {option}\n", "option") # Bullet
                     else: # Handle invalid correct_idx case if needed
                          review_text.insert(tk.END, f"   \u2022 {option}\n", "option") # Default display

                 if explanation:
                     review_text.insert(tk.END, f"Explanation: {explanation}\n", "explanation")

                 review_text.insert(tk.END, f"{'-'*50}\n", "separator")

            if not_found_questions:
                 review_text.insert(tk.END, "\nWarning: Some questions previously marked incorrect could not be found (they might have been removed from the source data and were removed from this list):\n", "warning")
                 for nf_text in not_found_questions:
                     review_text.insert(tk.END, f"- {nf_text[:80]}...\n", "warning")
            review_text.config(state=tk.DISABLED) # Make read-only

        populate_review_text() # Initial population

        # --- Action Buttons Frame (using pack inside review_win) ---
        button_frame = ttk.Frame(review_win, style="TFrame")
        button_frame.pack(pady=(10, 15), fill='x', side=tk.BOTTOM) # Pack this at the bottom

        # --- Buttons (using pack inside button_frame) ---
        # nonlocal history_changed # <<< REMOVED from here

        def clear_item_from_review_list():
            nonlocal history_changed # <<< MOVED here, start of function scope
            # Simple approach: Ask user which number to clear
            num_str = simpledialog.askstring("Clear Item", "Enter the number of the question to remove from this review list:", parent=review_win)
            if num_str:
                try:
                    num_to_clear = int(num_str) - 1 # Convert to 0-based index
                    if 0 <= num_to_clear < len(questions_to_review):
                        # Check if question data is valid before accessing text
                        if isinstance(questions_to_review[num_to_clear], (list, tuple)) and len(questions_to_review[num_to_clear]) > 0:
                            question_to_clear_text = questions_to_review[num_to_clear][0]
                            if messagebox.askyesno("Confirm Clear", f"Remove question {num_to_clear+1} from the review list?", parent=review_win):
                                 # Ensure list exists and is a list before removing
                                if isinstance(self.game_logic.study_history.get("incorrect_review"), list) and question_to_clear_text in self.game_logic.study_history["incorrect_review"]:
                                    self.game_logic.study_history["incorrect_review"].remove(question_to_clear_text)
                                    history_changed = True # Assign *after* nonlocal declaration
                                    messagebox.showinfo("Cleared", "Question removed from review list.", parent=review_win)
                                    # Remove from the list used by this window and refresh display
                                    del questions_to_review[num_to_clear]
                                    populate_review_text() # Refresh the text widget
                                    # Update main window button state if list becomes empty
                                    if not self.game_logic.study_history.get("incorrect_review", []):
                                         self.review_button.config(state=tk.DISABLED)
                                         # Disable clear button if list is now empty
                                         clear_button.config(state=tk.DISABLED)
                                else:
                                     messagebox.showerror("Error", "Question not found in history list.", parent=review_win)
                        else:
                             messagebox.showerror("Error", "Cannot clear invalid question data.", parent=review_win)
                    else:
                        messagebox.showwarning("Invalid Number", f"Please enter a number between 1 and {len(questions_to_review)}.", parent=review_win)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.", parent=review_win)

        clear_button_state = tk.NORMAL if questions_to_review else tk.DISABLED
        clear_button = ttk.Button(button_frame, text="Clear Item from List", command=clear_item_from_review_list, style="TButton", width=20, state=clear_button_state)
        clear_button.pack(side=tk.LEFT, padx=(15, 5)) # Add padding

        close_button = ttk.Button(button_frame, text="Close", style="TButton", width=12)
        close_button.pack(side=tk.RIGHT, padx=(5, 15)) # Add padding

        # Save history when closing the window if changes were made
        def on_close():
             if history_changed:
                  self.game_logic.save_history()
             review_win.destroy()
        review_win.protocol("WM_DELETE_WINDOW", on_close)
        # Also assign the command to the button
        close_button.config(command=on_close)


        self.root.wait_window(review_win)

    def _export_data_gui(self):
        """Exports study history data via GUI using asksaveasfilename."""
        initial_filename = f"linux_plus_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        export_filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Study History", # Updated title
            initialfile=initial_filename,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not export_filename:
            self._update_status("History export cancelled.")
            return # User cancelled

        try:
            export_path = os.path.abspath(export_filename)
            self._update_status(f"Exporting history to {os.path.basename(export_path)}...")
            self.root.update_idletasks() # Update status label before potential delay

            with open(export_filename, 'w', encoding='utf-8') as f: # Use encoding
                json.dump(self.game_logic.study_history, f, indent=2)

            messagebox.showinfo("Export Successful", f"Study history successfully exported to:\n{export_path}", parent=self.root)
            self._update_status("History export successful.")

        except IOError as e:
            messagebox.showerror("Export Error", f"Error exporting history: {e}\nPlease check permissions and filename.", parent=self.root)
            self._update_status("History export failed.")
        except Exception as e:
             messagebox.showerror("Export Error", f"An unexpected error occurred during history export: {e}", parent=self.root)
             self._update_status("History export failed.")

    def _export_questions_answers_gui(self):
        """Exports loaded questions and answers via GUI using asksaveasfilename."""
        # Check if there are questions loaded
        if not self.game_logic.questions:
             messagebox.showwarning("Export Q&A", "No questions are currently loaded to export.", parent=self.root)
             # Disable button if no questions? Update state maybe.
             self.export_qa_button.config(state=tk.DISABLED)
             return

        initial_filename = f"Linux_plus_QA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        export_filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Export Questions & Answers",
            initialfile=initial_filename,
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not export_filename:
            self._update_status("Q&A export cancelled.")
            return # User cancelled

        try:
            export_path = os.path.abspath(export_filename)
            self._update_status(f"Exporting Q&A to {os.path.basename(export_path)}...")
            self.root.update_idletasks()

            with open(export_filename, 'w', encoding='utf-8') as f:
                # --- Write Questions Section (Same logic as CLI method) ---
                f.write("# Questions\n\n")
                for i, q_data in enumerate(self.game_logic.questions):
                    if len(q_data) < 5: continue # Safety skip
                    question_text, options, _, category, _ = q_data
                    f.write(f"**Q{i+1}.** ({category})\n")
                    f.write(f"{question_text}\n")
                    for j, option in enumerate(options):
                        f.write(f"   {chr(ord('A') + j)}. {option}\n")
                    f.write("\n")

                f.write("---\n\n")

                # --- Write Answers Section (Same logic as CLI method) ---
                f.write("# Answers\n\n")
                for i, q_data in enumerate(self.game_logic.questions):
                     if len(q_data) < 5: continue # Safety skip
                     _, options, correct_answer_index, _, explanation = q_data
                     # Validate index before using
                     if 0 <= correct_answer_index < len(options):
                         correct_option_letter = chr(ord('A') + correct_answer_index)
                         correct_option_text = options[correct_answer_index]
                         f.write(f"**A{i+1}.** {correct_option_letter}. {correct_option_text}\n")
                         if explanation:
                             explanation_lines = explanation.split('\n')
                             f.write("   *Explanation:*")
                             first_line = True
                             for line in explanation_lines:
                                 if not first_line:
                                      f.write("   ") # Indent subsequent lines
                                 f.write(f" {line.strip()}\n") # Add space before each line, strip extra whitespace
                                 first_line = False
                         f.write("\n\n") # Blank line after each answer block
                     else:
                          f.write(f"**A{i+1}.** Error: Invalid correct answer index.\n\n")

            messagebox.showinfo("Export Successful", f"Questions & Answers successfully exported to:\n{export_path}", parent=self.root)
            self._update_status("Q&A export successful.")

        except IOError as e:
            messagebox.showerror("Export Error", f"Error exporting Q&A: {e}\nPlease check permissions and filename.", parent=self.root)
            self._update_status("Q&A export failed.")
        except Exception as e:
             messagebox.showerror("Export Error", f"An unexpected error occurred during Q&A export: {e}", parent=self.root)
             self._update_status("Q&A export failed.")

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
             print("Attempting to save history before quitting...") # Add console log
             self.game_logic.save_history()
             print("History saved (or attempted). Quitting GUI.")
             self.root.quit()
             self.root.destroy() # Ensure window closes fully


# --- Main Execution Block ---
if __name__ == "__main__":
    # --- Keep colorama init ---
    if 'colorama' in sys.modules:
        try:
             colorama.init(autoreset=True)
        except Exception as e:
             print(f"Warning: Failed to initialize colorama: {e}")

    # --- Keep game_engine creation ---
    game_engine = LinuxPlusStudyGame()

    # --- Keep interface choice logic ---
    interface_choice = ""
    # Detect if running in a non-interactive environment (e.g., pipe, redirect, some IDEs)
    # Also check if arguments were passed (e.g., `python script.py cli`)
    force_cli = not sys.stdin.isatty() or len(sys.argv) > 1

    if force_cli:
         if len(sys.argv) > 1 and sys.argv[1].lower() == 'gui':
              interface_choice = 'gui' # Allow forcing GUI via arg
         else:
              # print("Non-interactive environment or arguments detected. Defaulting to CLI.") # Optional print
              interface_choice = 'cli'
    else:
        # Interactive environment, ask the user
        # Use pre-defined color constants if available
        COLOR_PROMPT_STR = COLOR_PROMPT if 'COLOR_PROMPT' in globals() else ''
        COLOR_OPTIONS_STR = COLOR_OPTIONS if 'COLOR_OPTIONS' in globals() else ''
        COLOR_INPUT_STR = COLOR_INPUT if 'COLOR_INPUT' in globals() else ''
        COLOR_RESET_STR = COLOR_RESET if 'COLOR_RESET' in globals() else ''
        COLOR_INFO_STR = COLOR_INFO if 'COLOR_INFO' in globals() else ''
        COLOR_ERROR_STR = COLOR_ERROR if 'COLOR_ERROR' in globals() else ''
        COLOR_WARNING_STR = COLOR_WARNING if 'COLOR_WARNING' in globals() else ''

        while interface_choice not in ['cli', 'gui']:
            prompt_text = f"{COLOR_PROMPT_STR}Choose interface ({COLOR_OPTIONS_STR}CLI{COLOR_PROMPT_STR} or {COLOR_OPTIONS_STR}GUI{COLOR_PROMPT_STR}): {COLOR_INPUT_STR}"
            try:
                print(prompt_text, end='')
                sys.stdout.flush() # Ensure prompt appears before input
                interface_choice = input().lower().strip()
                print(COLOR_RESET_STR, end='')
            except EOFError:
                 print(f"\n{COLOR_ERROR_STR} Input interrupted. Defaulting to CLI. {COLOR_RESET_STR}")
                 interface_choice = 'cli' # Default to CLI on EOF
                 break
            except KeyboardInterrupt:
                 print(f"\n{COLOR_WARNING_STR} Operation cancelled by user. Exiting. {COLOR_RESET_STR}")
                 game_engine.save_history() # Attempt save on Ctrl+C exit
                 sys.exit(0)
            if interface_choice not in ['cli', 'gui']:
                 print(f"{COLOR_INFO_STR} Invalid choice. Please type 'cli' or 'gui'. {COLOR_RESET_STR}")

    # --- Keep interface launch logic ---
    if interface_choice == 'gui':
        try:
            root = tk.Tk()
            app = LinuxPlusStudyGUI(root, game_engine)
            # Ensure quit command saves history
            root.protocol("WM_DELETE_WINDOW", app._quit_app)
            root.mainloop()
        except tk.TclError as e:
            print(f"Error: Failed to initialize Tkinter GUI.")
            print(f"This might happen if you are running in an environment without a display server (like a basic SSH session).")
            print(f"Try running in CLI mode instead.")
            print(f"Error details: {e}")
            # Optionally fallback to CLI or just exit
            print("Exiting.")
            game_engine.save_history() # Attempt save
            sys.exit(1)
        except Exception as e:
            print(f"\nAn unexpected error occurred launching the GUI: {e}")
            import traceback
            traceback.print_exc()
            print("Attempting to save history...")
            game_engine.save_history()
            sys.exit(1)
    else: # CLI Mode
        try:
            game_engine.display_welcome_message()
            game_engine.main_menu()
        except KeyboardInterrupt:
             COLOR_WARNING_STR = COLOR_WARNING if 'COLOR_WARNING' in globals() else ''
             COLOR_RESET_STR = COLOR_RESET if 'COLOR_RESET' in globals() else ''
             print(f"\n{COLOR_WARNING_STR} Keyboard interrupt detected. Saving history and exiting. {COLOR_RESET_STR}")
             game_engine.save_history()
             sys.exit(0)
        except Exception as e:
             # Handle potential colorama issues here too
             COLOR_ERROR_STR = COLOR_ERROR if 'COLOR_ERROR' in globals() else ''
             COLOR_RESET_STR = COLOR_RESET if 'COLOR_RESET' in globals() else ''
             COLOR_INFO_STR = COLOR_INFO if 'COLOR_INFO' in globals() else ''
             print(f"\n{COLOR_ERROR_STR} An unexpected error occurred in CLI mode: {e} {COLOR_RESET_STR}")
             print(f"{COLOR_INFO_STR} Attempting to save history before exiting... {COLOR_RESET_STR}")
             game_engine.save_history()
             import traceback
             traceback.print_exc()
             sys.exit(1)

