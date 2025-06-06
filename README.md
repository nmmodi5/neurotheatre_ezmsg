# neurotheatre_ezmsg
This repo has EzMsg implementation for neurotheatre project application

This is a uv project.

# Getting Started
install the following packages:
- uv: https://docs.astral.sh/uv/getting-started/installation/
- portaudio (dependency needed for pyaudio, which will be installed by uv). just run `brew install portaudio` for mac
- LSL library if you are using muse Device by running `brew install labstreaminglayer/tap/lsl` (As a dependency for muselsl which will be installed by uv)

once above is installed, run the following command to setup the environment:
`uv sync`

# Project Structure
```
.
├── .venv
├── README.md
├── src
    └── neurotheatre
    └── test
├── pyproject.toml
└── uv.lock
```

# Project Description
- .venv : This is the virtual environment where uv will install all the packages; Will be created automatically on the root of project when you initialize the project
- src/neurotheatre: This contains modules describing individual ezmsg unit implementations, and collections to create ezmsg network
- main: Main unit and call to the experiment. when `uv run` command is run, it calls this script

# Running the project
currently following commands are implemented
- osc
- toaudio
- tomidi

To run a specific command, do `uv run <command> <parameters>`.  There is an associated command line interface with each command, use `-h` to access documentation related to the commandline interface.

*Examples:* 
- To run a server that sends IMU/EEG data to OSC-enabled software (like touchdesigner) run `uv run osc`

- To run the toaudio, with default parameters and input signal as simulator, you can do `uv run toaudio`. 
  This will open a new tab in browser, where you can see the signal (set filter order to 3, cuton fs = 1 and cutoff fs = 30 Hz to see the post processed signal). This will also play the audio for the signal.

- To run the tomidi, with default parameters and input signal as simulator, open up a new Garageband Project as midi type and then run `uv run tomidi`. This will open a new tab in browser, where you can see the signal (set filter order to 3, cuton fs = 1 and cutoff fs = 30 Hz to see the post processed signal). This will also play the audio for the signal in garageband.

# ENVIRONMENT NOTE
The dependencies are meant to be working on python version 3.10/3.11, which is what is reflected on the pyproject file. Please do not change that