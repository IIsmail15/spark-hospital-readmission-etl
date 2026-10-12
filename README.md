# Hospital Readmission ETL and Analysis with PySpark

A notebook-based data engineering project that uses PySpark and Spark SQL to clean hospital encounter data, create analysis features, and explore readmission rates by race, primary diagnosis, and length of stay. Selected results are exported as Parquet datasets for downstream analysis.

Start with the notebook workflow below to explore the data and generate Parquet outputs.

## Dataset

The repository includes the [Diabetes 130-US Hospitals for Years 1999–2008 dataset from UCI](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008), covering encounters involving patients with diabetes.

Verified directly from the bundled `data/diabetic_data.csv`:

| Measure | Value |
| --- | ---: |
| Hospital encounters | 101,766 |
| Unique patient identifiers | 71,518 |
| CSV columns, including identifiers and target | 50 |
| Encounters labelled `<30` | 11,357 (11.16%) |
| Encounters labelled `>30` | 35,545 |
| Encounters labelled `NO` | 54,864 |

Each row represents an **encounter**, so a patient can appear more than once. The notebooks set `readmitted_flag = 1` for `<30` and `0` otherwise, combining `>30` and `NO` into the negative class. Reported percentages are encounter-level summaries.

`data/IDs_mapping.csv` contains descriptions for admission type, discharge disposition, and admission source IDs.

Dataset credit: Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999–2008*. UCI Machine Learning Repository. [DOI: 10.24432/C5230J](https://doi.org/10.24432/C5230J). UCI lists the dataset under CC BY 4.0.

## Workflow

```text
diabetic_data.csv
    |
    v
Read CSV into a Spark DataFrame
    |
    v
Replace '?' with null and derive analysis features
    |
    +-- Basic notebook: cleaned encounter data --> Parquet
    |
    +-- Analysis notebook: DataFrame and SQL summaries
            |-- Race --> displayed tables
            |-- Primary diagnosis --> Parquet
            +-- Length of stay --> Parquet
```

The two notebooks are separate workflows; neither requires output from the other.

| Component | Implemented behavior |
| --- | --- |
| Missing values | Replaces `?` with Spark nulls. |
| Age | Extracts the lower bound of the age interval into `age_num`, e.g. `[50-60)` becomes `50`. |
| Readmission | Encodes the `<30` label as a binary flag. |
| Medications | The basic notebook creates four usage flags. The analysis notebook encodes 21 medication columns and calculates a summed score in `df_intensity`. |
| Diagnosis | Extracts three leading numeric characters from `diag_1` and applies a hand-written label dictionary. |
| Aggregation | Computes readmission percentages and encounter counts by race, diagnosis category, and length of stay. Diagnosis exports retain groups with at least 10 encounters. |
| Storage | Writes selected DataFrames as Parquet using overwrite mode. |

The analysis notebook explores encounter-level readmission patterns through descriptive comparisons.

## Technology

- **Python and PySpark:** ingestion, cleaning, feature creation, and aggregation.
- **Spark SQL:** temporary views and summary queries.
- **Jupyter Notebook:** interactive exploration and displayed results.
- **Docker / Docker Compose:** container configuration based on `jupyter/pyspark-notebook`.
- **Parquet:** columnar output datasets.
- **Pandas:** a small diagnostic CSV export in the analysis notebook.

## Repository layout

```text
.
|-- app/
|   |-- Spark_ETL.ipynb          # Basic cleaning and Parquet export
|   |-- Spark_ETL_Job.ipynb      # Feature creation and readmission analysis
|   |-- etl_job.py              # ETL script under development
|   |-- config.py               # Environment-variable settings for the script
|   `-- utils/
|       `-- transformations.py # Reserved for shared transformations
|-- data/
|   |-- diabetic_data.csv
|   `-- IDs_mapping.csv
|-- dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- output/                    # Generated locally; ignored by Git
```

## Run the notebooks

Install Docker with Linux-container support and start its engine. Run these commands from the repository root in PowerShell or Bash.

Build the image using the repository's lowercase Dockerfile name:

```sh
docker build -f dockerfile -t hospital-readmission-etl .
```

Start Jupyter with the repository mounted into the container:

```sh
docker run --rm --name hospital-readmission-notebooks -p 127.0.0.1:8888:8888 --mount "type=bind,source=${PWD},target=/home/jovyan/workspace" --workdir /home/jovyan/workspace hospital-readmission-etl jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser
```

This command binds the port to localhost and overrides the Dockerfile's command to retain Jupyter's default token authentication. Open the token URL printed in the terminal at `http://localhost:8888`.

1. Open `app/Spark_ETL.ipynb` for basic cleaning, or `app/Spark_ETL_Job.ipynb` for the analysis.
2. On a fresh kernel, run the initial `%cd ..` cell once. The working directory should become `/home/jovyan/workspace`, where `data/` is available. Repeating that cell moves up another directory; use `%cd /home/jovyan/workspace` to reset it if needed.
3. Skip the `!pip install pyspark` cell when using this image, which already supplies PySpark.
4. Run subsequent cells in order. In the analysis notebook, skip the optional helper cells referencing `/home/jovyan/work/to_map_later.csv` and `%ls /home/jovyan/work/`, or change their paths to a writable location. These cells inspect unmapped diagnoses and are not required for the Parquet exports.
5. Inspect generated datasets in the host repository's `output/` directory. Stop Jupyter with `Ctrl+C` when finished.

## Outputs

| Host path | Producer | Contents |
| --- | --- | --- |
| `output/patients_cleaned1.parquet/` | `Spark_ETL.ipynb` | Encounter data with missing-value replacement, age/readmission features, four medication flags, and numeric casts. |
| `output/readmission_by_diag.parquet/` | `Spark_ETL_Job.ipynb` | Diagnosis categories, labels where mapped, encounter counts, and readmission percentages for groups with at least 10 encounters. |
| `output/readmission_by_length.parquet/` | `Spark_ETL_Job.ipynb` | Length of stay, readmission percentages, and encounter counts. The count column is named `patient_count`, but counts encounters. |

Spark writes **directories containing part files**, even when the directory name ends in `.parquet`. Re-running export cells overwrites the corresponding dataset.

## Strengths

- **Concrete data engineering practice:** works with a real dataset containing missing values, categorical fields, repeated patients, and diagnosis codes.
- **Both DataFrame and SQL experience:** demonstrates complementary Spark APIs, temporary views, and grouped calculations.
- **Useful downstream format:** Parquet outputs can support additional analysis or a future reporting layer.
- **Visible transformation logic:** notebooks make the steps easy to inspect, and diagnosis summaries include group sizes alongside rates.
- **Foundation for further development:** container configuration and the initial script structure provide starting points for packaging the notebook logic into a repeatable job.

## Future work

- Package the notebook transformations into a standalone ETL job.
- Automate diagnosis labels through a lookup-table join.
- Extend the analysis with age-group summaries.
- Add automated validation and continuous integration.
- Build a dashboard over the Parquet outputs.

## Author

[Israa Ismail](https://www.linkedin.com/in/israa-ismail-ii/)
