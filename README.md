# ED Discharge Instruction Generator

## Aim
- The aim of this project is to create a retrieval augmented generation (RAG) discharge instruction generator.

## Motivation
- After a patient is seen in the emergency department and is deemed medically safe to be discharged, the standard practice is to counsel the patient and family regarding instructions to follow at home, and to provide a written summary of the discharge instructions. Although there are pre-generated templates (i.e., auto-text) available on the EMR, the list of templates is not exhaustive, and oftentimes, not tailored to the patient being discharged.
- As a result, for somewhat common diseases where template discharge instructions are not available, physicians need to manually type out the discharge instructions. For diseases with available templates on EMR, physicians are still required to manually modify the template according to the patient's situation. This leads to time wasted on writing/modifying discharge instructions and increases the risk of errors being made.
- The current state-of-the-art large language models (LLMs) may be able to generate reasonable and safe discharge instructions given the impression and plan of the patient. However, LLMs are susceptible to hallucinations, and without knowing where the LLMs derive the content from, there may be a lack of trust from adoption by physicians and patients/families.

## Solution
- An application that generates discharge instructions for patients and families based on the patient's diagnosis and physician's management plan. The information will be derived from up-to-date trusted healthcare information sources. In addition, the generated discharge instructions are not dependent on pre-generated templates and will be tailored to the individual patient. 
- The aim is to reduce the amount of time physician spend on writing/editing of discharge instructions. Physicians will only have to proofread the discharge instruction before printing it.

## Data Sources
- Openly available trusted healthcare information sources on the internet 

## Blueprint
- Data parsers that clean and transform raw information into chunks that can be embedded and stored in the vector database
- Vector database: custom-built vector database (chroma) using information from trusted healthcare information sources
- Inputs: De-identified information on the assessment and plan of the patient
- Prompt templates: 
    - for diagnosis extraction from the assessment statement provided
    - for discharge instruction generation
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
