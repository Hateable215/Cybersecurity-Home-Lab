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
- How to deploy and configure a full SIEM stack from scratch
- How to set up SSH access to a headless Linux server
- How to use VirtualBox NAT port forwarding to expose VM services to the host
- That Wazuh includes built-in support for MITRE ATT&CK, HIPAA, NIST 800-53, and PCI DSS frameworks

**Steps taken:**
- Installed VirtualBox on Windows 11 host
- Created Ubuntu-SIEM VM (8GB RAM, 4 CPUs, 50GB disk)
- Installed Ubuntu Server 25.04 via unattended install
- Enabled SSH server on the VM and configured port forwarding in VirtualBox (host 2222 to guest 22)
- Connected to VM via SSH from Windows for copy/paste workflow
- Ran Wazuh 4.11 all-in-one install script
- Configured port forwarding for Wazuh dashboard (host 8443 to guest 443)
- Reset admin password using wazuh-passwords-tool.sh
- Successfully logged into Wazuh dashboard

**Screenshots:**
![SSH connection to Ubuntu-SIEM]<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/b8610efe-3079-4044-8756-ec080330f68a" />

![Wazuh dashboard overview]<img width="2511" height="1332" alt="image" src="https://github.com/user-attachments/assets/4c83c75d-1f31-43ba-a97e-7151d79d4861" />



---

### 2. Wazuh Agent Deployment
**Status:** In Progress

**Goal:** Connect a Wazuh agent to the SIEM server to start collecting and analyzing 
real logs and security events.

**Steps taken:**
- 

---

### 3. Python Vulnerability Scanner
**Status:** Planned

**Goal:** Build a Python script using nmap to scan a target machine, enumerate open 
ports and services, and output a basic report.

**What I learned:**
- 

**Steps taken:**
- 

---

## Network & Access
| Service | Method | Details |
|---------|--------|---------|
| SSH | Port Forward | ssh david@127.0.0.1 -p 2222 |
| Wazuh Dashboard | Browser | https://127.0.0.1:8443 |

---

## Challenges & Troubleshooting
| Issue | Solution |
|-------|----------|
| Copy/paste not working in VirtualBox console | SSH into VM from Windows instead — full copy/paste via Ctrl+V |
| SSH connection aborted | OpenSSH server not installed by default — ran sudo apt install openssh-server |
| Wazuh password reset failing with special characters | Bash was interpreting ! and @ as special characters — wrapped password in single quotes and used - as the symbol |

---

## Resources
- [VirtualBox](https://www.virtualbox.org/)
- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Ubuntu](https://ubuntu.com/)

---

*This lab is ongoing. I update it as I complete new projects and learn new things.*
