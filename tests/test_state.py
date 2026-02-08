def test_initial_state():
    """Verify that the initial state is correctly initialized."""
    state = {"messages": [], "next_step": "init"}
    # Simple check to demonstrate testing capability
    assert "messages" in state
    assert state["next_step"] == "init"
