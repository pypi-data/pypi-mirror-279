# Algerian Forest Fire Prediction

Build a machine learning model that can accurately predict whether a forest fire will occur based on input features based on environmental and weather data. This is a binary classification problem, where the model needs to learn the patterns that distinguish between instances where a fire occurred ("fire") and instances where no fire occurred ("not fire").


This notebook explores a dataset of forest fire occurrences, including meteorological data, fuel characteristics, and date information. It performs EDA, hypothesis testing, and builds a machine learning model to predict fire occurrence.

**Key Considerations:**

* **Data Availability:** The dataset provides historical information on weather and environmental conditions and whether fires occurred.
* **Feature Importance:**  Determining which features have the strongest impact on fire occurrence is crucial for model accuracy.
* **Model Performance:**  The model's performance will be evaluated based on its ability to correctly classify future fire events.


## 🚩 Table of Contents

- [Project Overview](#-project-overview)
- [Getting Started](#-getting-started)
    - [Prerequisites](#-prerequisites)
    - [Installation](#-installtion)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Contributing](#-contributions)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## Project Overview

Forest fires pose a significant threat to the environment and human safety. This project aims to develop a machine learning model that can predict the likelihood of forest fires in Algeria, using historical data and environmental factors.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9 (or compatible)
- Conda (optional, but recommended)

### Installation

1. **Clone the repository:**
    ```bash
    $ git clone https://github.com/your-username/algerian-forest-fire-prediction.git
    ```
2. **Create a conda environment:**
    ```bash
    $ conda create -n forest-fire-env python=3.9 # Adjust python version as needed
    ```
3. **Activate the environment:**
    ```bash
    $ conda activate forest-fire-env
    ```
4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Setup your command line interface for better readability (Optional):**
   ```bash
   export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
   ```

## Dataset

This dataset contains information about forest fires in Algeria, focusing on two specific regions:

* **Bejaia region:** Located in the northeast of Algeria.
* **Sidi Bel-abbes region:** Located in the northwest of Algeria.

The dataset includes data collected between **June 2012 and September 2012**.

**Key Features:**

* **Instances:** 244 (122 for each region)
* **Attributes:** 11 attributes (features)
* **Output Attribute:** 1 output attribute (class)
* **Classes:**
    * **Fire:** 138 instances
    * **Not fire:** 106 instances

**Attributes:**

* **Date:** The date of the observation (DD/MM/YYYY).
* **Temp:** Temperature in Celsius.
* **RH:** Relative Humidity in percentage.
* **Ws:** Wind speed in km/h.
* **Rain:** Total amount of rainfall in mm.
* **FFMC:** Fine Fuel Moisture Code, representing the moisture content of fine fuels (0-100).
* **DMC:** Duff Moisture Code, representing the moisture content of decaying organic matter (0-100).
* **DC:** Drought Code, representing the overall drought level (0-100).
* **ISI:** Initial Spread Index, representing the ease of fire ignition (0-100).
* **BUI:** Buildup Index, representing the total amount of fuel available (0-100).
* **FWI:** Fire Weather Index, representing the overall fire danger (0-100).
* **Classes:** The output class, indicating whether a fire occurred (1) or not (0).


**Attributes Description:**

| Feature           | Description                                          | Data Type |
|--------------------|---------------------------------------------------|-----------|
| **Classes**        | Fire or not fire (target variable)                 | Categorical |
| **month**         | Month of the year (1-12)                            | Integer   |
| **RH**            | Relative humidity (%)                               | Integer   |
| **Temperature**    | Temperature (Celsius)                               | Integer   |
| **Ws**            | Wind speed (km/h)                                   | Integer   |
| **year**          | Year of the observation                              | Integer   |
| **DC**            | Drought Code Index                                    | Float     |
| **Rain**          | Total amount of precipitation (mm)                   | Float     |
| **DMC**           | Drought Code Index                                    | Float     |
| **FFMC**          | Fine Fuel Moisture Code                              | Float     |
| **BUI**           | Buildup Index                                       | Float     |
| **ISI**           | Initial Spread Index                                | Float     |
| **FWI**           | Fire Weather Index                                   | Float     |
| **day**           | Day of the month (1-31)                             | Integer   |


---

## Project Structure

```
Algerian-Forest-Fire-Prediction
├── .github
│   └── workflows
│       └── ci.yaml
├── Notebooks
│   └── Data_Expolration.ipynb
├── assets
├── data
│   ├── raw
│   │   └── Algerian_forest_fires.csv
│   └── processed
<!-- │       └── processed_data.csv -->
├── checkpoints
├── artifacts
├── src
│   ├── utils.py
│   ├── logger.py
│   ├── exception.py
│   ├── components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
<!-- │   │   ├── model_evaluation.py -->
│   └── pipeline
│       └── training_pipeline.py
│       └── evaluation_pipeline.py
├── tests
│   ├── unit
│   │   └── test_utils.py
│   └── integration
│       └── test_training_pipeline.py
├── requirements.txt
├── .env
├── .env.example
└── README.md

```

---

### Contributions

Contributions to this project are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

<!-- - [Dataset Source] - For providing the Algerian forest fire dataset.
- [Library Name] - For providing the machine learning library used. -->
``` 
