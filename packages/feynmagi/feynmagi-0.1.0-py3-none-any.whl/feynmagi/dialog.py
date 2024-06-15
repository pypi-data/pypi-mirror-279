###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################
import config as cfg
from llmsapis import *
from vectorsdb import *
from logger import *
from helper import *
from typing import Any, Dict, Union
import time 
import traceback
import re


import json
import re
from typing import Any, Dict, List, Union

from socketio_instance import init_socketio, get_socketio



def remove_comments(text):
    # This pattern matches '//' and all characters after it until the end of the line
    pattern = r'//.*?$'
    # re.MULTILINE flag is used to make the '$' anchor match the end of each line
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
    # Remove any potential trailing whitespace left after removing comments
    cleaned_text = re.sub(r'\s+$', '', cleaned_text, flags=re.MULTILINE)
    return cleaned_text
    
def split_jsons(input_string: str) -> List[str]:
    json_strings = []
    stack = []
    start_index = None
    
    for i, char in enumerate(input_string):
        if char == '{':
            stack.append(char)
            if len(stack) == 1:
                start_index = i
        elif char == '}' and stack:
            stack.pop()
            if len(stack) == 0 and start_index is not None:
                json_strings.append(input_string[start_index:i+1])
                start_index = None

    
    return json_strings


def balance_braces(json_string: str) -> str:
    """
    Balance the braces in a JSON string.

    Args:
        json_string (str): The JSON string.

    Returns:
        str: The JSON string with braces balanced.
    """

    open_braces_count = json_string.count('{')
    close_braces_count = json_string.count('}')

    while open_braces_count > close_braces_count:
        json_string += '}'
        close_braces_count += 1

    while close_braces_count > open_braces_count:
        json_string = json_string.rstrip('}')
        close_braces_count -= 1

    try:
        json.loads(json_string)
        return json_string
    except json.JSONDecodeError as e:
        pass

def fix_invalid_escape(json_str: str, error_message: str) -> str:
    while error_message.startswith('Invalid \\escape'):
        bad_escape_location = extract_char_position(error_message)
        json_str = json_str[:bad_escape_location] + \
            json_str[bad_escape_location + 1:]
        try:
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError as e:
            if cfg.debug_mode:
                logger.debug(f"json loads error - fix invalid escape {e}")
            error_message = str(e)
    return json_str


def extract_char_position(error_message: str) -> int:
    """Extraire la position du caractère à partir du message d'erreur JSONDecodeError."""
    import re
    match = re.search(r'\(char (\d+)\)', error_message)
    if match:
        return int(match.group(1))
    raise ValueError("Position du caractère non trouvée dans le message d'erreur.")

def add_quotes_to_property_names(json_str: str) -> str:
    """Ajouter des guillemets aux noms de propriétés dans une chaîne JSON."""
    import re
    json_str = re.sub(r'(?<!\\)"', '\\"', json_str)  # Échapper les guillemets existants
    json_str = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', json_str)  # Ajouter des guillemets
    return json_str

def correct_json(json_str: str, error_message: str) -> str:
    """Corriger les erreurs communes dans une chaîne JSON."""
    if 'Invalid \\escape' in error_message:
        bad_escape_location = extract_char_position(error_message)
        json_str = json_str[:bad_escape_location] + json_str[bad_escape_location + 1:]
    elif 'Expecting property name' in error_message:
        json_str = add_quotes_to_property_names(json_str)
    json_str = balance_braces(json_str)
    return json_str
    
def correct_json_llm(json_str):
    say_text("llm correcting json")
    correct_json_prompt= open('./prompts/correct_json_prompt.txt', 'r').read()
    tail_json_prompt= open('./prompts/tail_json_prompt.txt', 'r').read()
    prompt=f"{correct_json_prompt}{json_str}{tail_json_prompt}"

    return llmcraw(prompt)
    
'''
def llm_parse_json(json_str):
    say_text("llm interpreting json")
    interpret_json_prompt= open('./prompts/interpret_json_prompt.txt', 'r').read()
    prompt=format_prompt(message=f"{interpret_json_prompt}{json_str}")

    return llm(prompt)
'''
def llm_parse_json(json_str):

    return llm(json_str)    

def fix_and_parse_json(json_str: str) -> Union[Dict[Any, Any], str]:
    """Tenter de fixer et d'analyser une chaîne JSON."""

    json_str =  remove_comments(json_str)
    try:
        return "jason", json.loads(json_str)
    except json.JSONDecodeError as e:
        corrected_json_str = correct_json(json_str, str(e))
        try:
            if corrected_json_str is not None and corrected_json_str != "" :
                return "json", json.loads(corrected_json_str)
            else:
                # try llm prompt to correct
                corrected_json_str = correct_json_llm(json_str)
                try:
                    if corrected_json_str is not None and corrected_json_str != "" :
                        return "json",  json.loads(corrected_json_str)
                    else:
                        # try llm prompt to correc
                        return "llm", llm_parse_json(json_str)
                except json.JSONDecodeError:
                    return "llm", llm_parse_json(json_str)
                    
        except json.JSONDecodeError:
            return "llm", llm_parse_json(json_str)

