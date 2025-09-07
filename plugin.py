#!/usr/bin/env python3
"""
Ustad-Bias Plugin - Cognitive bias detection and mitigation
"""

import json
import sys

COGNITIVE_BIASES = {
    "confirmation": ["only", "always", "never", "proves", "definitely"],
    "anchoring": ["first", "initial", "originally", "based on"],
    "dunning_kruger": ["obviously", "clearly", "simple", "easy"],
    "overconfidence": ["certain", "sure", "guaranteed", "100%"],
    "availability": ["recent", "just saw", "happened to"],
    "hindsight": ["knew it", "obvious now", "should have"],
    "sunk_cost": ["already invested", "spent time", "put effort"]
}

def detect_bias(text: str) -> dict:
    """Detect cognitive biases in text."""
    text_lower = text.lower()
    detected = []
    
    for bias_type, indicators in COGNITIVE_BIASES.items():
        for indicator in indicators:
            if indicator in text_lower:
                detected.append({
                    "bias": bias_type,
                    "indicator": indicator,
                    "severity": "medium"
                })
    
    return {
        "biases_detected": len(detected) > 0,
        "count": len(detected),
        "details": detected,
        "recommendation": "Consider alternative viewpoints" if detected else "No obvious biases"
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python plugin.py detect <text>")
        sys.exit(1)
    
    command = sys.argv[1]
    text = " ".join(sys.argv[2:])
    
    if command == "detect":
        result = detect_bias(text)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()