"""
Testing for configuration module
"""

import os
import pytest
from server_metrics.utils.configuration import load_configuration, parse_arguments, load_env_variables, get_configuration
from server_metrics.utils.models import Server

# Constants
CMD_ARGS = [
    '--servers',
    '192.168.0.11:22,192.168.0.12:22',
    '--key_path',
    '/path/to/key',
    '--username',
    'testuser',
    '--combined_metrics_dir', '/path/to/metrics'
]
ENV_VARS = {
    'SERVERS': '192.168.0.13:22,192.168.0.14:22',
    'KEY_PATH': '/path/to/env_key',
    'USERNAME': 'envuser',
    'COMBINED_METRICS_DIR': '/path/to/metrics/envuser'
}
ENV_FILE_CONTENT = (
    "SERVERS=192.168.0.15:22,192.168.0.16:22\n"
    "KEY_PATH=/path/to/env_file_key\n"
    "USERNAME=fileuser\n"
    "COMBINED_METRICS_DIR=/path/to/metrics/fileuser"
)
ENV_FILE_VARS = {
    'SERVERS': '192.168.0.15:22,192.168.0.16:22',
    'KEY_PATH': '/path/to/env_file_key',
    'USERNAME': 'fileuser',
    'COMBINED_METRICS_DIR': '/path/to/metrics/fileuser'
}

@pytest.fixture
def mock_load_dotenv(mocker, tmp_path):
    """Fixture to mock loading environment variables from a temporary .env file."""
    env_file = tmp_path / '.env'
    env_file.write_text(ENV_FILE_CONTENT)

    def mock_load_dotenv_func(dotenv_path=None):
        if dotenv_path == str(env_file):
            os.environ.update(ENV_FILE_VARS)

    mocker.patch('dotenv.load_dotenv', side_effect=mock_load_dotenv_func)
    return env_file

def test_parse_arguments(mocker):
    """Test command-line argument parsing."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)
    args = parse_arguments()

    assert args.servers == '192.168.0.11:22,192.168.0.12:22'
    assert args.key_path == '/path/to/key'
    assert args.username == 'testuser'
    assert args.combined_metrics_dir == '/path/to/metrics'

def test_load_env_variables(mock_load_dotenv, monkeypatch):
    """Test loading environment variables from a .env file."""

    # Ensure no pre-existing environment variables interfere with the test
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

    # Mock the load_dotenv call to use the path to the temp .env file
    load_env_variables(dotenv_path=str(mock_load_dotenv))

    # Assert that the environment variables are set correctly
    assert os.getenv('SERVERS') == '192.168.0.15:22,192.168.0.16:22'
    assert os.getenv('KEY_PATH') == '/path/to/env_file_key'
    assert os.getenv('USERNAME') == 'fileuser'
    assert os.getenv('COMBINED_METRICS_DIR') == '/path/to/metrics/fileuser'

    # Cleanup environment variables
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

def test_get_configuration_cmd_args(mocker):
    """Test getting configuration from command-line arguments."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)
    args = parse_arguments()

    servers, combined_metrics_dir = get_configuration(args)

    starlyng01 = Server('starlyng01', '192.168.0.11', '/path/to/key', 22, 'testuser')
    starlyng02 = Server('starlyng02', '192.168.0.12', '/path/to/key', 22, 'testuser')

    assert servers == [starlyng01, starlyng02]
    assert combined_metrics_dir == '/path/to/metrics'

def test_get_configuration_env_vars(mocker):
    """Test getting configuration from environment variables."""
    mocker.patch.dict(os.environ, ENV_VARS)
    mocker.patch('sys.argv', ['configuration.py'])
    args = parse_arguments()

    servers, combined_metrics_dir = get_configuration(args)

    starlyng03 = Server('starlyng03', '192.168.0.13', '/path/to/env_key', 22, 'envuser')
    starlyng04 = Server('starlyng04', '192.168.0.14', '/path/to/env_key', 22, 'envuser')

    assert servers == [starlyng03, starlyng04]
    assert combined_metrics_dir == '/path/to/metrics/envuser'

def test_load_configuration_cmd_args(mocker):
    """Test loading configuration from command-line arguments."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)

    servers, combined_metrics_dir = load_configuration()

    starlyng01 = Server('starlyng01', '192.168.0.11', '/path/to/key', 22, 'testuser')
    starlyng02 = Server('starlyng02', '192.168.0.12', '/path/to/key', 22, 'testuser')

    assert servers == [starlyng01, starlyng02]
    assert combined_metrics_dir == '/path/to/metrics'

def test_load_configuration_env_vars(mocker):
    """Test loading configuration from environment variables."""
    mocker.patch.dict(os.environ, ENV_VARS)
    mocker.patch('sys.argv', ['configuration.py'])

    servers, combined_metrics_dir = load_configuration()

    starlyng03 = Server('starlyng03', '192.168.0.13', '/path/to/env_key', 22, 'envuser')
    starlyng04 = Server('starlyng04', '192.168.0.14', '/path/to/env_key', 22, 'envuser')

    assert servers == [starlyng03, starlyng04]
    assert combined_metrics_dir == '/path/to/metrics/envuser'

def test_load_configuration_env_file(mocker, mock_load_dotenv, monkeypatch):
    """Test loading configuration from a .env file."""
    # Mock sys.argv to simulate no command-line arguments
    mocker.patch('sys.argv', ['configuration.py'])

    # Mock Path.exists to return True for the .env file path
    mocker.patch('pathlib.Path.exists', return_value=True)

    # Ensure no pre-existing environment variables interfere with the test
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

    # Load the configuration using the temporary .env file path
    servers, combined_metrics_dir = load_configuration(dotenv_path=str(mock_load_dotenv))

    starlyng05 = Server('starlyng05', '192.168.0.15', '/path/to/env_file_key', 22, 'fileuser')
    starlyng06 = Server('starlyng06', '192.168.0.16', '/path/to/env_file_key', 22, 'fileuser')

    # Assert the configuration values
    assert servers == [starlyng05, starlyng06]
    assert combined_metrics_dir == '/path/to/metrics/fileuser'

    # Cleanup environment variables
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)
