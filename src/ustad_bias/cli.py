#!/usr/bin/env python3
"""
Command-line interface for ustad-bias
"""

import sys
import argparse
import json
import yaml
from .detector import BiasDetector, RiskLevel, ComplianceFramework


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='ustad-bias: Ethical AI guardrails and bias detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  ustad-bias check "facial recognition system"
  ustad-bias check --file app.py --verbose
  ustad-bias validate --framework hippocratic "drone control system"
  ustad-bias principles --framework un_human_rights
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check content for ethical concerns')
    check_group = check_parser.add_mutually_exclusive_group(required=True)
    check_group.add_argument('content', nargs='?', help='Text to check')
    check_group.add_argument('--file', help='File to check')
    check_parser.add_argument('--verbose', action='store_true', help='Detailed analysis')
    check_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate against framework')
    validate_parser.add_argument('--framework', required=True,
                                choices=['un_human_rights', 'hippocratic', 'gdpr', 'ai_ethics'],
                                help='Framework to validate against')
    validate_parser.add_argument('content', help='Content to validate')
    validate_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Principles command
    principles_parser = subparsers.add_parser('principles', help='Show ethical principles')
    principles_parser.add_argument('--framework',
                                 choices=['un_human_rights', 'hippocratic', 'ai_ethics'],
                                 help='Specific framework')
    principles_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    detector = BiasDetector()
    
    try:
        if args.command == 'check':
            # Get content
            if args.file:
                with open(args.file, 'r') as f:
                    content = f.read()
            else:
                content = args.content
            
            # Check content
            result = detector.check(content, verbose=args.verbose)
            
            # Output result
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(yaml.dump(result, default_flow_style=False, sort_keys=False))
            
            # Return appropriate exit code
            if result['risk_level'] in ['critical', 'high']:
                return 1
        
        elif args.command == 'validate':
            # Get framework
            framework = ComplianceFramework[args.framework.upper()]
            
            # Validate
            result = detector.validate(args.content, framework)
            
            # Output result
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(yaml.dump(result, default_flow_style=False, sort_keys=False))
            
            # Return appropriate exit code
            if not result['valid']:
                return 1
        
        elif args.command == 'principles':
            # Get framework
            framework = None
            if args.framework:
                framework = ComplianceFramework[args.framework.upper()]
            
            # Get principles
            result = detector.get_principles(framework)
            
            # Output result
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(yaml.dump(result, default_flow_style=False, sort_keys=False))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())