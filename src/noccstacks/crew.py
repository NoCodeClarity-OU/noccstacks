from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from noccstacks.tools.custom_tool import (
    ProjectSetupTool, FrontendTool, BackendTool,
    SmartContractTool, TestingTool, IntegrationTool
)

@CrewBase
class NoccstacksCrew():
    """NoccStacks crew for building full-stack dapps"""
    
    def __init__(self):
        self._inputs = {}

    def set_inputs(self, inputs):
        """Set the inputs for the crew"""
        self._inputs = inputs
        # Update the config with inputs
        if hasattr(self, 'agents_config'):
            for agent_name in self.agents_config:
                self.agents_config[agent_name] = {
                    k: v.format(**self._inputs) if isinstance(v, str) else v 
                    for k, v in self.agents_config[agent_name].items()
                }
        if hasattr(self, 'tasks_config'):
            for task_name in self.tasks_config:
                self.tasks_config[task_name] = {
                    k: v.format(**self._inputs) if isinstance(v, str) else v
                    for k, v in self.tasks_config[task_name].items()
                }

    @before_kickoff
    def before_kickoff_function(self, inputs):
        """Process inputs before crew kickoff"""
        # Store inputs internally
        self._inputs = inputs
        print(f"Starting project: {self._inputs.get('project_name', '')}")
        
        # Format all configs with inputs
        if hasattr(self, 'agents_config'):
            for agent_name in self.agents_config:
                self.agents_config[agent_name] = {
                    k: v.format(**self._inputs) if isinstance(v, str) else v
                    for k, v in self.agents_config[agent_name].items()
                }
        if hasattr(self, 'tasks_config'):
            for task_name in self.tasks_config:
                self.tasks_config[task_name] = {
                    k: v.format(**self._inputs) if isinstance(v, str) else v
                    for k, v in self.tasks_config[task_name].items()
                }
        
        return self._inputs

    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            tools=[ProjectSetupTool()],
            verbose=True
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            tools=[FrontendTool()],
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            tools=[BackendTool()],
            verbose=True
        )

    @agent
    def smart_contract_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['smart_contract_developer'],
            tools=[SmartContractTool()],
            verbose=True
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            tools=[TestingTool()],
            verbose=True
        )

    @agent
    def integrator(self) -> Agent:
        return Agent(
            config=self.agents_config['integrator'],
            tools=[IntegrationTool()],
            verbose=True
        )

    @task
    def project_setup(self) -> Task:
        return Task(
            config=self.tasks_config['project_setup']
        )

    @task
    def frontend_development(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_development']
        )

    @task
    def backend_development(self) -> Task:
        return Task(
            config=self.tasks_config['backend_development']
        )

    @task
    def smart_contract_development(self) -> Task:
        return Task(
            config=self.tasks_config['smart_contract_development']
        )

    @task
    def contract_testing(self) -> Task:
        return Task(
            config=self.tasks_config['contract_testing']
        )

    @task
    def frontend_contract_integration(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_contract_integration']
        )

    @task
    def backend_frontend_integration(self) -> Task:
        return Task(
            config=self.tasks_config['backend_frontend_integration']
        )

    @task
    def final_integration_and_testing(self) -> Task:
        return Task(
            config=self.tasks_config['final_integration_and_testing']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NoccStacks crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )