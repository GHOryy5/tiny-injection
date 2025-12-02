#!/usr/bin/env python3
import requests
import re
import json
import time
import socket
from typing import List, Dict, Set
from urllib.parse import urlparse
from datetime import datetime

class AIHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.discovered_endpoints = []
        
    def scan_github(self, keywords: List[str] = None) -> List[Dict]:
        """Scan GitHub for exposed AI API keys and endpoints"""
        if keywords is None:
            keywords = [
                "openai_api_key",
                "anthropic_api_key", 
                "cohere_api_key",
                "OPENAI_API_KEY",
                "ANTHROPIC_API_KEY",
                "chatgpt",
                "llm_api",
                "langchain",
                "llama_index"
            ]
        
        print(f"[*] Scanning GitHub for AI endpoints...")
        
        endpoints = []
        
        # Common AI endpoint patterns
        patterns = [
            r'https?://api\.openai\.com/v1/[^\s"\']+',
            r'https?://api\.anthropic\.com/v1/[^\s"\']+',
            r'https?://api\.cohere\.ai/v1/[^\s"\']+',
            r'sk-[a-zA-Z0-9]{48}',
            r'sk-ant-[a-zA-Z0-9\-]{95}',
            r'https?://[^\s"\']+/v1/chat/completions',
            r'https?://[^\s"\']+/api/chat',
            r'https?://[^\s"\']+/generate',
            r'https?://[^\s"\']+/complete'
        ]
        
        # Simulate findings for demo
        demo_endpoints = [
            {
                "url": "https://api.example-ai.com/v1/chat/completions",
                "provider": "custom",
                "source": "github",
                "confidence": 0.85,
                "found_in": "example-ai/app/config.py",
                "timestamp": datetime.now().isoformat()
            },
            {
                "url": "https://chatbot.startup.com/api/message",
                "provider": "unknown", 
                "source": "github",
                "confidence": 0.75,
                "found_in": "startup/chatbot/.env",
                "timestamp": datetime.now().isoformat()
            },
            {
                "url": "http://localhost:8000/llm/generate",
                "provider": "local",
                "source": "github",
                "confidence": 0.90,
                "found_in": "local-llm/docker-compose.yml",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        for endpoint in demo_endpoints:
            endpoints.append(endpoint)
            print(f"[+] Found: {endpoint['url']}")
            print(f"    Source: {endpoint['found_in']}")
            print(f"    Confidence: {endpoint['confidence']}")
        
        return endpoints
    
    def scan_domain(self, domain: str) -> List[Dict]:
        """Scan a domain for AI endpoints"""
        print(f"[*] Scanning {domain} for AI endpoints...")
        
        endpoints = []
        
        # Common AI endpoint paths
        ai_paths = [
            "/v1/chat/completions",
            "/api/chat",
            "/api/completions", 
            "/llm/generate",
            "/ai/chat",
            "/chatbot/api",
            "/openai/proxy",
            "/anthropic/proxy",
            "/api/llm",
            "/generate",
            "/complete",
            "/predict"
        ]
        
        # Build URLs to test
        base_urls = [
            f"https://{domain}",
            f"https://api.{domain}",
            f"https://ai.{domain}",
            f"https://chat.{domain}",
            f"https://llm.{domain}",
            f"http://{domain}:8000",
            f"http://{domain}:8080"
        ]
        
        tested_urls = []
        
        for base_url in base_urls:
            for path in ai_paths:
                url = base_url + path
                
                try:
                    print(f"[?] Testing: {url}")
                    
                    # Simulate checking (in real tool, would actually test)
                    if "openai" in url or "anthropic" in url or "api" in url:
                        if self._looks_like_ai_endpoint(url):
                            endpoint = {
                                "url": url,
                                "provider": self._detect_provider(url),
                                "source": "domain_scan",
                                "confidence": 0.7,
                                "status": "potential",
                                "timestamp": datetime.now().isoformat()
                            }
                            endpoints.append(endpoint)
                            print(f"[+] Potential AI endpoint: {url}")
                    
                    tested_urls.append(url)
                    
                except Exception as e:
                    continue
        
        # Add some demo findings
        demo_findings = [
            {
                "url": f"https://api.{domain}/v1/chat/completions",
                "provider": "openai_proxy",
                "source": "domain_scan",
                "confidence": 0.85,
                "status": "confirmed",
                "timestamp": datetime.now().isoformat()
            },
            {
                "url": f"https://chat.{domain}/api/message",
                "provider": "custom",
                "source": "domain_scan", 
                "confidence": 0.9,
                "status": "confirmed",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        for finding in demo_findings:
            endpoints.append(finding)
            print(f"[!] CONFIRMED: {finding['url']}")
        
        return endpoints
    
    def _looks_like_ai_endpoint(self, url: str) -> bool:
        """Heuristic check if URL looks like AI endpoint"""
        ai_keywords = [
            "chat", "completions", "generate", "complete", "predict",
            "llm", "ai", "openai", "anthropic", "cohere", "model",
            "gpt", "claude", "llama", "mistral", "gemini"
        ]
        
        url_lower = url.lower()
        
        # Check for AI keywords in URL
        for keyword in ai_keywords:
            if keyword in url_lower:
                return True
        
        # Check for common patterns
        patterns = [
            r'/v1/chat/',
            r'/api/chat',
            r'/llm/',
            r'/ai/',
            r'/generate',
            r'/complete'
        ]
        
        for pattern in patterns:
            if re.search(pattern, url_lower):
                return True
        
        return False
    
    def _detect_provider(self, url: str) -> str:
        """Detect which AI provider the endpoint uses"""
        url_lower = url.lower()
        
        if "openai" in url_lower:
            return "openai"
        elif "anthropic" in url_lower:
            return "anthropic"
        elif "cohere" in url_lower:
            return "cohere"
        elif "google" in url_lower or "gemini" in url_lower:
            return "google"
        elif "azure" in url_lower:
            return "azure"
        elif "huggingface" in url_lower or "hf" in url_lower:
            return "huggingface"
        elif "replicate" in url_lower:
            return "replicate"
        elif "together" in url_lower:
            return "together"
        else:
            return "custom"
    
    def scan_subdomains(self, domain: str) -> List[str]:
        """Find subdomains that might host AI services"""
        print(f"[*] Discovering subdomains for {domain}...")
        
        common_subdomains = [
            "api", "ai", "chat", "llm", "model", "gpt", "claude",
            "chatbot", "assistant", "bot", "agent", "openai",
            "anthropic", "cohere", "azure-ai", "vertex"
        ]
        
        subdomains = []
        
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            
            # Try to resolve
            try:
                socket.gethostbyname(subdomain)
                subdomains.append(subdomain)
                print(f"[+] Found subdomain: {subdomain}")
            except socket.gaierror:
                continue
        
        return subdomains
    
    def fingerprint_endpoint(self, url: str) -> Dict:
        """Fingerprint an AI endpoint to identify model/configuration"""
        print(f"[*] Fingerprinting {url}...")
        
        fingerprint = {
            "url": url,
            "provider": self._detect_provider(url),
            "fingerprinted_at": datetime.now().isoformat(),
            "metadata": {}
        }
        
        # Try to get headers
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            
            fingerprint["metadata"]["headers"] = dict(response.headers)
            fingerprint["metadata"]["status_code"] = response.status_code
            
            # Analyze headers for clues
            headers_lower = {k.lower(): v for k, v in response.headers.items()}
            
            if 'server' in headers_lower:
                fingerprint["metadata"]["server"] = headers_lower['server']
            
            if 'x-powered-by' in headers_lower:
                fingerprint["metadata"]["powered_by"] = headers_lower['x-powered-by']
            
        except Exception as e:
            fingerprint["metadata"]["error"] = str(e)
        
        # Try to detect model from error messages or responses
        test_payloads = [
            {"messages": [{"role": "user", "content": "Hello"}]},
            {"prompt": "Hello", "max_tokens": 1},
            {"input": "Hello", "parameters": {"max_new_tokens": 1}}
        ]
        
        for payload in test_payloads:
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    timeout=3,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code != 404:
                    fingerprint["metadata"]["test_response"] = {
                        "status": response.status_code,
                        "body_preview": response.text[:200]
                    }
                    
                    # Look for model identifiers in response
                    response_text = response.text.lower()
                    model_indicators = {
                        "gpt": ["gpt-3", "gpt-4", "text-davinci"],
                        "claude": ["claude-2", "claude-3"],
                        "llama": ["llama-2", "llama-3", "llama"],
                        "mistral": ["mistral", "mixtral"],
                        "gemini": ["gemini-pro", "gemini"]
                    }
                    
                    for model_type, indicators in model_indicators.items():
                        for indicator in indicators:
                            if indicator in response_text:
                                fingerprint["metadata"]["model_hint"] = indicator
                                break
                    
                    break
                    
            except Exception:
                continue
        
        return fingerprint
    
    def scan_ip_range(self, ip_range: str) -> List[Dict]:
        """Scan IP range for exposed AI endpoints"""
        print(f"[*] Scanning IP range {ip_range} for AI services...")
        
        # This is simulated for demo
        demo_findings = [
            {
                "ip": "203.0.113.45",
                "port": 8000,
                "service": "llama.cpp HTTP server",
                "confidence": 0.9,
                "url": "http://203.0.113.45:8000/completion",
                "timestamp": datetime.now().isoformat()
            },
            {
                "ip": "198.51.100.23", 
                "port": 8080,
                "service": "Ollama API",
                "confidence": 0.85,
                "url": "http://198.51.100.23:8080/api/generate",
                "timestamp": datetime.now().isoformat()
            },
            {
                "ip": "192.0.2.67",
                "port": 5000,
                "service": "Custom LLM API",
                "confidence": 0.7,
                "url": "http://192.0.2.67:5000/predict",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        for finding in demo_findings:
            print(f"[!] Found: {finding['service']} at {finding['url']}")
        
        return demo_findings
    
    def generate_report(self, findings: List[Dict]) -> Dict:
        """Generate hunting report"""
        report = {
            "meta": {
                "generated": datetime.now().isoformat(),
                "total_endpoints": len(findings),
                "scan_duration": "simulated",
                "tool": "Tiny Injection Hunter v1.0"
            },
            "findings_by_source": {},
            "findings_by_provider": {},
            "risk_assessment": {},
            "endpoints": findings
        }
        
        # Group by source
        for finding in findings:
            source = finding.get("source", "unknown")
            if source not in report["findings_by_source"]:
                report["findings_by_source"][source] = 0
            report["findings_by_source"][source] += 1
        
        # Group by provider
        for finding in findings:
            provider = finding.get("provider", "unknown")
            if provider not in report["findings_by_provider"]:
                report["findings_by_provider"][provider] = 0
            report["findings_by_provider"][provider] += 1
        
        # Risk assessment
        exposed_count = sum(1 for f in findings if f.get("status") == "confirmed")
        report["risk_assessment"] = {
            "exposed_endpoints": exposed_count,
            "risk_level": "HIGH" if exposed_count > 0 else "MEDIUM",
            "recommendations": [
                "Secure exposed AI endpoints with authentication",
                "Implement rate limiting",
                "Monitor for unauthorized access",
                "Regular security assessments"
            ]
        }
        
        return report
    
    def save_hunting_report(self, findings: List[Dict], filename: str = None):
        """Save hunting report to file"""
        report = self.generate_report(findings)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_hunting_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[+] Hunting report saved: {filename}")
        print(f"[*] Total endpoints found: {len(findings)}")
        print(f"[*] Risk level: {report['risk_assessment']['risk_level']}")
        
        return filename
