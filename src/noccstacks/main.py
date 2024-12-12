#!/usr/bin/env python
import sys
from typing import Optional, Dict, Any
from noccstacks.crew import NoccstacksCrew

def get_inputs() -> Dict[str, str]:
    """Get and validate user inputs"""
    try:
        project_name = input("Enter project name: ").strip()
        if not project_name:
            raise ValueError("Project name cannot be empty")
            
        project_description = input("Enter project description: ").strip()
        if not project_description:
            raise ValueError("Project description cannot be empty")
            
        return {
            'project_name': project_name,
            'project_description': project_description
        }
    except Exception as e:
        print(f"Error getting inputs: {str(e)}")
        sys.exit(1)

def run():
    """
    Run the crew with error handling.
    """
    try:
        inputs = get_inputs()
        noccstacks_crew = NoccstacksCrew()
        noccstacks_crew.set_inputs(inputs)
        crew = noccstacks_crew.crew()
        
        try:
            result = crew.kickoff()
            print("\nProject completed successfully!")
            print("\nResults:")
            print(result)
            return result
        except Exception as e:
            print(f"\nError during crew execution: {str(e)}")
            print("Task outputs may be incomplete or invalid.")
            sys.exit(1)
            
    except ValueError as e:
        print(f"\nValidation Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        sys.exit(1)

def train(n_iterations: Optional[int] = None, filename: Optional[str] = None):
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "project_name": "Sample Project",
        "project_description": "A sample project for training"
    }
    try:
        n_iter = int(sys.argv[1]) if n_iterations is None else n_iterations
        fname = sys.argv[2] if filename is None else filename
        
        if n_iter <= 0:
            raise ValueError("Number of iterations must be positive")
            
        NoccstacksCrew().crew().train(
            n_iterations=n_iter,
            filename=fname,
            inputs=inputs
        )
    except (IndexError, ValueError) as e:
        print(f"\nError: {str(e)}")
        print("Usage: train <n_iterations> <filename>")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        sys.exit(1)

def replay(task_id: Optional[str] = None):
    """
    Replay the crew execution from a specific task.
    """
    try:
        tid = sys.argv[1] if task_id is None else task_id
        if not tid:
            raise ValueError("Task ID is required")
            
        NoccstacksCrew().crew().replay(task_id=tid)
    except IndexError:
        print("\nError: Task ID is required")
        print("Usage: replay <task_id>")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        sys.exit(1)

def test(n_iterations: Optional[int] = None, model: Optional[str] = None):
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "project_name": "Test Project",
        "project_description": "A test project for evaluation"
    }
    try:
        n_iter = int(sys.argv[1]) if n_iterations is None else n_iterations
        model_name = sys.argv[2] if model is None else model
        
        if n_iter <= 0:
            raise ValueError("Number of iterations must be positive")
        if not model_name:
            raise ValueError("OpenAI model name is required")
            
        NoccstacksCrew().crew().test(
            n_iterations=n_iter,
            openai_model_name=model_name,
            inputs=inputs
        )
    except (IndexError, ValueError) as e:
        print(f"\nError: {str(e)}")
        print("Usage: test <n_iterations> <openai_model_name>")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()