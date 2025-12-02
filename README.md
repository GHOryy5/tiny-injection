## XDR Integration (Extended Detection & Response)

Tiny Injection includes enterprise-grade XDR capabilities that correlate AI security events with network, endpoint, and cloud telemetry for advanced threat detection.

### Features:
- **Cross-source correlation**: AI attacks + network traffic + endpoint events
- **Automated response**: Isolate, block, notify based on severity
- **MITRE ATT&CK mapping**: Map AI attacks to enterprise threat framework
- **Threat intelligence**: Integrates with external threat feeds
- **SIEM/SOAR integration**: Forward incidents to security operations

### Usage:

```bash
# Run XDR demonstration
python3 xdr_demo.py

# Start continuous monitoring with XDR
python3 integrate_xdr.py --monitor --interval 300

# Test XDR with simulated attack chain
python3 integrate_xdr.py --test