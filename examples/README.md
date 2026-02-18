# Domain-Specific Examples

This directory contains domain-specific implementations and examples. These are **optional** and serve only to demonstrate how the Decision Ecosystem can be applied to specific domains.

## Important Note

**These examples are for illustration only.** The core Decision Ecosystem is domain-agnostic. Domain-specific logic should be implemented in adapters, not in core repositories.

## Example Domains

### [Domain Name]
- **Description**: Brief description of the domain
- **Location**: `[domain-name]/`
- **Purpose**: Example only, not part of core ecosystem

## Structure

Each example domain should follow this structure:

```
[domain-name]/
├── README.md              # Domain-specific documentation
├── adapter.py             # Domain adapter implementation
├── examples/              # Domain-specific code examples
└── tests/                 # Domain-specific tests
```

## Adding a New Example

1. Create directory: `docs/examples/[domain-name]/`
2. Add README explaining the domain
3. Implement adapter mapping domain concepts to contract types
4. Provide code examples
5. Add tests
6. Update this README with link to new example

## Guidelines

- Keep examples isolated from core code
- Document domain-specific terminology
- Show how domain concepts map to universal contract types
- Provide clear separation between adapter and core logic
- Examples should not modify core contract

## Disclaimer

Examples in this directory are provided as-is for educational purposes. They demonstrate domain-specific applications but do not represent core functionality of the Decision Ecosystem.
