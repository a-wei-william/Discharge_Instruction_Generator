"""
generate discharge handouts for the cases defined in test
evaluate by asking for human evaluation
"""

import os
import gradio as gr


def create_test_set(dir):
    """generates the handouts from the patient cases in test_set"""
    print("generating handouts")
    test_set = {}
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            with open(os.path.join(dir,filename), 'r') as file:
                data = json.load(file)
                assessment = data['assessment']
                plan = data['plan']
                test_set[filename.replace(".txt","")] = generate(assessment, plan)

    print(f"total num of handout generated: {len(test_set)}")

    return test_set


def write_test_set(test_set, dir):
    """save the generated handouts"""
    print("saving generated handouts")
    for k,v in test_set.items():
        filename = f"{k}.txt"
        with open(os.path.join(dir,filename), 'w') as file:
            file.write(v)

def read_test_set(dir):
    """read generated handouts; both ml and human generated"""
    print("reading handouts")
    test_set = {}
    for filename in os.listdir(dir):
        if filename.endswith('.txt'):
            with open(os.path.join(dir,filename), 'r') as file:
                test_set[filename.replace(".txt","")] = file.read()
    
    print(f"total num of handout read: {len(test_set)}")
    
    return test_set


def combine_test_sets(llm, human):
    """combine the generated handouts from both ml and human"""
    print("combining handouts")
    test_set = {}
    for k,v in llm.items():
        test_set[k] = (v, human[k])
        
    return test_set



def render(generator, results):
    with gr.Blocks() as demo:
        gr.Markdown("""
            # Handout comparator 
        """)
        disease = gr.State()
        with gr.Row():
            with gr.Column():
                textbox1 = gr.Text(label="Handout 1", value="placeholder", lines=20)
            with gr.Column():
                textbox2 = gr.Text(label="Handout 2", value="placeholder", lines=20)
        with gr.Row():
            result = gr.Radio(label="Which handout is better?", choices=["Handout 1","Neutral", "Handout 2"])
        with gr.Row():
            submit = gr.Button("Submit")

        def refresh_and_save(result, disease):
            results[disease] = (result)        
            try:
                next_pair = next(generator)
            except StopIteration:
                print(results)
                return "No more handouts", "please exit", "please exit" 
            
            return next_pair

        submit.click(refresh_and_save, inputs=[result, disease], outputs=[disease,textbox1,textbox2])

    return demo

def _AB_generator(ts):
    for disease, handouts in ts.items():
        yield (disease, handouts[0], handouts[1])


def run_AB_test(ts):
    """run comparison between llm and human generated handout"""
    AB_generator = _AB_generator(ts)
    results = {} # dict of disease: superior handout
    demo = render(AB_generator, results)

    demo.launch(inbrowser=True)



if __name__ == '__main__':
    """
    ts_llm = create_test_set("./test_set/pt")
    write_test_set(ts, "./test_set/llm")
    ts_hum = read_test_set("./test_set/human")
    ts = combine_test_sets(ts_llm, ts_hum)
    """


    ts = {
        "asthma" : ("human generated handout", "llm generated handout"),
        "covid" : ("human generated handout", "llm generated handout"),
        "diabetes" : ("human generated handout", "llm generated handout"),
        "hypertension" : ("human generated handout", "llm generated handout"),
        "pneumonia" : ("human generated handout", "llm generated handout"),
    }


    run_AB_test(ts)


