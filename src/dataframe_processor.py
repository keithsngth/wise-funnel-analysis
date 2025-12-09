"""
DataFrame processing utilities for data cleaning and transformation.

This module provides utilities for:
- Cleaning and normalising input data before loading to database
- Processing query output DataFrames for analysis and visualisation
"""

from typing import List, Optional, Union

import pandas as pd
from loguru import logger


class DataFrameProcessor:
    """
    Utilities for DataFrame cleaning and transformation.

    Handles both input data cleaning (before DB load) and output data
    processing (after queries).
    """

    @staticmethod
    def normalise_columns(df: pd.DataFrame, uppercase: bool = True) -> pd.DataFrame:
        """
        Normalise column names.

        Args:
            df: Input DataFrame
            uppercase: If True, convert to uppercase. If False, to lowercase.

        Returns:
            DataFrame with normalised column names
        """
        if uppercase:
            df.columns = [col.upper() for col in df.columns]
        else:
            df.columns = [col.lower() for col in df.columns]

        logger.debug(
            f"Normalised {len(df.columns)} column names to {'uppercase' if uppercase else 'lowercase'}"
        )
        return df

    @staticmethod
    def remove_duplicates(
        df: pd.DataFrame, subset: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Remove duplicate rows.

        Args:
            df: Input DataFrame
            subset: Column names to consider for duplicates. If None, use all columns.

        Returns:
            DataFrame with duplicates removed
        """
        original_count = len(df)
        df = df.drop_duplicates(subset=subset)
        removed_count = original_count - len(df)

        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate rows")

        return df

    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame,
        strategy: str = "drop",
        fill_value: Optional[Union[str, int, float]] = None,
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Handle missing values in DataFrame.

        Args:
            df: Input DataFrame
            strategy: 'drop' to remove rows with NaN, 'fill' to fill with value
            fill_value: Value to use when strategy='fill'
            columns: Specific columns to check. If None, check all columns.

        Returns:
            DataFrame with missing values handled
        """
        if strategy == "drop":
            original_count = len(df)
            df = df.dropna(subset=columns)
            removed_count = original_count - len(df)
            if removed_count > 0:
                logger.info(f"Dropped {removed_count} rows with missing values")

        elif strategy == "fill":
            if fill_value is None:
                raise ValueError("fill_value must be provided when strategy='fill'")
            if columns:
                df[columns] = df[columns].fillna(fill_value)
            else:
                df = df.fillna(fill_value)
            logger.debug(f"Filled missing values with: {fill_value}")

        return df

    @staticmethod
    def convert_dtypes(df: pd.DataFrame, dtype_map: dict) -> pd.DataFrame:
        """
        Convert column data types.

        Args:
            df: Input DataFrame
            dtype_map: Dictionary mapping column names to desired dtypes
            Example: {'USER_ID': 'int64', 'EVENT_TIME': 'datetime64'}

        Returns:
            DataFrame with converted dtypes
        """
        for col, dtype in dtype_map.items():
            if col in df.columns:
                try:
                    if dtype == "datetime64":
                        df[col] = pd.to_datetime(df[col])
                    else:
                        df[col] = df[col].astype(dtype)
                    logger.debug(f"Converted {col} to {dtype}")
                except Exception as e:
                    logger.warning(f"Could not convert {col} to {dtype}: {e}")

        return df

    @staticmethod
    def clean_input_data(
        df: pd.DataFrame,
        uppercase_columns: bool = True,
        remove_duplicates: bool = True,
        handle_missing: str = "drop",
        convert_dtypes: Optional[dict] = None,
    ) -> pd.DataFrame:
        """
        Apply standard cleaning pipeline for input data.

        Args:
            df: Input DataFrame
            uppercase_columns: Whether to uppercase column names
            remove_duplicates: Whether to remove duplicate rows
            handle_missing: Strategy for missing values ('drop' or 'fill')
            convert_dtypes: Dictionary mapping column names to desired dtypes

        Returns:
            Cleaned DataFrame
        """
        logger.info(f"Cleaning input data: {len(df)} rows, {len(df.columns)} columns")

        # Normalise to uppercase
        if uppercase_columns:
            df = DataFrameProcessor.normalise_columns(df, uppercase=True)

        # Remove duplicates
        if remove_duplicates:
            df = DataFrameProcessor.remove_duplicates(df)

        # Handle missing values
        if handle_missing:
            df = DataFrameProcessor.handle_missing_values(df, strategy=handle_missing)

        # Convert data types
        if convert_dtypes:
            df = DataFrameProcessor.convert_dtypes(df, dtype_map=convert_dtypes)

        logger.success(f"Cleaned data: {len(df)} rows, {len(df.columns)} columns")
        return df

    @staticmethod
    def format_query_output(
        df: pd.DataFrame,
        round_decimals: Optional[int] = 2,
        sort_by: Optional[Union[str, List[str]]] = None,
        ascending: bool = True,
    ) -> pd.DataFrame:
        """
        Format query output DataFrame for display/analysis.

        Args:
            df: Query result DataFrame
            round_decimals: Number of decimals for float columns. None to skip rounding.
            sort_by: Column(s) to sort by
            ascending: Sort order

        Returns:
            Formatted DataFrame
        """
        # Round numeric columns
        if round_decimals is not None:
            numeric_cols = df.select_dtypes(include=["float64", "float32"]).columns
            df[numeric_cols] = df[numeric_cols].round(round_decimals)

        # Sort if requested
        if sort_by:
            df = df.sort_values(by=sort_by, ascending=ascending)

        return df
