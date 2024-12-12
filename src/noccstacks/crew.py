from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, task
from noccstacks.tools.custom_tool import (
    ProjectSetupTool, FrontendTool, BackendTool,
    SmartContractTool, TestingTool, IntegrationTool
)

class NoccstacksCrew:
    """Noccstacks crew"""

    def __init__(self):
        self._inputs = {}

    def set_inputs(self, inputs):
        """Set the inputs for the crew"""
        self._inputs = inputs

    @agent
    def project_manager(self) -> Agent:
        return Agent(
            role=f"Project Manager for {self._inputs.get('project_name', '')}",
            goal=f"Oversee the entire development process for {self._inputs.get('project_name', '')}",
            backstory=f"""You're an experienced project manager tasked with coordinating the development of {self._inputs.get('project_name', '')}.
            The project involves {self._inputs.get('project_description', '')}. Your expertise lies in coordinating
            complex projects and ensuring all components work seamlessly together.""",
            tools=[ProjectSetupTool()],
            verbose=True
        )

    def frontend_developer(self) -> Agent:
        return Agent(
            role=f"Frontend Developer for {self._inputs.get('project_name', '')}",
            goal=f"Create an appealing and functional user interface for {self._inputs.get('project_name', '')}",
            backstory=f"""You're a skilled frontend developer working on {self._inputs.get('project_name', '')}. 
            The project involves {self._inputs.get('project_description', '')}. You have expertise in HTML, CSS 
            (particularly Tailwind CSS), and JavaScript. You're adept at integrating frontend components with 
            smart contracts and backend systems.""",
            tools=[FrontendTool()],
            verbose=True
        )

    def backend_developer(self) -> Agent:
        return Agent(
            role=f"Backend Developer for {self._inputs.get('project_name', '')}",
            goal=f"Develop a robust backend system for {self._inputs.get('project_name', '')} and integrate with Supabase",
            backstory=f"""You're a proficient backend developer assigned to {self._inputs.get('project_name', '')}. 
            The project involves {self._inputs.get('project_description', '')}. You have extensive experience in 
            JavaScript and database integration, specializing in creating efficient server-side applications with 
            a deep understanding of Supabase for database management.""",
            tools=[BackendTool()],
            verbose=True
        )

    def smart_contract_developer(self) -> Agent:
        return Agent(
            role=f"Smart Contract Developer for {self._inputs.get('project_name', '')}",
            goal=f"Design and implement secure and efficient smart contracts for {self._inputs.get('project_name', '')}",
            backstory=f"""You're an expert in blockchain technology and smart contract development, particularly
            using Clarity for the Stacks blockchain. You're working on {self._inputs.get('project_name', '')}, 
            which involves {self._inputs.get('project_description', '')}. You have a strong focus on security 
            and efficiency in your contract designs.""",
            tools=[SmartContractTool()],
            verbose=True
        )

    def test_engineer(self) -> Agent:
        return Agent(
            role=f"Test Engineer for {self._inputs.get('project_name', '')}",
            goal=f"Ensure the reliability and correctness of the smart contracts for {self._inputs.get('project_name', '')}",
            backstory=f"""You're a meticulous test engineer focused on blockchain technologies, working on {self._inputs.get('project_name', '')}.
            The project involves {self._inputs.get('project_description', '')}. You have extensive experience in writing comprehensive
            test suites using TypeScript, particularly for smart contracts on the Stacks blockchain.""",
            tools=[TestingTool()],
            verbose=True
        )

    def integrator(self) -> Agent:
        return Agent(
            role=f"System Integrator for {self._inputs.get('project_name', '')}",
            goal=f"Seamlessly integrate all components of {self._inputs.get('project_name', '')}",
            backstory=f"""You're a versatile developer with expertise in both frontend and backend technologies,
            as well as blockchain integration. You're working on {self._inputs.get('project_name', '')}, which involves 
            {self._inputs.get('project_description', '')}. Your strength lies in connecting different parts of a system 
            to work harmoniously together.""",
            tools=[IntegrationTool()],
            verbose=True
        )

    def project_setup(self) -> Task:
        return Task(
            description=f"Set up the project structure and coordinate the development process for {self._inputs.get('project_name', '')}. Create a detailed plan based on the project description: {self._inputs.get('project_description', '')}",
            expected_output="A comprehensive project plan including milestones, task assignments, and integration points.",
            agent=self.project_manager()
        )

    def frontend_development(self) -> Task:
        return Task(
            description=f"Create a complete frontend for {self._inputs.get('project_name', '')} using HTML, Tailwind CSS, and JavaScript. Implement all necessary pages and features as described in the project: {self._inputs.get('project_description', '')}",
            expected_output="A fully functional frontend with responsive design and Stacks.js integration",
            agent=self.frontend_developer(),
            context=[self.project_setup()]
        )

    def backend_development(self) -> Task:
        return Task(
            description=f"Develop the backend system for {self._inputs.get('project_name', '')} using Supabase for database management and API creation. Integrate with Stacks.js for blockchain interactions. Ensure it meets the requirements described in: {self._inputs.get('project_description', '')}",
            expected_output="A fully functional backend system with Supabase integration and API endpoints",
            agent=self.backend_developer(),
            context=[self.project_setup()]
        )

    def smart_contract_development(self) -> Task:
        return Task(
            description=f"Design and implement smart contract(s) for {self._inputs.get('project_name', '')} using Clarity language. Ensure the contract is secure, efficient, and meets the project requirements: {self._inputs.get('project_description', '')}",
            expected_output="Complete Clarity smart contract(s) ready for deployment",
            agent=self.smart_contract_developer(),
            context=[self.project_setup()]
        )

    def contract_testing(self) -> Task:
        return Task(
            description=f"Write comprehensive tests for the {self._inputs.get('project_name', '')} smart contract(s) using Clarinet and its testing framework. Ensure all possible scenarios and edge cases are covered based on: {self._inputs.get('project_description', '')}",
            expected_output="Complete test suite for smart contracts",
            agent=self.test_engineer(),
            context=[self.smart_contract_development()]
        )

    def frontend_contract_integration(self) -> Task:
        return Task(
            description=f"Integrate the {self._inputs.get('project_name', '')} smart contract(s) with the frontend using Stacks.js. Implement necessary functions to interact with the contract from the UI, considering: {self._inputs.get('project_description', '')}",
            expected_output="Frontend integrated with smart contracts via Stacks.js",
            agent=self.integrator(),
            context=[self.frontend_development(), self.smart_contract_development(), self.contract_testing()]
        )

    def backend_frontend_integration(self) -> Task:
        return Task(
            description=f"Integrate the Supabase backend system with the frontend for {self._inputs.get('project_name', '')}, ensuring proper data flow and API usage. Consider the specific requirements outlined in: {self._inputs.get('project_description', '')}",
            expected_output="Backend and frontend fully integrated with proper data flow",
            agent=self.integrator(),
            context=[self.frontend_development(), self.backend_development()]
        )

    def final_integration_and_testing(self) -> Task:
        return Task(
            description=f"Perform final integration of all components for {self._inputs.get('project_name', '')} and conduct thorough testing of the entire system. Ensure all aspects of {self._inputs.get('project_description', '')} are met and functioning correctly with Stacks blockchain, Supabase, and the frontend.",
            expected_output="Fully integrated and tested system ready for deployment",
            agent=self.project_manager(),
            context=[self.frontend_contract_integration(), self.backend_frontend_integration()]
        )

    def crew(self) -> Crew:
        """Create the crew with all agents and tasks"""
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