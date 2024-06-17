###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################
from flask import Flask, request, jsonify
import librosa
import numpy as np
# from faster_whisper import WhisperModel

import librosa
import soundfile as sf

from transformers import WhisperProcessor, WhisperForConditionalGeneration
# from datasets import load_dataset

#from faster_whisper import WhisperModel

#model_size = "large-v3"

# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8



def resample_audio(input_path, output_path, new_sample_rate=16000):
    # Charger l'audio avec le taux d'échantillonnage d'origine
    audio, sr = librosa.load(input_path, sr=None)
    
    # Rééchantillonner l'audio au nouveau taux d'échantillonnage
    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=new_sample_rate)
    
    # Sauvegarder l'audio rééchantillonné dans un nouveau fichier
    # sf.write(output_path, audio_resampled, new_sample_rate)
    return audio_resampled


# Initialize your model here (adjust according to your specific setup)
# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
model.config.forced_decoder_ids = None
model=model.to("cuda")

import torch  # Assurez-vous d'importer torch

def inference(sample):
    # Réduction de la consommation de mémoire en évitant le calcul du gradient
    
    with torch.no_grad():
        input_features = processor(sample, sampling_rate=16000, return_tensors="pt").input_features
        input_features = input_features.to("cuda")
        predicted_ids = model.generate(input_features)
        # Déplacer les prédictions en mémoire CPU
        predicted_ids = predicted_ids.cpu()
    
    # Conversion des IDs prédits en texte
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    # Libération explicite de la mémoire CUDA n'est généralement pas nécessaire ici
    torch.cuda.empty_cache()  # Utilisez avec prudence; peut affecter les performances

    return {'result': transcription}
    '''
    segments, info = model.transcribe(sample, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    '''

app = Flask(__name__)


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if request.data:
        # Decode the audio file
        audio_data = np.frombuffer(request.data, dtype=np.int16) 
        # Perform inference
        transcription = inference(audio_data)
        print("===========> inference OK",transcription)
        # Return the transcription result
        return jsonify({"transcription": transcription})
    else:
        return jsonify({"error": "No audio data received."}), 400



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False,port=8889)
