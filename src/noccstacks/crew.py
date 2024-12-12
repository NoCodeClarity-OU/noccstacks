from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from noccstacks.tools.custom_tool import (
    ProjectSetupTool, FrontendTool, BackendTool,
    SmartContractTool, TestingTool, IntegrationTool
)
from typing import Dict, Any, List

@CrewBase
class NoccstacksCrew():
    """Noccstacks crew"""

    def __init__(self):
        super().__init__()
        self.inputs = {}

    def validate_inputs(self):
        """Validate required inputs are present"""
        required_inputs = ['project_name', 'project_description']
        missing_inputs = [input for input in required_inputs if not self.inputs.get(input)]
        if missing_inputs:
            raise ValueError(f"Missing required inputs: {', '.join(missing_inputs)}")

    def _replace_placeholders(self, config, inputs):
        """Replace placeholders in config with actual values"""
        if isinstance(config, dict):
            return {k: self._replace_placeholders(v, inputs) for k, v in config.items()}
        elif isinstance(config, str):
            return config.format(
                project_name=inputs.get('project_name', ''),
                project_description=inputs.get('project_description', '')
            )
        return config

    def _format_context(self, task_output: Dict[str, Any], task_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format task output as proper context with required fields"""
        if not task_output:
            return []
        return [{
            "description": task_config.get('description', ''),
            "expected_output": task_config.get('expected_output', ''),
            **task_output
        }]

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
            context=[{
                "description": config['description'],
                "expected_output": config['expected_output'],
                "project_name": self.inputs.get('project_name', ''),
                "project_description": self.inputs.get('project_description', '')
            }]
        )

    @task
    def frontend_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['frontend_development'], self.inputs)
        setup_output = self.project_setup().output
        return Task(
            config=config,
            context=self._format_context(setup_output, self.tasks_config['project_setup'])
        )

    @task
    def backend_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['backend_development'], self.inputs)
        setup_output = self.project_setup().output
        return Task(
            config=config,
            context=self._format_context(setup_output, self.tasks_config['project_setup'])
        )

    @task
    def smart_contract_development(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['smart_contract_development'], self.inputs)
        setup_output = self.project_setup().output
        return Task(
            config=config,
            context=self._format_context(setup_output, self.tasks_config['project_setup'])
        )

    @task
    def contract_testing(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['contract_testing'], self.inputs)
        contract_output = self.smart_contract_development().output
        return Task(
            config=config,
            context=self._format_context(contract_output, self.tasks_config['smart_contract_development'])
        )

    @task
    def frontend_contract_integration(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['frontend_contract_integration'], self.inputs)
        frontend_output = self.frontend_development().output
        contract_output = self.smart_contract_development().output
        
        # Combine context from both frontend and contract tasks
        context = []
        if frontend_output:
            context.extend(self._format_context(frontend_output, self.tasks_config['frontend_development']))
        if contract_output:
            context.extend(self._format_context(contract_output, self.tasks_config['smart_contract_development']))
            
        return Task(
            config=config,
            context=context
        )

    @task
    def backend_frontend_integration(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['backend_frontend_integration'], self.inputs)
        frontend_output = self.frontend_development().output
        backend_output = self.backend_development().output
        
        # Combine context from both frontend and backend tasks
        context = []
        if frontend_output:
            context.extend(self._format_context(frontend_output, self.tasks_config['frontend_development']))
        if backend_output:
            context.extend(self._format_context(backend_output, self.tasks_config['backend_development']))
            
        return Task(
            config=config,
            context=context
        )

    @task
    def final_integration_and_testing(self) -> Task:
        config = self._replace_placeholders(self.tasks_config['final_integration_and_testing'], self.inputs)
        frontend_output = self.frontend_development().output
        backend_output = self.backend_development().output
        contract_output = self.smart_contract_development().output
        test_output = self.contract_testing().output
        
        # Combine context from all previous tasks
        context = []
        if frontend_output:
            context.extend(self._format_context(frontend_output, self.tasks_config['frontend_development']))
        if backend_output:
            context.extend(self._format_context(backend_output, self.tasks_config['backend_development']))
        if contract_output:
            context.extend(self._format_context(contract_output, self.tasks_config['smart_contract_development']))
        if test_output:
            context.extend(self._format_context(test_output, self.tasks_config['contract_testing']))
            
        return Task(
            config=config,
            context=context
        )

    @crew
    def crew(self) -> Crew:
        """Create the crew with all agents and tasks"""
        self.validate_inputs()
        
        return Crew(
            agents=[
                self.project_manager(),
                self.frontend_developer(),
                self.backend_developer(),
                self.smart_contract_developer(),
                self.test_engineer(),
                self.integrator()
            ],
            tasks=[
                self.project_setup(),
                self.frontend_development(),
                self.backend_development(),
                self.smart_contract_development(),
                self.contract_testing(),
                self.frontend_contract_integration(),
                self.backend_frontend_integration(),
                self.final_integration_and_testing()
            ],
            process=Process.sequential
        )

    def set_inputs(self, inputs):
        """Set the inputs for the crew"""
        self.inputs = inputs