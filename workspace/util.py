import os
import shutil
import subprocess
from glob import glob

import parse


def parse_stat(benchmark, config):
    cur_path = os.getcwd()
    os.chdir(f"/home/davidchencsl/code/accel-sim")
    env = {}
    proc = subprocess.Popen(['bash', '-c', 'source env.sh > /dev/null && env'],stdout = subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode('utf-8').partition("=")
        env[key] = value.strip()
    proc.communicate()
    cmd = f"/home/davidchencsl/miniconda3/envs/gem5/bin/python ./util/job_launching/get_stats.py -B {benchmark} -C {config} > tmp.stats.csv"
    proc = subprocess.Popen(cmd, shell=True, text=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    stat = parse_stat_csv("./tmp.stats.csv")

    # DRAM stats
    log_file = glob(f"sim_run_11.5/{benchmark}/*/{config}/*.o1")[0]
    dram_utils = []
    with open(log_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            s = parse.search('bwutil = {:f}', line)
            if s:
                dram_utils.append(s[0])
    stat['dram_util'] = sum(dram_utils) / len(dram_utils)
    os.chdir(cur_path)
    return stat

def parse_stat_csv(stat_file):
    stat = {}
    with open(stat_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('-'):
                key = lines[i+1].split(',')[0].strip()
                value = lines[i+3].split(',')[1].strip()
                stat[key] = value
    return stat

def run_experiment(benchmark, trace_file, name, params, extra_args=''):
    cur_path = os.getcwd()
    os.chdir(f"/home/davidchencsl/code/accel-sim")
    env = {}
    proc = subprocess.Popen(['bash', '-c', 'source env.sh > /dev/null && env'],stdout = subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode('utf-8').partition("=")
        env[key] = value.strip()
    proc.communicate()
    
    generate_config(name.split('-')[0], params)

    cmd = f"/home/davidchencsl/miniconda3/envs/gem5/bin/python ./util/job_launching/run_simulations.py -B {benchmark} -C {name} -T {trace_file} -N {name} {extra_args}"
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True, text=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir(cur_path)
    return proc 

def generate_config(name, params):
    TEMPLATE_CONFIG_DIR = '/home/davidchencsl/code/accel-sim/gpu-simulator/gpgpu-sim/configs/tested-cfgs/GPU_template/'
    CONFIG_DIR = f'/home/davidchencsl/code/accel-sim/gpu-simulator/gpgpu-sim/configs/tested-cfgs/{name}/'
    TEMPLATE_GPUSIM_CONFIG_DIR = f'/home/davidchencsl/code/accel-sim/gpu-simulator/configs/tested-cfgs/GPU_template/'
    GPUSIM_CONFIG_DIR = f'/home/davidchencsl/code/accel-sim/gpu-simulator/configs/tested-cfgs/{name}/'
    YAML_CONFIG = '/home/davidchencsl/code/accel-sim/util/job_launching/configs/define-wsm-cfgs.yml'
    if os.path.exists(CONFIG_DIR):
        shutil.rmtree(CONFIG_DIR)
    os.mkdir(CONFIG_DIR)

    with open(TEMPLATE_CONFIG_DIR + 'gpgpusim.config', 'r') as f:
        content = f.read()
    with open(CONFIG_DIR + 'gpgpusim.config', 'w') as f:
        for key, value in params.items():
            if f'${key}' in content:
                content = content.replace(f'${key}', str(value))
        f.write(content)
    
    with open(TEMPLATE_CONFIG_DIR + 'config_ampere_islip.icnt', 'r') as f:
        content = f.read()
    with open(CONFIG_DIR + 'config_ampere_islip.icnt', 'w') as f:
        for key, value in params.items():
            if f'${key}' in content:
                content = content.replace(f'${key}', str(value))
        f.write(content)
    
    if os.path.exists(GPUSIM_CONFIG_DIR):
        shutil.rmtree(GPUSIM_CONFIG_DIR)
    os.mkdir(GPUSIM_CONFIG_DIR)
    shutil.copy(TEMPLATE_GPUSIM_CONFIG_DIR + 'trace.config', GPUSIM_CONFIG_DIR + 'trace.config')
    
    with open(YAML_CONFIG, 'a+') as f:
        f.write(f'\n{name}:\n')
        f.write(f'    base_file: "$GPGPUSIM_ROOT/configs/tested-cfgs/{name}/gpgpusim.config"')
