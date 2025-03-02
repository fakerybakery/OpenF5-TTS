# OpenF5 TTS (WIP)

A retrain of F5-TTS on permissively-licensed data to create a freely-licensed TTS model.

**The model is still undergoing training. Intermediate checkpoints are available on [Hugging Face](https://huggingface.co/mrfakename/OpenF5-Intermediate) - but the model is not ready yet.**

## Model

Trained using F5-TTS Small configuration. The official F5-TTS model is trained using the Base configuration which is larger.

## Training Data

Trained on Emilia-YODAS (CC-BY licensed). Trained using the F5-TTS framework on ~100K hours of speech.

## Usage

```
pip install f5-tts
huggingface-cli download mrfakename/OpenF5-Intermediate --local-dir openf5
f5-tts_infer-cli -mc openf5/model_config.yaml -p openf5/model_last.pt  -v openf5/vocab.txt
```

## License

Scripts are licensed under MIT. Model is licensed under CC-BY 4.0 - you can use it commercially.
