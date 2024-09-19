import pandas as pd
from util import *
import itertools

# benchmarks = ['ece511-polybench']
# traces = ['./hw_run/polybench/11.0']
# n_mems = [32,64,128,256]

benchmarks = ['llama3-8b-d1']
traces = ['./hw_run/llm-inference/11.5']
n_mems = [32]

processes = []
for b, t, n_mem in itertools.product(benchmarks, traces, n_mems):
    name = f"{b.replace('-', '_')}_nmem={n_mem}-SASS"
    print(f'Running {name}')
    params = {
        'k': n_mem + 108,
        'gpgpu_n_mem': n_mem,
    }
    proc = run_experiment(b, t, name, params)
    processes.append(proc)
    out, err = proc.communicate()
    print(out)
    print(err)




# for p in processes:
#     out, err = p.communicate()
#     print(out)
#     print(err)
