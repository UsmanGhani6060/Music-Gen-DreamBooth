# Music-Gen-DreamBooth

* Meta's music generation module's FAST-API implementation for Music Gen DreamBooth method.


## Installation

For installing, follow these instructions

#### Cloning the Main Repository :
```
git clone -b main https://github.com/UsmanGhani6060/Music-Gen-DreamBooth.git
```

#### Navigate to Main Repository :
```
cd musicgen-dreamboothing
```

#### Creating Virtual Enviromrnt :
```
pip install virtualenv
python3.9 -m venv music-gen-dreambooth
source music-gen-dreambooth/bin/activate
```
#### Installing requirements and dependencies:
```
pip install -e .
pip install -U git+https://github.com/huggingface/transformers
pip install demucs
pip install fastapi[all]
pip install uvicorn

###download the models(there are two models)
# model drive link
Model_1
"https://drive.google.com/file/d/154q7mQ6XZQgqNjUy0pheIiLVE3Qhl46O/view?usp=sharing"

Model_2
"https://drive.google.com/file/d/1X76rfpFhArujXNx6j0b3WJhmpli0baQ5/view?usp=sharing"
```
## Run


1. go to the inf.py file
2. change "repo_id" path to the one of downloaded model into the folder of musicgen-dreamboothing
3. change text if you want to (by default it is "indian traditional music")
4. run the inf.py file.
5. resulting audio file named "musicgen.wav" will be saved in the folder musicgen-dreamboothing.