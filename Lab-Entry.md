# Lab Entry: Host-Only Networking, DHCP, and Firewall Hardening

This entry documents connecting the SIEM VM and a target VM on an isolated VirtualBox network, switching both from manual static IPs to DHCP, and hardening the target with a host-based firewall. The scanner is then re-run to verify the firewall reduced the target's attack surface.

## Environment

| Role | Hostname | Adapter 1 (NAT) | Adapter 2 (Host-Only) |
|------|----------|-----------------|------------------------|
| SIEM / scanner | Ubuntu-SIEM (Ubuntu Server) | enp0s3 | enp0s8 |
| Scan target | Ubuntu-Target (Ubuntu Desktop) | enp0s3 | enp0s8 |

Both VMs use two adapters. Adapter 1 stays on NAT so SSH port forwarding and internet access keep working. Adapter 2 is the Host-Only adapter that lets the two VMs talk to each other on an isolated `192.168.56.0/24` network.

## Networking: from static IPs to DHCP

### The problem

Adapter 2 (enp0s8) was not getting a usable address. Running `ip a` showed a link-local `169.254.x.x` address instead of one on the `192.168.56.0/24` network. A link-local address is the fallback a host assigns itself when it asks for a DHCP lease and gets no answer.

Two root causes were found:

1. The VirtualBox Host-Only DHCP server was enabled, but Adapter 2 on each VM was attached to an **Internal Network** named `labnet` rather than the **Host-Only Adapter**. There is no DHCP server on that internal network, so the lease request went unanswered.
2. The SIEM's netplan config (`/etc/netplan/00-installer-config.yaml`) only defined enp0s3. There was no entry for enp0s8 at all, so it never requested a lease.

### The fix

On both VMs, Adapter 2 was switched in VirtualBox to **Host-only Adapter**, pointing at the **VirtualBox Host-Only Ethernet Adapter** (`192.168.56.1/24`, DHCP enabled, pool `192.168.56.101` to `192.168.56.254`).

On the SIEM, the netplan config was updated to add enp0s8 as a DHCP client:

```yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: true
      dhcp6: true
      match:
        macaddress: 08:00:27:b3:56:ce
      set-name: enp0s3
    enp0s8:
      dhcp4: true
      dhcp6: false
  version: 2
```

Then applied with:

```bash
sudo netplan apply
```

The Ubuntu Desktop target already had DHCP configured by default, so it needed only the adapter change.

### Result

After applying the changes, both VMs pulled addresses from the VirtualBox DHCP pool:

| VM | enp0s8 address | Source |
|----|----------------|--------|
| Ubuntu-SIEM | 192.168.56.102/24 | DHCP (dynamic, lease ~600s) |
| Ubuntu-Target | 192.168.56.103/24 | DHCP (dynamic, lease ~600s) |

Connectivity confirmed from the SIEM:

```
ping -c 3 192.168.56.103
3 packets transmitted, 3 received, 0% packet loss
```

The static addresses used earlier (`192.168.56.10` and `192.168.56.20`) sat outside the DHCP pool, so static and DHCP would not collide. Moving the config into netplan means the setup now survives reboots instead of needing manual `ip addr add` each session.

## Firewall hardening on the target

### Baseline scan (firewall off)

Running the Python scanner from the SIEM against the target showed two exposed services:

```
22/tcp open ssh    OpenSSH 10.2p1 Ubuntu
80/tcp open http   Apache httpd 2.4.66
Not shown: 998 closed tcp ports (conn-refused)
```

Two MEDIUM findings: SSH and an Apache web server. All other ports reported `closed`, meaning the host actively refused them (no firewall dropping traffic).

### Applying the firewall

The Linux kernel's packet filtering (netfilter) is always present. What gets enabled is a userspace tool that loads rules into it. UFW (Uncomplicated Firewall) was used here since it is the standard front-end on Ubuntu and the one most hardening benchmarks reference.

On the target:

```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw status verbose
```

Resulting policy:

```
Status: active
Default: deny (incoming), allow (outgoing)

To          Action      From
22/tcp      ALLOW IN    Anywhere
```

This applies a default-deny incoming policy with a single deliberate exception for SSH. UFW is set to start on boot. The nftables service unit shows inactive, which is expected: UFW manages its own netfilter rules directly and should not be run alongside a separately managed nftables config.

### Verification scan (firewall on)

Re-running the same scanner from the SIEM:

```
22/tcp open ssh    OpenSSH 10.2p1 Ubuntu
Not shown: 999 filtered tcp ports (no-response)
```

### Before and after

| | Firewall off | Firewall on |
|---|---|---|
| Port 22 (SSH) | open | open (explicitly allowed) |
| Port 80 (HTTP) | open | hidden (dropped) |
| Other ports | closed (conn-refused) | filtered (no-response) |
| Risk findings | 2 MEDIUM | 1 MEDIUM |

Three changes confirm the firewall is working as intended. Apache disappeared from the scan because it was not allowed (the service is still running, just no longer reachable from the network). The non-allowed ports flipped from `closed` to `filtered`, which is the signature of packets being silently dropped rather than refused. Port 22 stayed open because it was explicitly allowed, proving the allow-list works rather than a blanket block.

## Takeaways

This was a full defensive workflow: scan a target, identify exposed services, apply a host-based firewall with a least-privilege allow-list, then re-scan to verify the attack surface shrank. It also reinforced the difference between an Internal Network and a Host-Only network in VirtualBox, why a link-local address means DHCP failed, and how netplan makes interface config persistent across reboots.

---

*Author: Vithyear Nuon*
