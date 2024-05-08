"""main application"""

import gradio as gr
from operator import itemgetter
from _global import path_to_resources, hf_embed
from templates import discharge_instructions, discharge_instructions_2, queries_ddx, extract_diagnosis, compress_context
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# set up LLM
llm_gpt = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0)
llm_llama = Ollama(model="llama2:13b", temperature=0)

# set up db
db = Chroma(collection_name="main_collection", persist_directory=f"{path_to_resources}/db_wiki", embedding_function=hf_embed)
retriever = db.as_retriever(
                search_type = "similarity",
                search_kwargs = {"k":4},
            )

# compress context
prompt_compress = PromptTemplate.from_template(compress_context)
compressor =  prompt_compress | llm_llama | StrOutputParser()

# set up prompts
prompt_extract_diagnosis = PromptTemplate.from_template(extract_diagnosis)
prompt_main = ChatPromptTemplate.from_messages([("system",discharge_instructions_2)])


# set up parallel chain components
#chain_extract_diagnosis = prompt_extract_diagnosis | llm_gpt

fill_queries = RunnableParallel( # fill in queries with the diagnosis 
    query_definition = lambda x: queries_ddx["definition"].format(diagnosis=x["diagnosis"]),
    query_presentation = lambda x: queries_ddx["presentation"].format(diagnosis=x["diagnosis"]),
    query_course = lambda x: queries_ddx["course"].format(diagnosis=x["diagnosis"]),
    query_management = lambda x: queries_ddx["management_supportive"].format(diagnosis=x["diagnosis"]),
    query_follow_up = lambda x: queries_ddx["follow_up"].format(diagnosis=x["diagnosis"]),
    query_redflags = lambda x: queries_ddx["redflags"].format(diagnosis=x["diagnosis"]),
    md_plan = itemgetter("md_plan"),    
)


get_cotext = {
    "definition": {"context": itemgetter("query_definition") | retriever, "query": RunnablePassthrough()} | compressor,
    "presentation": {"context": itemgetter("query_presentation") | retriever, "query": RunnablePassthrough()} | compressor,
    "course": {"context": itemgetter("query_course") | retriever, "query": RunnablePassthrough()} | compressor,
    "management": {"context": itemgetter("query_management") | retriever, "query": RunnablePassthrough()} | compressor,
    "follow_up": {"context": itemgetter("query_follow_up") | retriever, "query": RunnablePassthrough()} | compressor,
    "redflags": {"context": itemgetter("query_redflags") | retriever, "query": RunnablePassthrough()} | compressor,
}


# main chain
main_chain = (
    {
        "diagnosis": itemgetter("assessment"), #RunnablePassthrough() | chain_extract_diagnosis,
        "md_plan": itemgetter("md_plan"),
    }
    | fill_queries
    | {
        "context_definition": get_cotext["definition"],
        "context_presentation": get_cotext["presentation"],
        "context_course": get_cotext["course"],
        "context_management": get_cotext["management"],
        "context_follow_up": get_cotext["follow_up"],
        "context_redflags": get_cotext["redflags"],
        "context_md_plan": itemgetter("md_plan"),
    }
    | prompt_main
    | llm_gpt
    | StrOutputParser()
)


def generate(assessment, plan):
    return main_chain.invoke({"assessment": assessment, "md_plan": plan})


    

if __name__ == "__main__":
    # UI
    eg_assessment = """\
    5 yo M, first asthma exacerbation. 
    """
    eg_plan = """\
    - continue q4h ventolin for the next 48hr then prn
    - continue flovent 125mcg qdaily
    - follow-up with family doctor if not improved by 2 days
    """


    with gr.Blocks() as demo:
        gr.Markdown("""
            # Discharge Instruction Generator
            This is a demo for the discharge instruction generator. 
            Please input your assessment and plan of the patient in the corresponding boxes. 
        """)
        with gr.Row():
            with gr.Column():
                assessment = gr.Text(label="Assessment/Impression", lines=10,
                                     value=eg_assessment)
                plan = gr.Text(label="Plan", lines=10, 
                               value=eg_plan)
                btn_gen = gr.Button("Generate", variant="primary")
            with gr.Column():
                output = gr.Text(label="Generated Discharge Instructions", lines=20)
        
        btn_gen.click(generate, inputs=[assessment, plan], outputs=[output])
    
    demo.launch(inbrowser=True)

    """    import time
        start_time = time.time()

        result = main_chain.invoke({
            "assessment": "5 yo M, first asthma exacerbation of the year likely secondary to a viral infection, responded well to asthma protocol, now stable in room air on q4h venolin. Reduced fluid intake due to sore throat (likely viral pharyngitis) but euvolemic on exam and no signs of bacterial infection of the throat.",
            "md_plan":"continue q4h ventolin for the next 24hours. follow-up with your family doctor in the next few days."
        })

        end_time = time.time()
        print("Time taken: ", end_time - start_time)

        print(result)
    """