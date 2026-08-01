# ADR-005: Formalization of AI Memory Layer Architecture

- **Status**: Approved
- **Date**: 2026-08-01
- **Deciders**: Principal Software Architect, Lead Architect, Security Lead
- **Technical Story**: Establishing a domain-agnostic, multi-tiered cognitive memory substrate for NeuroFlow AI.

---

## Context and Problem Statement

Stateless Large Language Models (LLMs) and simple chatbot context window buffers cannot support long-horizon multi-step reasoning, cross-session user personalization, agent learning, procedural skill retention, or multi-agent collaboration.

Naive message history passing suffers from:
1. **Context Window Overflow**: Token budgets rapidly fill with raw past turns.
2. **High Token Costs**: Re-sending complete histories on every request increases API costs.
3. **Attention Loss**: Models suffer from "lost-in-the-middle" attention degradation over long context windows.
4. **Zero Cross-Session Learning**: Stateless runs lose user preferences and procedural strategies when a session ends.

The platform requires a dedicated, domain-agnostic **AI Memory Layer**.

---

## Decision Drivers

1. **Multi-Tier Cognitive Taxonomy**: Clear separation between Working Memory, Episodic Memory, Semantic Memory, Procedural Memory, and Long-Term Memory.
2. **Reflection & Noise Reduction**: Experiences must be summarized and abstracted into higher-order facts rather than naively persisting raw event logs.
3. **Asynchronous Processing**: Reflection, decay recalculation, and archival must execute out-of-band to prevent blocking ASGI API threads.
4. **Clean Architecture Adherence**: Abstract ports in `core/ports/memory.py` (Layer 0), technical storage drivers in `infrastructure/memory/` (Layer 1), capability engines in Platform Runtime (Layer 3).
5. **Security & Multi-Tenancy**: Granular Attribute-Based Access Control (ABAC), tenant collection isolation, PII scrubbing, and immutable audit versioning.

---

## Considered Options

1. **Option 1: Rely solely on Chatbot Context Buffers & Redis Session Caches**  
   *Rejected*. Fails to provide cross-session persistence, skill learning, or reflection.
2. **Option 2: Use RAG Vector Search directly as the Memory Engine**  
   *Rejected*. Confuses static reference documentation (RAG) with dynamic, agentic experiential learning (Memory).
3. **Option 3: Establish a 5-Tier Memory Architecture with Reflection Engine and Asynchronous Consolidation in Platform Runtime**  
   *Selected*. Delivers comprehensive cognitive capabilities, decay math, relationship linking, and multi-tenant security while maintaining clean layer boundaries.

---

## Decision Outcome

**Selected Option 3**: Formalize the **AI Memory Layer Architecture** within **Platform Runtime** (Layer 3).

### Key Architectural Choices

1. **5-Tier Cognitive Memory Structure**:
   - Working Memory (scratchpad RAM)
   - Episodic Memory (event/experience logs)
   - Semantic Memory (distilled facts & preferences)
   - Procedural Memory (reusable workflow routines)
   - Long-Term Memory (unified persistent store)
2. **Reflection & Consolidation Engine**: Asynchronous background workers summarize episodic runs into semantic facts and procedural strategies using Ebbinghaus decay math.
3. **Confidence Scoring & Provenance**: Multi-factor scoring ($0.0 - 1.0$) influencing retrieval ranking, paired with immutable source origin tracking (`source_type`, `causation_event_id`).
4. **Memory Relationships**: Explicit graph-ready links (`related_to`, `derived_from`, `supports`, `contradicts`, `depends_on`, `supersedes`).
5. **Clean Architecture Placement**:
   - `core/ports/memory.py` (Layer 0)
   - `infrastructure/memory/` (Layer 1)
   - `backend/ai/memory/` or `backend/memory/` (Layer 3)

---

## Consequences

### Positive Consequences
- **Cognitive Agent Learning**: Agents retain procedural strategies and user preferences across execution sessions.
- **Token & Cost Efficiency**: Multi-stage retrieval supplies concise, relevant memory context rather than bloated chat logs.
- **Graph-RAG Alignment**: Directional memory relationships prepare the platform for future Knowledge Graph integration.
- **Enterprise Security & Compliance**: ABAC permissions, PII redaction, tenant collection isolation, and immutable version history.

### Negative Consequences / Trade-offs
- **Background Worker Load**: Asynchronous reflection and decay jobs require scheduled background execution infrastructure.
- **Re-Scoring Hyperparameter Tuning**: Weight parameters ($w_1, w_2, w_3, w_4$) in the retrieval scoring equation require empirical tuning for optimal recall.

---

## Compliance & Enforcement

- **Documentation**: Comprehensive technical specification maintained in [`docs/architecture/memory-layer.md`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/memory-layer.md).
- **Automated Verification**: AST import linter rules in `tests/architecture/` verify layer dependencies.

---

## References

- [AI Memory Architecture Specification](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/memory-layer.md)
- [Platform Runtime Architecture Specification](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/platform-runtime.md)
- [ADR-003: Platform Runtime Layer](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/adr/ADR-003-platform-runtime.md)
- [ADR-004: Internal Event Bus Architecture](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/adr/ADR-004-event-bus.md)
