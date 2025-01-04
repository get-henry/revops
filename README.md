# RevOps
Collection of Revenue Operations Stuff

---

## Table of Contents

- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [salesforceimportappend.py](#salesforceimportappend.py)
- [02 salesforcejoin.py](#02-salesforcejoin.py)
- [03 salesforceconversionrate.py](#03-salesforceconversionrate.py)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Folder Structure
```plaintext
.
├── data/                     # Folder for input CSV files (lead, contact, and account reports)
│   ├── old salesforce_contact_report.csv
│   ├── old salesforce_lead_report.csv
│   ├── salesforce_account_report.csv
│   ├── salesforce_combined_report.csv
│   ├── salesforce_contact_report.csv
│   ├── salesforce_joined_report.csv
│   └── salesforce_lead_report.csv
├── salesforceimportappend.py
├── 02 salesforcejoin.py
├── 03 salesforceconversionrate.py
├── README.md                 # Project documentation
├── LICENSE                   # License

```
---

## Installation

### Prerequisites
- **Python 3.7+**
- Required libraries:
  - `pandas`
  - `matplotlib`

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/salesforce-conversion-reporting.git
   cd salesforce-conversion-reporting
   ```
2.	Install dependencies:
    ```bash
    pip install pandas matplotlib
    ```
3.	Place Salesforce Lead, Contact, and Account CSV files in the data/ directory.

---


## salesforceimportappend.py
Python Script to Import Salesforce Lead and Contact Reports into a combined report output.

---

## 02 salesforcejoin.py
Python script to join Salesforce Account into the combined report output from salesforceimportappend.py

---

## 03 salesforceconversionrate.py
Python script to calculate converted divided by total metric per lead & account grouped by lead, contact, or combined
A Python script to automate the reporting of Salesforce lead, contact, and account conversion rates. This tool helps RevOps teams streamline reporting, eliminate manual data processing, and ensure consistent, accurate data.

### Features

1. **Data Aggregation**:
   - Summarizes:
     - Total Leads
     - Converted Leads
     - Total Accounts
     - Accounts Converted
     - Conversion Rate (%)
     - Account Conversion Rate (%)
   - Groups data by record type (Lead, Contact) and includes a combined summary row.

2. **Automation**:
   - Automates the process of joining Salesforce lead, contact, and account reports.
   - Eliminates manual errors and ensures consistent data processing.

3. **Visualization**:
   - Generates a professional tabular report using Matplotlib.

---

### How It Works

#### Steps in the Script:
1. **Group & Aggregate**:
   - Groups Salesforce data by record type (Lead, Contact) and calculates key metrics:
     - Total Leads
     - Converted Leads
     - Total Accounts
     - Accounts Converted
     - Conversion Rate (%)
     - Account Conversion Rate (%)

2. **Create a Combined Row**:
   - Adds an overall summary row combining lead and contact metrics.

3. **Visualize the Data**:
   - Creates a clean, easy-to-read table using Matplotlib.

#### Example Output:

##### Tabular Report:
Total_Leads | Converted | Total_Accounts | Accounts_Converted | Converted Rate (%) | Account Converted Rate (%)
100.0       | 32.0      | 58.0           | 26.0               | 32.0               | 44.83
100.0       | 20.0      | 63.0           | 19.0               | 20.0               | 30.0
200.0       | 52.0      | 121.0          | 45.0               | 26.0               | 37.19

---

## Custom Salesforce Automation

Need tailored Salesforce automation solutions? Contact me for custom scripts and solutions that fit your business needs.

---

## License

This project is distributed under the same license as the original [get-henry/revops](https://github.com/get-henry/revops) repository. Refer to the [LICENSE](LICENSE) file for full details. If you forked this repository, please retain the license and reference to the original authors as required.

---

## Acknowledgments
-	Pandas for data manipulation.
-	Matplotlib for visualization.
- **Original Repo**: [get-henry/revops](https://github.com/get-henry/revops)  
- **Contributors**: We thank the authors of the original code for providing a great starting point.

**Happy coding** and please feel free to open an issue or submit a pull request if you have improvements or questions!
