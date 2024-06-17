import pandas as pd
import os
import sys

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class ExcelSheetCombiner:
    
    # Function to check if a column is blank
    @staticmethod
    def is_blank_column(col):
        # Correctly evaluates if column header is empty or NaN
        return (isinstance(col, str) and col.strip() == '') or str(col) == ''

    @staticmethod
    def extract_list_headers( file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("extract_list_headers"):
            try:                 
                # Load the 'lists' sheet into a DataFrame
                lists_df = pd.read_excel(file_path, sheet_name='lists')
                lists_df['data_product_id'] = data_product_id
                lists_df['code_type'] = "local_valueset"
                lists_df['valueset_code'] = "code_" + lists_df['list'].astype(str)

                # Example of renaming columns
                lists_df = lists_df.rename(columns={
                    'old_list': 'list',
                    'old_item_code': 'item_code',
                    # Add other renamings as needed
                })
                
                                                                
                return lists_df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

 
    @classmethod
    def is_blank_column(cls, col):
        # Handle non-string types
        if isinstance(col, str):
            return not col or col.strip() == ""
        return False

    @classmethod
    def combine_sheets(cls, file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("combine_sheets", attributes={"data_product_id": str(data_product_id), "environment": str(environment)}):
            try:
                # Load the Excel file
                xls = pd.ExcelFile(file_path)
                logger.info(f"Loaded Excel file: {file_path}")
                
                # Retrieve all sheet names
                sheets = xls.sheet_names
                logger.info(f"Found sheets: {sheets}")
                
                # Find the first sheet that contains 'lists' in its name to determine the cutoff
                list_sheets = [sheet for sheet in sheets if 'lists' in sheet.lower()]
                if not list_sheets:
                    raise ValueError("No 'lists' tabs found in the Excel file.")
                
                logger.info(f"'Lists' sheets found: {list_sheets}")
                
                # Determine the index of the last 'lists' sheet
                last_list_index = max(sheets.index(sheet) for sheet in list_sheets)
                logger.info(f"Last 'lists' sheet index: {last_list_index}")

                # Define the new column names
                new_columns = ['list', 'item_code', 'item_name', 'item_category', 'item_sort', 'item_description', 'item_visibility', 'item_color', 'data_product_id', 'sheet_name']
                
                # Initialize an empty DataFrame to append data
                combined_data = pd.DataFrame(columns=new_columns)

                # Process each sheet past the last 'lists' sheet
                for sheet in sheets[last_list_index + 1:]:
                    data = pd.read_excel(file_path, sheet_name=sheet, header=0)
                    logger.info(f"Processing sheet: {sheet}, Number of rows: {data.shape[0]}, Number of columns: {data.shape[1]}")
                    
                    # Strip and lowercase column names
                    data.columns = [col.strip().lower() for col in data.columns]

                    # Align the columns with the predefined set of columns
                    for col in new_columns:
                        if col not in data.columns:
                            data[col] = pd.NA

                    data = data[new_columns]
                    
                    data = data[new_columns[:-1]]  # Exclude 'sheet_name' temporarily
                    data['sheet_name'] = sheet
                    
                    combined_data = pd.concat([combined_data, data], ignore_index=True)
                    logger.info(f"Combined data shape after processing sheet {sheet}: {combined_data.shape}")

                if combined_data.empty:
                    logger.warning("Combined data is empty after processing all sheets.")
                else:
                    # Remove blank rows based on all columns being NaN
                    combined_data = combined_data.dropna(how='all')
                    logger.info(f"Shape after dropping blank rows: {combined_data.shape}")

                    # Finding the last non-blank column
                    last_valid_index = len(combined_data.columns) - 1
                    for col in reversed(combined_data.columns):
                        if cls.is_blank_column(col) and combined_data[col].isna().all():
                            last_valid_index -= 1
                        else:
                            break

                    # Dropping blank columns from the end
                    if last_valid_index + 1 < len(combined_data.columns):
                        combined_data = combined_data.iloc[:, :last_valid_index + 1]
                    logger.info(f"Shape after dropping blank columns: {combined_data.shape}")

                    # Add the data_product_id to the final dataframe
                    combined_data['data_product_id'] = data_product_id
                    
                    # Remove duplicate rows
                    combined_data = combined_data.drop_duplicates()
                    logger.info(f"Final data shape: {combined_data.shape}")

                return combined_data

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise