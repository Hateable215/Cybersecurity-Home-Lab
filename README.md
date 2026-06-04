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
**Status:** Complete

**Goal:** Deploy Wazuh on Ubuntu to collect and analyze logs, write detection rules, 
and monitor for suspicious activity.

**What I learned:**
- How to deploy and configure a full SIEM stack from scratch
- How to set up SSH access to a headless Linux server
- How to use VirtualBox NAT port forwarding to expose VM services to the host
- How to reset service credentials via command line tools
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
![SSH connection to Ubuntu-SIEM]<img width="1115" height="628" alt="image" src="https://github.com/user-attachments/assets/e638a144-60ce-42d6-b1b2-fe3b9668a118" />


![Wazuh dashboard overview]<img width="2511" height="1332" alt="image" src="https://github.com/user-attachments/assets/068e30ab-cae6-4640-a274-35389bfd8a12" />



---

### 2. Wazuh Agent Deployment
**Status:** Complete

**Goal:** Connect a Wazuh agent to the SIEM server to start collecting and analyzing 
real logs and security events from a live endpoint.

**What I learned:**
- How Wazuh agents register and authenticate with the manager
- How NAT port forwarding affects agent connectivity and how to work around it
- How to troubleshoot agent connection issues using ossec.log and agent_control
- That agents can register successfully but still fail to connect if the server address is wrong

**Steps taken:**
- Installed Wazuh agent on Windows 11 host via PowerShell
- Added port forwarding rules for ports 1514 and 1515 in VirtualBox
- Diagnosed connection failure using agent logs and manage_agents tool
- Updated ossec.conf to point agent at 127.0.0.1 instead of 10.0.2.15
- Confirmed agent active in Wazuh dashboard with live alerts flowing in
- Windows host immediately generated 435 medium and 180 low severity alerts

**Screenshots:**
![Wazuh agent active](screenshots/wazuh-agent-active.png)

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
| Wazuh Agent | Port Forward | Host 1514/1515 to Guest 1514/1515 |

---

## Challenges & Troubleshooting
| Issue | Solution |
|-------|----------|
| Copy/paste not working in VirtualBox console | SSH into VM from Windows instead — full copy/paste via Ctrl+V |
| SSH connection aborted | OpenSSH server not installed by default — ran sudo apt install openssh-server |
| Wazuh password reset failing with special characters | Bash interpreted ! and @ as special characters — wrapped password in single quotes and used - as the symbol |
| Wazuh agent registered but never connected | Agent config had 10.0.2.15 as server address — updated ossec.conf to 127.0.0.1 to route through NAT port forwarding |

---

## Resources
- [VirtualBox](https://www.virtualbox.org/)
- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Ubuntu](https://ubuntu.com/)

---

*This lab is ongoing. I update it as I complete new projects and learn new things.*
