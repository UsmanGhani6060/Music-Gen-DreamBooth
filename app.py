from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
import torch
from transformers import AutoModelForTextToWaveform, AutoProcessor
import soundfile as sf
import os
import logging
from starlette.background import BackgroundTask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize FastAPI app
app = FastAPI()
logger = logging.getLogger("music-gen-aws")

# Define the device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load the model and processor
repo_id = "/home/hypersoft-gpu/hypersoft-projects/usman-projs/Dreambooth-Dep/musicgen-dreamboothing/musicgen-small"
model = AutoModelForTextToWaveform.from_pretrained(repo_id, torch_dtype=torch.float16).to(device)
processor = AutoProcessor.from_pretrained(repo_id)

# Path for saving the generated audio
audio_file_path = "generated_audio.wav"

def cleanup(file_path):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"{file_path} deleted from storage!")
    else:
        logger.warning("File path is None or does not exist, skipping cleanup.")
    # Clean up GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

@app.post("/generate_music")
async def generate_music(request: Request):
    data = await request.json()
    style = data['style'][0]  # Extract the style string from the list
    time = data['time'][0]    # Extract the time integer from the list

    # Determine the number of tokens based on the time
    token = {5: 256, 10: 512, 15: 768, 20: 1024, 30: 1536}.get(time, 500)

    try:
        # Process the input
        inputs = processor(text=[style], padding=True, return_tensors="pt").to(device)
        audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=token)
        
        # Convert audio values to WAV file
        sampling_rate = model.config.audio_encoder.sampling_rate
        audio_values = audio_values.cpu().float().numpy()
        sf.write(audio_file_path, audio_values[0].T, sampling_rate)
        
        # Check if the audio file was generated
        if not os.path.exists(audio_file_path):
            raise HTTPException(status_code=500, detail="Audio generation failed")

        return FileResponse(audio_file_path, media_type="audio/wav", filename="generated_audio.wav", background=BackgroundTask(cleanup, audio_file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
