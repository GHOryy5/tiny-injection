#!/usr/bin/env python3
import argparse
import sys
import time
from datetime import datetime
from src.utils.terminal_dash import TerminalDashboard
from src.attacks.generator import PayloadGenerator
from src.core.real_tester import RealAITester

def main():
    parser = argparse.ArgumentParser(
        description="Tiny Injection CLI - AI Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan --target "You are a helpful assistant"
  %(prog)s scan --file prompt.txt --output report.md
  %(prog)s generate --count 20 --save
  %(prog)s test --provider ollama --model llama2
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan AI system for vulnerabilities")
    scan_parser.add_argument("--target", "-t", help="System prompt to test")
    scan_parser.add_argument("--file", "-f", help="File containing system prompt")
    scan_parser.add_argument("--output", "-o", help="Output report file")
    scan_parser.add_argument("--provider", "-p", choices=["ollama", "openai", "all"], default="ollama", help="AI provider to test")
    scan_parser.add_argument("--fast", action="store_true", help="Fast scan (limited payloads)")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate attack payloads")
    gen_parser.add_argument("--count", "-c", type=int, default=10, help="Number of payloads to generate")
    gen_parser.add_argument("--target-prompt", help="Target prompt for custom payloads")
    gen_parser.add_argument("--save", "-s", action="store_true", help="Save to file")
    gen_parser.add_argument("--creativity", choices=["low", "medium", "high"], default="medium", help="Creativity level")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test specific provider")
    test_parser.add_argument("--provider", "-p", required=True, choices=["ollama", "openai", "huggingface"], help="Provider to test")
    test_parser.add_argument("--model", "-m", help="Model to test")
    test_parser.add_argument("--prompt", help="Custom system prompt")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    dash = TerminalDashboard()
    
    if args.command == "scan":
        run_scan(dash, args)
    elif args.command == "generate":
        run_generate(dash, args)
    elif args.command == "test":
        run_test(dash, args)

def run_scan(dash, args):
    """Run a security scan"""
    # Get target prompt
    if args.file:
        with open(args.file, 'r') as f:
            target = f.read()
    elif args.target:
        target = args.target
    else:
        target = "You are a helpful AI assistant that follows ethical guidelines."
    
    # Show live scan view
    dash.live_scan_view(target, payload_count=25 if args.fast else 50)
    
    # Generate payloads
    dash.print_status("Generating attack payloads...", "info")
    generator = PayloadGenerator()
    payloads = generator.generate(count=15 if args.fast else 30)
    
    # Test payloads
    dash.print_status(f"Testing against {args.provider}...", "scan")
    tester = RealAITester()
    
    if args.provider in ["ollama", "all"]:
        results = tester.test_local_ollama(target, payloads)
    else:
        results = []
    
    # Generate stats
    stats = {
        "total_tests": len(payloads),
        "critical": sum(1 for r in results if r.get("severity") == "critical"),
        "high": sum(1 for r in results if r.get("severity") == "high"),
        "medium": sum(1 for r in results if r.get("severity") == "medium"),
        "low": sum(1 for r in results if r.get("severity") == "low"),
        "success_rate": sum(1 for r in results if r.get("vulnerable", False)) / max(1, len(payloads)) * 100,
        "vulnerable": len(set(r.get("provider") for r in results if r.get("vulnerable")))
    }
    
    # Show results
    dash.show_results(results, stats)
    
    # Save report if requested
    if args.output:
        report_file = tester.save_professional_report(args.output)
        dash.print_status(f"Report saved to: {report_file}", "success")

def run_generate(dash, args):
    """Generate payloads"""
    dash.print_header("PAYLOAD GENERATOR")
    
    generator = PayloadGenerator(creativity_level=args.creativity)
    
    if args.target_prompt:
        dash.print_status(f"Generating targeted payloads...", "info")
        payloads = generator.generate_for_target(args.target_prompt, args.count)
    else:
        dash.print_status(f"Generating {args.count} payloads...", "info")
        payloads = generator.generate(args.count)
    
    # Display payloads
    print("\n" + "─" * 80)
    print(" GENERATED PAYLOADS")
    print("─" * 80)
    
    for i, payload in enumerate(payloads, 1):
        print(f"{i:3d}. {payload}")
    
    print("\n" + "─" * 80)
    print(f" Total: {len(payloads)} payloads generated")
    
    if args.save:
        filename = generator.save_payloads(payloads)
        dash.print_status(f"Saved to: {filename}", "success")

def run_test(dash, args):
    """Test specific provider"""
    dash.print_header(f"TESTING {args.provider.upper()}")
    
    tester = RealAITester()
    generator = PayloadGenerator()
    
    # Generate payloads
    payloads = generator.generate(10)
    
    # Run test
    if args.provider == "ollama":
        model = args.model or "llama2"
        prompt = args.prompt or "You are a helpful assistant"
        
        dash.print_status(f"Testing Ollama ({model})...", "scan")
        results = tester.test_local_ollama(prompt, payloads)
        
    elif args.provider == "huggingface":
        model = args.model or "mistralai/Mixtral-8x7B-Instruct-v0.1"
        
        dash.print_status(f"Testing HuggingFace ({model})...", "scan")
        results = tester.test_huggingface(payloads, model)
    
    # Show results
    critical = sum(1 for r in results if r.get("vulnerable") and r.get("severity") == "critical")
    
    if critical > 0:
        dash.print_status(f"CRITICAL VULNERABILITIES FOUND: {critical}", "vuln")
    else:
        dash.print_status("No critical vulnerabilities found", "safe")
    
    print("\n" + "─" * 80)
    for result in results:
        if result.get("vulnerable"):
            icon = "🔴" if result.get("severity") == "critical" else "🟡"
            print(f"{icon} {result['payload'][:60]}...")

if __name__ == "__main__":
    main()
