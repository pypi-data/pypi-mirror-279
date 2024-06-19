# Copyright (C) Prizmi, LLC - All Rights Reserved
# Unauthorized copying or use of this file is strictly prohibited and subject to prosecution under applicable laws
# Proprietary and confidential

"""The main module for validating a data set against the requirements that are either defined in a separate
metadata file or provided by user in the configuration file"""

import sys
import warnings
import logging
import valideer as v
import numpy as np
import pandas as pd

from learner.configuration.configuration import Configuration


class DataValidator:
    def __init__(self, conf: Configuration, data: pd, data_type="train"):
        """Accept a dataset and a conf object to validate the data set against the information provided in the conf
        object

        :param conf: a conf object (an instance of the Configuration class in configuration module)
        :param data: a pandas dataframe
        :param data_type: the data type, it can be "train", "validation" or "test"
        """
        self._conf = conf
        self._data = data
        self._data_type = data_type

    @property
    def conf(self):
        return self._conf

    @property
    def data(self):
        return self._data

    @property
    def data_type(self):
        return self._data_type

    def validate_against_meta_data(self, meta_data):
        """Validate the data against a meta_data file

        :param meta_data: the meta_data file
        :return: None
        """
        logging.info("Validating the data against the meta_data file...")

        # loop through columns and create new dict with just column and schema needed for validation
        schema_dict = dict()
        for col in meta_data['column']:
            for key, value in meta_data['column'][col].items():
                if key == 'schema':
                    schema_dict[col] = [value]
                    
        val = v.parse(schema_dict)
        for col in self._data.columns:
            if not val.is_valid(self._data[[col]].dropna().to_dict('list')):
                message = f"Data in column {col} is Not Valid, type expected: {schema_dict[col]}"
                if self.conf.validation.dtypes_against_metadata_behavior == "error":
                    raise Exception(message)
                else:
                    warnings.warn(message, Warning)

        logging.info("Finished validating against meta_data...")

    def check_nulls_in_col(self, data, col):
        """Check if the target column has any missing values.

        :param data: a pandas dataframe
        :param col: the column to check for missing values. This is usually the target column
        :return: None
        """
        logging.info("Checking if the target contains missing values...")
        try:
            num_nulls = data[col].isnull().sum()
            if num_nulls:
                if self.conf.validation.nulls_in_target_behavior == "error":
                    logging.critical("The target column contains {num_nulls} rows with missing values. Exiting...")
                    sys.exit(1)
                else:
                    data.dropna(subset=[col], inplace=True)
                    warnings.warn(f"The target column contains {num_nulls} rows with missing values. Those rows will be dropped "
                                  "from the dataset", Warning)
                    if data.empty:
                        logging.error("Looks like all values in the target column are missing, please check your data."
                                      " Exiting...")
                        sys.exit(1)

        except KeyError:
            logging.info("target_col is not in the data or not loaded. Skipping check_nulls_in_target...")

    def check_dtype_of_num_cols(self):
        """Ensure the columns passed as numerical columns are actually numeric. Learner only issues a warning if it
        finds out some columns are not numeric.

        :return: None
        """
        if self._conf.process.to_numeric_cols and self._conf.process.to_numeric_activate:
            logging.info("Checking data types of numerical columns...")
            # get columns with numeric datatypes
            numeric_columns_types = [np.issubdtype(self.data[col].dtype, np.number)
                                     for col in self._conf.process.to_numeric_cols]
            # first check to see any num_cols is defined, if not just return the data
            # if num_cols is defined, make sure all passed columns are of type number (int and float).
            if not all(numeric_columns_types):
                message = """Column(s) passed {0} can't be converted to numeric data type. This may cause some 
                              errors. Check the data""".format([col_name for col_name in self._conf.process.to_numeric_cols
                                                               if np.issubdtype(self.data[col_name].dtype, np.number)
                                                               is False])
                if self.conf.validation.to_numeric_behavior == "error":
                    logging.critical(f"{message}. Exiting...")
                    sys.exit(1)
                else:
                    warnings.warn(message, UserWarning)

    def check_nulls_portion(self):
        """Perform the data validation related to the null portion. In this method, we first obtain a dataframe
        containing the features and the missing ratio. Then, depending on the input parameters, we'll use that
        information to validate the data. We first do the validation for specific columns, then do all other columns.

        :return: None
        """
        missing_df = self._get_missing_df()
        if missing_df.empty:
            return

        sample_count = self.data.shape[0]
        for param in self.conf.validation.nulls_portion_specific_cols_params:
            if sample_count >= param["min_sample"]:
                missing_portion = missing_df[missing_df["feature"] == param["name"]]["missing_ratio"].values[0]
                if missing_portion > param["threshold"]:
                    message = (f"The portion of nulls in {param['name']} is {round(missing_portion, 2)}, " 
                               f"which is higher than the defined threshold of {param['threshold']}. Exiting...")
                    if param["behavior"] == "error":
                        logging.critical(message)
                        sys.exit(1)
                    else:
                        warnings.warn(message, Warning)

        if self.conf.validation.nulls_portion_all_cols_activate:
            if sample_count >= self.conf.validation.nulls_portion_all_cols_min_sample:
                df = missing_df[
                          (~missing_df["feature"].isin(self.conf.validation.nulls_portion_specific_cols)) &\
                          (missing_df["missing_ratio"] > self.conf.validation.nulls_portion_all_cols_threshold)
                      ]
                if not df.empty:
                    message = (f"The null portion is greater than the defined threshold of "
                               f"{self.conf.validation.nulls_portion_all_cols_threshold} in some columns. "
                               f"Below is the detailed information:\n {df}")
                    if self.conf.validation.nulls_portion_all_cols_behavior == "error":
                        logging.critical(message)
                        sys.exit(1)
                    else:
                        warnings.warn(message, Warning)

    def _get_missing_df(self):
        """Use the self.data pandas dataframe and construct a new dataframe with the columns: "feature", "missing_count",
        and "missing_ratio". Here we make sure we only do the calculation for relevant columns for performance reasons.

        :return: a pandas dataframe containing three columns: "feature", "missing_count", and "missing_ratio"
        """
        missing_df = pd.DataFrame()
        # we do the nulls portion calculations for all the columns if all_cols is activated
        # otherwise we use the specified columns
        if self.conf.validation.nulls_portion_all_cols_activate:
            missing_df = self.data.isnull().sum(axis=0).reset_index()
        elif self.conf.validation.nulls_portion_specific_cols_params:
            missing_df = self.data[self.conf.validation.nulls_portion_specific_cols].isnull().sum(axis=0).reset_index()
        if missing_df.empty is False:
            missing_df.columns = ["feature", "missing_count"]
            missing_df['missing_ratio'] = (missing_df["missing_count"] / self.data.shape[0])
        return missing_df

    def validate_data(self):
        """The main function that runs all the instance methods if the validation flag is set to true

        :return: None
        """
        logging.info("Validating the data...")

        if self._conf.data.meta_data_file and self._conf.validation.dtypes_against_metadata_activate:
            self.validate_against_meta_data(self._conf.data.meta_data)

        # we care about nulls in target only when data_type is train or validation
        if self.data_type != "test" and self.conf.validation.nulls_in_target_activate:
            self.check_nulls_in_col(self.data, self._conf.column.target_col)
        if self.conf.validation.to_numeric_activate:
            self.check_dtype_of_num_cols()
        self.check_nulls_portion()
        logging.info("Successfully validated the data")


def check_nulls_in_col(data, col):
    """Check if the col column has any missing values.

    :param data: a pandas dataframe
    :param col: the column to check for missing values. This is usually the target column
    :return: None
    """
    logging.info(f"Checking if the {col} contains missing values...")
    try:
        num_nulls = data[col].isnull().sum()
        if num_nulls:
            data.dropna(subset=[col], inplace=True)
            warnings.warn(f"The {col} column contains {num_nulls} rows with missing values. Those rows will be dropped "
                          "from the dataset", Warning)
            if data.empty:
                logging.error("Looks like all values in the target column are missing, please check your data."
                              " Exiting...")
                sys.exit(1)
    except KeyError:
        logging.info(f"{col} is not in the data or not loaded. Exiting...")
        sys.exit(1)
