# SmartCareers — MVP System Architecture

**Version:** v1.0  
**Status:** Active (MVP)  
**Related PRD:** docs/00_prd.md  
**Related API Contract:** docs/03_api_contract.md  

---

## 1. Overview

This document describes the system architecture for the SmartCareers MVP (Job Seeker Intelligence Platform).

The architecture is designed to:
- support long-running AI analysis safely
- enforce explainability and grounding
- scale incrementally without premature complexity
- keep responsibilities clearly separated

The MVP follows an **API-first, async-by-default** design.

---

## 2. High-Level Architecture

The system consists of five primary components:

1. Frontend (Next.js)
2. Backend API (FastAPI)
3. Background Worker (Celery or arq)
4. Database (PostgreSQL)
5. File Storage (Object Storage)

Each component has a single, well-defined responsibility.

---

## 3. Component Responsibilities

### 3.1 Frontend (Next.js)

**Responsibilities**
- User authentication flow
- CV upload and text confirmation UI
- Job description input
- Triggering analysis requests
- Polling task status
- Rendering explainable results
- Displaying history

**Key Characteristics**
- No business logic
- No AI logic
- No scoring logic
- Stateless beyond UI state

The frontend treats the backend API as the single source of truth.

---

### 3.2 Backend API (FastAPI)

**Responsibilities**
- Authentication and authorization (JWT)
- Input validation
- Task creation and lifecycle management
- Orchestration (not execution) of AI analysis
- Exposing task and result endpoints
- Enforcing API contracts

**Key Characteristics**
- Fast request/response times
- Never performs long-running analysis
- Persists all state changes
- Owns validation and failure handling

The API is the **control plane** of the system.

---

### 3.3 Background Worker (Celery / arq)

**Responsibilities**
- Perform all heavy AI computation
- Execute the explainable matching pipeline
- Interact with AI models
- Enforce grounding and evidence rules
- Compute scores
- Generate controlled text outputs
- Persist final results
- Update task status

**Key Characteristics**
- Fully asynchronous
- Retry-aware
- Isolated from request lifecycle
- Scalable independently from API

No worker means no MVP.

---

### 3.4 Database (PostgreSQL)

**Responsibilities**
- Persist users
- Persist tasks and statuses
- Persist raw and structured CV data
- Persist job descriptions
- Persist explainable results
- Support history and auditability

**Key Characteristics**
- Source of truth
- No ephemeral task state
- Structured JSON fields where appropriate

---

### 3.5 File Storage (Object Storage)

**Responsibilities**
- Store uploaded CV files (PDF/DOCX)
- Decouple file storage from database
- Support secure access patterns

**Key Characteristics**
- S3-compatible storage
- Files referenced by URL in database
- Files never stored directly in DB

---

## 4. End-to-End Request Flow

### 4.1 Analysis Submission Flow

1. User uploads CV and confirms extracted text
2. User pastes job description
3. Frontend sends `POST /analyze`
4. Backend:
   - validates input
   - creates task record (status = pending)
   - enqueues background job
   - returns `202 Accepted` + task_id

---

### 4.2 Background Processing Flow

1. Worker receives task_id
2. Worker sets task status = running
3. Worker executes pipeline:
   - CV sanity checks
   - structured CV extraction
   - JD requirement extraction
   - evidence audit (CV → JD)
   - score computation
   - controlled generation
4. Worker persists explainable result
5. Worker sets task status = completed
6. On failure, worker sets status = failed with error metadata

---

### 4.3 Result Retrieval Flow

1. Frontend polls `GET /tasks/{task_id}`
2. When status = completed:
   - frontend calls `GET /results/{task_id}`
3. Backend returns explainable result JSON
4. Frontend renders results without transformation

---

## 5. Explainability and Grounding Architecture

Explainability is enforced structurally, not cosmetically.

**Key mechanisms**
- Structured CV facts stored separately from raw text
- JD requirements extracted explicitly
- Evidence mapping required for every requirement
- CV quotes stored alongside reasoning
- Missing evidence explicitly marked

The AI is treated as an **auditor**, not an author.

---

## 6. Async Design Rationale

AI analysis can take 10–30 seconds.

The system avoids:
- HTTP request blocking
- browser timeouts
- partial responses

The async design ensures:
- API responsiveness
- predictable failure handling
- horizontal scalability

---

## 7. Failure Handling Strategy

Failures are explicit and persisted.

**Examples**
- Unreadable CV → task failed
- Job description too long → request rejected
- Model timeout → retry, then fail
- Grounding violation → fail immediately

No silent degradation.

---

## 8. Security Boundaries

- Frontend never accesses database directly
- Workers never expose public endpoints
- API enforces all authorization
- User data always scoped by user_id
- Files accessed via signed URLs if required

---

## 9. Scalability Path (Post-MVP)

This architecture supports:
- multiple workers
- model swapping
- queue-based load control
- eventual microservice separation

None of these are required for MVP.

---

## 10. Out of Scope (MVP)

- Real-time WebSockets (polling is sufficient)
- Recruiter-facing services
- Job ingestion pipelines
- Auto-apply systems
- Mobile applications

---

## 11. Definition of Done

System architecture is complete when:
- all components have a single responsibility
- async execution is enforced
- explainability is structurally guaranteed
- failure paths are explicit
- architecture aligns with API contract and PRD

---

End of document.
