# Project Dependencies Deprecations Analyzer

## Overview

`Project Dependencies Deprecations Analyzer` is a Python tool designed to analyze Python projects and detect the usage of deprecated APIs (such as changed methods, classes, or parameters). It helps developers identify code that may become incompatible with future versions of the libraries or Python itself, ensuring smoother upgrades and maintaining long-term code stability.

This tool generates a comprehensive report detailing all detected deprecated APIs, giving developers the information they need to update their code efficiently.

## Features

- Scans Python code for deprecated methods, classes, and parameters.
- Generates a report highlighting deprecated APIs.

## Installation

To install `Project Dependencies Deprecations Analyzer`, you can clone the repository and install the dependencies:

```bash
# Clone the repository
git clone https://github.com/YoniShpund/OU-Final-Project.git

# Navigate into the directory
cd OU-Final-Project/src

# Install the required dependencies
pip install -r requirements.txt
```

## Usage

To use the tool, run the following command from the root directory of your project:

```bash
python pdda.py -d /path/to/your/python/project
```
You can use other options as well:
```bash
usage: pdda.py [-h] -d DIR [-t THREADS] [-v VERBOSE] [-l [1-4]]

Project Dependencies Deprecations Analyzer

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Project to analyze - full path
  -t THREADS, --threads THREADS
                        Number of threads
  -v VERBOSE, --verbose VERBOSE
                        Allow all logs
  -l [1-4], --logging_level [1-4]
                        Logging level (ERROR = 1, WARN = 2, INFO = 3, DEBUG = 4)
```

## Example
```bash
python pdda.py ./my-python-project
```
### Output

```
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/mas.py
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[warn] Warning found in the code of <class 'argparse.ArgumentParser'>
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/masModeBuild.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/masModeTest.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modAllocResource.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modConfig.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modDefines.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modErrors.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modLogging.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modRPI.py
[info] ==================================================
[info] Analyzing - /path/to/your/python/project/modScenario.py
==================================================
=================== RESULT =======================
==================================================
0 errors, 8 warnings in - /path/to/your/python/project/mas.py
0 errors, 0 warnings in - /path/to/your/python/project/masModeBuild.py
0 errors, 0 warnings in - /path/to/your/python/project/masModeTest.py
0 errors, 0 warnings in - /path/to/your/python/project/modAllocResource.py
0 errors, 0 warnings in - /path/to/your/python/project/modConfig.py
0 errors, 0 warnings in - /path/to/your/python/project/modDefines.py
0 errors, 0 warnings in - /path/to/your/python/project/modErrors.py
0 errors, 0 warnings in - /path/to/your/python/project/modLogging.py
0 errors, 0 warnings in - /path/to/your/python/project/modRPI.py
0 errors, 0 warnings in - /path/to/your/python/project/modScenario.py
```

## Contributing
Contributions are welcome! If you'd like to contribute:

1. Fork the repository.
1. Create a feature branch (`git checkout -b feature-branch`).
1. Commit your changes (`git commit -m "Add some feature"`).
1. Push to the branch (`git push origin feature-branch`).
1. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/YoniShpund/OU-Final-Project/blob/main/LICENSE) file for details.

## Contact
If you have any questions, feel free to contact me through GitHub Issues.
