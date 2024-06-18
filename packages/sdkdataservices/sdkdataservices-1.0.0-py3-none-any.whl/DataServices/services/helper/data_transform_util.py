import logging
import pandas as pd
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DataTransformUtil:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def aggregate_response(self, response):
        values = {}
        try:
            if "GDSSDKResponse" in response:
                for item in response["GDSSDKResponse"]:
                    if item["ErrMsg"] == "":
                        if item["Function"] == "GDSP":
                            row_data = item["Rows"][0]["Row"]
                            values[item["Identifier"]] = [row_data]
                        elif item["Function"] == "GDST":
                            pair = [
                                [row, header]
                                for row, header in zip(
                                    item["Rows"][0]["Row"], item["Headers"]
                                )
                            ]
                            values[item["Identifier"]] = pair
                        elif item["Function"] == "GDSHE":
                            row_data = [
                                [row["Row"][0], row["Row"][1]]
                                for row in item["Rows"]
                            ]
                            values[item["Identifier"]] = row_data
                    else:
                        if "Identifier" in item:
                            values[item["Identifier"]] = [[item["ErrMsg"]]]
                        else:
                            values["ErrMsg"] = [[item["ErrMsg"]]]
            else:
                values = [[response]]

        except Exception as e:
            values = [[response.reason]]
        return values



    def convert_to_dataframe(self, results):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 1)
        df = pd.DataFrame(results)
        df_styled = df.style.set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]}]
        )
        return df_styled
