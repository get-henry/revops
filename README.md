# RevOps Salesforce Data Pipeline

This project is **forked** from [get-henry/revops](https://github.com/get-henry/revops). It aims to provide a modular, class-based Python tool for merging Salesforce **Lead**, **Contact**, and **Account** CSV data, with an option to join them in a single report. The fork introduces refactored code, improved tests, and a GitHub Actions workflow for automated continuous integration.

---

## Table of Contents

- [Background](#background)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Continuous Integration](#continuous-integration)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Background

The original project was designed to consolidate multiple Salesforce reports. This fork refactors the legacy code to:
- Use a centralized class (`SalesforceDataHandler`) for reading and merging CSVs.
- Improve maintainability and reusability with a test suite based on **pytest**.
- Provide a **Pipenv** environment and a ready-to-use GitHub Actions workflow.

---

## Features

- **Class-Based Architecture**  
  Encapsulates reading, combining, and joining CSV reports in a single class.  

- **Modular & Maintainable**  
  Clear method separation for reading & preparing data, combining, and joining.  

- **Pipenv**  
  Dependency management handled by `Pipfile` and `Pipfile.lock`.  

- **pytest**  
  A robust, straightforward test suite for ensuring your data workflows remain correct.  

- **GitHub Actions**  
  Automated testing across multiple Python versions (e.g., 3.9, 3.10, 3.11) for CI/CD.

---

## Folder Structure

```plaintext
.
├── data
│   ├── old salesforce_contact_report.csv
│   ├── old salesforce_lead_report.csv
│   ├── salesforce_account_report.csv
│   ├── salesforce_combined_report.csv
│   ├── salesforce_contact_report.csv
│   ├── salesforce_joined_report.csv
│   └── salesforce_lead_report.csv
├── libs
│   ├── __init__.py
│   └── salesforce_data_handler.py
├── tests
│   └── test_salesforce_data_handler.py
├── Pipfile
├── Pipfile.lock
├── LICENSE
├── README.md
└── .github
    └── workflows
        └── ci.yml
```

- **`data/`**: Contains various Salesforce CSV inputs and outputs.  
- **`libs/`**: Holds source code (`salesforce_data_handler.py`).  
- **`tests/`**: Houses the pytest suite (`test_salesforce_data_handler.py`).  
- **`.github/workflows/`**: GitHub Actions config for CI.

---

## Installation

1. **Clone** this repository (or your fork):

   ```bash
   git clone https://github.com/your-username/revops.git
   cd revops
   ```

2. **Install Dependencies with Pipenv**:

   ```bash
   pipenv install --dev
   ```

   This installs both standard and dev dependencies (like `pytest`).

---

## Usage

Below is an example script showing how to use the `SalesforceDataHandler` class to generate combined and joined reports.

```python
# run_salesforce_reports.py

import os
from libs.salesforce_data_handler import SalesforceDataHandler

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    handler = SalesforceDataHandler(
        base_dir=base_dir,
        lead_filename="salesforce_lead_report.csv",
        contact_filename="salesforce_contact_report.csv",
        account_filename="salesforce_account_report.csv"
    )

    # 1. Create and save combined Lead/Contact report
    handler.save_combined_lead_contact("salesforce_combined_report.csv")

    # 2. Join the combined data with Account data
    combined_df = handler.get_combined_lead_contact()
    handler.save_joined_report(combined_df, "salesforce_joined_report.csv")
```

1. **Activate** your Pipenv environment:

   ```bash
   pipenv shell
   ```

2. **Run** the script:

   ```bash
   python run_salesforce_reports.py
   ```

This will place updated CSVs in the `data/` folder:
- `salesforce_combined_report.csv`  
- `salesforce_joined_report.csv`  

---

## Running Tests

The test suite lives in `tests/`, powered by **pytest**.

1. **Activate** your Pipenv environment (if not already):

   ```bash
   pipenv shell
   ```

2. **Run tests**:

   ```bash
   pytest
   ```

Or, without activating the shell:

```bash
pipenv run pytest
```

You should see output showing the test results (e.g. `==== 4 passed in 0.12s ====`).

---

## Continuous Integration

This repository includes a GitHub Actions workflow, found in [`.github/workflows/ci.yml`](.github/workflows/ci.yml), which:
- Checks out the repository.
- Sets up Python for versions `3.9`, `3.10`, and `3.11`.
- Installs dependencies via Pipenv.
- Runs `pytest` to verify functionality.

This workflow is triggered on `push` and `pull_request` events for the `main` branch. You can see the results in the **Actions** tab of your GitHub repository.

---

## License

This project is distributed under the same license as the original [get-henry/revops](https://github.com/get-henry/revops) repository. Refer to the [LICENSE](LICENSE) file for full details. If you forked this repository, please retain the license and reference to the original authors as required.

---

## Acknowledgments

- **Original Repo**: [get-henry/revops](https://github.com/get-henry/revops)  
- **Contributors**: We thank the authors of the original code for providing a great starting point.

**Happy coding** and please feel free to open an issue or submit a pull request if you have improvements or questions!
