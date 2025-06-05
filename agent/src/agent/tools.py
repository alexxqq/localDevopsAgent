from langchain_core.tools import tool

import psutil
import shutil
import platform
import socket
import subprocess
import os

from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def execute_bash_command(command: str, timeout: int = 60) -> str:
    """
    DANGEROUS TOOL: Executes a given bash command directly on the system.
    This tool should ONLY be used in highly isolated, sandboxed environments.
    Be extremely cautious with its usage.

    Args:
        command (str): The bash command to execute.
        timeout (int): Maximum time in seconds to wait for the command to complete.
                       Defaults to 60 seconds.

    Returns:
        str: The stdout and stderr of the command, or an error message if it fails.
    """
    try:
        logger.info(f'Running command: {command}')
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return output
    except subprocess.CalledProcessError as e:
        error_output = f"Command failed with exit code {e.returncode}.\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        logger.info(f"Bash command failed. Error:\n{error_output[:200]}...")
        return f"Error executing command: {error_output}"
    except subprocess.TimeoutExpired as e:
        error_output = f"Command timed out after {timeout} seconds. STDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        logger.info(f"Bash command timed out. Error:\n{error_output[:200]}...")
        return f"Error: Command timed out: {error_output}"
    except Exception as e:
        error_output = f"An unexpected error occurred: {e}"
        logger.info(f"Bash command unexpected error. Error:\n{error_output[:200]}...")
        return f"Error: {error_output}"
