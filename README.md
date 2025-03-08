# AI-Powered SQL Query Generator and Corrector

This project is a **Streamlit-based AI-powered application** that translates natural language queries into SQL and corrects incorrect SQL queries using the **Groq API**. It connects to a **PostgreSQL database**, fetches schema information, and utilizes **machine learning datasets** to improve query generation and correction.

## Features
- **Natural Language to SQL Translation**: Convert plain English queries into SQL.
- **SQL Query Correction**: Fix incorrect SQL queries.
- **PostgreSQL Database Connection**: Fetches schema dynamically.
- **Groq API Integration**: Uses AI to generate and correct SQL queries.
- **Streamlit UI**: Interactive web interface for ease of use.

## Technologies Used
- **Python**
- **Streamlit**
- **PostgreSQL** (`psycopg2`)
- **Groq API**
- **Pandas** (for data processing)
- **JSON** (for training data)

## Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/Pavan1456/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file and add:
   ```env
   GROQ_API_KEY=your_groq_api_key
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

4. **Run the Application**:
   ```sh
   streamlit run app.py
   ```

## Usage
1. Enter a **natural language query** to generate an SQL query.
2. Paste an **incorrect SQL query** to get a corrected version.
3. View query results directly from the PostgreSQL database.

## File Structure
```
📂 your-repo-name
 ├── app.py                  # Main Streamlit application
 ├── database.py             # Database connection functions
 ├── utils.py                # Helper functions for prompt generation
 ├── requirements.txt        # Required Python packages
 ├── train_generate_task.json # Training dataset for NL-to-SQL
 ├── train_query_correction_task.json # Training dataset for SQL correction
 ├── .env.example            # Example environment variables file
 ├── README.md               # Project documentation
```

## Contributing
Feel free to open issues or pull requests if you find bugs or have suggestions for improvements!

## License
This project is licensed under the MIT License.

---
Made with ❤️ by Pawan.

