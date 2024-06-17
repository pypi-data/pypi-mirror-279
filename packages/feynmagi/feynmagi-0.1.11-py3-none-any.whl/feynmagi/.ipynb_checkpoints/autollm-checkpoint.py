###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################
import threading
import re
from datetime import datetime
from socketio_instance import get_socketio
import helper
import logger
import commands as cmd

import llmsapis 
import config as cfg

# Protéger les variables globales avec des verrous
lock = threading.Lock()

actual_max_tokens = 8000

def get_global_variable(var_name):
    with lock:
        value = globals().get(var_name)
        print(f"[DEBUG] Getting global variable {var_name}: {value}")
        return value

def set_global_variable(var_name, value):
    with lock:
        globals()[var_name] = value
        print(f"[DEBUG] Setting global variable {var_name} to: {value}")

def parse_agent(response):
    print("[DEBUG] ----- parsing -----")
    print(response)
    print("[DEBUG] end ----- parsing -----")
    
    command_pattern = re.compile(r"""
    ###\s*AGENT\s*###\s*      # Match the COMMAND header
    Agent\s*(.*?)\s*          # Match the command name after 'Agent'
    (?:Args?|Arguments?)\s*:?\s*(.*)  # Match 'Arg', 'Args', 'Arguments' followed by optional ':' and then capture the rest
    """, re.VERBOSE | re.IGNORECASE)
    
    match = command_pattern.search(response)
    
    if match:
        print("[DEBUG] matched")
        command_name = match.group(1).strip() if match.group(1) else None
        arguments = match.group(2).strip() if match.group(2) else None
        print("[DEBUG] found ....", command_name, arguments)
        command_name = command_name.lower()
        if "web" in command_name:
            command_name = "web"
        elif "developer" in command_name:
            command_name = "developer"
        elif "interpreter" in command_name:
            command_name = "interpreter"
        elif "rag" in command_name:
            command_name = "rag"
        elif "memory" in command_name:
            command_name = "memory"
        elif "creator" in command_name:
            command_name = "agent"
        return command_name, arguments
    
    return None, None

def parse_command(response):
    print("[DEBUG] ----- parsing -----")
    print(response)
    print("[DEBUG] end ----- parsing -----")
    
    command_pattern = re.compile(r"""
    ###\s*COMMAND\s*###\s*      # Match the COMMAND header
    Command\s*:\s*(.*?)\s*      # Match the command name after 'Command:'
    Args\s*:\s*(.*)             # Match 'Args:' followed by the arguments
    """, re.VERBOSE | re.IGNORECASE)
    
    match = command_pattern.search(response)
    
    if match:
        print("[DEBUG] matched")
        command_name = match.group(1).strip().lower() if match.group(1) else None
        arguments_str = match.group(2).strip() if match.group(2) else None
        
        print("[DEBUG] found ....", command_name, arguments_str)
        
        if "google" in command_name:
            command_name = "google"
        elif "calc" in command_name:
            command_name = "calculate"
        elif "write" in command_name:
            command_name = "write-to-file"
        elif "read" in command_name:
            command_name = "read-file"
        elif "append" in command_name:
            command_name = "append-to-file"
        elif "display" in command_name:
            command_name = "display-file"
        
         # Parse the arguments into a dictionary
        arguments = {}
        if arguments_str:
            arguments_list = re.split(r'\s*[;,]\s*', arguments_str)  # Split by ',' or ';' with optional whitespace
            for arg in arguments_list:
                if ':' in arg:
                    key, value = arg.split(':', maxsplit=1)  # Split by ':' with optional whitespace
                    key = key.strip().strip('"')
                    value = value.strip().strip('"')
                    arguments[key.lower()] = value
                    
        return command_name, arguments
    
    return None, None

def current_datetime_string():
    now = datetime.now()
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time_str

def get_context():
    return f"Please note that current date and time is : {current_datetime_string()}"

def update_session_history(m_history, new_message, max_tokens):
    m_history.append(new_message)
    total_tokens = sum(helper.count_tokens(msg['content']) for msg in m_history)
    while total_tokens > max_tokens:
        total_tokens -= helper.count_tokens(m_history.pop(0)['content'])

