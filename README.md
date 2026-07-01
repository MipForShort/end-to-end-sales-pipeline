# End-to-End Sales Pipeline

This project consists of an automated end-to-end data pipeline designed to transform raw data from various sources into structured information, ready for analysis in a PostgreSQL database.

## Project Description
The system extracts data from CSV files, Excel spreadsheets, PDF documents (using specialized extraction techniques), and performs web scraping to gather country data, ensuring all information is normalized and correctly loaded into a defined relational schema.

## Technologies Used
* **Language:** Python
* **Data Processing:** Pandas
* **Database:** PostgreSQL
* **ORM / Connectors:** SQLAlchemy, psycopg2
* **Web Scraping:** BeautifulSoup
* **PDF Extraction:** Tabula-py
* **Environment Management:** Python-dotenv

## Pipeline Architecture
1. **Extraction:** Loading data from multiple heterogeneous sources.
2. **Transformation:** Cleaning, data type normalization, date handling, and duplicate resolution.
3. **Loading:** Insertion into a relational schema with guaranteed referential integrity (Foreign Keys).

---

## How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/MipForShort/end-to-end-sales-pipeline.git
```

2. Create and activate a virtual environment:

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
# PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# CMD
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a .env file in the root directory with the following structure:

```
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=edutin_sales
```

5. Create the database from your terminal if using Linux/MacOS by executing `psql` first. Once done, create the database with the next command:

```sql
CREATE DATABASE edutin_sales;
```

If using Windows:
- Open pgAdmin
- Expand Servers
- Expand PostgreSQL
- Right click on Databases
- Hover Create, select Database
- Name it sales_db

6. Execute the pipeline:

```bash
# Linux/macOS
python3 src/main.py

# Windows
python .\src\main.py
```
