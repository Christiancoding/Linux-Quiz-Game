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
        self.load_questions()
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def load_history(self):
        """Load study history from file if it exists."""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
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
        """Load sample Linux+ questions."""
        # Question format: (question_text, [options], correct_answer_index, category, explanation)
        # Formatted questions for the load_questions function in d.py
        self.questions = [
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
	]
# Extract unique categories
        for _, _, _, category, _ in self.questions:
            self.categories.add(category)
        
        self.total_questions = len(self.questions)
    
    def display_welcome(self):
        """Display the welcome screen."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*20 + "LINUX+ STUDY GAME" + " "*20 + "*")
        print("="*60)
        print("\nWelcome to the CompTIA Linux+ Study Game!")
        print("\nThis game will test your knowledge with questions similar to those")
        print("you might encounter on the CompTIA Linux+ certification exam.")
        print("\nYou'll be presented with multiple-choice questions, and")
        print("after answering, you'll see an explanation of the correct answer.")
        print("\nLet's get started!")
        print("\nPress Enter to continue...")
        input()
    
    def display_menu(self):
        """Display the main menu."""
        while True:
            self.clear_screen()
            print("\n" + "="*60)
            print("*" + " "*20 + "MAIN MENU" + " "*27 + "*")
            print("="*60)
            print("\n1. Start a new quiz (all categories)")
            print("2. Quiz by category")
            print("3. Verify your knowledge")
            print("4. Review incorrect answers")
            print("5. View your statistics")
            print("6. Export study data")
            print("7. Exit")
            print("\nEnter your choice (1-7): ", end="")
            
            choice = input().strip()
            
            if choice == "1":
                self.start_quiz()
            elif choice == "2":
                self.category_quiz()
            elif choice == "3":
                self.verify_answers()
            elif choice == "4":
                self.review_incorrect()
            elif choice == "5":
                self.view_score()
            elif choice == "6":
                self.export_study_data()
            elif choice == "7":
                self.exit_game()
                break
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
    
    def category_quiz(self):
        """Start a quiz for a specific category."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*20 + "SELECT CATEGORY" + " "*20 + "*")
        print("="*60)
        
        # Display categories
        categories_list = list(self.categories)
        for i, category in enumerate(categories_list, 1):
            print(f"{i}. {category}")
        
        print(f"{len(categories_list) + 1}. Back to main menu")
        print("\nEnter your choice: ", end="")
        
        try:
            choice = int(input().strip())
            if 1 <= choice <= len(categories_list):
                selected_category = categories_list[choice - 1]
                # Filter questions by the selected category
                category_questions = [q for q in self.questions if q[3] == selected_category]
                self.start_quiz(category_questions)
            elif choice == len(categories_list) + 1:
                return
            else:
                print("\nInvalid choice. Please try again.")
                time.sleep(1)
                self.category_quiz()
        except ValueError:
            print("\nPlease enter a number.")
            time.sleep(1)
            self.category_quiz()
    
    def start_quiz(self, questions=None):
        """Start a new quiz with given questions or all questions if None."""
        if questions is None:
            questions = self.questions.copy()
            category = None
        else:
            # Determine category if we're using a filtered list
            category = questions[0][3] if questions else None
        
        if not questions:
            print("\nNo questions available for this category.")
            print("\nPress Enter to continue...")
            input()
            return
        
        # Shuffle questions
        random.shuffle(questions)
        
        correct_answers = 0
        total = len(questions)
        quiz_results = []  # To store question results for history
        
        for i, (question, options, correct_index, category, explanation) in enumerate(questions, 1):
            self.clear_screen()
            print(f"\nQuestion {i} of {total}:")
            print(f"\n{question}\n")
            
            # Display options
            for j, option in enumerate(options):
                print(f"{j + 1}. {option}")
            
            # Get user answer
            while True:
                try:
                    print("\nYour answer (1-{}): ".format(len(options)), end="")
                    user_answer = int(input().strip())
                    if 1 <= user_answer <= len(options):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(options)}.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Check answer
            is_correct = (user_answer - 1) == correct_index
            if is_correct:
                correct_answers += 1
                self.score += 1
                print("\n✅ Correct!")
            else:
                print(f"\n❌ Incorrect. The correct answer is: {options[correct_index]}")
            
            # Display explanation
            print(f"\nExplanation: {explanation}")
            
            # Store answer for history
            quiz_results.append((question, user_answer - 1, correct_index, category))
            
            print("\nPress Enter to continue...")
            input()
        
        # Update history with quiz results
        self.update_history(quiz_results, correct_answers, category)
        
        # Quiz summary
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*20 + "QUIZ RESULTS" + " "*24 + "*")
        print("="*60)
        print(f"\nYou got {correct_answers} out of {total} questions correct!")
        print(f"Score: {(correct_answers / total) * 100:.1f}%")
        
        if (correct_answers / total) >= 0.8:
            print("\nGreat job! You're well on your way to Linux+ certification!")
        elif (correct_answers / total) >= 0.6:
            print("\nGood effort! Keep studying to improve your knowledge.")
        else:
            print("\nKeep practicing! The Linux+ exam requires more preparation.")
        
        # Offer to review incorrect answers
        if correct_answers < total:
            incorrect_questions = [questions[i] for i, (_, user_answer, correct_index, _, _) 
                              in enumerate(zip(questions, [r[1] for r in quiz_results], 
                                              [r[2] for r in quiz_results], 
                                              [r[3] for r in quiz_results],
                                              [0] * len(quiz_results)))
                              if user_answer != correct_index]
            
            print("\nWould you like to review your incorrect answers? (y/n): ", end="")
            choice = input().strip().lower()
            if choice == 'y':
                self.review_specific_questions(incorrect_questions)
        
        print("\nPress Enter to return to the main menu...")
        input()
    
    def view_score(self):
        """View the current score and detailed statistics."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*20 + "YOUR SCORE" + " "*25 + "*")
        print("="*60)
        
        if self.study_history["total_attempts"] > 0:
            print(f"\nLifetime Statistics:")
            print(f"Total questions attempted: {self.study_history['total_attempts']}")
            print(f"Correct answers: {self.study_history['total_correct']}")
            print(f"Overall success rate: {(self.study_history['total_correct'] / self.study_history['total_attempts']) * 100:.1f}%")
            
            # Display category performance
            if self.study_history["categories"]:
                print("\nPerformance by Category:")
                for category, data in self.study_history["categories"].items():
                    if data["attempts"] > 0:
                        success_rate = (data["correct"] / data["attempts"]) * 100
                        print(f"- {category}: {success_rate:.1f}% ({data['correct']}/{data['attempts']})")
            
            # Display recent session
            if self.study_history["sessions"]:
                last_session = self.study_history["sessions"][-1]
                print(f"\nLast Study Session ({last_session['date']}):")
                print(f"Questions: {last_session['questions']}")
                print(f"Correct: {last_session['correct']}")
                print(f"Success Rate: {(last_session['correct'] / last_session['questions']) * 100:.1f}%")
            
            # Display areas that need improvement
            print("\nAreas for Improvement:")
            weak_categories = []
            for category, data in self.study_history["categories"].items():
                if data["attempts"] >= 3 and (data["correct"] / data["attempts"]) < 0.7:
                    weak_categories.append(category)
            
            if weak_categories:
                for category in weak_categories:
                    print(f"- {category}")
            else:
                print("- You're doing well in all categories! Keep practicing!")
                
        else:
            print("\nYou haven't taken any quizzes yet!")
        
        print("\nPress Enter to return to the main menu...")
        input()
    
    def review_incorrect(self):
        """Review questions that were answered incorrectly."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*15 + "REVIEW INCORRECT ANSWERS" + " "*15 + "*")
        print("="*60)
        
        # Get questions with incorrect answers
        incorrect_questions = []
        for question_id, data in self.study_history["questions"].items():
            if data["attempts"] > 0 and data["correct"] / data["attempts"] < 0.7:
                # Find the actual question from question_id
                for q in self.questions:
                    if self.get_question_id(q[0]) == question_id:
                        incorrect_questions.append(q)
                        break
        
        if not incorrect_questions:
            print("\nNo questions to review! You're doing great!")
            print("\nPress Enter to return to the main menu...")
            input()
            return
            
        print(f"\nFound {len(incorrect_questions)} questions that need review.")
        print("\nLet's go through them one by one.")
        print("\nPress Enter to start...")
        input()
        
        for i, (question, options, correct_index, category, explanation) in enumerate(incorrect_questions, 1):
            self.clear_screen()
            print(f"\nQuestion {i} of {len(incorrect_questions)}:")
            print(f"\n{question}\n")
            
            # Display options
            for j, option in enumerate(options):
                print(f"{j + 1}. {option}")
            
            print(f"\nCorrect answer: {correct_index + 1}. {options[correct_index]}")
            print(f"\nExplanation: {explanation}")
            
            print("\nPress Enter to continue...")
            input()
        
        print("\nReview completed! Good job studying your weak areas.")
        print("\nPress Enter to return to the main menu...")
        input()
    
    def verify_answers(self, questions=None):
        """Verify answers to questions from previous attempts."""
        if questions is None:
            questions = self.questions.copy()
        
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*15 + "VERIFY YOUR KNOWLEDGE" + " "*15 + "*")
        print("="*60)
        
        print("\nThis mode will test your knowledge and verify your answers.")
        print("You won't be told if you're right or wrong until the end.")
        print("\nReady? Press Enter to start...")
        input()
        
        # Shuffle questions
        random.shuffle(questions)
        
        # Limit to 10 questions for a quick verification session
        questions = questions[:10]
        
        answers = []
        for i, (question, options, correct_index, category, _) in enumerate(questions, 1):
            self.clear_screen()
            print(f"\nQuestion {i} of {len(questions)}:")
            print(f"\n{question}\n")
            
            # Display options
            for j, option in enumerate(options):
                print(f"{j + 1}. {option}")
            
            # Get user answer
            while True:
                try:
                    print("\nYour answer (1-{}): ".format(len(options)), end="")
                    user_answer = int(input().strip())
                    if 1 <= user_answer <= len(options):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(options)}.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Store the answer
            answers.append((i-1, user_answer-1, correct_index, question, options, category))
        
        # Show results
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*20 + "VERIFICATION RESULTS" + " "*17 + "*")
        print("="*60)
        
        correct_count = 0
        incorrect_questions = []
        
        for i, (q_index, user_answer, correct_index, question, options, category) in enumerate(answers, 1):
            is_correct = user_answer == correct_index
            if is_correct:
                correct_count += 1
                result = "✅ Correct"
            else:
                result = f"❌ Incorrect (You chose: {user_answer+1}, Correct: {correct_index+1})"
                incorrect_questions.append(questions[q_index])
            
            print(f"\n{i}. {question}")
            print(f"   Your answer: {options[user_answer]}")
            print(f"   {result}")
        
        print(f"\nScore: {correct_count}/{len(questions)} ({(correct_count/len(questions))*100:.1f}%)")
        
        # Ask if they want to review incorrect answers
        if incorrect_questions:
            print("\nWould you like to review the questions you got wrong? (y/n): ", end="")
            choice = input().strip().lower()
            if choice == 'y':
                self.review_specific_questions(incorrect_questions)
        
        print("\nPress Enter to return to the main menu...")
        input()
    
    def review_specific_questions(self, questions):
        """Review specific questions with detailed explanations."""
        for i, (question, options, correct_index, category, explanation) in enumerate(questions, 1):
            self.clear_screen()
            print(f"\nReviewing question {i} of {len(questions)}:")
            print(f"\n{question}\n")
            
            # Display options
            for j, option in enumerate(options):
                if j == correct_index:
                    print(f"{j + 1}. {option} ✅")
                else:
                    print(f"{j + 1}. {option}")
            
            print(f"\nExplanation: {explanation}")
            
            print("\nPress Enter to continue...")
            input()
    
    def get_question_id(self, question):
        """Generate a unique ID for a question based on its text."""
        return str(hash(question) % 10000)
    
    def update_history(self, questions_asked, correct_answers, category=None):
        """Update the study history with results from a quiz session."""
        # Update session data
        session = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "questions": len(questions_asked),
            "correct": correct_answers,
            "category": category
        }
        self.study_history["sessions"].append(session)
        
        # Update overall stats
        self.study_history["total_attempts"] += len(questions_asked)
        self.study_history["total_correct"] += correct_answers
        
        # Update per-question and per-category stats
        for question, user_answer, correct_answer, category in questions_asked:
            q_id = self.get_question_id(question)
            is_correct = user_answer == correct_answer
            
            # Update question stats
            if q_id not in self.study_history["questions"]:
                self.study_history["questions"][q_id] = {
                    "attempts": 0,
                    "correct": 0,
                    "text": question[:50] + "..." if len(question) > 50 else question  # Store abbreviated question
                }
            self.study_history["questions"][q_id]["attempts"] += 1
            if is_correct:
                self.study_history["questions"][q_id]["correct"] += 1
            
            # Update category stats
            if category not in self.study_history["categories"]:
                self.study_history["categories"][category] = {
                    "attempts": 0,
                    "correct": 0
                }
            self.study_history["categories"][category]["attempts"] += 1
            if is_correct:
                self.study_history["categories"][category]["correct"] += 1
        
        # Save updated history
        self.save_history()
    
    def exit_game(self):
        """Exit the game."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*15 + "THANK YOU FOR STUDYING!" + " "*15 + "*")
        print("="*60)
        print("\nGood luck with your CompTIA Linux+ certification!")
        print("\nExiting the game...")
        time.sleep(2)
        sys.exit()

    def export_study_data(self):
        """Export study data to a readable format."""
        self.clear_screen()
        print("\n" + "="*60)
        print("*" + " "*15 + "EXPORT STUDY DATA" + " "*20 + "*")
        print("="*60)
        
        if not self.study_history["sessions"]:
            print("\nNo study data available to export yet.")
            print("\nPress Enter to return to the main menu...")
            input()
            return
            
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"linux_plus_study_report_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("="*60 + "\n")
                f.write("LINUX+ CERTIFICATION STUDY REPORT\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                # Overall statistics
                f.write("OVERALL STATISTICS\n")
                f.write("-----------------\n")
                f.write(f"Total questions attempted: {self.study_history['total_attempts']}\n")
                f.write(f"Correct answers: {self.study_history['total_correct']}\n")
                if self.study_history['total_attempts'] > 0:
                    success_rate = (self.study_history['total_correct'] / self.study_history['total_attempts']) * 100
                    f.write(f"Overall success rate: {success_rate:.1f}%\n\n")
                
                # Category performance
                f.write("CATEGORY PERFORMANCE\n")
                f.write("-------------------\n")
                for category, data in self.study_history["categories"].items():
                    if data["attempts"] > 0:
                        success_rate = (data["correct"] / data["attempts"]) * 100
                        f.write(f"{category}: {success_rate:.1f}% ({data['correct']}/{data['attempts']})\n")
                f.write("\n")
                
                # Study sessions
                f.write("STUDY SESSIONS\n")
                f.write("--------------\n")
                for i, session in enumerate(self.study_history["sessions"], 1):
                    f.write(f"Session {i} - {session['date']}\n")
                    f.write(f"  Questions: {session['questions']}\n")
                    f.write(f"  Correct: {session['correct']}\n")
                    if session['questions'] > 0:
                        success_rate = (session['correct'] / session['questions']) * 100
                        f.write(f"  Success Rate: {success_rate:.1f}%\n")
                    if session['category']:
                        f.write(f"  Category: {session['category']}\n")
                    f.write("\n")
                
                # Areas for improvement
                f.write("AREAS FOR IMPROVEMENT\n")
                f.write("--------------------\n")
                weak_categories = []
                for category, data in self.study_history["categories"].items():
                    if data["attempts"] >= 3 and (data["correct"] / data["attempts"]) < 0.7:
                        weak_categories.append((category, (data["correct"] / data["attempts"]) * 100))
                
                if weak_categories:
                    for category, rate in sorted(weak_categories, key=lambda x: x[1]):
                        f.write(f"{category}: {rate:.1f}%\n")
                else:
                    f.write("You're doing well in all categories! Keep practicing!\n")
                    
                # Most challenging questions
                f.write("\nMOST CHALLENGING QUESTIONS\n")
                f.write("------------------------\n")
                challenging_questions = []
                for q_id, data in self.study_history["questions"].items():
                    if data["attempts"] >= 2 and (data["correct"] / data["attempts"]) < 0.5:
                        challenging_questions.append((data["text"], data["correct"], data["attempts"]))
                
                if challenging_questions:
                    for i, (text, correct, attempts) in enumerate(sorted(challenging_questions, 
                                                                      key=lambda x: x[1]/x[2]), 1):
                        success_rate = (correct / attempts) * 100
                        f.write(f"{i}. {text} ({success_rate:.1f}% - {correct}/{attempts})\n")
                else:
                    f.write("No particularly challenging questions identified yet.\n")
                    
                f.write("\n")
                f.write("="*60 + "\n")
                f.write("STUDY RECOMMENDATIONS\n")
                f.write("="*60 + "\n\n")
                
                # Add some recommendations based on performance
                if weak_categories:
                    f.write("1. Focus on these categories:\n")
                    for category, _ in sorted(weak_categories, key=lambda x: x[1]):
                        f.write(f"   - {category}\n")
                    f.write("\n")
                    
                total_sessions = len(self.study_history["sessions"])
                if total_sessions < 5:
                    f.write("2. Increase your study frequency. You've only had {total_sessions} study sessions.\n")
                else:
                    f.write("2. You're maintaining good study consistency with {total_sessions} sessions.\n")
                    
                overall_rate = (self.study_history['total_correct'] / self.study_history['total_attempts']) * 100 if self.study_history['total_attempts'] > 0 else 0
                if overall_rate < 70:
                    f.write("3. Your overall success rate of {overall_rate:.1f}% indicates you should review fundamental concepts.\n")
                elif overall_rate < 80:
                    f.write("3. Your success rate of {overall_rate:.1f}% is good, but aim for 80% or higher before the exam.\n")
                else:
                    f.write("3. Your success rate of {overall_rate:.1f}% is excellent! Keep up the good work.\n")
                    
            print(f"\nStudy data exported to {filename}")
            print("\nPress Enter to return to the main menu...")
            input()
            
        except Exception as e:
            print(f"\nError exporting data: {e}")
            print("\nPress Enter to return to the main menu...")
            input()

if __name__ == "__main__":
    game = LinuxPlusStudyGame()
    game.display_welcome()
    game.display_menu()
