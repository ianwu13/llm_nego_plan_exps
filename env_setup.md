### Create Conda Environment
```
conda create -n llm_exps python=3 anaconda
```

### Install Requirements
```
conda activate llm_exps
pip3 install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