def extract_and_fix_jsons(input_string: str) -> List[Union[Dict[Any, Any], str]]:
    """Extraire, corriger et analyser plusieurs objets JSON d'une chaîne."""
    json_strings = split_jsons(input_string)
    parsed_jsons = [fix_and_parse_json(json_str) for json_str in json_strings]
    # print("*************************",type(parsed_jsons), type(parsed_jsons[0]), parsed_jsons)
    return parsed_jsons


    
JSON_SCHEMA = """
{
   "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    },
     "command": {
        "name": "command name",
        "args":{ "arg name": "value"
        }
    }
}
"""

def format_string(sin):
    s = sin.strip()
    return s


def print_assistant_thoughts(assistant_reply_json):
    """Prints the assistant's thoughts to the console"""
    global cfg
    
    try:
        
        assistant_thoughts_reasoning = None
        assistant_thoughts_plan = None
        assistant_thoughts_speak = None
        assistant_thoughts_criticism = None
        assistant_thoughts = assistant_reply_json.get("thoughts", {})
        assistant_thoughts_text = assistant_reply_json.get("text")

        if assistant_thoughts:
            
            assistant_thoughts_reasoning = assistant_reply_json.get("thoughts", {}).get("reasoning","")
            assistant_thoughts_plan = assistant_reply_json.get("thoughts", {}).get("plan","")
            assistant_thoughts_criticism = assistant_reply_json.get("thoughts", {}).get("criticism","")
            assistant_thoughts_speak = assistant_reply_json.get("thoughts", {}).get("speak", "")
            
        else:
            say_text("No assistant_thoughts")
            
                
        typewriter_log(f"THOUGHTS: {assistant_thoughts_text}")
        typewriter_log(f"REASONING: {assistant_thoughts_reasoning}")

        if assistant_thoughts_plan:
            typewriter_log(f"PLAN: ")
            # If it's a list, join it into a string
            if isinstance(assistant_thoughts_plan, list):
                assistant_thoughts_plan = "\n".join(assistant_thoughts_plan)
            elif isinstance(assistant_thoughts_plan, dict):
                assistant_thoughts_plan = str(assistant_thoughts_plan)

            # Split the input_string using the newline character and dashes
            lines = assistant_thoughts_plan.split('\n')
            for line in lines:
                line = line.lstrip("- ")
                typewriter_log(f"-  {line.strip()}")

        typewriter_log(f"CRITICISM: {assistant_thoughts_criticism}")
        # Speak the assistant's thoughts
        if cfg.cfg.speak_mode and assistant_thoughts_speak:
            #say_text(assistant_thoughts_speak)
            send_text(assistant_thoughts_speak)

        return assistant_reply_json
    except json.decoder.JSONDecodeError as e:
        print("")
        print("")
        print("Error: Invalid JSON\n", assistant_reply)
        cfg.logger.error("Error: Invalid JSON\n", assistant_reply)
        if cfg.cfg.speak_mode:
            say_text("I have received an invalid JSON response from the API. I cannot ignore this response.")

def trim_messages(full_message_history, lim):
    # Calculer la somme initiale
    total = sum(message[2] for message in full_message_history)
    
    # Continuer à retirer les éléments du début tant que la somme dépasse lim
    while total > lim and full_message_history:
        total -= full_message_history[0][2]
        print("deleting message histor")
        del full_message_history[0]
    
    return full_message_history

'''
def generate_context(full_message_history,tokens_limit):

    full_message_history = trim_messages(full_message_history, tokens_limit)
    texts = [message[0] for message in full_message_history]

    # Joindre les textes avec '\n' comme séparateur
    cont = '\n'.join(texts)
    #cont='\n'.join(full_message_history)
    print(">>>>>>>>>>>>>>>>>>> context start")
    print(cont)
    print(">>>>>>>>>>>>>>>>>>> context end")
    if len(cont) == 0 :
        current_context = f"the current time and date is {time.strftime('%c')}\n\n"
    else:
        current_context = f"the current time and date is {time.strftime('%c')}\n\n"\
                          f"bellow events of the history of your responses and commands or user feed back returns : \n\n{cont}\n\n"
    print("returning")                  
    return current_context
'''

