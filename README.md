# 🏥 Hospital Readmission Analysis with PySpark

This project uses Apache Spark to process and analyze real hospital admission data to identify key factors influencing 30-day patient readmissions.

## 🚀 Project Goals
- Build a Spark-based ETL pipeline for healthcare data
- Clean and transform raw CSV data into analysis-ready form
- Derive insights about patient demographics, diagnoses, and outcomes

## 🧰 Tech Stack
- Python
- PySpark
- JupyterLab
- Docker
- Pandas (for light export)

## 📊 Key Transformations
- Encoded readmission flags
- Extracted numeric ages and diagnosis groups
- Mapped medication usage into effect scores
- Created temp views for diagnosis labels using ICD-9 codes

## 📈 Insights Discovered
1. **Readmission by Age Group**
2. **Readmission by Race**
3. **Readmission by Primary Diagnosis**
4. **Readmission vs Time in Hospital**

## 📂 Output Files
- `/output/cleaned_data.parquet`
- `/output/readmission_by_diag.parquet`
- `/output/readmission_by_length.parquet`

## ✅ Future Work
- Automate ICD-9 diagnosis mapping via lookup join
- Integrate with a BI dashboard (e.g., Tableau or Superset)
- Convert to production ETL job using Spark scripts

## 👤 Author
- Israa Ismail
- www.linkedin.com/in/israa-ismail-ii
