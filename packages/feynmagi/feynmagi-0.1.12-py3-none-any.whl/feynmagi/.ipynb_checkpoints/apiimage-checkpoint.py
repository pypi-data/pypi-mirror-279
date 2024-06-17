###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################
import sys
from pathlib import Path

# Assuming your Jupyter notebook or interactive shell is running in the 'current' directory
# And you want to add '../dir/pythonpackage' to sys.path

# Get the current working directory (where your notebook or interactive session is running)
current_dir = Path.cwd()

# Construct the path to the directory you want to add (the parent of 'dir')
# Adjust the path as necessary based on your actual directory structure
parent_dir = current_dir.parent.parent / 'moondream'

# Convert the parent directory path to a string and add it to sys.path
sys.path.append(str(parent_dir))

from moondream import Moondream, detect_device
import torch
from PIL import Image
from transformers import (
    TextIteratorStreamer,
    CodeGenTokenizerFast as Tokenizer,
)
import re
from flask import Flask, request, jsonify

def detect_device():
    """
    Detects the appropriate device to run on, and return the device and dtype.
    """
    if torch.cuda.is_available():
        return torch.device("cuda"), torch.float16
    elif torch.backends.mps.is_available():
        return torch.device("mps"), torch.float16
    else:
        return torch.device("cpu"), torch.float32
device, dtype = detect_device()

model_id = "vikhyatk/moondream1"
tokenizer = Tokenizer.from_pretrained(model_id)
moondream = Moondream.from_pretrained(model_id).to(device=device, dtype=dtype)
moondream.eval()

def inference(image_path,prompt):
    image = Image.open(image_path)
    image_embeds = moondream.encode_image(image)
    answer = moondream.answer_question(image_embeds, prompt, tokenizer)
    return answer

app = Flask(__name__)


@app.route('/question', methods=['POST'])
def question_image():
    if not request.is_json:
        app.logger.debug('Missing JSON in request')
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    if 'image_path' not in data or 'question' not in data:
        print('Missing data in request: {}'.format(data))
        app.logger.debug('Missing data in request: {}'.format(data))
        return jsonify({"error": "Missing data in request"}), 400

    image_path = data['image_path']
    question = data['question']

    answer = inference(image_path, question)
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False,port=8890)

