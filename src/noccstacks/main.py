#!/usr/bin/env python
import sys
from noccstacks.crew import NoccstacksCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'project_name': input("Enter project name: "),
        'project_description': input("Enter project description: ")
    }
    noccstacks_crew = NoccstacksCrew()
    noccstacks_crew.set_inputs(inputs)
    crew = noccstacks_crew.crew()
    result = crew.kickoff()
    print("Project completed successfully!")
    print(result)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "project_name": "Sample Project",
        "project_description": "A sample project for training"
    }
    try:
        NoccstacksCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        NoccstacksCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "project_name": "Test Project",
        "project_description": "A test project for evaluation"
    }
    try:
        NoccstacksCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()