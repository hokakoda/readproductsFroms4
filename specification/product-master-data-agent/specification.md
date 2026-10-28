# Specification: product-master-data-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md`, `intent.md`)
- [x] Bootstrap agent code in `assets/product-master-data-agent/` using instructions from the sap-agent-bootstrap section.
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

- [x] Create a runtime skill for product data lookup guidance in `assets/product-master-data-agent/app/skills/product-lookup/SKILL.md`

---

## Project-Specific Tasks

### Natural Language Product Query (R1)

- [x] Configure the agent system prompt in `assets/product-master-data-agent/app/agent.py`
- [x] Verify the agent correctly interprets natural-language queries

### Search by Name, ID, or Category (R2)

- [x] Ensure the agent uses the MCP tool to support lookup by product ID, name, and category
- [x] Instruct the agent to return a list when multiple results are returned
- [x] Instruct the agent to present the closest match and ask the user to confirm

### SAP Joule Integration (R3)

- [x] Ensure the agent `/.well-known/agent.json` card is correctly populated
- [x] Validate the agent card is accessible and well-formed

### Graceful No-Answer Handling (R4)

- [x] Implement logic for empty result set handling
- [x] Ensure the agent never fabricates product data
- [x] Handle MCP tool errors gracefully

### Real-Time Data from SAP S/4HANA (R5)

- [x] Confirm no local caching of product records
- [x] Verify the agent's MCP tool call returns data from `API_PRODUCT_SRV:v1` in real time

---

## Data Dependencies

MCP API: `sap.s4:apiResource:API_PRODUCT_SRV:v1`
MCP tool scope: read-only
Resources in scope: `A_Product, A_ProductDescription, A_ProductBasicText, A_ProductSalesDelivery`

API spec file: `specification/product-master-data-agent/api-specs/API_PRODUCT_SRV_v1.edmx`

---

## Business Instrumentation

- [x] Implement structured logging and OpenTelemetry spans for all 5 milestones from the PRD (M1–M4 in agent.py, M5 at go-live)
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

- [x] Invoke `mcp-translation-file` skill — translation.json generated at `specification/product-master-data-agent/mcps/API_PRODUCT_SRV_v1/`
- [x] Invoke `setup-solution` skill — `solution.yaml`, agent `asset.yaml`, and MCP server `asset.yaml` created
- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from `mcp_tools` module
- [x] Add MCP server dependency to `asset.yaml` under `requires`
- [x] Generate `mcp-mock.json` using `mcp-mock-config` skill

---

## Testing

- [x] `conftest.py` sets `IBD_TESTING=true`
- [x] Write 5 unit tests + 1 integration test in `assets/product-master-data-agent/tests/`
- [x] Run `pytest` — 108 passed, 75% coverage (above 70% threshold)
- [x] Run `pytest` again to generate `test_report.json`
- [x] Verify `test_report.json` exists in `assets/product-master-data-agent/`
