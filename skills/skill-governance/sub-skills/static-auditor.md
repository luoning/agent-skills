# Sub-skill: Static Auditor (Codebase Integrity)

## Overview
Ensures absolute file-system portability and blocks configuration leaks.

## 1. Rules
- **No Absolute Paths**: Block any local absolute disk-drive prefix (such as local drive letters C or D followed by backslashes) or local relative links that fail.
- **YAML Frontmatter Gate**: Validate name and description naming patterns.
- **Audit Blacklist**: Filter out any keyword listed inside `.skill_audit_blacklist`.
