from qshield.cbom.schema import Finding
from qshield.migration.recommendations import get_code_replacement_diff

def generate_developer_ticket(finding: Finding) -> str:
    """
    Generates an actionable Markdown developer ticket suitable for Jira or GitHub Issues.
    """
    diff = get_code_replacement_diff(finding)
    
    return f"""### [{finding.id}] Remediate Quantum-Vulnerable {finding.algorithm}
**Component:** `{finding.file_path}` (Line {finding.line_number})
**Severity:** `{finding.severity.value}` | **Quantum Risk:** `{finding.quantum_risk.value}`
**Target Phase:** Phase {finding.phase}

#### Problem Description
{finding.description}

#### Current Code
```
{finding.code_snippet}
```

#### Recommended Replacement
**Target Standard:** {finding.recommended_replacement}

#### Suggested Code Diff
```diff
{diff}
```

#### Acceptance Criteria
- [ ] Replace classical algorithm with NIST FIPS 203 (ML-KEM) or FIPS 204 (ML-DSA).
- [ ] Verify unit tests and integration tests pass with zero regression.
- [ ] Run Q-SHIELD CBOM re-scan to confirm `{finding.id}` is remediated.
"""
