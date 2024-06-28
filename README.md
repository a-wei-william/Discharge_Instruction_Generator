# ED Discharge Instruction Generator

## Aim
- The aim of this project is to create a discharge instruction/handout generator that utilizes retrieval augmented generation (RAG) to improve information accuracy.

## Problem Statement
- After a patient is deemed medically safe to be discharged from the emergency department, the standard of care involves counseling the patient and their family on discharge instructions and providing a written summary. While electronic medical records offer pre-generated templates, these templates are often not exhaustive and may not be tailored to the patient's circumstances.
- For common conditions without available templates, physicians must manually type discharge instructions. Even when templates are available, physicians often need to modify them to suit the patient's situation. This process is time-consuming and increases the risk of errors.
- Current large language models (LLMs) can generate reasonable and safe discharge instructions based on the patient's condition. However, LLMs can produce hallucinations, leading to potential mistrust from physicians and patients due to the lack of transparency in content generation.

## Solution
- An application that generates personalized discharge instructions based on the patient's individaul clinical scenario, using information from up-to-date and trusted healthcare sources. 
- This approach eliminates dependency on pre-generated templates and tailors instructions to individual patients, aiming to reduce the time physicians spend writing or editing discharge instructions. Physicians will only need to proofread the generated instructions before printing.

## Data Sources
- Openly available, trusted healthcare information sources on the internet 

## Blueprint
- Data parsers: clean and transform raw information into chunks that can be embedded and stored in the vector database
- Vector database: custom-built Chroma database using information from trusted healthcare information sources
- Inputs: De-identified information on the assessment and plan of the patient
- Prompt templates: 
    - Diagnosis extraction from the assessment statement provided
    - Discharge instruction generation
- Embedding: BAAI/llm-embedder
- LLM: 
    - OpenAI-GPT3.5: for context compression and handout generation
    - (in progess) to test with OpenAI-GPT4
- Framework: 
    - LangChain: for prototyping the application
    - LangSmith: for evaluation 
- UI: Gradio

## Workflow

![scehmatic](schematic.png)

## Demo

![demo img](demo.png)