def generate_first_context(user_input ):

    rag_context=""

    # get dialog context then history context

    user_rag_context=cfg.ragdb.find_similar_d(user_input)
    
    print(user_input, user_rag_context)

    if len(user_rag_context) != 0:
        # add context
        # Extract the first element of each tuple and join them into a string separated by "\n"
        first_elements_string = "\n".join([element[0] for element in user_rag_context])
        dialog_prompt= open('./prompts/dialog_context_prompt.txt', 'r').read()
        rag_context+=dialog_prompt.format(dialog_context=first_elements_string)   

     # get dialog context then history context

    hist_context=""
    user_hist_context=cfg.vdb.find_similar_d(user_input)
    
    print(user_input, user_hist_context)

    if len(user_hist_context) != 0:
        # add context
        # Extract the first element of each tuple and join them into a string separated by "\n"
        first_elements_string = "\n".join([element[0] for element in user_hist_context])
        hist_prompt= open('./prompts/hist_context_prompt.txt', 'r').read()
        hist_context+=hist_prompt.format(hist_context=first_elements_string)   
        
    return  rag_context, hist_context
    
def generate_context(user_input, full_message_history,tail_prompt):
    # trim history if context > limit ==> todo !
    
    current_context=""
    nb_messages=len(full_message_history)
    i=0
    for m in full_message_history:
        i+=1
        # assistant_replay=format_prompt(response=m[0])
        assistant_replay=f"\nAssistant Replay : {m[0]} \n"
        if i == nb_messages:
            # command_replay=format_prompt(message=m[1]+tail_prompt)
            command_replay = f"\ncommand replay : {m[1]} \n"
        else:
            # command_replay=format_prompt(message=m[1])
            command_replay = f"\ncommand replay : {m[1]} \n"
            
        current_context+=f"\n{assistant_replay}\n{command_replay}\n"  
    return current_context

def trim_string_to_json_bounds(json_string: str) -> str:
    """
    Supprime tout ce qui est avant le premier '{' et après le dernier '}'
    dans la chaîne donnée.

    Args:
        json_string (str): La chaîne à traiter.

    Returns:
        str: La sous-chaîne entre le premier '{' et le dernier '}',
             # ou la chaîne originale si aucun '{' ou '}' n'est trouvé.
             chaine json vide
    """
    start_index = json_string.find('{')
    end_index = json_string.rfind('}')

    if start_index != -1 and end_index != -1:
        # +1 pour inclure le dernier '}' dans le résultat
        return json_string[start_index:end_index + 1]
    else:
        # Retourne la chaîne originale si aucun '{' ou '}' n'est trouvé
        #return json_string
        #print("Avant !!!")
        ret= {
              "command" :
               {'name': 'output', 
              "args" :  {
              'message' : json_string 
              }
             }
        }
        json_string = json.dumps(ret)
        return json_string
        
def chat_with_ai(
        main_prompt,
        user_input,
        system_prompt,
        tail_prompt,
        full_message_history):

    #if first call in the session construct main context/history

    #else add relative history   
    socketio = get_socketio()
    final_prompt=""
    try:
        # logger.debug(f"Token limit: {token_limit}")
        # if first call construct first context 
        if len(full_message_history) == 0:
            
            rag_context,hist_context = generate_first_context(user_input)
            
            main_prompt=format_prompt(message="\nuser query  : "+user_input+"\n"+rag_context+"\n"+hist_context+tail_prompt,system=system_prompt)
            #main_prompt=system_prompt+"\nuser query  : "+user_input+"\n"+rag_context+"\n"+hist_context
            final_prompt=main_prompt
            

        if len(full_message_history) != 0: 
            
            current_context= generate_context(user_input, full_message_history,tail_prompt)
            
            contexted_prompt=format_prompt(message=user_input+current_context)
            
            final_prompt=main_prompt+contexted_prompt
            
            
            
        write_log("000 =========================================================================================================")
        write_log(final_prompt)
        write_log("111 =========================================================================================================")

        print("===============>llm",final_prompt)
        # ===>  assistant_reply=llm(final_prompt+tail_prompt)
        assistant_reply=""
        for response_text in llmcgenerator(final_prompt, temperature=0, stream=True, raw=False):
            assistant_reply+=response_text
            socketio.emit('response_token', {'token': response_text})
        
        if assistant_reply == None:
            say_text(f"LLM {cfg.cfg.connect_llm} returned None ... exiting")
            print("===============>llm", assistant_reply)
            assistant_reply=""
        write_log(assistant_reply)
        write_log("222 =========================================================================================================")
        return final_prompt, assistant_reply
            
    except Exception as e:
        
        cfg.logger.debug(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        time.sleep(10)

def summhist(txt):

    prompt=f"summarize following dialog in question/response format, output only readable text :\n{txt}"
    write_log("summ hist dialog =========================================================================================================")
    ret=llmcraw(prompt)
    write_log(ret)
    return ret

