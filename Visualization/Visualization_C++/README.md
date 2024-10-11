
# Advanced Processor Debugging Tool

## Overview
The project consists of two main parts:

1. The first part provides efficient log filtering logic for a Python project that visually and user-friendly displays a specific workflow on the chip. This part is exported using the pybind11 library. More details can be found in the project's README file at this link: [GitHub README](https://github.com/KamaTechOrg/NextUtils/blob/main/Visualization/Visualization_Python/README.md).

2. The second part is a command-line interface (CLI) tool that allows log data analysis before displaying it in the simulator. This tool enables highly efficient execution using multi-threads and also offers improved performance by processing on the GPU using Intel oneAPI SYCL with an enhancement of around 97.5%. This project utilizes Intel oneAPI Threading Building Blocks (TBB) to optimize GPU utilization in the CLI section. Intel TBB provides a high-level interface for parallelism, making it easier to efficiently use the GPU in the project.

Moreover, the project incorporates advanced design patterns like the Decorator pattern to provide flexible and extensible functionality. It also enhances response times by leveraging modern C++ features such as coroutines and generators, ensuring smooth and efficient data processing.

# Project Setup and Installation Instructions

## Step 1: Installation

### Option 1:
For a significant **performance boost** of around 97.5%, it's highly recommended to use Intel's oneAPI. To run the project with this performance enhancement, install the Intel oneAPI Base Toolkit:
- [Intel oneAPI Base Toolkit](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html)
  
After installation, set the following environment variables to configure your environment properly:

```bash
setx PATH "%PATH%;C:\Program Files (x86)\Intel\oneAPI\tbb\latest\bin"
setx PATH "%PATH%;C:\Program Files (x86)\Intel\oneAPI\compiler\latest\bin"
```
### Option 2:
If you are not using oneAPI, ensure that **G++** is installed on your machine.

## Step 2: Generating the Executable (EXE)

### Windows:

### Option 1: Download Pre-built EXE Files
If you prefer to run the project without building it, you can download pre-built EXE files. Two EXE files are available under the `DIST` directory in the project's root folder:

- **LogsProcessorOnGPU.exe**: Runs with GPU acceleration.
- **LogsProcessor.exe**: Runs without GPU acceleration.

### Option 2: Compile and Build the EXE File
To build the project, download the source code and use one of the batch files located in the `BUILD` directory:

- **For GPU execution using oneAPI**: Run `buildWithOneAPI.bat`.
- **For CPU-only execution**: Run `build.bat`.

The EXE will be generated in the `RELEASE` directory. Add this path to your environment variables to execute the EXE from any location.

### Linux:

### Option 1: Download Pre-built EXE Files
If you prefer to run the project without building it, you can download pre-built EXE files. Two EXE files are available under the `DIST` directory in the project's root folder:

- **LogsProcessorOnGPU**: Runs with GPU acceleration.
- **LogsProcessor**: Runs without GPU acceleration.

### Option 2: Compile and Build the EXE File
To build the project, download the source code and use one of the batch files located in the `BUILD` directory:

- **For GPU execution using oneAPI**: Run `buildWithOneAPI.sh`:
  ```bash
  ./buildWithOneAPI.sh
  ```
- **For CPU-only execution**: Run `build.sh`:
    ```bash
  ./build.sh
  ```

The EXE will be generated in the `RELEASE` directory. Add this path to your environment variables to execute the EXE from any location.
## Step 3: Running the EXE

You can run the  from any directory using the terminal.


### Log File Filtering
To filter an existing log file and generate a refined log, use the following command:
```bash
<LogsProcessor[OnGPU].exe> -i <full path to original log file> -o <filtered file name> -f <filter format>
```
Replace `<LogsProcessor[OnGPU].exe>` with either `LogsProcessorOnGPU.exe` (if running on GPU) or `LogsProcessor.exe` (if running without GPU).

### Available Filter Options
- **TimeRange**: Filters logs between specific start and end times (e.g., `TimeRange=1726671491.525302,1726671531.525302`).
- **Time**: Filters logs matching a specific timestamp (e.g., `Time=1726671491.525302`).
- **Quad**: Quad=Chip:<value>,Die:<value>,Quad:<value> (e.g., `Quad=Chip:0,Die:1,Quad:2`).
- **ThreadId**: Filters logs by thread IDs (e.g., `ThreadId=7,10,15`).
- **Unit**: Filters logs by processor units (e.g., `Unit=iqr`).
- **Area**: Filters logs by processor areas (e.g., `Area=bmt`).
- **Cluster**: Filters logs by cluster (chip, die, quad, row, column) (e.g., `Cluster=chip:0, die:1, quad:2, row:3, col:4`).

### Interactive Log Count Mode
To enter interactive mode and dynamically count parameters from the log file, run:
```bash
<LogsProcessor[OnGPU].exe> -i <full path to original log file> -c
```
This mode allows you to count occurrences of parameters like Thread IDs, Units, Areas, Clusters, and Quads in real-time. Once logs are processed, you will be prompted to select the count type:
```
What to dispaly ? Enter ThreadId / Unit / Area / Cluster / Quad:
To exit - enter exit
```
Select one of the options, or type `Exit` to leave the counting mode.

## Example Commands
- **Filtering by Time Range**:
  ```bash
  LogsProcessorOnGPU.exe -i logs.csv -o filtered_logs.csv -f "TimeRange=1726671491.525302,1726671531.525302"
  ```
- **Counting Thread IDs**:
  ```bash
  LogsProcessor.exe -i logs.csv -c
  ```
 for testing the code add the USE_TEST flag to the compilation command
## Contributors
This project was developed by a talented and dedicated team:
- [Chaya Avramovitz](https://github.com/chayaleA)
- [Elisheva Volpo](https://github.com/Elisheva-Volpo)
- [Nechama Shavrin](https://github.com/Nechama-Sha)
- [Rachel Bardenshtain](https://github.com/RacheliBardenshtain)

Feel free to contribute or provide suggestions to make this tool even more powerful.
