"""
generate discharge handouts for the cases defined in test
evaluate by asking for human evaluation
"""

import os
import random
import json
import gradio as gr
from main import generate


def create_test_set(dir, write=False, dir_save=None):
    """generates the handouts from the patient cases in test_set"""
    print("generating handouts")
    test_set = {}
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            with open(os.path.join(dir,filename), 'r') as file:
                disease = filename.replace(".json","")
                data = json.load(file)
                assessment = data['assessment']
                plan = data['plan']
                print(f"Disease: {disease} \n", assessment,"\n", plan)
                test_set[disease] = generate(assessment, plan)

                if write:
                    with open(os.path.join(dir_save, f"{disease}.txt"), 'w') as file:
                        file.write(test_set[disease])

    print(f"total num of handout generated: {len(test_set)}")
    if write:
        print(f"generated handout saved at {dir_save}")

    return test_set



def write_test_case(dir):
    """write jason files"""
    while True:
        print([x for x in os.listdir(dir) if x.endswith(".json")])
        disease = input("Name of disease/condition/diagnosis: ").lower().replace(" ","_")
        assessment = input("Assessment: ")
        plan = input("Plan: ")
        filename = os.path.join(dir, f"{disease}.json")
        with open(filename, 'w') as file:
            json.dump({"assessment": assessment, "plan": plan}, file)


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


def save_test_results(results, dir):
    """save the results of the AB test"""
    print("saving results")
    filename = os.path.join(dir, 'results.json')
    with open(filename, 'w') as file:
        json.dump(results, file)


def render(generator, results):
    with gr.Blocks() as demo:
        gr.Markdown("""
            # Handout comparator 
            Please select the handout that you think is better.
        """)

        first_set = next(generator)
        disease = gr.State(value=first_set[0])

        left_llm = gr.State(value=random.random() < 0.5) # by default pos0 in the tuple generated by generator is llm handout
        if left_llm.value: # need to use .value to access the state
            left_text = first_set[1]
            right_text = first_set[2]
        else:
            left_text = first_set[2]
            right_text = first_set[1]


        with gr.Row():
            with gr.Column():
                textbox1 = gr.Text(label="Handout 1", value=left_text, lines=20)
            with gr.Column():
                textbox2 = gr.Text(label="Handout 2", value=right_text, lines=20)
        with gr.Row():
            radio_result = gr.Radio(label="Which handout is better?", choices=["Handout 1","Neutral", "Handout 2"])
        with gr.Row():
            btn_submit = gr.Button("Submit", variant="primary", interactive=False)


        def radio_callback(selected_value):
            """callback for radio button to show the submit button"""
            if selected_value is not None:
                return gr.Button("Submit", variant="primary", interactive=True)
            else:
                return gr.Button("Submit", variant="primary", interactive=False)


        def refresh_and_save(result, disease, left_llm):
            """callback function for submit button
                records the user input
                generates the next test pair
                randomize the display so llm handout can be on the left or right
                resets radio button
            """
            # process the input
            if result == "Neutral":
                results[disease] = (result)        
            else:
                if result == "Handout 1":
                    if left_llm:
                        results[disease] = "llm"
                    else:
                        results[disease] = "human"
                elif result == "Handout 2":
                    if left_llm:
                        results[disease] = "human"
                    else:
                        results[disease] = "llm"

            try:
                disease, hd1, hd2 = next(generator)
            except StopIteration:
                print(results)
                save_test_results(results, "./test_results")
                return None, "Test is finished. Thank you for participating. You can close this window now", "Test is finished. Thank you for participating. You can close this window now", None, None

            
            # randomize the display
            left_llm = random.random() < 0.5

            if left_llm:
                return disease, hd1, hd2, left_llm, None
            else:
                return disease, hd2, hd1, left_llm, None

            
        radio_result.change(radio_callback, inputs=[radio_result], outputs=btn_submit)
        btn_submit.click(refresh_and_save, inputs=[radio_result, disease, left_llm], outputs=[disease,textbox1,textbox2, left_llm, radio_result])

    return demo



def _AB_generator(ts):
    """generator that goes through the test set"""
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
    ts_llm = create_test_set("./test_set/cases")
    
    ts_hum = read_test_set("./test_set/human")
    ts = combine_test_sets(ts_llm, ts_hum)
    """

    #run_AB_test(ts)

    #write_test_case("./test_set/cases")

    #ts_llm = create_test_set("./test_set/cases", write=True, dir_save="./test_set/llm")
