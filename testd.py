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
            ),
            # ... (other existing questions would go here) ...
             (
                "What command would you use to display detailed information about the CPU architecture on a Linux system?",
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
