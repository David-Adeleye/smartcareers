# SmartCareers – MVP Product Requirements Document (PRD)

**Product:** SmartCareers  
**MVP Name:** Job Seeker Intelligence Platform  
**Status:** MVP – Scope Locked  
**Owner:** David  
**Version:** v0.1  

---

## 1. Problem Statement

Many qualified job seekers repeatedly apply for roles without receiving interviews.  
The root problem is not always lack of skill, but poor alignment between CVs and job descriptions, unclear seniority signals, missing keywords, or misrepresentation of experience.

Current tools focus on:
- generic CV templates
- text generation without explanation
- automation without insight

They fail to answer the most important question:

> **“Why am I not a good fit for this role, and what exactly should I change?”**

---

## 2. Product Vision

SmartCareers is an **AI-powered, explainable career intelligence platform** that helps job seekers understand and improve their fit for specific roles.

The MVP prioritises **insight, explainability, and controlled AI output**, not job aggregation or application automation.

---

## 3. Target User (MVP)

### Primary User
Individual job seekers, including:
- graduates
- career switchers
- experienced professionals
- international candidates navigating competitive job markets

### Explicitly Out of Scope (MVP)
- recruiters
- employers
- hiring managers
- staffing agencies

---

## 4. Value Proposition (MVP)

For a given CV and job description, SmartCareers will:
- compute a **match score (0–100)**
- explain **why** the score is what it is
- highlight **missing or weak areas**
- generate **tailored improvements** (CV bullets and cover letter)
- ensure outputs are **grounded strictly in the user’s real experience**

---

## 5. MVP Scope (What’s In)

### Core Capabilities

#### User Authentication
- email + password
- secure login

#### CV Ingestion
- upload PDF or DOCX
- extract raw text

#### Job Description Input
- paste job description text

#### Career Matching Intelligence
- skills overlap
- keyword alignment
- seniority match
- role responsibility coverage

#### Explainable Match Score
- numeric score (0–100)
- breakdown by category

#### AI-Assisted Outputs
- tailored cover letter
- suggested CV bullet rewrites

#### History
- saved analyses
- revisit past results

#### Download
- export outputs (DOCX initially)

---

## 6. Explicit Non-Goals (MVP)

The MVP will **not** include:
- job postings
- recruiter accounts
- job applications
- auto-apply
- job scraping
- LinkedIn, Indeed, or ATS APIs
- mobile apps
- AI agents performing autonomous workflows
- subscription payments (can be added post-MVP)

These are deferred intentionally to ensure fast, focused delivery.

---

## 7. User Journey (MVP)

1. User lands on SmartCareers
2. Signs up or logs in
3. Uploads CV
4. Pastes job description
5. Clicks **“Analyze Match”**
6. System returns:
   - match score
   - explanation panel
   - gaps and suggestions
   - tailored outputs
7. User saves or downloads results
8. User returns to history for future applications

---

## 8. Explainability Requirement (Critical)

SmartCareers must:
- map **CV evidence → job requirements**
- clearly indicate **what matched**, **what didn’t**, and **why**
- avoid hallucinating experience
- restrict AI outputs to **verified CV facts only**

Explainability is a **core differentiator**, not a nice-to-have.

---

## 9. AI Design Principles (MVP)

- deterministic pipeline (not autonomous agents)
- prompt versioning
- reproducible outputs
- auditable inputs and outputs
- cost-aware execution

### High-Level Pipeline
1. Extract structured facts from CV
2. Extract requirements from job description
3. Compute alignment signals
4. Generate explainable insights
5. Generate tailored outputs

---

## 10. Success Metrics (MVP)

### Activation
- percentage of users completing:
  - signup → CV upload → first analysis

### Engagement
- average analyses per user
- percentage of returning users within 7 days

### Quality
- user feedback on insight usefulness
- reduction in repeated CV mistakes (observed via history)

### Technical
- average analysis latency
- AI cost per analysis

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|-----|-----------|
| Hallucinated experience | Strict grounding to CV facts |
| High LLM cost | Caching and prompt optimisation |
| Slow response | Async execution and background tasks |
| Scope creep | PRD acts as scope contract |

---

## 12. Phase 2+ (Explicitly Future)

Not part of the MVP, but enabled by MVP foundations:
- job ingestion from job boards
- recruiter-facing insights
- filtering jobs by match score (e.g. ≥80%)
- subscription tiers
- application automation
- mobile apps

These features **must not block MVP shipping**.

---

## 13. Definition of Done (MVP)

The MVP is complete when:
- a user can upload a CV
- analyze fit against a job description
- receive an explainable match score
- get tailored outputs
- save and download results
- the system is deployed and usable on **smartcareers.uk**

---

## 14. Strategic Importance

This MVP:
- demonstrates technical innovation through explainable AI
- provides a credible foundation for scale
- supports Innovator Founder and Global Talent visa narratives
- validates real user demand before expansion
