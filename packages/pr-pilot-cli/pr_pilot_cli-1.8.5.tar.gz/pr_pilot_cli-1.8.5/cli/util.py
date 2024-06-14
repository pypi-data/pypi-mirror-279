import os
import subprocess

import click
import yaml

from cli.constants import CONFIG_LOCATION, CONFIG_API_KEY


def clean_code_block_with_language_specifier(response):
    lines = response.split("\n")

    # Check if the first line starts with ``` followed by a language specifier and the last line is just ```
    if lines[0].startswith("```") and lines[-1].strip() == "```":
        # Remove the first and last lines
        cleaned_lines = lines[1:-1]
    else:
        cleaned_lines = lines

    clean_response = "\n".join(cleaned_lines)
    return clean_response


def load_config():
    """Load the configuration from the default location. If it doesn't exist,
    ask user to enter API key and save config."""
    if not os.path.exists(CONFIG_LOCATION):
        if os.getenv("PR_PILOT_API_KEY"):
            click.echo("Using API key from environment variable.")
            api_key = os.getenv("PR_PILOT_API_KEY")
        else:
            api_key_url = "https://app.pr-pilot.ai/dashboard/api-keys/"
            click.echo(f"Configuration file not found. Please create an API key at {api_key_url}.")
            api_key = click.prompt("PR Pilot API key")
        with open(CONFIG_LOCATION, "w") as f:
            f.write(f"{CONFIG_API_KEY}: {api_key}")
        click.echo(f"Configuration saved in {CONFIG_LOCATION}")
    with open(CONFIG_LOCATION) as f:
        config = yaml.safe_load(f)
    return config


def pull_branch_changes(status_indicator, console, branch, debug=False):
    status_indicator.update(f"Pull latest changes from {branch}")
    try:
        # Fetch origin and checkout branch
        subprocess_params = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(['git', 'fetch', 'origin'], **subprocess_params)
        subprocess.run(['git', 'checkout', branch], **subprocess_params)
        # Capture output of git pull
        result = subprocess.run(['git', 'pull', 'origin', branch], **subprocess_params)
        output = result.stdout
        error = result.stderr
        status_indicator.success()
        if debug:
            console.line()
            console.print(output)
            console.line()
    except Exception as e:
        status_indicator.fail()
        console.print(f"[bold red]An error occurred:[/bold red] {type(e)} {str(e)}\n\n{error if error else ''}")