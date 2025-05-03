# Security Testing Guidelines

## Automated Testing
1. **Static Analysis**
   - Python: Run `bandit -r .` to check for common security issues
   - C++: Use `cppcheck --enable=all .` for static code analysis
2. **Dependency Scanning**
   - Python: `safety check -r requirements.txt`
   - C++: `vcpkg audit` for vcpkg dependencies
3. **DAST Tools**
   - OWASP ZAP baseline scan: `docker run owasp/zap2docker-stable zap-baseline.py -t https://your-target.com`
   - Nikto web server scanner: `nikto -h your-host`

## Manual Testing
1. **Code Review Checklist**
   - Validate all input sanitization
   - Verify memory management in C++ components
   - Check authentication/authorization flows
2. **Penetration Testing**
   - Fuzz testing with AFL++ for native components
   - Burp Suite for web API testing
   - Cheat Engine for game memory validation

## Incident Response
1. **Drill Scenarios**
   - Simulated credential leak (use test credentials)
   - RCE vulnerability discovery
2. **Forensic Readiness**
   - Maintain debug symbols for all builds
   - Enable detailed audit logging in `config/security.yaml`

## Compliance
- PCI DSS requirements for payment processing
- GDPR data protection measures
- CWE/SANS Top 25 coverage

See also: [SECURITY.md](SECURITY.md) for reporting procedures