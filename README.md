# Cybersecurity Home Lab

## Overview
This repository documents my personal cybersecurity home lab. I built this to get hands-on 
experience with tools and concepts I'm studying in my cybersecurity program at SNHU. 
The goal is to practice real skills outside of coursework and build a portfolio of 
projects I can talk about.

---

## Host Machine
| Component | Details |
|-----------|---------|
| OS | Windows 11 Home |
| CPU | Intel Core i7-12700KF |
| RAM | 32GB DDR5 |
| GPU | AMD Radeon RX 9070 XT |
| Hypervisor | VirtualBox 7.x |

---

## Lab Environment
| VM Name | OS | Role | RAM | CPUs | Disk |
|---------|----|------|-----|------|------|
| Ubuntu-SIEM | Ubuntu 25.04 | SIEM Server (Wazuh) | 8GB | 4 | 50GB |

---

## Projects

### 1. SIEM Setup (Wazuh)
**Status:** In Progress

**Goal:** Deploy Wazuh on Ubuntu to collect and analyze logs, write detection rules, 
and monitor for suspicious activity.

**What I learned:**
- 

**Steps taken:**
- Installed VirtualBox on Windows 11 host
- Created Ubuntu-SIEM VM (8GB RAM, 4 CPUs, 50GB disk)
- Installed Ubuntu Server 25.04 via unattended install
- Enabled SSH server on the VM and configured port forwarding in VirtualBox
- Connected to VM via SSH from Windows for copy/paste workflow
- 
**Screenshots:**
<img width="1115" height="628" alt="image" src="https://github.com/user-attachments/assets/793b343b-4581-4e76-805a-bd802b12ddfb" />


---

### 2. Python Vulnerability Scanner
**Status:** Planned

**Goal:** Build a Python script using nmap to scan a target machine, enumerate open 
ports and services, and output a basic report.

**What I learned:**
- 

**Steps taken:**
- 

---

## Network & Access
| Method | Details |
|--------|---------|
| SSH | ssh david@127.0.0.1 -p 2222 |
| Port Forwarding | Host 2222 → Guest 22 (NAT) |

---

## Challenges & Troubleshooting
| Issue | Solution |
|-------|----------|
| Copy/paste not working in VirtualBox console | SSH into VM from Windows instead — full copy/paste via Ctrl+V |
| SSH connection aborted | OpenSSH server not installed by default — ran sudo apt install openssh-server |

---

## Resources
- [VirtualBox](https://www.virtualbox.org/)
- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Ubuntu](https://ubuntu.com/)

---

*This lab is ongoing. I update it as I complete new projects and learn new things.*
