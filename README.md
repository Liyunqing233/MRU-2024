# MRU-ASTP

## Acknowledgments

**Our code utilizes the framework from the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory). We extend our gratitude to the contributors of this project. Additionally, we declare that the code we use adheres to the original project's copyright and licensing agreements.**

## Getting Started

### Installation

```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

### Using llama3-8b-instruct
Download the model file to the same directory as the llama factory.
https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

### About Dataset
We provide all data in our experiments in the directory "data/" about ASQP, ASTE, ACOS, TASD. You can just copy them into the "LLaMA-Factory/data"
### Quickstart

To run MRU-ASTP with the LLaMA-Factory framework, follow these steps:

1. **Update `LLaMA-Factory/data/dataset_info.json`**: Add dataset information for MRU to the  file. Ensure the format and details are consistent with existing entries . You can use our file(data_config/dataset_info.json)

2. **Add YAML Files**: Add the YAML files to this directory (LLaMA-Factory/examples/lora_multi_gpu/) . Ensure the paths and dataset names in the YAML files match the entries in `LLaMA-Factory/data/dataset_info.json`.
Here we provide some yaml files about multi-task, single-task, low-resource setting in the directory (scripts/)

#### Fine-tuning
First step into LLaMA-Factory dictory.
```bash
llamafactory-cli train examples/train_lora/qwen7b_lora_sft.yaml
```

#### Prediction

```bash
llamafactory-cli train examples/train_lora/qwen7b_lora_predict.yaml
```

#### Evaluation
First set your prediction file(.jsonl) address in the evaluate/evaluate_group_plus.py
Than use the evaluate/evaluate_group_plus.py script. 

```bash
python evaluate/evaluate_group_plus.py  
```

