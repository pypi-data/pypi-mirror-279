
<h1 align="left">
    STaRK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases
</h1>

<div align="left">


**Dataset website:** [STaRK Website](https://stark.stanford.edu/)


## What is STaRK?
STaRK is a large-scale semi-structure retrieval benchmark on Textual and Relational Knowledge Bases. Given a user query, the task is to extract nodes from the knowledge base that are relevant to the query. 


## Why STaRK?
- **Novel Task**: Recently, large language models have demonstrated significant potential on information retrieval tasks. Nevertheless, it remains an open
question how effectively LLMs can handle the complex interplay between textual and relational
requirements in queries.

- **Large-scale and Diverse KBs**: We provide three large-scale knowledge bases across three areas, which are constructed from public sources.

- **Natural-sounding and Practical Queries**: The queries in our benchmark are crafted to incorporate rich relational information and complex textual properties, and closely mirror questions in real-life scenarios, e.g., with flexible query formats and possibly with extra contexts.


# Access benchmark data

## 1) Package installation
```bash
pip install stark_qa
```

## 2) Data loading 

```python
from stark_qa import load_qa, load_skb

dataset_name = 'amazon'

# Load the retrieval dataset
qa_dataset = load_qa(dataset_name)
idx_split = qa_dataset.get_idx_split()

# Load the semi-structured knowledge base
skb = load_skb(dataset_name, download_processed=True, root=None)
```
The root argument for load_skb specifies the location to store SKB data. With default value `None`, the data will be stored in [huggingface cache](https://huggingface.co/docs/datasets/en/cache).

### Data of the Retrieval Task

Question answer pairs for the retrieval task will be automatically downloaded in `data/{dataset}/stark_qa` by default. We provided official split in `data/{dataset}/split`.

### Data of the Knowledge Bases

There are two ways to load the knowledge base data:
- (Recommended) Instant downloading: The knowledge base data of all three benchmark will be **automatically** downloaded and loaded when setting `download_processed=True`. 
- Process data from raw: We also provided all of our preprocessing code for transparency. Therefore, you can process the raw data from scratch via setting `download_processed=False`. In this case, STaRK-PrimeKG takes around 5 minutes to download and load the processed data. STaRK-Amazon and STaRK-MAG may takes around an hour to process from the raw data.

## 3) LLM API usage

### Specify under config/ directory
Please specify API keys at `config/openai_api_key.txt` for openai models or `config/claude_api_key.txt` for Claude models.
### Specify in command line
```
ANTHROPIC_API_KEY=YOUR_API_KEY
```
or
```
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_ORG=YOUR_ORGANIZATION
```

## 4) More usage
Please refer to the [documentation](https://stark.stanford.edu/doc.html) for more details.