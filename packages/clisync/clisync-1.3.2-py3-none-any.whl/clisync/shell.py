import os
import logging

from typing import Optional

logger = logging.getLogger()


def setup_autocomplete(command: str, conda_env: Optional[str] = None, rc_path: Optional[str] = None):
    """Setup the autocomplete for the CLI. This adds the following to the shell configuration file:
    - For zsh: `eval "$(_COMMAND_COMPLETE=zsh_source command)"`
    - For bash: `eval "$(_COMMAND_COMPLETE=bash_source command)"`
    If a Conda environment is activated, it will add the autocompletion to the environment's activate.d directory.

    Args:
        command (str): The command to add autocompletion for.
        conda_env (Optional[str], optional): The conda environment to add autocompletion to. Defaults to None.
        rc_path (Optional[str], optional): The path to the shell configuration file. Defaults to None.
    """
    # If using conda
    if setup_autocomplete_for_conda(command, conda_env=conda_env):
        return

    upper = command.replace("-", "_").upper()

    description = f"\n# Added automatically autocompletion for CliSync command `{command}`.\n"
    shell_cmd = f'eval "$(_{upper}_COMPLETE={{{{SHELL}}}}_source {command})"'
    try:
        rc_path = os.path.expanduser("~") if rc_path is None else rc_path
        zshpath = os.path.join(rc_path, ".zshrc")
        bashpath = os.path.join(rc_path, ".bashrc")
        if os.path.exists(zshpath):
            logger.info(f"🔧 Adding autocompletion to your {zshpath}.")
            # Check if the autocompletion is already added
            shell_cmd = shell_cmd.replace("{{SHELL}}", "zsh")
            if not (shell_cmd in os.popen(f"cat {zshpath}").read()):
                with open(zshpath, "a") as f:
                    f.write(description)
                    f.write(shell_cmd)
            else:
                logger.info("The autocompletion is already added to your shell.")
        elif os.path.exists(bashpath):
            logger.info(f"🔧 Adding autocompletion to your {bashpath}.")
            shell_cmd = shell_cmd.replace("{{SHELL}}", "bash")
            if not (shell_cmd in os.popen(f"cat {bashpath}").read()):
                with open(bashpath, "a") as f:
                    f.write(description)
                    f.write(shell_cmd)
            else:
                logger.info("The autocompletion is already added to your shell.")
        else:
            logger.info(
                "Could not find a shell configuration file. Please add the following to your shell configuration file."
            )
    except Exception as e:
        logger.info("Could not add autocompletion to your shell.")
        logger.info(
            f"""
            For zsh, add the following to your ~/.zshrc:
                {shell_cmd.replace("{{SHELL}}", "zsh")}
                    
            For bash, add the following to your ~/.bashrc:
                {shell_cmd.replace("{{SHELL}}", "bash")}
            """
        )
        pass


def setup_autocomplete_for_conda(command: str, conda_env: Optional[str] = None) -> bool:

    if conda_env is None:
        conda_env = os.getenv("CONDA_PREFIX")
    if not conda_env:
        return False

    upper = command.replace("-", "_").upper()
    description = f"\n# Added automatically autocompletion for CliSync command `{command}`.\n"
    shell_cmd = f'eval "$(_{upper}_COMPLETE={{{{SHELL}}}}_source {command})"'

    if os.path.exists(os.path.join(os.path.expanduser("~"), ".bashrc")):
        shell = "bash"
    elif os.path.exists(os.path.join(os.path.expanduser("~"), ".zshrc")):
        shell = "zsh"
    else:
        raise ValueError("Cannot infer shell (no .bashrc or .zshrc found), please specify the shell.")

    shell_cmd = shell_cmd.replace("{{SHELL}}", shell)

    os.makedirs(os.path.join(conda_env, "etc/conda/activate.d"), exist_ok=True)
    os.makedirs(os.path.join(conda_env, "etc/conda/deactivate.d"), exist_ok=True)

    file = os.path.join(conda_env, "etc/conda/activate.d/env_vars.sh")

    if not os.path.exists(file):
        with open(file, "a") as f:
            f.write("#!/bin/zsh\n")
            f.write(description)
            f.write(shell_cmd)
        logger.info(f"🔧 Adding autocompletion to your conda environment at {file}")
    else:
        # Check if the autocompletion is already added
        if not (shell_cmd in os.popen(f"cat {file}").read()):
            with open(file, "a") as f:
                f.write(shell_cmd)
            logger.info(f"🔧 Adding autocompletion to your conda environment at {file}")

        else:
            logger.info("The autocompletion is already added to your shell.")

    return True
