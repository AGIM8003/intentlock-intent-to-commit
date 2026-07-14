# IntentLock

**Subtitle:** A Deterministic Intent-to-Commit Control and Evidence Architecture
for AI-Assisted Software Development  
**Author:** Agim Haxhijaha  
**Role:** Independent Researcher  
**Edition:** v5.0 Public Research Edition  
**Publication:** Independent Research Publication No. 3  
**Status:** Proposed architecture; reference implementation not built  
**License:** CC BY-NC-ND 4.0

IntentLock is a proposed local-first control and evidence architecture for
binding a signed human-approved software task to the repository state that is
ultimately accepted after an AI coding session.

Its proposed control chain is:

```
SIGNED HUMAN INTENT
-> DETERMINISTIC POLICY
-> VERIFIED CAPABILITY VECTOR
-> NON-AUTHORITATIVE EXECUTION
-> DIFF AND SECURITY GATES
-> INDEPENDENT ACCEPTANCE
-> REVERSAL OBJECT
-> OFFLINE INTENT-TO-COMMIT PROOF
```

The work does not claim that sandboxing, policy evaluation, Git review, or
software attestations are individually new. Its research contribution is the
integrated authority model, the separation of runtime containment from
repository acceptance, and the complete intent-to-commit evidence path.

It does not claim implementation, scientific validation, legal compliance,
patentability, universal security, or production readiness.

## About the Author

Agim Haxhijaha is an independent researcher with over 30 years of experience
in electrotechnical engineering and industrial automation. He has spent 10+
years in independent AI research and is completing an MBA in Artificial
Intelligence at Robert Kennedy College (Switzerland) under the University of
Cumbria (UK). He has founded and operated businesses in industrial
electrotechnics, automation, and full-cycle real estate development for over
20 years (vertogroup.be).

## Start Here

1. Read `INTENTLOCK_v5.0_PUBLIC_RESEARCH_EDITION.pdf`.
2. 2. Review `PRIOR_ART_AND_STANDARDS_REVIEW.md`.
   3. 3. Read `PUBLICATION_READINESS_REPORT.md`.
     
      4. ## Collaboration
     
      5. Researchers, developers, security engineers, software-governance teams,
      6. investors, and implementation partners may contact the author through the
      7. public repository issue tracker or the linked ORCID profile after publication.
     
      8. ## Citation
     
      9. Use `CITATION.cff` or the final citation supplied by the Zenodo record.
