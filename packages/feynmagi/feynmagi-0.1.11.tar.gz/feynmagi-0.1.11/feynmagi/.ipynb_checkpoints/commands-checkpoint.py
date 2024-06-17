###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################
from logger import * 
import abc
import dataclasses
import orjson
from typing import Any, List, Optional

import numpy as np
import os
import helper
import logger
import vectorsdb 
import traceback
import websearch as webs
import config as cfg

import os
import html
import json
import base64

import threading
import autollm

import agentdev as dev
from tasks import add_task, thread_manager

def calculate(num1, operator, num2):
    num1=float(num1)
    num2=float(num2)
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*' or operator == 'x':
        return num1 * num2
    elif operator == '/' or operaror == '÷':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero."
    else:
        return "Error: Unsupported operator."
        

def get_command(response_json):
    """Parse the response and return the command name and arguments"""
    logger.debug(f"get_command {response_json}")
    print("=========================> get command")
    print("get command",type(response_json),response_json)
    try:
        if "command" not in response_json:
            return "exit" , "Missing 'command' object in JSON"

        command = response_json["command"]

        if "name" not in command:
            return "exit", "Missing 'name' field in 'command' object"

        command_name = command["name"]

        if command_name == None:
            return "exit", "Missing 'name' field in 'command' object"


        # Use an empty dictionary if 'args' field is not present in 'command' object
        arguments = command.get("args", {})

        return command_name, arguments
    except json.decoder.JSONDecodeError:
        return "exit", "Invalid JSON"
    # All other errors, return "Error: + error message"
    except Exception as e:
        return "Error:", str(e)

def get_thoughts(response_json):
    """Parse the response and return the command name and arguments"""
    logger.debug(f"get_thoughts {response_json}")
    print("=========================> get command")
    print("get thoughts",type(response_json),response_json)
    try:
        if "thoughts" not in response_json:
            return "Error:" , "Missing 'command' object in JSON"

        thoughts = response_json["thoughts"]

        if "speak" not in thoughts:
            return "Error:", "Missing 'speak' field in 'thoughts' object"

        speak = thoughts["speak"]

        # Use an empty dictionary if 'args' field is not present in 'command' object

        return speak
    except json.decoder.JSONDecodeError:
        return "Error:", "Invalid JSON"
    # All other errors, return "Error: + error message"
    except Exception as e:
        return "Error:", str(e)


