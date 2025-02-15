# gpt-3.5-turbo /1M tokens
#                           IP       OP
#    gpt-3.5-turbo-0125    $0.50    $1.50
#    gpt-3.5-turbo-0125    $0.50    $1.50
#    gpt-3.5-turbo-1106    $1.00    $2.00
#    gpt-3.5-turbo-0613    $1.50    $2.00
#    gpt-3.5-0301          $1.50    $2.00

# "gpt-4o-mini"    $0.150    $0.600

# https://openai.com/api/pricing/

from openai import OpenAI
import os
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm
import json, time, os, sys

from evaluate import *
from plot import *


os.environ["OPENAI_API_KEY"] = "<YOUR_API_KEY>"
model_name = "gpt-3.5-turbo"    # "gpt-4o-mini"
shot, complexity = 100, 100


filenames = ["LinearOrderDec_50.json", "LinearOrderBin_50.json", "DIV_30.json"]
tasks = ["LO", "LO_BIN", "DIV"]
client = OpenAI()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(10))
def call_gpt(prompt, system_prompt, model_name=model_name):  # "gpt-3.5-turbo"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
        seed=0,
        # max_tokens=300,
        temperature=0.5,
    )
    return chat_completion.choices[0].message.content


def produce_response(model_name, Input, p):
    system_prompt = 'Answer in specified Format. Do not generate explanation.'
    send_back = call_gpt(Input, system_prompt, model_name) # ''
    if int(p.split('_')[1])%15 == 0:
        print(send_back)
    return send_back

    
def run():
    for filename, task in zip(filemames, tasks):
        st = time.time()
        with open(filename) as f:
            problems = json.load(f)
        st_m = time.time()
        for cnt, p in enumerate(problems['enumeration']):
            st_p = time.time()
            Instruction = 'Relation Description\n\n' + problems[p]['Relation Description']+ '\n\n\n'
            Examples = 'Examples\n\n' + '\n'.join(problems[p]['examples']) + '\n\n\n'
            Task = 'Task Description\n\n' + problems[p]['Task Description'] + '\nfollow the specified format for answering. \n\n\n'
            Tests = ''
            for t in problems[p]['test']:
                Tests= Tests + list(t.keys())[0] + '\n'
            Input = Instruction + Examples + Task + Tests

            if 'answer' not in problems[p].keys():
                problems[p]['answer'] = {}
            problems[p]['answer'][model_name] = produce_response(model_name, Input, p)
            sys.stdout.write("\r----Model: %s Performing: %s after (%0.2f)sec. \t Model Running: (%d)min \t Total Time: (%d)min or (%d)days-----"%(model_name, p, (time.time()-st_p), (time.time()-st_m)//60, (time.time()-st)//60, (time.time()-st)//86400))
            if int(p.split('_')[1])%5 == 0 or p == problems['enumeration'][-1]:
                with open("OP_/"+task+"/"+filename[:-5]+'_op'+'.json', 'w') as f:
                    json.dump(problems, f)
                with open("OP_/"+task+"/"+filename[:-5]+'_op'+'.ckpt', 'a') as f:
                    f.write(f"Model: %s Saved: %s after (%0.2f)sec. \t Model Running: (%d)min \t Total Time: (%.2f)min\n"%(model_name, p, (time.time()-st_p), (time.time()-st_m)//60, (time.time()-st)//60))
            time.sleep(0.02)
        evaluate_mismatch(model_name, task, filename)
        compare(shot, complexity, task, filename)
        showPlotsRow(shot, complexity, task, filename)
        showPlotsCol(shot, complexity, task, filename)
        print('\n'*3+"-"*20+task+' Completed'+'-'*20+'\n'*3)
        
    plot()
    print("Plots have been saved!!!!!")
    
run()
