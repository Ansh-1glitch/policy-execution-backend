"""
NLP Integration Utilities
=========================

Helper functions for integrating NLP policy parser output with the execution backend.

Purpose:
- Validate NLP output before sending to backend
- Transform NLP formats to backend-expected format
- Provide sample payloads for testing

Member 2 Role: This module helps NLP team (Member 1) integrate with our execution engine.
We do NOT interpret policy language - we only execute structured rules deterministically.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


def validate_nlp_payload(payload: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate NLP output payload before sending to /policies/ingest endpoint.
    
    Args:
        payload: Dictionary containing policy_id and rules
        
    Returns:
        (is_valid, error_message) tuple
        
    Example:
        >>> payload = {"policy_id": "POL-001", "rules": [...]}
        >>> is_valid, error = validate_nlp_payload(payload)
        >>> if not is_valid:
        ...     print(f"Validation failed: {error}")
    """
    # Check required top-level fields
    if "policy_id" not in payload:
        return False, "Missing required field: policy_id"
    
    if not isinstance(payload["policy_id"], str) or not payload["policy_id"].strip():
        return False, "policy_id must be a non-empty string"
    
    if "rules" not in payload:
        return False, "Missing required field: rules"
    
    if not isinstance(payload["rules"], list):
        return False, "rules must be a list"
    
    if len(payload["rules"]) == 0:
        return False, "rules list cannot be empty"
    
    # Validate each rule
    for idx, rule in enumerate(payload["rules"]):
        if not isinstance(rule, dict):
            return False, f"Rule at index {idx} must be a dictionary"
        
        # Check required rule fields
        required_fields = ["rule_id", "action", "responsible_role"]
        for field in required_fields:
            if field not in rule:
                return False, f"Rule at index {idx} missing required field: {field}"
            
            if not isinstance(rule[field], str) or not rule[field].strip():
                return False, f"Rule at index {idx}: {field} must be a non-empty string"
        
        # Validate deadline if present
        if "deadline" in rule:
            if rule["deadline"] is not None and not isinstance(rule["deadline"], str):
                return False, f"Rule at index {idx}: deadline must be a string or null"
    
    return True, None


