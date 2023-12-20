def __getattr__(name):
    if name == "ToolAgent":
        from promptulate.agents.tool_agent.agent import ToolAgent

        return ToolAgent
    elif name == "WebAgent":
        from promptulate.agents.web_agent.agent import WebAgent

        return WebAgent
    elif name == "BaseAgent":
        from promptulate.agents.base import BaseAgent

        return BaseAgent


__all__ = ["ToolAgent", "BaseAgent", "WebAgent"]
