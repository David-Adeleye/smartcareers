# SmartCareers — MVP API Contract

**Version:** v1.0  
**Status:** Active (MVP)  
**Related PRD:** docs/00_prd.md  

---

## 1. Purpose

This document defines the core API contract for the SmartCareers MVP (Job Seeker Intelligence Platform).

It specifies:
- the interaction between frontend and backend
- the asynchronous analysis workflow
- all request and response schemas
- explicit error and failure handling

This contract is authoritative for MVP implementation.

---

## 2. Design Principles

- Async-first to accommodate LLM latency
- Deterministic schemas (no free-form AI output)
- Strict explainability and grounding
- No long-running HTTP requests
- Backend owns all business logic

**Interaction pattern:**  
Submit → Process (async) → Poll → Retrieve Result

---

## 3. High-Level Flow

Client submits analysis request  
→ Backend accepts request and returns task_id  
→ Client polls task status  
→ Client retrieves completed explainable result

---

## 4. Authentication

- All endpoints require authentication
- Authentication mechanism: JWT (Bearer token)
- user_id is inferred from the token and attached to all tasks

---

## 5. Endpoint: POST /analyze

### Description

Submits a CV and job description for explainable career matching analysis.  
This endpoint does not perform analysis synchronously.

### Request Body

```json
{
  "cv_text": "string",
  "job_description": "string",
  "job_title": "string",
  "company": "string (optional)"
}
```

### Validation Rules

- cv_text must be at least 300 characters
- job_description must be at least 200 characters
- job_description must not exceed the configured maximum length
- job_title must be non-empty

Invalid requests return HTTP 400.

### Response

```json
{
  "task_id": "uuid",
  "status": "accepted"
}
```

**HTTP Status:** 202 Accepted

---

## 6. Endpoint: GET /tasks/{task_id}

### Description

Returns the current status of an analysis task.

### Response

```json
{
  "task_id": "uuid",
  "status": "pending | running | completed | failed",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp"
}
```

### Failure Response

```json
{
  "task_id": "uuid",
  "status": "failed",
  "error_code": "UNREADABLE_CV | JD_TOO_LONG | MODEL_ERROR | TIMEOUT",
  "message": "Human-readable explanation"
}
```

---

## 7. Endpoint: GET /results/{task_id}

### Description

Returns the completed explainable analysis for a task.

- Available only when task status is completed
- If task is not completed, return HTTP 404 or 409

### Response Schema: ExplainableMatchScore

```json
{
  "overall_score": 78,
  "breakdown": {
    "skills_match_score": 82,
    "experience_match_score": 70,
    "seniority_match_score": 65,
    "keyword_alignment_score": 88
  },
  "requirements_analysis": [
    {
      "requirement": "Python backend development",
      "status": "matched",
      "evidence": {
        "cv_quote": "Built REST APIs using FastAPI and Django",
        "explanation": "Direct evidence of backend development experience"
      }
    },
    {
      "requirement": "5+ years leadership experience",
      "status": "missing",
      "evidence": {
        "cv_quote": null,
        "explanation": "No leadership duration stated in CV"
      }
    }
  ],
  "strengths": [
    "Strong backend engineering background",
    "Experience building production APIs"
  ],
  "gaps": [
    "Leadership scope not clearly defined",
    "Cloud ownership not explicitly stated"
  ],
  "recommendations": [
    "Clarify leadership responsibilities and duration",
    "Highlight any cloud infrastructure exposure"
  ],
  "prompt_version": "v1.0"
}
```

---

## 8. Explainability Requirements

The system must:

- Map each job requirement to explicit CV evidence
- Use direct CV quotes or mark requirements as missing
- Never invent experience or qualifications
- Treat AI as an auditor, not a creative writer

Explainability is a core product requirement.

---

## 9. Background Worker Responsibilities

All analysis is executed in a background worker (e.g., Celery or arq).

Worker steps:

1. CV sanity checks  
2. Structured CV extraction (facts only)  
3. Job description requirement extraction  
4. Evidence audit (CV → JD)  
5. Score computation  
6. Controlled text generation  
7. Result persistence  
8. Task status update  

No worker means the MVP is incomplete.

---

## 10. Persistence

Each analysis task stores:

- user_id
- raw CV text
- structured CV JSON
- job description text
- explainable result JSON
- prompt version
- timestamps

No data is ephemeral.

---

## 11. Failure Modes

| Scenario                 | Behaviour                     |
|--------------------------|-------------------------------|
| CV unreadable            | Task fails with UNREADABLE_CV |
| Job description too long | Request rejected (400)        |
| LLM timeout              | Retry then fail               |
| Grounding violation      | Fail immediately              |
| Worker crash             | Task marked failed            |

Trust and correctness take precedence over completion.

---

## 12. Out of Scope (MVP)

This API explicitly excludes:

- job listings
- job applications
- recruiter endpoints
- third-party job APIs
- auto-apply workflows

These belong to Phase 2 and beyond.

---

## 13. Definition of Done

The API is complete when:

- async analysis functions end-to-end
- explainable results strictly follow schema
- failures are explicit and deterministic
- frontend integration requires no inference or guesswork

---

End of document.