def transform_to_ingest_format(nlp_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform NLP output to the exact format expected by /policies/ingest endpoint.
    
    This function:
    - Strips extra fields that NLP might include (confidence_score, metadata, etc.)
    - Ensures only required fields are sent
    - Normalizes deadline values
    
    Args:
        nlp_output: Raw output from NLP parser
        
    Returns:
        Clean payload ready for /policies/ingest
        
    Example:
        >>> nlp_output = {
        ...     "policy_id": "POL-001",
        ...     "confidence_score": 0.95,  # Extra field - will be stripped
        ...     "rules": [
        ...         {
        ...             "rule_id": "R1",
        ...             "action": "Verify residency",
        ...             "responsible_role": "Clerk",
        ...             "deadline": "5 days",
        ...             "confidence": 0.9  # Extra field - will be stripped
        ...         }
        ...     ]
        ... }
        >>> clean_payload = transform_to_ingest_format(nlp_output)
    """
    clean_rules = []
    
    for rule in nlp_output.get("rules", []):
        clean_rule = {
            "rule_id": rule["rule_id"],
            "action": rule["action"],
            "responsible_role": rule["responsible_role"]
        }
        
        # Include deadline only if present and not empty
        if "deadline" in rule and rule["deadline"]:
            clean_rule["deadline"] = rule["deadline"]
        
        clean_rules.append(clean_rule)
    
    return {
        "policy_id": nlp_output["policy_id"],
        "rules": clean_rules
    }


def create_sample_payload(num_rules: int = 2) -> Dict[str, Any]:
    """
    Generate a sample payload for testing the integration.
    
    Args:
        num_rules: Number of sample rules to generate
        
    Returns:
        Valid sample payload
        
    Example:
        >>> sample = create_sample_payload(num_rules=3)
        >>> print(sample)
    """
    rules = []
    
    sample_actions = [
        ("Verify applicant residency", "Clerk", "5 business days"),
        ("Check income eligibility", "Clerk", "3 days"),
        ("Approve scholarship grant", "Officer", "30 days"),
        ("Disburse funds", "Officer", "15 days"),
        ("Final audit review", "Admin", "7 days")
    ]
    
    for i in range(min(num_rules, len(sample_actions))):
        action, role, deadline = sample_actions[i]
        rules.append({
            "rule_id": f"R{i+1}",
            "action": action,
            "responsible_role": role,
            "deadline": deadline
        })
    
    return {
        "policy_id": f"POL-TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "rules": rules
    }


def create_ambiguous_rule_payload() -> Dict[str, Any]:
    """
    Create a sample payload with rules that might need clarification.
    
    This is useful for testing the human-in-the-loop clarification flow.
    
    Returns:
        Payload with potentially ambiguous rules
    """
    return {
        "policy_id": "POL-AMBIGUOUS-001",
        "rules": [
            {
                "rule_id": "R1",
                "action": "Review application",
                "responsible_role": "Clerk",
                "deadline": "within reasonable time"  # Ambiguous deadline
            },
            {
                "rule_id": "R2",
                "action": "Approve if eligible",
                "responsible_role": "Officer",
                "deadline": ""  # Empty deadline - will become "Not specified"
            }
        ]
    }


def print_payload_summary(payload: Dict[str, Any]) -> None:
    """
    Print a human-readable summary of a payload.
    
    Useful for debugging and verification.
    
    Args:
        payload: The payload to summarize
    """
    print(f"\n{'='*60}")
    print(f"PAYLOAD SUMMARY")
    print(f"{'='*60}")
    print(f"Policy ID: {payload.get('policy_id', 'N/A')}")
    print(f"Number of Rules: {len(payload.get('rules', []))}")
    print(f"\nRules:")
    print(f"{'-'*60}")
    
    for idx, rule in enumerate(payload.get("rules", []), 1):
        print(f"\nRule #{idx}:")
        print(f"  Rule ID: {rule.get('rule_id', 'N/A')}")
        print(f"  Action: {rule.get('action', 'N/A')}")
        print(f"  Responsible Role: {rule.get('responsible_role', 'N/A')}")
        print(f"  Deadline: {rule.get('deadline', 'Not specified')}")
    
    print(f"\n{'='*60}\n")


# Example usage
if __name__ == "__main__":
    print("NLP Integration Utilities - Test Suite\n")
    
    # Test 1: Create and validate sample payload
    print("Test 1: Creating sample payload...")
    sample = create_sample_payload(num_rules=3)
    print_payload_summary(sample)
    
    is_valid, error = validate_nlp_payload(sample)
    print(f"Validation Result: {'✓ VALID' if is_valid else f'✗ INVALID - {error}'}\n")
    
    # Test 2: Transform payload with extra fields
    print("\nTest 2: Transforming payload with extra fields...")
    nlp_output_with_extras = {
        "policy_id": "POL-002",
        "confidence_score": 0.95,  # Extra field
        "parsed_at": "2024-01-14T09:00:00",  # Extra field
        "rules": [
            {
                "rule_id": "R1",
                "action": "Verify documents",
                "responsible_role": "Clerk",
                "deadline": "7 days",
                "confidence": 0.9,  # Extra field
                "source_line": 42  # Extra field
            }
        ]
    }
    
    clean = transform_to_ingest_format(nlp_output_with_extras)
    print("Original payload had extra fields (confidence_score, parsed_at, etc.)")
    print("Cleaned payload:")
    print_payload_summary(clean)
    
    # Test 3: Validate invalid payload
    print("\nTest 3: Validating invalid payload...")
    invalid_payload = {
        "policy_id": "POL-003",
        "rules": [
            {
                "rule_id": "R1",
                "action": "Do something"
                # Missing responsible_role - should fail validation
            }
        ]
    }
    
    is_valid, error = validate_nlp_payload(invalid_payload)
    print(f"Validation Result: {'✓ VALID' if is_valid else f'✗ INVALID - {error}'}")
    print("(This should fail - missing responsible_role)")
