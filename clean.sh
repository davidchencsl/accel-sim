rm -rf /home/davidchencsl/code/accel-sim/sim_run_11.0
rm -rf /home/davidchencsl/code/accel-sim/sim_run_11.5
rm -rf /home/davidchencsl/code/accel-sim/util/job_launching/logfiles
rm -rf /home/davidchencsl/code/accel-sim/util/job_launching/procman
rm -rf /home/davidchencsl/code/accel-sim/util/job_launching/job*.txt

rm -rf /home/davidchencsl/code/accel-sim/gpu-simulator/configs/tested-cfgs/ece511*
rm -rf /home/davidchencsl/code/accel-sim/gpu-simulator/gpgpu-sim/configs/tested-cfgs/ece511*

pkill accel-sim.out
pkill procman.py