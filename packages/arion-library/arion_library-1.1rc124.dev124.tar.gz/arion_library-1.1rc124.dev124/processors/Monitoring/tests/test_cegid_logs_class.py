from ..lib.CegidLogProcessor import CegidLogProcessor
import pytest
import pandas as pd
import logging
# Configure logging
logging.basicConfig(filename='logfile.log', 
                    format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture
def processor():
    csv_file_path = "TransformedItems-04-06-2024_10-10.csv"
    log_file_path = "LOG-20240604103045.TXT"
    output_csv_path = "merged_output3.csv"
    return CegidLogProcessor(csv_file_path, log_file_path, output_csv_path)


def test_main(processor, caplog):  
    result = processor.main()
    logging.warning("Test result: %s", result)

    assert isinstance(result, pd.DataFrame) or isinstance(result, str)
    for record in caplog.records:
        print(record.message)