def execute_command(command_name, arguments):
    """Execute the command and return the result"""

    print(f"__________________ //{command_name}//",command_name,"  args : ", arguments)
    print("____________________________________________//")
    memory = cfg.vdb
    command_name=command_name.lower().strip()
    try:
        if command_name == "output" :
            message=arguments.get("output","")
            if message == "" or message == None :
                message=arguments["message"]

            print("printing output",message)
            send_text(message)
            return "exit"
            
        if command_name == "do-nothing" or  command_name == "exit" :
            return "exit"
        elif command_name == "ask":
            question=arguments["question"]
            if question ==  None:
                question = "Any additional information?"
            return send_popup(question)
            
        elif command_name == "google" or command_name == "google search" :
           
            return webs.quick_search(arguments['query'])
            
        elif command_name == "calculate" :
            return calculate(arguments["num1"],arguments["operator"],arguments["num2"])
        elif command_name == "rag" :
            return " Nothing found "
        elif command_name == "agent" :
            return " Agent started "
        elif command_name == "memory" :
            return " Memorized "
        elif command_name == "developer" :
            return " agent started "
        elif command_name == "interpreter" :
            return " started  "
            
        elif command_name == "start-agent":
            logger.say_text(f"Starting agent {arguments['agent']} for {arguments['objective']}")
            return start_agent(
                arguments["agent"],
                arguments["objective"])

        elif command_name == "help":
            message="Help" # arguments["file"]
            return logger.say_text(message)
            
        elif command_name == "write-code":
            objective=arguments["objective"]
            language = arguments["language"]
            framework = arguments["framework"]
            file_name = arguments["file_name"]
            print(")))))))))))))))))))) calling dev")
            return dev.dev_code(objective,language,framework,file_name)
            
        elif command_name == "execute-code":
            
            file_name=arguments["file_name"]
            input=arguments["input"]
            environment=arguments["environment"]
            return dev.exec_code(file_name,input,environment)   
        
        elif command_name == "read-file":
            return read_file(arguments["file"])    
        elif command_name == "display-file":
            return display_file(arguments["file"])       
        elif command_name == "write-to-file":
            return write_to_file(arguments["file"], arguments["text"])
        elif command_name == "append-to-file":
            return append_to_file(arguments["file"], arguments["text"])
        elif command_name == "delete-file":
            return delete_file(arguments["file"])
            
       
        elif command_name == "browse-website":
            return webs.browse_website(arguments["url"], arguments["question"])
        # TODO: Change these to take in a file rather than pasted code, if
        # non-file is given, return instructions "Input should be a python
        # filepath, write your code to file and try again"
        elif command_name == "evaluate-code":
            return ai.evaluate_code(arguments["code"])
        elif command_name == "improve-code":
            return ai.improve_code(arguments["suggestions"], arguments["code"])
        elif command_name == "write-tests":
            return ai.write_tests(arguments["code"], arguments.get("focus"))
        elif command_name == "execute_python_file":  # Add this command
            return execute_python_file(arguments["file"])
        elif command_name == "generate-image":
            return generate_image(arguments["prompt"])
        elif command_name == "do-nothing":
            return "No action performed."
        elif command_name == "task-complete":
            shutdown()
        else:
            return f"Unknown command '{command_name}'. Please refer to the 'COMMANDS' list for available commands and only respond in the specified JSON format."
    # All errors, return "Error: + error message"
    except Exception as e:
        return "Error: " + str(e)


def get_datetime():
    """Return the current date and time"""
    return "Current date and time: " + \
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def google_search(query, num_results=8):
    """Return the results of a google search"""
    search_results = []
    for j in ddg(query, max_results=num_results):
        search_results.append(j)

    return json.dumps(search_results, ensure_ascii=False, indent=4)

def google_official_search(query, num_results=8):
    """Return the results of a google search using the official Google API"""
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import json

    try:
        # Get the Google API key and Custom Search Engine ID from the config file
        api_key = cfg.google_api_key
        custom_search_engine_id = cfg.custom_search_engine_id

        # Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=api_key)

        # Send the search query and retrieve the results
        result = service.cse().list(q=query, cx=custom_search_engine_id, num=num_results).execute()

        # Extract the search result items from the response
        search_results = result.get("items", [])

        # Create a list of only the URLs from the search results
        search_results_links = [item["link"] for item in search_results]

    except HttpError as e:
        # Handle errors in the API call
        error_details = json.loads(e.content.decode())

        # Check if the error is related to an invalid or missing API key
        if error_details.get("error", {}).get("code") == 403 and "invalid API key" in error_details.get("error", {}).get("message", ""):
            return "Error: The provided Google API key is invalid or missing."
        else:
            return f"Error: {e}"

    # Return the list of search result URLs
    return search_results_links

def browse_website(url, question):
    """Browse a website and return the summary and links"""
    summary = get_text_summary(url, question)
    links = get_hyperlinks(url)

    # Limit links to 5
    if len(links) > 5:
        links = links[:5]

    result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""

    return result


def get_text_summary(url, question):
    """Return the results of a google search"""
    text = browse.scrape_text(url)
    summary = browse.summarize_text(text, question)
    return """ "Result" : """ + summary


def get_hyperlinks(url):
    """Return the results of a google search"""
    link_list = browse.scrape_links(url)
    return link_list


def commit_memory(string):
    """Commit a string to memory"""
    _text = f"""Committing memory with string "{string}" """
    mem.permanent_memory.append(string)
    return _text


def delete_memory(key):
    """Delete a memory with a given key"""
    if key >= 0 and key < len(mem.permanent_memory):
        _text = "Deleting memory with key " + str(key)
        del mem.permanent_memory[key]
        print(_text)
        return _text
    else:
        print("Invalid key, cannot delete memory.")
        return None


