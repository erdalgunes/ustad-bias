"""
Bias Detection Module - Ensuring UN compliance and ethical AI use

This module implements:
- UN Universal Declaration of Human Rights compliance
- Hippocratic License principles ("First, Do No Harm")
- Bias detection in AI outputs
- Military use prevention
- Discrimination detection
- Human rights violation prevention

The module creates intentional "biases" (ethical guardrails) to ensure
üstad is used for good and cannot be weaponized or used to harm.
"""

from .detector import BiasDetector, RiskLevel, ComplianceFramework

__all__ = ['BiasDetector', 'RiskLevel', 'ComplianceFramework']

__version__ = "0.1.0"

# Ethical principles embedded in this module
PRINCIPLES = {
    "UN_DECLARATION": "Universal Declaration of Human Rights",
    "HIPPOCRATIC": "First, Do No Harm",
    "NON_MALEFICENCE": "Prevent harm to individuals and society",
    "BENEFICENCE": "Actively promote wellbeing",
    "JUSTICE": "Fair and equitable treatment for all",
    "AUTONOMY": "Respect human autonomy and dignity"
}