def check_command_name(command_name):

    if command_name in ['default','web','memeory','rag','interreter','developer']:
        return command_name
    return "na"
    
def start_autosession(user_input):
    print("[DEBUG] Starting autosession...")  # Log de diagnostic
    socketio = get_socketio()
    print(f"[DEBUG] SocketIO instance: {socketio}")  # Log de diagnostic
    context = get_context()
    
    # m_history = []

    if cfg.actual_agent == "default":
        m_history = cfg.session_message_history
        if not get_global_variable('session_message_history'):
            system_prompt = open('./prompts/system_default.txt', 'r').read()
            actual_message = system_prompt + context + '\nuser input : ' + user_input
            
        else:
            actual_message = user_input
    else:
        m_history = cfg.agent_message_history
        if not get_global_variable('agent_message_history'):
            system_prompt = open(f'./prompts/system_{cfg.actual_agent}.txt', 'r').read()
            actual_message = system_prompt + context + '\nYour mission : ' + user_input + '\nNow help me please'
            
        else:
            actual_message = user_input

    while True:
        logger.send_text(f"<BR>_______________{cfg.actual_agent}___________________<BR>")
        '''
        for i, h in enumerate(m_history):
            print(f"[DEBUG] ==== _______________________ i={i}")
            print(h)
            print(f"[DEBUG] ==== _______________________ i={i}")
        '''

        logger.write_log("000 =========================================================================================================")
        logger.write_log(actual_message)
        update_session_history(m_history, {"role": "user", "content": actual_message}, actual_max_tokens)
        logger.write_log("111 =========================================================================================================")

        assistant_reply = ""
        for response_text in llmsapis.llmchatgenerator(m_history, temperature=0., stream=True, raw=False):
            assistant_reply += response_text
            socketio.emit('response_token', {'token': response_text})
        logger.write_log(assistant_reply)
        logger.write_log("222 =========================================================================================================")

        if not assistant_reply:
            logger.say_text(f"Auto LLM assistant returned None ... breaking")
            break

        new_message = {
            "role": "assistant",
            "content": assistant_reply
        }
        cfg.session_message_history.append(new_message)
        update_session_history(m_history, new_message, actual_max_tokens)

        if cfg.actual_agent == "default":
            command_name, arguments = parse_agent(assistant_reply)
        else:
            command_name, arguments = parse_command(assistant_reply)
            

        if cfg.actual_agent == "default":
            if command_name:
                print(f"[DEBUG] calling agent ....{command_name}.{arguments}")
                command_name=check_command_name(command_name)
                if command_name=="na":
                    result = f"Agent {command_name} does not exit !  " 
                    break
                    
                cfg.actual_agent= command_name
                restart_autosession(arguments)  # Relancer start_autosession avec les arguments
                break
            else:
                print("[DEBUG] no agent name provided")
                break
        else:
            if command_name:
                print("[DEBUG] calling command ....")
                if command_name == "exit":
                    logger.say_text(f"{cfg.actual_agent} exiting to default agent")
                    cfg.actual_agent= "default"
                    break
                ret_cmd=cmd.execute_command(command_name, arguments)
                if ret_cmd is not None:
                    result = f"Command {command_name} returned : " + ret_cmd
                    restart_autosession(result)  # Relancer start_autosession avec le résultat
                    cfg.session_message_history.append({"role": "user", "content": result})
                    break
            else:
                break

def restart_autosession(new_user_input):
    #print(f"[DEBUG] Restarting autosession with new user input: {new_user_input}")  # Log de diagnostic
    #with lock:
    set_global_variable('user_input', new_user_input)
    print("[DEBUG] _____ get socket")
    socketio = get_socketio()
    #print(f"[DEBUG] socketio instance: {socketio}")  # Log de diagnostic
    #print("[DEBUG] _____ start_background_task")
    socketio.start_background_task(target=start_autosession, user_input=new_user_input)