def overwrite_memory(key, string):
    """Overwrite a memory with a given key and string"""
    # Check if the key is a valid integer
    if is_valid_int(key):
        key_int = int(key)
        # Check if the integer key is within the range of the permanent_memory list
        if 0 <= key_int < len(mem.permanent_memory):
            _text = "Overwriting memory with key " + str(key) + " and string " + string
            # Overwrite the memory slot with the given integer key and string
            mem.permanent_memory[key_int] = string
            print(_text)
            return _text
        else:
            print(f"Invalid key '{key}', out of range.")
            return None
    # Check if the key is a valid string
    elif isinstance(key, str):
        _text = "Overwriting memory with key " + key + " and string " + string
        # Overwrite the memory slot with the given string key and string
        mem.permanent_memory[key] = string
        print(_text)
        return _text
    else:
        print(f"Invalid key '{key}', must be an integer or a string.")
        return None


def shutdown():
    """Shut down the program"""
    print("Shutting down...")
    quit()


def start_agent(name, objective):
    """Start an agent with a given name, task, and prompt"""
    # strat thread here
    '''
    agent_thread = threading.Thread(target=autollm.start_autosession, args=(objective,name))
    agent_thread.start()
    agent_thread.join()
    '''
    add_task(1,autollm.start_autosession, objective,name)
    # exiting initial session 
    return f"agent {name} started, now you MUST exit"



def display_file(file_path):
    """
    Reads the contents of a file and displays them in a black background box with buttons to copy and download.
    
    :param file_path: Path to the file to be read
    """
    file_path="../working/"+file_path
    if not os.path.exists(file_path):
        return logger.say_text(f"Error: File '{file_path}' does not exist.")
    
    with open(file_path, 'r') as file:
        contents = file.read()
        
    file_name = os.path.basename(file_path)
    
    html_content = f"""
    <div style="background-color: black; color: white; padding: 20px; border-radius: 5px; position: relative;">
        <pre id="fileContent" style="white-space: pre-wrap; word-wrap: break-word; color: white;">{contents}</pre>
        <button id="copyButton" title="Copy" style="position: absolute; top: 10px; right: 60px; background-color: white; color: black; border: none; padding: 10px; cursor: pointer;"><span class="bi bi-copy"></span></button>
        <a id="downloadButton" href="data:text/plain;charset=utf-8,{contents}" download="{file_name}" style="position: absolute; top: 10px; right: 10px; background-color: white; color: black; border: none; padding: 10px; text-decoration: none; text-align: center;"><span class="bi bi-download"></span></a>
    </div>
    <script>
        $(document).ready(function() {{
            $('#copyButton').click(function() {{
                const text = $('#fileContent').text();
                const tempInput = $('<input>');
                $('body').append(tempInput);
                tempInput.val(text).select();
                document.execCommand('copy');
                tempInput.remove();
                alert('Copied to clipboard');
            }});
        }});
    </script>
    """
   
    send_textfile(html_content)
    return("File Displyed")

def read_file(file_path):
    file_path="../working/"+file_path
    """
    Reads the contents of a file and returns them.
    
    :param file_path: Path to the file to be read
    :return: Contents of the file
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    
    with open(file_path, 'r') as file:
        contents = file.read()
    return f"\n\n--start\n{contents}\n--end"

def write_to_file(file_path, text):
    file_path="../working/"+file_path
    """
    Writes text to a file, overwriting any existing content.
    
    :param file_path: Path to the file to be written to
    :param text: Text to write to the file
    :return: Success message
    """
    with open(file_path, 'w') as file:
        file.write(text)
        file.close()
    
    return f"Successfully wrote to '{file_path}'."

def append_to_file(file_path, text):
    file_path="../working/"+file_path
    """
    Appends text to a file.
    
    :param file_path: Path to the file to append to
    :param text: Text to append to the file
    :return: Success message
    """
    with open(file_path, 'a') as file:
        file.write(text)
    return f"Successfully appended to '{file_path}'."