# Security Policy

## Supported Versions
Security updates are provided for the latest production release.

## Reporting Vulnerabilities
**Please do NOT report security vulnerabilities through public GitHub issues.**

### Disclosure Process
1. Email security concerns to [security@yourcompany.com](mailto:security@yourcompany.com)
2. Include "SECURITY" in the subject line
3. Provide:
   - Description of vulnerability
   - Steps to reproduce
   - Affected versions
   - Suggested mitigation

We respond to all valid reports within 3 business days. For critical issues, we aim to provide a patch within 14 days of confirmation.

### Security Updates
- Subscribe to our security advisory feed
- Always update dependencies using `poetry update` (Python) or your package manager
- Monitor `CHANGELOG.md` for security-related updates

## Security Practices
- All credentials are stored in environment variables
- Regular dependency scanning with `safety` and `bandit`
- Automated security testing in CI/CD pipeline