from functools import reduce
import re
from typing import Any, Tuple, List
import base64

from pandas import DataFrame
import pandas as pd
import decimal

from .. import metamodel as m

#--------------------------------------------------
# Constants
#--------------------------------------------------

UNIXEPOCH = 62135683200000
MILLISECONDS_PER_DAY = 24 * 60 * 60 * 1000

def format_columns(result_frame:DataFrame, types:List[str]):
    for i, col in enumerate(result_frame.columns):
        if "UInt128" in types[i]:
            result_frame[col] = result_frame[col].apply(lambda x: base64.b64encode(x.tobytes()).decode()[:-2])
        elif "FixedDecimal" in types[i]:
            decimal_info = re.search(r"FixedDecimal\{Int(\d+), (\d+)\}", types[i])
            if decimal_info:
                bits = int(decimal_info.group(1))
                scale = int(decimal_info.group(2))
                if bits == 128:
                    result_frame[col] = result_frame[col].apply(lambda x: (decimal.Decimal(str((int(x[1]) << 64) + int(x[0]))) if x[1] > 0 else decimal.Decimal(str(x[0]))) / (10 ** scale))
                else:
                    result_frame[col] = result_frame[col].apply(lambda x: decimal.Decimal(str(x)) / (10 ** scale))
        elif "Int128" in types[i]:
            result_frame[col] = result_frame[col].apply(lambda x: (int(x[1]) << 64) + int(x[0]) if x[1] > 0 else x[0])
        elif "Missing" in types[i]:
            result_frame[col] = result_frame[col].apply(lambda x: None)
        elif types[i] == "Dates.DateTime":
            result_frame[col] = pd.to_datetime(result_frame[col] - UNIXEPOCH, unit="ms")
        elif types[i] == "Dates.Date":
            result_frame[col] = pd.to_datetime(result_frame[col] * MILLISECONDS_PER_DAY - UNIXEPOCH, unit="ms")
    return result_frame

def format_results(results, task:m.Task) -> Tuple[DataFrame, List[Any]]:
    data_frame = DataFrame()
    if len(results.results):
        has_cols = []
        for result in results.results:
            types = [t for t in result["relationId"].split("/") if t != "" and not t.startswith(":")]
            result_frame:DataFrame = result["table"].to_pandas()
            result_frame = format_columns(result_frame, types)

            result["table"] = result_frame
            if ":output/:cols" in result["relationId"]:
                col_ix = int(re.search(r":col([0-9]+)", result["relationId"]).group(1))
                key_cols = [f"id{i}" for i in range(0, len(result_frame.columns) - 1)]
                result_frame.columns = [*key_cols, f"v{col_ix}"]
                if col_ix < len(has_cols):
                    has_cols[col_ix] = pd.concat([has_cols[col_ix], result_frame], ignore_index=True)
                else:
                    has_cols.append(result_frame)
            elif ":output" in result["relationId"]:
                data_frame = pd.concat([data_frame, result_frame], ignore_index=True)
        if len(has_cols):
            key_cols = [f"id{i}" for i in range(0, len(has_cols[0].columns) - 1)]
            df_wide_reset = reduce(lambda left, right: pd.merge(left, right, on=key_cols, how='outer'), has_cols)
            data_frame = df_wide_reset.drop(columns=key_cols)
            data_frame.sort_values(by=[str(c) for c in data_frame.columns], ascending=[True] * len(data_frame.columns), inplace=True)
            data_frame = data_frame.reset_index(drop=True)

            # data_frame = df_wide
        ret_cols = task.return_cols() if task else []
        if len(ret_cols) and len(data_frame.columns) == len(ret_cols):
            data_frame.columns = task.return_cols()[0:len(data_frame.columns)]
    return (data_frame, results.problems)