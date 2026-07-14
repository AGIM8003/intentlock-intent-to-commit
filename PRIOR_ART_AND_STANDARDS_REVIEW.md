# IntentLock Prior-Art and Standards Review

**Review date:** July 13, 2026  
**Scope:** Public product documentation, official standards, primary research
papers, and public intellectual-property guidance available during the review.

## Executive Finding

IntentLock remains a credible publication candidate as a proposed integrated
architecture. The review does not support claiming that its individual
mechanisms are new.

Strong existing overlap includes:

- platform-native coding-agent sandboxing and approvals;
- isolated workspaces and branches;
- hooks, network firewalls, human merge review, signed commits, and audit logs;
- deterministic policy engines;
- tool-call policy enforcement derived from user intent;
- provenance, attestations, verification bundles, and SBOM metadata.

The defensible public research boundary is narrower:

1. a signed, versioned human Intent Contract as the root authority;
2. deterministic contract-to-policy compilation with clause-level source maps;
3. separate measurement of authority, runtime, acceptance, and evidence;
4. an independent repository-acceptance boundary that the agent cannot control;
5. one offline proof capsule binding intent, policy, achieved controls,
   operations, approvals, candidate diff, accepted commit, and reversal.

## Current Comparators

### OpenAI Codex

Official documentation describes OS-enforced sandboxing, approvals, network-off
defaults, isolated cloud environments, workspaces, platform-native macOS
controls, Linux isolation, and native Windows security profiles. IntentLock
therefore must not claim operating-system sandboxing as its invention.

- https://learn.chatgpt.com/docs/agent-approvals-security
- https://learn.chatgpt.com/docs/sandboxing
- https://learn.chatgpt.com/docs/windows/windows-sandbox

### Anthropic Claude Code

Official documentation describes permission controls, sandboxed commands,
working-directory boundaries, MCP safeguards, isolated cloud sessions, network
controls, and audit-related features. IntentLock's public distinction cannot be
generic permission gating.

- https://code.claude.com/docs/en/security

### GitHub Copilot Cloud Agent

GitHub documents isolated development environments, a single writable branch,
required human merge, signed commits, session and audit logs, security scans,
hooks, and a configurable firewall. This is strong overlap with the original
IntentLock control-plane narrative.

- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/use-hooks
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-firewall

### Policy and Agent-Safety Research

AgentSpec proposes runtime safety rules for agents. ClawGuard derives a
user-confirmed rule set and enforces it at tool-call boundaries. A June 2026
paper proposes converting natural-language policies and agent instructions into
Cedar policy. These works materially narrow any novelty claim about compiling
human intent into enforceable agent rules.

- https://arxiv.org/abs/2503.18666
- https://arxiv.org/abs/2604.11790
- https://arxiv.org/abs/2606.26649

### Policy Engines and Provenance Standards

OPA/Rego and Cedar provide maintained deterministic policy foundations. SLSA,
in-toto, Sigstore, SPDX, and RFC 8785 provide relevant provenance,
attestation, bundle, metadata, and canonicalization foundations.

- https://www.openpolicyagent.org/docs/policy-language
- https://docs.cedarpolicy.com/
- https://slsa.dev/spec/v1.2/provenance
- https://in-toto.io/
- https://docs.sigstore.dev/about/bundle/
- https://spdx.dev/use/specifications/
- https://www.rfc-editor.org/rfc/rfc8785.html

## Platform Corrections Made

- Replaced a single security ladder with a multi-dimensional capability vector.
- Separated runtime prevention from repository-acceptance control.
- Reclassified Git-based verification as acceptance gating, not OS prevention.
- Replaced hardcoded platform promises with tested platform adapters.
- Removed dependence on deprecated command-line sandbox interfaces.
- Removed the private `50.X`, ProjectMind, and unpublished verifier claims.
- Removed the unverified machine-executed receipt and duplicate test number.

## Standards Added

- Linux Landlock documentation
- Microsoft AppContainer and Job Objects documentation
- Apple App Sandbox documentation
- Model Context Protocol security guidance
- NIST Secure Software Development Framework
- NIST AI Risk Management Framework
- NIST FIPS 204
- OWASP Prompt Injection guidance
- SLSA, in-toto, Sigstore, SPDX, RFC 8785
- GDPR and the EU Artificial Intelligence Act

## Novelty and Patent Boundary

This was not an exhaustive patent search. Patentability cannot be concluded
from product documentation or keyword searching. WIPO identifies novelty,
inventive step, industrial applicability, patentable subject matter, and
sufficient disclosure as separate requirements.

WIPO also warns that public disclosure before filing can become prior art and
may severely limit later patent protection in many jurisdictions:

https://www.wipo.int/en/web/patents/faq_patents

## Assessment

- **Technical concept strength:** 9/10
- **Engineering depth:** 9/10
- **Potential integrated differentiation:** 7/10
- **Public research publication readiness after this revision:** 9/10
- **Patentability:** unknown; professional search required
- **Implementation readiness:** not demonstrated

## Final Research Verdict

Publish only as a proposed integrated intent-to-commit architecture. Do not
publish claims that IntentLock invented sandboxing, permission gates, policy
engines, Git review, provenance, or attestations. The strongest research claim
is the complete signed authority-to-accepted-commit evidence chain and its
independent acceptance boundary.
