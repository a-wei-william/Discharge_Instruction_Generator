""" Templates for db queries and LLM

"""


# LLM
discharge_instructions = """
    Instruction:
        You are a doctor in the emergency department preparing a discharge instruction handout for a patient. 
        You will be provided with information regarding a diagnosis in the Context below.
        Use the provided Context to fill in the Template below. 
        Include the source of the information at the end of the sentence. Include a reference list at the end of the document.
        Write in clear, concise, jargon-free style. The instructions should be directed to the parent and address the patient as "your child". 
        If you are unsure or if no relevant information was retrieved, just say you don't know. Don't make up information or hallucinate.
    ---
    Context:
        Information on the definition: {context_definition}


        Information on the presentation: {context_presentation}


        Information on the course: {context_course}


        Information on supportive management: {context_management_supportive}


        Information on treatment: {context_management_pharmacologic}


        Information on follow-up plan : {context_follow_up}


        Information on when to seek urgent medical attention : {context_redflags}


    ---
    Template:
        Diagnosis: <Insert diagnosis>

        <Insert explanation of the main diagnosis using information in Context>

        <Insert when to seek urgent medical attention using Information on when to seek urgent medical attention>

        <Insert reference list>
"""


discharge_instructions_2 = """
    Instruction:
        You are a doctor in the emergency department preparing a discharge instruction handout for a patient. 
        You will be provided with information regarding a diagnosis in the Context below, which you will use to generate the handout by filling in the Template below.
        Include a reference list of urls at the bottom of the handout.
        Write in clear, concise, no jargon language. 
        The instructions should be directed to the parent and address the patient as "your child". 
        If you are unsure or if no relevant information was retrieved, say you do not know. Do NOT make up information not provided in the Context.
        If there is discrepancy between "Information on Management" provided in the Context and "Input on Management" provided by the physician, use the information in "Input on Management".
    ---
    Context:
        Information on the Definition of the disease: {context_definition}


        Information on the Presentation of the disease: {context_presentation}


        Information on the Course of the disease: {context_course}


        Information on Management of the disease: {context_management}, {context_follow_up}


        Doctor's input on Management of the disease: {context_md_plan}


        Information on when to seek urgent medical attention for the diesease: {context_redflags}


    ---
    Template:
        Diagnosis: <Insert diagnosis>

        <Insert explanation of the main diagnosis using information in Context>

        <Insert management plan>

        <Insert when to seek urgent medical attention using Information on when to seek urgent medical attention>

        <Insert reference list>
"""


extract_diagnosis = """
    Extract the diagnosis from the given text below. Output should only include the diagnosis.
    ---
    Text: {assessment}
"""


compress_context = """
Task: Extract information that can be used to answer the given query from each of the documents in the given context.
Details:
- Extract the information verbatim from the context. 
- Use the output template below to format the extracted information from each document; [] are fields that you need to fill in.

### Query ###
{query}

### Context ###
{context}

### Output Template ###
Doc: [Document number]
Context: [content extracted from the documen]
Source: [source of the document]
\n
"""


# DB queries
"""
the template should include information on:
- definition of diagnosis
- how diagnosis presents
- the course of diagnosis
- management for diagnosis
    - supportive
    - pharmacologic
    - follow-up
- red flags to look out for
"""

queries_ddx = {
    "definition": "definition of {diagnosis}",
    "presentation": "manifestations of {diagnosis}",
    "course": "natural history of {diagnosis}",
    "management_supportive": "conservative treatment for {diagnosis}",
    "management_pharmacologic": "treatment for {diagnosis}",
    "follow_up": "follow-up plan for {diagnosis}",
    "redflags": "signs and symptoms that indicate the need for urgent medical attention for patients with {diagnosis}",
}
