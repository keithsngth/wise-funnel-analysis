"""
DatabaseManager - A streamlined DuckDB database manager for analytics workflows.

This module provides a robust interface for:
- Initialising and connecting to DuckDB databases
- Creating tables from SQL schema files
- Loading CSV data into tables
- Executing SQL queries and retrieving results as pandas DataFrames
- Managing database connections with context manager support
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union

import duckdb
import pandas as pd
from loguru import logger

from .dataframe_processor import DataFrameProcessor


class DatabaseManager:
    """
    Context-aware database manager for DuckDB operations.

    Handles connection, table creation, data loading, and query execution.
    """

    def __init__(self, db_path: str):
        """
        Initialise the DatabaseManager.

        Args:
            db_path: Path to the DuckDB database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[duckdb.DuckDBPyConnection] = None
        logger.debug(f"DatabaseManager initialised with database path: {self.db_path}")

    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Establish connection to the DuckDB database.

        Returns:
            Active database connection
        """
        if self.connection is None:
            self.connection = duckdb.connect(str(self.db_path))
            logger.debug(f"Connected to database: {self.db_path}")
        return self.connection

    def close(self):
        """Close the database connection."""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            logger.debug("Database connection closed")

    def __enter__(self):
        """Enter context manager and connect to database."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and close connection."""
        self.close()

    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Execute SQL query and return results.

        Args:
            query: SQL query to execute
            params: Optional parameters for parameterized queries

        Returns:
            Query results as DataFrame
        """
        conn = self.connect()
        try:
            if params:
                result = conn.execute(query, params).df()
            else:
                result = conn.execute(query).df()
            logger.debug(f"Query executed successfully. Returned {len(result)} rows.")
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            raise

    def execute_sql_file(self, sql_file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Execute SQL query from file.

        Args:
            sql_file_path: Path to SQL file

        Returns:
            Query results as DataFrame
        """
        sql_path = Path(sql_file_path)
        if not sql_path.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_path}")

        with open(sql_path, "r") as f:
            query = f.read()

        logger.info(f"Executing SQL file: {sql_path}")
        return self.execute_query(query)

    def initialise_database(
        self,
        csv_file: Union[str, Path],
        table_name: str = "TRANSACTIONS",
        if_exists: str = "replace",
        table_schema: Optional[Union[str, Path]] = None,
    ):
        """
        Initialise database by creating tables and loading data.

        Args:
            csv_file: Path to CSV file to load
            table_name: Name of target table
            if_exists: 'replace' to truncate, 'append' to add data
            table_schema: Path to SQL schema file. Defaults to 'sql/create_transactions_table.sql'
        """
        logger.info(f"Initialising database: {self.db_path}")

        if table_schema:
            self.create_table_from_schema(table_schema)
        else:
            self.create_table_from_schema("sql/create_transactions_table.sql")

        csv_path = Path(csv_file)
        if csv_path.exists():
            logger.info(f"Loading data from: {csv_path}")
            self.load_csv_to_table(csv_path, table_name, if_exists=if_exists)
            logger.success("Database initialisation complete")
        else:
            logger.error(f"CSV file not found: {csv_path}")
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

    def create_table_from_schema(self, schema_file: Union[str, Path]):
        """
        Create database table from SQL schema file.

        Args:
            schema_file: Path to SQL schema file
        """
        schema_path = Path(schema_file)
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        logger.info(f"Creating table from schema: {schema_path}")
        self.execute_sql_file(schema_path)

    def load_csv_to_table(
        self,
        csv_path: Union[str, Path],
        table_name: str,
        if_exists: str = "replace",
        clean_data: bool = True,
    ):
        """
        Load CSV data into database table.

        Args:
            csv_path: Path to CSV file
            table_name: Name of target table
            if_exists: 'replace' to truncate, 'append' to add data
            clean_data: Whether to clean data (normalize, deduplicate, type conversion)
        """
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        # Read CSV
        df = pd.read_csv(csv_file)

        # Clean data using DataFrameProcessor
        if clean_data:
            df = DataFrameProcessor.clean_input_data(
                df,
                uppercase_columns=True,
                remove_duplicates=True,
                handle_missing="drop",
                convert_dtypes={
                    "USER_ID": "int64",
                    "EVENT_NAME": "string",
                    "PLATFORM": "string",
                    "EXPERIENCE": "string",
                    "EVENT_TIME": "datetime64[ns]",
                },
            )
        else:
            # Just normalise column names
            df = DataFrameProcessor.normalise_columns(df, uppercase=True)

        logger.info(f"Loading CSV file: {csv_file} into table: {table_name}")

        conn = self.connect()
        try:
            # Register DataFrame with DuckDB
            conn.register("temp_df", df)

            if if_exists == "replace":
                # Clear existing data but keep table structure
                conn.execute(f"TRUNCATE TABLE {table_name}")
                logger.debug(f"Cleared existing data from table: {table_name}")

            # Insert data into existing table
            insert_query = f"""
            INSERT INTO {table_name}
            SELECT * FROM temp_df
            """

            conn.execute(insert_query)
            conn.unregister("temp_df")

            # Get row count
            row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            logger.success(f"Loaded {row_count:,} rows into table: {table_name}")

        except Exception as e:
            logger.error(f"Error loading CSV to table: {e}")
            raise
