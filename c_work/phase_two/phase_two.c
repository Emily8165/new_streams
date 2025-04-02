// Phase 2: System-Level Programming
// 📌 Goal: Learn how C interacts with hardware, OS, and memory.
// Understand Memory Layout and Stack vs Heap

// How local/global variables are stored
// Stack frames and function calls
// How malloc and free interact with the heap
// Practice: Write a simple memory pool allocator.
// Learn About System Calls and the OS Interface

// Understanding how the OS provides services to programs
// Important syscalls: read(), write(), open(), close()
// Practice: Implement a custom version of cat using read() and write().
// Signals and Process Management

// Forking processes (fork, exec, wait)
// Signal handling (SIGINT, SIGTERM)
// Practice: Write a simple shell that can execute commands.
// Inter-Process Communication (IPC)

// Pipes and named pipes (FIFO)
// Message queues and shared memory
// Practice: Implement a chat program using pipes.
// 📚 Recommended Resources:

// Advanced Programming in the UNIX Environment by W. Richard Stevens
// "Linux Programming Interface" by Michael Kerrisk
// Phase 3: Performance, Debugging, and Security
// 📌 Goal: Learn to write high-performance and secure C code.
// Optimization Techniques

// Compiler optimizations (-O2, -O3, -march=native)
// Loop unrolling, memory access patterns
// Practice: Write a fast matrix multiplication program.
// Debugging and Profiling

// Using gdb to debug C programs
// Memory debugging with valgrind
// Performance profiling with perf
// Practice: Find and fix memory leaks in a program.
// Understanding Security Pitfalls
// Buffer overflows and stack smashing
// Use-after-free and double-free errors
// Practice: Implement safe string handling functions.
// 📚 Recommended Resources:

// Hacking: The Art of Exploitation by Jon Erickson
// MIT OpenCourseWare on Computer Systems Security
// Phase 4: Writing Good C Code
// 📌 Goal: Learn what makes C code maintainable, efficient, and safe.
// Learn and Apply C Best Practices
// Modular design (.h and .c files)
// Defensive programming
// Using static and const correctly
// Practice: Refactor an old project using best practices.
// Reading and Understanding Existing Code
// Read and analyze open-source C projects:
// Simple: sqlite (database)
// Intermediate: coreutils (Linux command-line tools)
// Advanced: Linux kernel (device drivers, scheduling)
// Practice: Try fixing a bug or optimizing a small part of an open-source project.
// 📚 Recommended Resources:

// Clean Code in C by Robert C. Seacord
// "SEI CERT C Coding Standard" (for secure C coding practices)
// 📌 Final Projects
// To reinforce your learning, build one of these:

// A Lightweight HTTP Server

// Uses sockets (bind, listen, accept)
// Supports GET requests
// A Simple Virtual Memory Simulator

// Simulates page tables and memory allocation
// Helps understand OS memory management
// A Minimal x86 Bootloader (Advanced)

// Write raw C and Assembly
// Boot into a tiny kernel


// books go get:
// The C Programming language - Brian W. Kernighan & Dennis M. Ritchie file:///Users/emily.harris/Downloads/The.C.Programming.Language.2nd.Edition.pdf
// The Rust Programming language - https://doc.rust-lang.org/book/
// C Primer Plus - Stephen Prata
// Understanding Pointers in C – Yashavant Kanetkar
// Expert C Programming: Deep C Secrets – Peter van der Linden

/*
NETWORKS:
phase 1:
Book: Computer Networking: A Top-Down Approach by Kurose & Ross
Course: Introduction to Computer Networking (Coursera)
Hands-on: Draw the OSI & TCP/IP models with explanations

phase 2:
Watch: OSI Model Explained
Practical: Use Wireshark to capture network packets

phase 3:
Subnetting Practice: Subnetting.net
Hands-on: Configure a router & assign IP addresses (Use Packet Tracer)

phase 4:
Read: RFC 793 (TCP) and RFC 768 (UDP)
Hands-on: Use Netcat or Telnet to test ports

phase 5: 
Watch: Routing Explained ()
Hands-on: Simulate routing in Cisco Packet Tracer

phase 6:
Course: Wireless Networking Basics (Udemy)
Hands-on: Set up & secure a Wi-Fi router

phase 7:
Read: Network Security Essentials by William Stallings
Hands-on: Use Wireshark to detect network attacks

phase 8:
Course: AWS Networking Fundamentals
Hands-on: Try GNS3 for network simulation

CYBER SEC:
phase 1:
Intro to Cybersecurity (Coursera)
Book: Cybersecurity Essentials by Charles Brooks
Hands-on: Set up a Virtual Lab (VMware/VirtualBox + Kali Linux)

phase 2:
Course: Networking Basics (Cisco)
Hands-on: Use Wireshark to analyze network traffic

phase 3: 
Course: Linux Security Fundamentals
Hands-on: Use fail2ban to secure SSH on Linux

phase 4: look into common cyber securty flaws
OWASP Top 10 Guide (google this)
Hands-on: Use Burp Suite & DVWA (Damn Vulnerable Web App) for testing


phase 5: common cyber sec issues
Course: Practical Ethical Hacking (TCM Security)
Hands-on: Scan a target machine using Nmap

phase 6: cryptography and encryption
Book: Cryptography & Network Security by William Stallings
Hands-on: Encrypt data using OpenSSL

phase 7: social engineering
Watch: Social Engineering Attacks Explained
Hands-on: Try GoPhish for phishing simulations

phase 8: digital faransics
Book: Practical Malware Analysis by Michael Sikorski
Hands-on: Use Remnux to analyze a malware sample

phase 9: cloud application and security
Course: AWS Security Fundamentals
Hands-on: Set up AWS IAM Policies for access control

phase 10: security team and blue teaming. 
Read: The Blue Team Handbook
Hands-on: Use Splunk for log analysis

work towards Certified Information Systems Security Professional (CISSP)


*/