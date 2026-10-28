# Product Master Data AI Agent for Sales Representatives

AI agent enabling Sales Representatives to query product master data from SAP S/4HANA Public Cloud Edition using natural language via SAP Joule.

## Business Challenge

Sales Representatives waste time navigating complex SAP S/4HANA screens to look up product master data (descriptions and specifications). Direct system access is slow and requires technical knowledge, reducing selling time and delaying customer responses.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time per product data lookup | 5 minutes | Under 30 seconds | Within 4 weeks | Lead to Cash – Sales Order Management | user |

## Key Milestones

1. **Agent scaffolding complete** – Python A2A agent boots and responds to a basic test prompt via SAP Joule.
2. **S/4HANA API connected** – Agent successfully retrieves product master data (descriptions & specifications) from SAP S/4HANA via MCP layer.
3. **Natural language query working** – Agent correctly interprets and answers at least 5 representative product questions from Sales Reps.
4. **Joule integration validated** – Agent is accessible and functional through the SAP Joule interface.
5. **Go-live** – Agent deployed and available to Sales Representatives within the 4-week target.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash (E2E)

### Process Hierarchy

```
Lead to Cash (E2E)
└── Order to Fulfill (generic)
    └── Manage customer orders and contracts (generic) [BPS-361]
        └── Manage customer orders
└── Plan to Optimize Marketing and Sales (generic)
    └── Plan sales and manage performance (generic) [BPS-369]
        └── Develop sales forecast
```

### Summary

Sales Representatives using natural language to access product master data maps to the Lead to Cash E2E — specifically the Order to Fulfill and Plan Sales sub-processes — where fast access to accurate product information is critical to quoting, ordering, and customer responsiveness.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|-------------------|-------------------|-------------------|------|---------------------|
| Retrieve product descriptions & specifications | SAP S/4HANA Cloud Public Edition – Sales Order Management (SC1001) | `sap.s4:apiResource:API_PRODUCT_SRV:v1` | — | — | — | — | No | Product Master (A2X) OData API available; no MCP server — custom MCP translation required |
| Product data including classification | SAP S/4HANA Cloud Public Edition | `sap.s4:apiResource:API_CLFN_PRODUCT_SRV:v1` | — | — | — | — | No | Classification data available via dedicated API |
| Conversational / natural language access to product data | No standard SAP product covers this | — | — | — | — | — | Yes | Requires custom AI agent (Python A2A) integrated with SAP Joule |
| Sales performance & analytics context | SAP S/4HANA Cloud Public Edition – Sales Analytics (SC1103) | — | — | — | — | — | No | Available in S/4HANA; not in scope for initial agent |

### Key Findings

- SAP S/4HANA Cloud Public Edition covers the core sales capabilities required (Sales Order Management, Product Availability, Sales Analytics).
- Product Master Data is available via OData APIs (`API_PRODUCT_SRV:v1`, `API_CLFN_PRODUCT_SRV:v1`, `CE_PRODUCT_0003:v3`) — no pre-built MCP server exists; a custom MCP translation file will be generated.
- The primary gap is not data availability but conversational access — addressed by a custom Python AI agent.
- The agent will be surfaced through SAP Joule as the interaction channel for Sales Representatives.
- Initial scope is limited to product descriptions and specifications; availability, pricing, and substitutes are out of scope for v1.

## Recommendations

### AI Agent for Conversational Product Master Data Access

#### Executive Summary

Python A2A agent on SAP BTP, connected to S/4HANA via MCP, surfaced in Joule.

#### Recommended Solution

Build a Python-based AI agent following the A2A protocol, deployed on SAP BTP. The agent connects to SAP S/4HANA Cloud Public Edition via a generated MCP translation layer over the Product Master OData API (`API_PRODUCT_SRV:v1`). Sales Representatives interact with the agent through SAP Joule using plain-language questions such as "What are the specifications of product X?" or "Show me all products in category Y." The agent retrieves accurate, real-time data and returns concise answers.

#### Problem Statement

Sales Representatives must navigate multiple SAP S/4HANA screens to find basic product data, consuming an average of 5 minutes per lookup. This reduces selling time and slows responses to customer product inquiries.

#### Affected User Roles

- Sales Representatives

#### Important Factors

##### Reduces time-to-information through conversational AI
Sales Reps ask questions in plain English and receive instant answers — no training on SAP navigation required.

##### Leverages existing S/4HANA investment
The agent reads directly from SAP S/4HANA's product master data APIs, ensuring answers are always current and authoritative.

##### Integrates into SAP Joule
No new tool adoption required — the agent is surfaced within Joule, which Sales Reps already use.

#### Potential Risks

##### No pre-built MCP server for Product Master API
A custom MCP translation file must be generated from the OData spec. This is a known, well-supported pattern but adds an implementation step.

##### Scope creep
Sales Reps may request pricing, availability, and substitutes after seeing the agent. These are out of scope for v1 and should be addressed in a follow-on iteration.

#### Recommended solution category

AI Agent

#### Intent fit
95%
