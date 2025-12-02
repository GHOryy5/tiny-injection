#!/usr/bin/env python3
from src.core.scanner import AIScanner
import json
from datetime import datetime

def load_payloads(filepath: str):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    scanner = AIScanner()
    
    payloads = load_payloads("data/payloads/basic.txt")
    
    print("[*] Starting AI Security Scan")
    print("[*] Target: GPT-4 API simulation")
    print(f"[*] Payloads loaded: {len(payloads)}")
    print("-" * 50)
    
    results = scanner.test_openai(
        system_prompt="You are a helpful AI assistant",
        payloads=payloads
    )
    
    for finding in results:
        if finding["vulnerable"]:
            print(f"[{finding['severity'].upper()}] {finding['payload'][:60]}...")
            print(f"     CVSS: {finding['cvss_score']} - {finding['explanation']}")
            print()
    
    stats = scanner.get_stats()
    
    print("-" * 50)
    print("[+] Scan Complete")
    print(f"    Critical: {stats['critical_findings']}")
    print(f"    High: {stats['high_findings']}")
    print(f"    Medium: {stats['medium_findings']}")
    print(f"    Success Rate: {stats['success_rate']}%")
    
    if stats['critical_findings'] > 0:
        print("\n🔴 SECURITY ALERT: Critical vulnerabilities detected")
        print("   Immediate remediation required")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"scan_results_{timestamp}.json", 'w') as f:
        json.dump({
            "scan_date": timestamp,
            "findings": results,
            "stats": stats
        }, f, indent=2)
    
    print(f"\n[*] Full report saved to: scan_results_{timestamp}.json")

if __name__ == "__main__":
    main()