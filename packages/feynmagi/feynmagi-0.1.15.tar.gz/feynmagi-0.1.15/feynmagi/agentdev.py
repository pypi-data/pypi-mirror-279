###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################

import concurrent.futures
import docker
import shlex
import os
import ast

from .llmsapis import *
from .config import stop_event, logger
from .helper import *

def dev_code(objective, language, framework, file_name):
    prompt = f"""Act as an AI agent expert in code developing, write me a {language} code for this objective: {objective}.
please output only the full code including requirements importations.
please include comments to explain the code.
output nothing else but the code as to write into a code file delemited by markdowns.
"""
    
    f_prompt = format_prompt(message=prompt)
    ret = llm(f_prompt)

    # Extract the code from the markdown text
    code = extract_code_from_markdown(ret)
    
    if code:
        write_code_to_file(file_name, code)
        extract_requirements_from_py(f"../working/{file_name}")
        return file_name + " file code generated"
    else:
        return "Failed to extract code from the response."

def write_code_to_file(file_path, text):
    file_path = "../working/" + file_path
    with open(file_path, 'w') as file:
        file.write(text)
    
    return f"Successfully wrote to '{file_path}'."


def extract_requirements_from_py(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])

    # Create a requirements.txt file
    requirements_path = os.path.join(os.path.dirname(file_path), 'requirements.txt')
    with open(requirements_path, 'w') as req_file:
        for imp in sorted(imports):
            req_file.write(f"{imp}\n")
    
    return f"Successfully wrote requirements to '{requirements_path}'"

def generate_dockerfile(file_name):
    dockerfile_content = f"""
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY {file_name} .

CMD ["python", "{file_name}"]
"""
    with open("../working/Dockerfile", 'w') as file:
        file.write(dockerfile_content)
    
    return "Dockerfile generated"

def exec_code(file_name, input, environment):
    client = docker.from_env()

    try:
        # Build Docker image
        image, build_logs = client.images.build(path="../working", tag="custom-python-image")
        for log in build_logs:
            print(log)

        # Run Docker container
        container = client.containers.run("custom-python-image", detach=True, name="my-python-container")

        # Wait for the container to finish execution
        container.wait()

        # Get the logs from the container
        logs = container.logs().decode('utf-8')
        
        # Remove the container
        container.remove()

        return logs

    except docker.errors.ContainerError as e:
        return e.stderr.decode('utf-8')
    except Exception as e:
        return str(e)
