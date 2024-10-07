import pytest
from unittest.mock import patch, MagicMock
from noccstacks.main import run, train, replay, test
from noccstacks.crew import NoccstacksCrew
from noccstacks.tools.custom_tool import TestingTool

@pytest.fixture
def mock_crew():
    with patch('noccstacks.crew.NoccstacksCrew') as MockCrew:
        mock_instance = MagicMock()
        MockCrew.return_value = mock_instance
        yield mock_instance

def test_run(mock_crew, capsys):
    with patch('builtins.input', side_effect=["Test Project", "A test project for Noccstacks"]):
        run()
    
    mock_crew.set_inputs.assert_called_once_with({
        'project_name': 'Test Project',
        'project_description': 'A test project for Noccstacks'
    })
    mock_crew.crew.assert_called_once()
    mock_crew.crew().kickoff.assert_called_once()
    
    captured = capsys.readouterr()
    assert "Project completed successfully!" in captured.out

def test_train(mock_crew):
    with patch('sys.argv', ['train', '5', 'test_file.json']):
        train()
    
    mock_crew.crew().train.assert_called_once_with(
        n_iterations=5,
        filename='test_file.json',
        inputs={
            "project_name": "Sample Project",
            "project_description": "A sample project for training"
        }
    )

def test_replay(mock_crew):
    with patch('sys.argv', ['replay', 'task_123']):
        replay()
    
    mock_crew.crew().replay.assert_called_once_with(task_id='task_123')

def test_test(mock_crew):
    with patch('sys.argv', ['test', '3', 'gpt-3.5-turbo']):
        test()
    
    mock_crew.crew().test.assert_called_once_with(
        n_iterations=3,
        openai_model_name='gpt-3.5-turbo',
        inputs={
            "project_name": "Test Project",
            "project_description": "A test project for evaluation"
        }
    )

def test_testing_tool():
    testing_tool = TestingTool()
    result = testing_tool._run("Write a test for the smart contract")
    assert "Testing task completed: Write a test for the smart contract" in result
    assert "Example test structure:" in result
    assert "describe('my-contract', () => {" in result