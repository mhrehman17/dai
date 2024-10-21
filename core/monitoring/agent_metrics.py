class AgentMetrics:
    def __init__(self, agent_id: str, cpu_usage: float, memory_usage: float, tasks_completed: int):
        self.agent_id = agent_id
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.tasks_completed = tasks_completed