import ollama
import json, time, os, sys
 
models = ["gemma2", "llama3", "mathstral"]

filename = 'LinearOrderDec_50.json'
if not os.path.exists('OP'):
    os.makedirs('OP')

def produce_response(model_name, Input, p):
    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': Input}], stream=True, options={'seed':0, 'temperature':0.5, 'raw': True})
        # response = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": Input}], stream=True)
    send_back = ''
    for chunk in response:
        if int(p.split('_')[1])%15 == 0:
            print(chunk['message']['content'], end='', flush=True)
        send_back += chunk['message']['content']
    return send_back
    
def infer():
    st = time.time()
    with open(filename) as f:
        problems = json.load(f)
    for model_name in models:
        st_m = time.time()
        for cnt, p in enumerate(problems['enumeration']):
            st_p = time.time()
            Instruction = 'Relation Description\n\n' + problems[p]['Relation Description']+ '\n\n\n'
            Examples = 'Examples\n\n' + '\n'.join(problems[p]['examples']) + '\n\n\n'
            Task = 'Task Description\n\n' + problems[p]['Task Description'] + '\nfollow the specified format for answering. \n\n\n'
            Tests = ''
            for t in problems[p]['test']:
                Tests= Tests + list(t.keys())[0] + '\n'
                # print(t)
            # print('-'*20)
            Input = Instruction + Examples + Task + Tests

            if 'answer' not in problems[p].keys():
                problems[p]['answer'] = {}
            problems[p]['answer'][model_name] = produce_response(model_name, Input, p)
            # print('\n'+ '=='*20 + 'Was performing: ' + model_name + " ___ " + p  + '=='*20)
            sys.stdout.write("\r----Model: %s Performing: %s after (%0.2f)sec. \t Model Running: (%d)min \t Total Time: (%d)min or (%d)days-----"%(model_name, p, (time.time()-st_p), (time.time()-st_m)//60, (time.time()-st)//60, (time.time()-st)//86400))
            if int(p.split('_')[1])%25 == 0 or p == problems['enumeration'][-1]:
                with open('OP/'+filename[:-5]+'_op'+'.json', 'w') as f:
                    json.dump(problems, f)
                with open('OP/'+filename[:-5]+'_op'+'.ckpt', 'a') as f:
                    f.write(f"Model: %s Saved: %s after (%0.2f)sec. \t Model Running: (%d)min \t Total Time: (%.2f)min\n"%(model_name, p, (time.time()-st_p), (time.time()-st_m)//60, (time.time()-st)//60))
            time.sleep(0.2)