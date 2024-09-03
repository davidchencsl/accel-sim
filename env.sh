export CUDA_INSTALL_PATH=/usr/local/cuda
export NVBIT_TRACER_TOOL=/home/davidchencsl/code/accel-sim/util/tracer_nvbit/tracer_tool/tracer_tool.so

cd gpu-simulator
source setup_environment.sh
cd gpgpu-sim
source setup_environment
cd ../../

#LD_PRELOAD=/home/davidchencsl/code/accel-sim/util/tracer_nvbit/tracer_tool/tracer_tool.so ./llama-cli -m /home/davidchencsl/.cache/llama.cpp/Meta-Llama-3-8B-Instruct-Q8_0.gguf -p "The meaning of life is" -n 128