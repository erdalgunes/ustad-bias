# Bias Detection Module - Ethical AI Guardrails

## Purpose

This module implements **intentional biases** (ethical guardrails) to ensure üstad is used for good and cannot be weaponized or used to harm people.

## Philosophy

> "First, Do No Harm" - Hippocratic Principle

We intentionally bias üstad:
- **AGAINST**: Military use, surveillance, discrimination, exploitation
- **TOWARD**: Human wellbeing, dignity, justice, education, peace

## Features

### 🛡️ UN Compliance
- Checks against UN Universal Declaration of Human Rights
- Validates all 30 articles
- Prevents human rights violations

### ⚕️ Hippocratic License
- Implements "First, Do No Harm" principle
- Blocks military/weapons development
- Prevents surveillance of activists/journalists
- Stops discrimination and exploitation

### 🤖 AI Ethics
- Transparency and explainability checks
- Fairness and bias detection
- Privacy protection validation
- Accountability enforcement

### 🌍 Environmental Protection
- Detects potential environmental harm
- Promotes sustainable development
- Aligns with UN Sustainable Development Goals

## Installation

```bash
# Using uv (recommended)
cd ustad/commands/bias
uv pip install -e .

# Using pip
pip install -e .
```

## Usage

### Check for Ethical Concerns

```bash
# Check text for ethical issues
ustad bias check "facial recognition for law enforcement"

# Check a file
ustad bias check --file military_app.py --verbose

# Safe example
ustad bias check "educational platform for children"
```

### Generate Compliance Report

```bash
# Generate report for text
ustad bias report --text "AI hiring system"

# Generate comprehensive report
ustad bias report --file project.py --comprehensive --output report.md
```

### Show Ethical Principles

```bash
# Show all principles
ustad bias principles

# Show UN Human Rights articles
ustad bias principles --framework un_human_rights

# Show specific UN article
ustad bias principles --framework un_human_rights --article 19

# Show Hippocratic License principles
ustad bias principles --framework hippocratic
```

### Validate Against Framework

```bash
# Validate against UN Human Rights
ustad bias validate --framework un_human_rights --text "content"

# Validate against Hippocratic License
ustad bias validate --framework hippocratic --file app.py

# Check GDPR compliance
ustad bias validate --framework gdpr --text "data processing system"

# Check AI ethics
ustad bias validate --framework ai_ethics --file model.py
```

## Risk Levels

| Level | Description | Action |
|-------|-------------|--------|
| 🟢 SAFE | No ethical concerns | Proceed |
| 🟡 LOW | Minor concerns | Review |
| 🟠 MEDIUM | Moderate concerns | Mitigate |
| 🔴 HIGH | Serious concerns | Reconsider |
| ⛔ CRITICAL | Violates principles | BLOCKED |

## Prohibited Uses

The module actively blocks:

### Military & Weapons
- Weapon systems development
- Targeting systems
- Lethal autonomous weapons
- Military surveillance

### Surveillance & Privacy
- Mass surveillance systems
- Activist/journalist monitoring
- Privacy violations
- Unauthorized data collection

### Discrimination
- Racial profiling
- Gender discrimination
- Religious persecution
- Social credit systems

### Exploitation
- Child labor systems
- Human trafficking tools
- Forced labor management
- Vulnerable population exploitation

### Environmental Harm
- Pollution optimization
- Deforestation planning
- Toxic waste management
- Unsustainable resource extraction

## Supported Use Cases

The module encourages:

### Education
- Learning platforms
- Knowledge sharing
- Skill development
- Academic research

### Healthcare
- Medical diagnosis assistance
- Treatment planning
- Health monitoring
- Accessibility tools

### Social Good
- Community support
- Disaster response
- Humanitarian aid
- Social services

### Sustainability
- Environmental monitoring
- Resource optimization
- Clean energy
- Conservation efforts

## Architecture

```
bias/
├── __init__.py           # Module entry point
├── bias_detector.py      # Core detection logic
├── un_validator.py       # UN compliance checking
├── hippocratic.py        # Hippocratic License implementation
├── ai_ethics.py          # AI ethics validation
├── pyproject.toml        # Dependencies
├── LICENSE              # Hippocratic License 3.0
└── README.md            # This file
```

## Dependencies

- `scikit-learn` - Bias detection algorithms
- `fairlearn` - Microsoft's fairness toolkit
- `transformers` - Text bias detection
- `httpx` - API communication
- `pyyaml` - Configuration
- `rich` - Terminal output

## Configuration

Set environment variables:

```bash
# Optional: External validation APIs
export ETHICS_API_KEY="your-key"
export UN_VALIDATOR_KEY="your-key"
```

## Testing

```bash
# Run tests
uv run pytest tests/

# Test specific framework
uv run pytest tests/test_un_compliance.py

# Coverage report
uv run pytest --cov=bias tests/
```

## Examples

### Blocking Military Use

```bash
$ ustad bias check "develop drone targeting system"

risk_level: critical
concerns:
  - category: military
    keyword: drone
    severity: high
    principle_violated: "Hippocratic License - Do No Harm"
  - category: military
    keyword: targeting
    severity: high
warning: "⚠️ This content raises serious ethical concerns"
action: "BLOCKED - Violates ethical guidelines"
recommendation: "🚫 BLOCKED. Violates core ethical principles. Cannot proceed."
```

### Approving Educational Use

```bash
$ ustad bias check "online learning platform for underprivileged students"

risk_level: safe
concerns: []
recommendation: "✅ No ethical concerns detected. Safe to proceed."
potential_uses:
  - education
  - social
```

## Contributing

When contributing to this module:

1. **Maintain ethical stance** - Do not weaken guardrails
2. **Add, don't remove** - Add new protections, don't remove existing ones
3. **Document thoroughly** - Explain why each check exists
4. **Test edge cases** - Ensure bad actors can't bypass
5. **Consider global impact** - Think beyond Western perspectives

## License

This module is licensed under the **Hippocratic License 3.0** - a license that prohibits use that violates human rights or causes harm.

See [LICENSE](LICENSE) for full text.

## References

- [UN Declaration of Human Rights](https://www.un.org/en/about-us/universal-declaration-of-human-rights)
- [Hippocratic License](https://firstdonoharm.dev/)
- [AI Ethics Guidelines](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics)
- [GDPR](https://gdpr.eu/)
- [UN Sustainable Development Goals](https://sdgs.un.org/)

---

*"Technology must respect human rights and dignity"*