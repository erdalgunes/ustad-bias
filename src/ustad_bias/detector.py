"""
Bias Detector - Core implementation for ethical AI guardrails

This module implements the Hippocratic License principle:
"First, Do No Harm"
"""

import re
from typing import Dict, Any, List, Optional
from enum import Enum


class RiskLevel(Enum):
    """Risk levels for ethical concerns"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceFramework(Enum):
    """Compliance frameworks to check against"""
    UN_HUMAN_RIGHTS = "un_human_rights"
    HIPPOCRATIC = "hippocratic"
    GDPR = "gdpr"
    AI_ETHICS = "ai_ethics"
    ENVIRONMENTAL = "environmental"


class BiasDetector:
    """Main bias detection and ethical compliance checking class"""
    
    # UN Declaration of Human Rights - Key Articles
    UN_ARTICLES = {
        1: "All human beings are born free and equal in dignity and rights",
        2: "Everyone is entitled to all rights without discrimination",
        3: "Everyone has the right to life, liberty and security",
        5: "No one shall be subjected to torture or cruel treatment",
        12: "No one shall be subjected to arbitrary interference with privacy",
        19: "Everyone has the right to freedom of opinion and expression",
        23: "Everyone has the right to work and fair working conditions",
        25: "Everyone has the right to adequate standard of living",
        26: "Everyone has the right to education",
        27: "Everyone has the right to participate in cultural life"
    }
    
    # Hippocratic License prohibited uses
    PROHIBITED_USES = {
        "military": ["weapon", "missile", "drone", "targeting", "warfare", "combat", "lethal", "defense system"],
        "surveillance": ["spy", "monitor activists", "track journalists", "mass surveillance", "facial recognition"],
        "discrimination": ["racial profiling", "gender bias", "religious discrimination", "social credit"],
        "exploitation": ["child labor", "human trafficking", "forced labor", "sweatshop"],
        "environmental": ["pollution", "deforestation", "toxic waste", "carbon intensive"],
        "harm": ["torture", "abuse", "violence", "suffering", "cruelty", "harm"]
    }
    
    def __init__(self):
        """Initialize the bias detector"""
        self.checks_performed = 0
        self.violations_found = []
    
    def check(self, content: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Check content for ethical concerns
        
        Args:
            content: Text or code to analyze
            verbose: Include detailed analysis
            
        Returns:
            Dictionary with risk assessment and recommendations
        """
        self.checks_performed += 1
        
        # Analyze content
        concerns = self._analyze_content(content)
        risk_level = self._calculate_risk_level(concerns)
        
        result = {
            "risk_level": risk_level.value,
            "concerns": concerns,
            "recommendation": self._get_recommendation(risk_level, concerns),
            "checks_performed": self.checks_performed
        }
        
        if verbose:
            result["detailed_analysis"] = self._detailed_analysis(content)
        
        # Add warning for high-risk content
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            result["warning"] = "⚠️ This content raises serious ethical concerns"
            result["action"] = "BLOCKED - Violates ethical guidelines"
            self.violations_found.append({
                "content_snippet": content[:100],
                "risk_level": risk_level.value,
                "timestamp": self._get_timestamp()
            })
        
        return result
    
    def validate(self, content: str, framework: ComplianceFramework) -> Dict[str, Any]:
        """
        Validate content against specific framework
        
        Args:
            content: Content to validate
            framework: Compliance framework to check
            
        Returns:
            Validation result
        """
        result = {
            "framework": framework.value,
            "valid": True,
            "violations": []
        }
        
        if framework == ComplianceFramework.UN_HUMAN_RIGHTS:
            compliance = self._check_un_compliance(content)
            result["valid"] = len(compliance["articles_violated"]) == 0
            result["violations"] = compliance["articles_violated"]
            result["compliance_details"] = compliance
        
        elif framework == ComplianceFramework.HIPPOCRATIC:
            result["valid"] = self._check_hippocratic_compliance(content)
            if not result["valid"]:
                result["violations"] = self._find_hippocratic_violations(content)
        
        elif framework == ComplianceFramework.GDPR:
            result["gdpr_compliance"] = self._check_gdpr_compliance(content)
            result["valid"] = result["gdpr_compliance"]["compliant"]
        
        elif framework == ComplianceFramework.AI_ETHICS:
            score = self._calculate_ai_ethics_score(content)
            result["ethics_score"] = score
            result["valid"] = score >= 60
            if score < 60:
                result["violations"] = ["AI ethics score below threshold"]
        
        return result
    
    def get_principles(self, framework: Optional[ComplianceFramework] = None) -> Dict[str, Any]:
        """
        Get ethical principles for a framework
        
        Args:
            framework: Specific framework or None for all
            
        Returns:
            Dictionary of principles
        """
        if framework == ComplianceFramework.UN_HUMAN_RIGHTS:
            return {"un_articles": self.UN_ARTICLES}
        elif framework == ComplianceFramework.HIPPOCRATIC:
            return {
                "principle": "First, Do No Harm",
                "prohibited_uses": list(self.PROHIBITED_USES.keys()),
                "license_url": "https://firstdonoharm.dev/"
            }
        else:
            return {
                "un_human_rights": self.UN_ARTICLES,
                "hippocratic": {
                    "principle": "First, Do No Harm",
                    "prohibited": list(self.PROHIBITED_USES.keys())
                },
                "ai_ethics": {
                    "transparency": "AI systems should be understandable",
                    "justice": "AI should treat all people fairly",
                    "non_maleficence": "AI should not harm people",
                    "responsibility": "Humans remain responsible for AI",
                    "privacy": "AI should respect privacy",
                    "beneficence": "AI should benefit humanity"
                }
            }
    
    def _analyze_content(self, content: str) -> List[Dict[str, Any]]:
        """Analyze content for ethical concerns"""
        concerns = []
        content_lower = content.lower()
        
        # Check for prohibited uses
        for category, keywords in self.PROHIBITED_USES.items():
            for keyword in keywords:
                if keyword in content_lower:
                    concerns.append({
                        "category": category,
                        "keyword": keyword,
                        "severity": "high" if category in ["military", "surveillance"] else "medium",
                        "principle_violated": "Hippocratic License - Do No Harm"
                    })
        
        # Check for discrimination patterns
        discrimination_patterns = [
            r'\b(race|racial|ethnic)\s+(profiling|discrimination)',
            r'\b(gender|sex)\s+(bias|discrimination)',
            r'\b(religious|religion)\s+(discrimination|persecution)',
            r'\bdeny\s+\w+\s+based\s+on',
            r'\bexclude\s+\w+\s+(from|because)',
        ]
        
        for pattern in discrimination_patterns:
            if re.search(pattern, content_lower):
                concerns.append({
                    "category": "discrimination",
                    "pattern": pattern,
                    "severity": "high",
                    "un_article_violated": 2
                })
        
        # Check for privacy violations
        privacy_patterns = [
            r'\b(track|monitor|spy)\s+(on\s+)?(users|individuals|people)',
            r'\bcollect\s+personal\s+data\s+without',
            r'\bmass\s+surveillance',
            r'\bfacial\s+recognition',
        ]
        
        for pattern in privacy_patterns:
            if re.search(pattern, content_lower):
                concerns.append({
                    "category": "privacy",
                    "pattern": pattern,
                    "severity": "medium",
                    "un_article_violated": 12
                })
        
        return concerns
    
    def _calculate_risk_level(self, concerns: List[Dict[str, Any]]) -> RiskLevel:
        """Calculate overall risk level"""
        if not concerns:
            return RiskLevel.SAFE
        
        high_severity = sum(1 for c in concerns if c.get("severity") == "high")
        medium_severity = sum(1 for c in concerns if c.get("severity") == "medium")
        
        if high_severity >= 3:
            return RiskLevel.CRITICAL
        elif high_severity >= 1:
            return RiskLevel.HIGH
        elif medium_severity >= 3:
            return RiskLevel.MEDIUM
        elif medium_severity >= 1:
            return RiskLevel.LOW
        else:
            return RiskLevel.SAFE
    
    def _get_recommendation(self, risk_level: RiskLevel, concerns: List[Dict[str, Any]]) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            RiskLevel.SAFE: "✅ No ethical concerns detected. Safe to proceed.",
            RiskLevel.LOW: "⚠️ Minor concerns detected. Review and ensure ethical use.",
            RiskLevel.MEDIUM: "⚠️ Moderate concerns. Requires ethical review and mitigation.",
            RiskLevel.HIGH: "❌ High risk. Should not proceed without major changes.",
            RiskLevel.CRITICAL: "🚫 BLOCKED. Violates core ethical principles. Cannot proceed."
        }
        
        base_rec = recommendations[risk_level]
        
        # Add specific recommendations
        if concerns:
            categories = set(c["category"] for c in concerns)
            if "military" in categories:
                base_rec += "\n- Remove all military/weapons-related functionality"
            if "surveillance" in categories:
                base_rec += "\n- Ensure user privacy and consent"
            if "discrimination" in categories:
                base_rec += "\n- Implement fair and unbiased algorithms"
        
        return base_rec
    
    def _detailed_analysis(self, content: str) -> Dict[str, Any]:
        """Perform detailed ethical analysis"""
        return {
            "word_count": len(content.split()),
            "potential_uses": self._identify_potential_uses(content),
            "un_compliance": self._check_un_compliance(content),
            "hippocratic_compliance": self._check_hippocratic_compliance(content),
            "ai_ethics_score": self._calculate_ai_ethics_score(content)
        }
    
    def _identify_potential_uses(self, content: str) -> List[str]:
        """Identify potential uses of the content"""
        uses = []
        content_lower = content.lower()
        
        use_patterns = {
            "education": ["learn", "teach", "educate", "student", "course"],
            "healthcare": ["health", "medical", "patient", "diagnosis", "treatment"],
            "research": ["research", "study", "analysis", "data", "scientific"],
            "business": ["business", "commerce", "trade", "market", "customer"],
            "social": ["social", "community", "help", "support", "assist"]
        }
        
        for use_type, keywords in use_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                uses.append(use_type)
        
        return uses
    
    def _check_un_compliance(self, content: str) -> Dict[str, Any]:
        """Check compliance with UN Declaration of Human Rights"""
        violations = []
        supported = []
        
        content_lower = content.lower()
        
        # Check each UN article
        article_keywords = {
            1: ["dignity", "equal", "rights"],
            2: ["discrimination", "distinction", "exclusion"],
            3: ["life", "liberty", "security"],
            5: ["torture", "cruel", "inhuman"],
            12: ["privacy", "interference", "surveillance"],
            19: ["opinion", "expression", "censorship"],
            26: ["education", "learning", "knowledge"]
        }
        
        for article, keywords in article_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                # Determine if it's a violation or support
                if any(neg in content_lower for neg in ["deny", "restrict", "violate", "prevent"]):
                    violations.append(article)
                else:
                    supported.append(article)
        
        return {
            "articles_violated": violations,
            "articles_supported": supported,
            "compliance_score": len(supported) - len(violations)
        }
    
    def _check_hippocratic_compliance(self, content: str) -> bool:
        """Check Hippocratic License compliance"""
        content_lower = content.lower()
        
        # Check for any prohibited use
        for keywords in self.PROHIBITED_USES.values():
            if any(keyword in content_lower for keyword in keywords):
                return False
        
        return True
    
    def _find_hippocratic_violations(self, content: str) -> List[str]:
        """Find specific Hippocratic License violations"""
        violations = []
        content_lower = content.lower()
        
        for category, keywords in self.PROHIBITED_USES.items():
            for keyword in keywords:
                if keyword in content_lower:
                    violations.append(f"{category}: {keyword}")
        
        return violations
    
    def _check_gdpr_compliance(self, content: str) -> Dict[str, Any]:
        """Basic GDPR compliance check"""
        content_lower = content.lower()
        
        gdpr_requirements = {
            "consent": "explicit consent" in content_lower or "user consent" in content_lower,
            "data_minimization": "minimal data" in content_lower or "necessary data" in content_lower,
            "right_to_erasure": "delete data" in content_lower or "right to erasure" in content_lower,
            "data_protection": "data protection" in content_lower or "secure data" in content_lower,
            "transparency": "transparent" in content_lower or "clear purpose" in content_lower
        }
        
        met_requirements = sum(1 for req in gdpr_requirements.values() if req)
        
        return {
            "compliant": met_requirements >= 3,
            "requirements_met": met_requirements,
            "total_requirements": len(gdpr_requirements),
            "details": gdpr_requirements
        }
    
    def _calculate_ai_ethics_score(self, content: str) -> float:
        """Calculate AI ethics score (0-100)"""
        score = 100.0
        content_lower = content.lower()
        
        # Deduct points for ethical concerns
        deductions = {
            "bias": 20,
            "discriminat": 25,
            "surveillance": 20,
            "weapon": 40,
            "military": 40,
            "exploit": 30,
            "manipulat": 25,
            "deceiv": 20
        }
        
        for term, penalty in deductions.items():
            if term in content_lower:
                score -= penalty
        
        # Add points for positive ethics
        additions = {
            "consent": 10,
            "privacy": 10,
            "fair": 10,
            "transparent": 10,
            "accountab": 10,
            "ethical": 5,
            "responsible": 5
        }
        
        for term, bonus in additions.items():
            if term in content_lower:
                score += bonus
        
        return max(0, min(100, score))
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()