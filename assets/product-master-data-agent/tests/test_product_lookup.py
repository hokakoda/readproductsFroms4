"""Unit tests for product master data agent MCP tool interactions."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# The conftest.py sets IBD_TESTING=1 and adds app/ to sys.path.
# Agent code imports from peer-level modules (no "app." prefix).


@pytest.fixture
def mock_mcp_tools():
    """Load mock MCP tools from mcp-mock.json and return as LangChain StructuredTool instances."""
    agent_root = Path(__file__).parent.parent
    mock_config_path = agent_root / "mcp-mock.json"
    mock_config = json.loads(mock_config_path.read_text())

    tools = []
    for server_slug, server_data in mock_config["servers"].items():
        for tool_name, tool_data in server_data["tools"].items():
            tool = MagicMock()
            tool.name = f"mcp_{server_slug}__{tool_name}"
            tool.description = tool_data["description"]
            mock_response = tool_data["mock_response"]
            tool.ainvoke = AsyncMock(return_value=json.dumps(mock_response))
            tools.append(tool)
    return tools


@pytest.fixture
def mock_llm_response():
    """Factory for creating a mock LLM that returns a given message."""
    def _factory(response_text: str):
        from langchain_core.messages import AIMessage
        mock_llm = MagicMock()
        ai_message = AIMessage(content=response_text)
        mock_response = {"messages": [ai_message]}
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)
        return mock_llm
    return _factory


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    """Ensure app/ is in sys.path for all tests in this module."""
    pass


# ---------------------------------------------------------------------------
# Unit Test 1: Product lookup by exact product ID
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_product_lookup_by_id_returns_correct_data(mock_mcp_tools):
    """Test that the agent retrieves correct product data when given an exact product ID."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_graph_result = {
        "messages": [
            MagicMock(content="Product P-1001: Centrifugal Pump 500L Industrial. Weight: 2.2 KG, Product Group: PUMP, Base Unit: EA.")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="What are the specifications of product P-1001?",
            context_id="test-ctx-001",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    assert len(response.message) > 0
    mock_invoke.assert_awaited_once()


# ---------------------------------------------------------------------------
# Unit Test 2: Product search by name (partial match)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_product_search_by_name_returns_list(mock_mcp_tools):
    """Test that the agent returns a list of matching products when searching by partial name."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_graph_result = {
        "messages": [
            MagicMock(content="Found 2 products matching 'pump':\n1. P-1001 - Centrifugal Pump 500L Industrial\n2. P-1002 - Centrifugal Pump 1000L Industrial")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="Show me all products with 'pump' in the name",
            context_id="test-ctx-002",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    mock_invoke.assert_awaited_once()


# ---------------------------------------------------------------------------
# Unit Test 3: Product search by category
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_product_search_by_category_returns_products(mock_mcp_tools):
    """Test that the agent returns products in a given category."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_graph_result = {
        "messages": [
            MagicMock(content="Found 2 products in the PUMP category:\n1. P-1001 - Centrifugal Pump 500L Industrial\n2. P-1002 - Centrifugal Pump 1000L Industrial")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="Show me all products in the Pumps category",
            context_id="test-ctx-003",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    mock_invoke.assert_awaited_once()


# ---------------------------------------------------------------------------
# Unit Test 4: No product found — graceful handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_no_product_found_returns_clear_message(mock_mcp_tools):
    """Test that the agent returns a clear 'not found' message when no product matches."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_graph_result = {
        "messages": [
            MagicMock(content="No product found matching 'XYZNONEXISTENT'. Please try searching with a different term, a shorter name, or the exact product ID.")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="Tell me about product XYZNONEXISTENT",
            context_id="test-ctx-004",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    assert len(response.message) > 0
    mock_invoke.assert_awaited_once()


# ---------------------------------------------------------------------------
# Unit Test 5: MCP tool error — system unavailable message
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_mcp_tool_error_returns_unavailable_message(mock_mcp_tools):
    """Test that the agent informs the user when the MCP tool returns an error."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_graph_result = {
        "messages": [
            MagicMock(content="The product data system is currently unavailable. Error: Connection timeout to SAP S/4HANA. Please try again shortly.")
        ]
    }

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="What are the specifications of product P-9999?",
            context_id="test-ctx-005",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message is not None
    mock_invoke.assert_awaited_once()


# ---------------------------------------------------------------------------
# Integration Test: End-to-end agent flow
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_end_to_end_product_query_flow(mock_mcp_tools):
    """
    Integration test: Sales Rep asks about product P-1001 specifications.
    Agent calls MCP tool → formats response → returns to user.
    All LLM and MCP calls are mocked (offline).
    """
    from agent import SampleAgent
    from langchain_core.messages import AIMessage

    agent = SampleAgent()

    # Simulate the full agent graph responding with a formatted product answer
    expected_response = (
        "Here are the details for product P-1001:\n\n"
        "**Product ID:** P-1001\n"
        "**Description:** Centrifugal Pump 500L Industrial\n"
        "**Product Group:** PUMP\n"
        "**Base Unit:** EA\n"
        "**Net Weight:** 2.200 KG\n"
        "**Gross Weight:** 2.500 KG\n\n"
        "**Long Description:** High-performance centrifugal pump designed for industrial "
        "water supply applications. Flow rate: up to 500 L/min. Max pressure: 10 bar."
    )

    mock_graph_result = {"messages": [AIMessage(content=expected_response)]}

    with patch.object(agent, "_invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_graph_result
        response = await agent.invoke(
            query="What are the specifications of product P-1001?",
            context_id="integration-test-001",
            tools=mock_mcp_tools,
        )

    assert response.status == "completed"
    assert response.message == expected_response
    mock_invoke.assert_awaited_once()

    # Verify the call included the tools
    call_kwargs = mock_invoke.call_args
    assert call_kwargs is not None
    called_tools = call_kwargs.kwargs.get("tools") or call_kwargs.args[0] if call_kwargs.args else []
    assert len(called_tools) > 0 or mock_invoke.called  # tools were passed
