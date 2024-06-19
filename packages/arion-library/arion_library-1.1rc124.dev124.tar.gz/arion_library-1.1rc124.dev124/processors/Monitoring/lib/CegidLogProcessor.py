import pandas as pd
import re

from .MonitoringBase import MonitoringBase


class CegidLogProcessor(MonitoringBase):
    """
    A class to process Cegid log files and merge them with CSV data.

    Attributes:
        csv_path (str): Path to the CSV file.
        log_path (str): Path to the log file.
        output_csv_path (str): Path to save the output CSV file.
    """

    def __init__(self, csv_path, log_path, output_csv_path):
        """
        Initializes the CegidLogProcessor with the given file paths.

        Args:
            csv_path (str): Path to the CSV file.
            log_path (str): Path to the log file.
            output_csv_path (str): Path to save the output CSV file.
        """
        self.csv_path = csv_path
        self.log_path = log_path
        self.output_csv_path = output_csv_path

    def merge_error_output(self, error_output, df, warning_message):
        """
        Merges error output with the given DataFrame and adds warning messages if present.

        Args:
            error_output (pd.DataFrame): DataFrame containing error information.
            df (pd.DataFrame): DataFrame to merge with the error information.
            warning_message (str): Warning message to include in the merge.

        Returns:
            pd.DataFrame: Merged DataFrame containing error and warning information.
        """
        if error_output['Error rate per File'].iloc[0] == "100.00%" and warning_message is not None:
            merged_data = {
                'Files': [error_output['Files'].iloc[0] for _, row in df.iterrows()],
                'Rejected Lines': [';'.join(map(str, row[0:].tolist())) for _, row in df.iterrows()],
                'Reject Reasons per Line': warning_message,
                'Error rate per File': [error_output['Error rate per File'].iloc[0] for _ in df.iterrows()],
                'Success': [error_output['Success'].iloc[0] for _ in df.iterrows()]
            }
            merged_df = pd.DataFrame(merged_data)
            return merged_df

        if error_output['Error rate per File'].iloc[0] == "100.00%":
            merged_data = {
                'Files': [error_output['Files'].iloc[0] for _, row in df.iterrows()],
                'Rejected Lines': [';'.join(map(str, row[0:].tolist())) for _, row in df.iterrows()],
                'Reject Reasons per Line': [error_output['Reject Reasons per Line'].iloc[0] for _ in df.iterrows()],
                'Error rate per File': [error_output['Error rate per File'].iloc[0] for _ in df.iterrows()],
                'Success': [error_output['Success'].iloc[0] for _ in df.iterrows()]
            }
            merged_df = pd.DataFrame(merged_data)
            return merged_df

        if error_output['Error rate per File'].iloc[0] != "100.00%":
            def replace_indices(row):
                indices = row['Rejected Lines']
                corresponding_row = df.iloc[int(indices)-1]  # Fetch the corresponding row from df
                return ';'.join(corresponding_row.astype(str))  # Join the values into a single string

            error_output['Rejected Lines'] = error_output.apply(replace_indices, axis=1)
            return error_output

    def process_successful_records(self, log_data, common_value=0):
        """
        Processes the successful records from the log data.

        Args:
            log_data (str): The log data as a string.
            common_value (int, optional): A common value used in the process. Defaults to 0.

        Returns:
            pd.DataFrame: DataFrame containing the processed successful records.
        """
        log_lines = log_data.strip().split('\n')
        df = pd.DataFrame()
        file_names = []
        records_read_list = []
        records_processed_list = []
        records_integrated_list = []
        integration_errors_list = []
        output_data = [['', '', '', '', '', '']]
        
        for line in log_lines:
            file_match = re.search(r'File processing: .*\\(.*\.csv)', line)
            records_match = re.search(r'-> (\d+) record(?:s)? read', line)
            processed_match = re.search(r'-> (\d+) record(?:s)? processed', line)
            integrated_match = re.search(r'-> (\d+) integrated record(?:s)', line)
            integrated_match2 = re.search(r'-> (\d+) record(?:s)? integrated', line)

            if file_match:
                file_name = file_match.group(1)
                file_names.append(file_name)
            elif records_match:
                records_read = int(records_match.group(1))
                records_read_list.append(records_read)
            elif processed_match:
                records_processed = int(processed_match.group(1))
                records_processed_list.append(records_processed)
            elif integrated_match:
                records_integrated = int(integrated_match.group(1))
                records_integrated_list.append(records_integrated)
            elif integrated_match2:
                records_integrated = int(integrated_match2.group(1))
                records_integrated_list.append(records_integrated)

            if line.strip().startswith("--->") or line.strip().startswith("---->"):
                for file_name in file_names:
                    for records_read, records_processed, records_integrated, integration_errors in zip(records_read_list, records_processed_list, records_integrated_list, integration_errors_list):
                        output_data.append([file_name, records_read, records_processed, records_integrated, integration_errors, False])

        data = []
        if records_read_list and records_integrated_list:
            for i in range(len(file_names)):
                if records_read_list[i] == records_integrated_list[i]:
                    data.append([file_names[i], '', '', '0', 'True'])
                
            columns = ["Files", "Rejected Lines", "Reject Reasons per Line", "Error rate per File", "Success"]
            df = pd.DataFrame(data, columns=columns)

        return df

    def process_error_records(self, log_data):
        """
        Processes the error records from the log data.

        Args:
            log_data (str): The log data as a string.

        Returns:
            tuple: A tuple containing the formatted DataFrame and the warning message.
        """
        log_lines = log_data.strip().split('\n')
        file_name = None
        error_id = None
        error_message = None
        records_read = None
        records_processed = None
        records_integrated = None
        integration_errors = None
        error_data = []
        warning_message = None

        for line in log_lines:
            file_match = re.search(r'File processing: .*\\(.*\.csv)', line)
            error_match = re.search(r'^error\s+-\s+(\d+)\s+-\s+(.*?)\s*$', line)
            system_error_match = re.search(r'^system error\s+-\s+(\d+)\s+-\s+(.*?)\s*$', line)
            records_match = re.search(r'-> (\d+) record(?:s)? read', line)
            processed_match = re.search(r'-> (\d+) record(?:s)? processed', line)
            integrated_match = re.search(r'-> (\d+) integrated record(?:s)', line)
            errors_match = re.search(r'-> (\d+) record(?:s)? (?:contain|has) errors', line)
            integrated_match2 = re.search(r'-> (\d+) record(?:s)? integrated', line)
            warning_match = re.search(r'^Warning\s+-\s+(\d+)\s+-\s+(.*?)\s*$', line)

            if file_match:
                file_name = file_match.group(1)
            elif records_match:
                records_read = int(records_match.group(1))
            elif processed_match:
                records_processed = int(processed_match.group(1))
            elif integrated_match:
                records_integrated = int(integrated_match.group(1))
            elif integrated_match2:
                records_integrated = int(integrated_match2.group(1))
            elif warning_match:
                error_id = warning_match.group(1)
                warning_message = warning_match.group(2).strip()
                warning_message = warning_message.split('       -')[-1]
                warning_message = warning_message.replace('--->', '').strip()
                error_data.append([file_name, error_id, '', records_read, records_processed, records_integrated, integration_errors])
            elif errors_match:
                integration_errors = int(errors_match.group(1))
            elif system_error_match:
                error_id = system_error_match.group(1)
                error_message = system_error_match.group(2).strip()
                error_message = error_message.split('       -')[-1]
                error_message = error_message.replace('--->', '').strip()
                error_data.append([file_name, error_id, error_message, records_read, records_processed, records_integrated, integration_errors])
            elif error_match:
                error_id = error_match.group(1)
                error_message = error_match.group(2).strip()
                error_message = error_message.split('       -')[-1]
                error_message = error_message.replace('--->', '').strip().replace(';', '').replace('.', '')
                error_data.append([file_name, error_id, error_message, records_read, records_processed, records_integrated, integration_errors])
            else:
                not_recovered = re.search(r'^warning\s+-\s+(\d+)\s+-\s+.*?--->  records of type (\w+) are not recovered\s*$', line)
                if not_recovered:
                    error_id = not_recovered.group(1)
                    error_message = f'records of type {not_recovered.group(2).strip()} are not recovered'
                    error_data.append([file_name, error_id, error_message, records_read, records_processed, records_integrated, integration_errors])

            df = pd.DataFrame(error_data, columns=["File Name", "Error ID", "Error Message", "Records Read", "Records Processed", "Records Integrated", "Integration Errors"])
            common_value = 0
            df["Records Read"] = records_read if records_read is not None else common_value
            df["Records Processed"] = records_processed if records_processed is not None else common_value
            df["Records Integrated"] = records_integrated if records_integrated is not None else common_value
            df["Integration Errors"] = integration_errors if integration_errors is not None else common_value

        if records_read == integration_errors and warning_message is not None:
            df['Error Message'] = warning_message

        agg_functions = {
            "File Name": "first",
            "Error Message": "/".join,
            "Records Read": "first",
            "Records Processed": "first",
            "Records Integrated": "first",
            "Integration Errors": "first",
        }

        result_df = df.groupby("Error ID").agg(agg_functions).reset_index()
        result_df["Error Rate"] = ((result_df["Records Read"] - result_df["Records Integrated"]) / result_df["Records Read"]).apply(lambda x: "{:.2%}".format(x))
        result_df["Success"] = (result_df["Records Read"] == result_df["Records Integrated"]).map({True: "True", False: "False"})

        formatted_data = {
            "Files": result_df["File Name"],
            "Rejected Lines": result_df["Error ID"],
            "Reject Reasons per Line": result_df["Error Message"],
            "Error rate per File": result_df["Error Rate"],
            "Success": result_df["Success"],
        }

        formatted_df = pd.DataFrame(formatted_data)
        
        return formatted_df, warning_message

    def main(self):
        """
        Main method to read, process, and merge CSV and log files, and save the output to a CSV file.

        Returns:
            pd.DataFrame or str: The merged DataFrame or an error message if files are not found.
        """
        try:
            df_csv = pd.read_csv(self.csv_path, sep='|')
        except FileNotFoundError:
            return "CSV file not found."

        try:
            with open(self.log_path, 'r', encoding='utf-16') as log_file:
                log_data = log_file.read()
        except FileNotFoundError:
            return "Log file not found."

        success_df = self.process_successful_records(log_data)

        error_df, warning_message = self.process_error_records(log_data)

        if not error_df.empty or warning_message:
            merged_df = self.merge_error_output(error_df, df_csv, warning_message)
        else:
            merged_df = pd.DataFrame()

        if not merged_df.empty:
            merged_df.to_csv(self.output_csv_path, index=False)
            print(f"Merged dataframe saved to {self.output_csv_path}")

        return merged_df
    



    
