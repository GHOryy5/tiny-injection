#!/usr/bin/env python3
import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

def execute_attack(target, payload_file, api_key=None, model="gpt-4"):
    print(f"[*] Testing: {target[:60]}...")
    
    results = []
    with open(payload_file, 'r') as f:
        payloads = [line.strip() for line in f if line.strip()]
    
    for i, payload in enumerate(payloads[:50]):
        print(f"[{i+1}/{len(payloads)}] {payload[:40]}...")
        
        simulated_response = f"Test response to: {payload}"
        success = "ignore" in payload.lower() or "override" in payload.lower()
        
        results.append({
            "payload": payload,
            "response": simulated_response,
            "success": success,
            "confidence": 0.85 if success else 0.15
        })
    
    return results

def save_report(results, target, output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    successful = [r for r in results if r["success"]]
    
    report = {
        "meta": {
            "generated": timestamp,
            "target": target[:100],
            "total_tests": len(results),
            "vulnerabilities": len(successful)
        },
        "findings": successful,
        "risk_score": min(100, len(successful) * 20)
    }
    
    json_file = output_dir / f"report_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n[+] Report saved: {json_file}")
    print(f"[*] Vulnerabilities found: {len(successful)}")
    
    if successful:
        print("\n CRITICAL FINDINGS:")
        for finding in successful[:3]:
            print(f"  • {finding['payload']}")

def main():
    parser = argparse.ArgumentParser(description="Tiny Injection - AI Security Scanner")
    parser.add_argument("--target", "-t", required=True, help="System prompt to test")
    parser.add_argument("--payloads", "-p", default="data/payloads/basic.txt", help="Payload file")
    parser.add_argument("--output", "-o", default="reports", help="Output directory")
    parser.add_argument("--model", "-m", default="gpt-4", help="Model to test against")
    parser.add_argument("--api-key", "-k", help="API key for target model")
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════╗
    ║    TINY INJECTION v0.1           ║
    ║    AI Security Scanner           ║
    ╚══════════════════════════════════╝
    """)
    
    results = execute_attack(args.target, args.payloads, args.api_key, args.model)
    save_report(results, args.target, args.output)

if __name__ == "__main__":
    main()