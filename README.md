# Work in progress

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
