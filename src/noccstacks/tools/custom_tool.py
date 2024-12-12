from crewai_tools import BaseTool
from typing import Dict, Any, Union, List
from pydantic import BaseModel, Field

class TaskContext(BaseModel):
    description: str
    expected_output: str
    task: str = ""
    project_name: str = ""
    project_description: str = ""

class TaskInput(BaseModel):
    description: str
    context: List[Dict[str, Any]] = Field(default_factory=list)

class ProjectSetupTool(BaseTool):
    name: str = "Project Setup Tool"
    description: str = "Tool for setting up the project structure and initial configurations."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Get project details from context
        project_context = task_input.context[0] if task_input.context else {}
        project_name = project_context.get('project_name', '')
        project_description = project_context.get('project_description', '')

        return {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Project setup completed",
            "project_name": project_name,
            "project_description": project_description,
            "setup_completed": True,
            "project_structure": {
                "frontend": ["src/frontend/", "src/frontend/js/", "src/frontend/css/"],
                "backend": ["src/backend/", "src/backend/api/"],
                "contracts": ["contracts/", "tests/"],
                "config": ["Clarinet.toml", "package.json"]
            }
        }

class FrontendTool(BaseTool):
    name: str = "Frontend Development Tool"
    description: str = "Tool for creating HTML and Tailwind CSS frontend."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Get project details from context
        project_context = task_input.context[0] if task_input.context else {}
        project_name = project_context.get('project_name', '')

        return {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Frontend components created",
            "project_name": project_name,
            "frontend_completed": True,
            "frontend_files": {
                "index.html": "Main application page",
                "js/app.js": "Application logic",
                "css/styles.css": "Tailwind styles"
            },
            "components": ["Header", "MainContent", "ContractInteraction"]
        }

class BackendTool(BaseTool):
    name: str = "Backend Development Tool"
    description: str = "Tool for developing backend with JavaScript and Supabase integration."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Get project details from context
        project_context = task_input.context[0] if task_input.context else {}
        project_name = project_context.get('project_name', '')

        return {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Backend components created",
            "project_name": project_name,
            "backend_completed": True,
            "api_endpoints": ["/api/messages", "/api/contracts"],
            "database_schema": {
                "tables": ["messages", "contracts"],
                "functions": ["get_message", "set_message"]
            }
        }

class SmartContractTool(BaseTool):
    name: str = "Smart Contract Development Tool"
    description: str = "Tool for developing Clarity smart contracts."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Convert string task to TaskInput format
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Get project details from context if available
        project_context = task_input.context[0] if task_input.context else {}
        project_name = project_context.get('project_name', 'hello_nocc_devs')

        return {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Smart contract created",
            "project_name": project_name,
            "contract_completed": True,
            "contract_functions": ["get-message", "set-message"],
            "contract_details": {
                "name": project_name,
                "functions": {
                    "get-message": {"type": "read-only", "returns": "string"},
                    "set-message": {"type": "public", "params": ["string"]}
                }
            }
        }

class TestingTool(BaseTool):
    name: str = "Testing Tool"
    description: str = "Tool for writing and running tests for Clarity smart contracts using Clarinet and Vitest."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Get contract details from context
        contract_context = task_input.context[0] if task_input.context else {}
        contract_functions = contract_context.get('contract_functions', [])
        project_name = contract_context.get('project_name', '')

        return {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Test suite created",
            "project_name": project_name,
            "tests_completed": True,
            "tested_functions": contract_functions,
            "test_files": {
                f"tests/{project_name}.test.ts": "Main contract test file",
                "tests/utils.ts": "Test utilities"
            }
        }

class IntegrationTool(BaseTool):
    name: str = "Integration Tool"
    description: str = "Tool for integrating frontend, backend, and smart contracts."

    def _run(self, task: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        # Convert string task to TaskInput format
        if isinstance(task, str):
            task_input = TaskInput(description=task, context=[])
        else:
            task_input = TaskInput(**task)

        # Merge all context
        merged_context = {}
        for ctx in task_input.context:
            merged_context.update(ctx)

        project_name = merged_context.get('project_name', '')
        frontend_files = merged_context.get('frontend_files', {})
        api_endpoints = merged_context.get('api_endpoints', [])
        contract_functions = merged_context.get('contract_functions', [])

        # Create the integration result
        result = {
            "task": task_input.description,
            "description": task_input.description,
            "expected_output": "Components integrated",
            "project_name": project_name,
            "integration_completed": True,
            "integrated_components": {
                "frontend": list(frontend_files.keys()) if frontend_files else [],
                "backend": api_endpoints,
                "contract": contract_functions
            },
            "integration_files": {
                "src/integration/stacks-integration.js": "Stacks.js integration",
                "src/integration/api-client.js": "API client",
                "src/integration/types.ts": "TypeScript types"
            }
        }

        return result