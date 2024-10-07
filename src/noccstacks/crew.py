from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from noccstacks.tools.custom_tool import ProjectSetupTool, FrontendTool, BackendTool, SmartContractTool, TestingTool, IntegrationTool

@CrewBase
class NoccstacksCrew():
    """Noccstacks crew"""

    def __init__(self):
        super().__init__()
        self.inputs = {}  # Initialize inputs as an empty dictionary

    def _replace_placeholders(self, config, inputs):
        for key, value in config.items():
            if isinstance(value, str):
                config[key] = value.format(project_name=inputs.get('project_name', ''), 
                                           project_description=inputs.get('project_description', ''))
            elif isinstance(value, dict):
                self._replace_placeholders(value, inputs)
        return config

    @agent
    def project_manager(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['project_manager'], self.inputs)
        return Agent(
            config=config,
            tools=[ProjectSetupTool()],
            verbose=True
        )

    @agent
    def frontend_developer(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['frontend_developer'], self.inputs)
        return Agent(
            config=config,
            tools=[FrontendTool()],
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['backend_developer'], self.inputs)
        return Agent(
            config=config,
            tools=[BackendTool()],
            verbose=True
        )

    @agent
    def smart_contract_developer(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['smart_contract_developer'], self.inputs)
        return Agent(
            config=config,
            tools=[SmartContractTool()],
            verbose=True
        )

    @agent
    def test_engineer(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['test_engineer'], self.inputs)
        return Agent(
            config=config,
            tools=[TestingTool()],
            verbose=True
        )

    @agent
    def integrator(self) -> Agent:
        config = self._replace_placeholders(self.agents_config['integrator'], self.inputs)
        return Agent(
            config=config,
            tools=[IntegrationTool()],
            verbose=True
        )

    @task
    def project_setup(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['project_setup'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def frontend_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['frontend_development'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def backend_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['backend_development'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def smart_contract_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['smart_contract_development'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def contract_testing(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['contract_testing'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def frontend_contract_integration(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['frontend_contract_integration'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def backend_frontend_integration(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['backend_frontend_integration'], self.inputs)
        return Task(
            config=config,
        )

    @task
    def final_integration_and_testing(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['final_integration_and_testing'], self.inputs)
        return Task(
            config=config,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Noccstacks crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def set_inputs(self, inputs):
        """Set the inputs for the crew"""
        self.inputs = inputs