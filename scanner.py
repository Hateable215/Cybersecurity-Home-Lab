#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

HIGH_RISK_PORTS = [21, 23, 25, 445, 3389, 4444, 5900]
MEDIUM_RISK_PORTS = [22, 80, 443, 8080, 8443, 3306, 5432]

def get_risk(port):
    if port in HIGH_RISK_PORTS:
        return "HIGH"
    elif port in MEDIUM_RISK_PORTS:
        return "MEDIUM"
    return "LOW"

def parse_ports(nmap_output):
    ports = []
    for line in nmap_output.splitlines():
        if "/tcp" in line and "open" in line:
            parts = line.split()
            port_num = int(parts[0].split("/")[0])
            service = parts[2] if len(parts) > 2 else "unknown"
            version = " ".join(parts[3:]) if len(parts) > 3 else ""
            risk = get_risk(port_num)
            ports.append((port_num, service, version, risk))
    return ports

def generate_html(target, ports, timestamp):
    rows = ""
    for port, service, version, risk in ports:
        color = {"HIGH": "#ff4444", "MEDIUM": "#ffaa00", "LOW": "#44bb44"}[risk]
        rows += f"""
        <tr>
            <td>{port}</td>
            <td>{service}</td>
            <td>{version}</td>
            <td style="color:{color}; font-weight:bold;">{risk}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Scan Report - {target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #00d4ff; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #16213e; padding: 12px; text-align: left; color: #00d4ff; }}
        td {{ padding: 10px; border-bottom: 1px solid #333; }}
        tr:hover {{ background: #16213e; }}
        .info {{ background: #16213e; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>Vulnerability Scan Report</h1>
    <div class="info">
        <p><strong>Target:</strong> {target}</p>
        <p><strong>Scan Time:</strong> {timestamp}</p>
        <p><strong>Scanner:</strong> nmap 7.98</p>
    </div>
    <table>
        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Version</th>
            <th>Risk</th>
        </tr>
        {rows}
    </table>
</body>
</html>"""
    return html

def scan(target):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"scan_{target}_{timestamp}.txt"
    html_name = f"scan_{target}_{timestamp}.html"

    header = f"""
{'=' * 50}
VULNERABILITY SCAN REPORT
{'=' * 50}
Target:     {target}
Started:    {datetime.now()}
Scanner:    nmap 7.98
{'=' * 50}
"""

    print(header)

    try:
        result = subprocess.run(
            ["nmap", "-sV", "-T4", target],
            capture_output=True,
            text=True
        )
        raw_output = result.stdout
        ports = parse_ports(raw_output)

        risk_summary = "\nPORT RISK SUMMARY\n" + "-" * 50 + "\n"
        for port, service, version, risk in ports:
            risk_summary += f"[{risk}] Port {port} - {service} {version}\n"

        print(raw_output)
        print(risk_summary)

    except Exception as e:
        raw_output = f"Scan failed: {e}"
        risk_summary = ""
        ports = []
        print(raw_output)

    footer = f"""
{'=' * 50}
Scan completed: {datetime.now()}
Reports saved to: {report_name} and {html_name}
{'=' * 50}
"""

    print(footer)

    with open(report_name, "w") as f:
        f.write(header)
        f.write(raw_output)
        f.write(risk_summary)
        f.write(footer)

    with open(html_name, "w") as f:
        f.write(generate_html(target, ports, timestamp))

    print(f"HTML report saved to: {html_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scanner.py <target1> <target2> ...")
        sys.exit(1)

    targets = sys.argv[1:]
    for target in targets:
        scan(target)
