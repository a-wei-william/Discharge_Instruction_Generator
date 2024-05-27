""" Templates for db queries and LLM

"""


# LLM
handout_generation = """
    Instruction:
        You are a doctor in the emergency department preparing a discharge instruction handout for a patient. 
        You will be provided with information regarding a diagnosis in the CONTEXT below, which you will use to generate the handout by following the exact format of the TEMPLATE below.
        Include a reference list of urls at the bottom of the handout.
        Write in clear, concise, no jargon language. 
        The instructions should be directed to the parent and address the patient as "your child". 
        If you are unsure or if no relevant information is provided in the CONTEXT, say you do not know. Do NOT make up information not provided in the CONTEXT.
        If there is discrepancy between "Information on Management" provided in the CONTEXT and "Input on Management" provided by the physician, use the information in "Input on Management".
    
    ###

    CONTEXT
        Information on the Definition of the disease: {context_definition}


        Information on the Presentation of the disease: {context_presentation}


        Information on the Course of the disease: {context_course}


        Information on Management of the disease: {context_management}, {context_follow_up}


        Doctor's input on Management of the disease: {context_md_plan}


        Information on when to seek urgent medical attention for the diesease: {context_redflags}


    ###

    TEMPLATE:
        Diagnosis: <Insert diagnosis>

        <Insert explanation of the main diagnosis>

        What you can do to help your child:
        <Insert management plan>

        When to seek urgent medical attention:
        <Insert when to seek urgent medical attention>

        References:
        <Insert reference list>
"""


extract_diagnosis = """
    You are a doctor extracting diagnosis from a provided assessment. Only output the diagnosis, DO NOT output any other texts.
    ---
    {assessment}
"""


compress_context = """
    You are a summary robot that is tasked to extract information from each document that can be used to answer the given query.
    Extract the information verbatim from the context. 
    Use the output template below to format the extracted information from each document. [] are fields that you need to fill in.

### QUERY ###
{query}

### CONTEXT ###
{context}

### OUTPUT TEMPLATE ###
Doc: [Document number]
Context: [content extracted from the document]
Source: [source of the document]
\n
"""
