import pandas as pd
from langchain.tools import Tool

_dataframe = None

def set_dataframe(df: pd.DataFrame):
    global _dataframe
    _dataframe = df

def get_dataframe():
    return _dataframe

def run_python_code(code: str) -> str:
    global _dataframe
    if _dataframe is None:
        return "Error: Koi CSV upload nahi hua."
    local_vars = {"df": _dataframe, "pd": pd}
    try:
        exec(code, {"pd": pd}, local_vars)
        for var in ["result", "output", "ans"]:
            if var in local_vars:
                return str(local_vars[var])
        output_vars = {k: v for k, v in local_vars.items()
                      if k not in ["df", "pd"] and not k.startswith("_")}
        if output_vars:
            last_key = list(output_vars.keys())[-1]
            return str(output_vars[last_key])
        return "Code executed successfully."
    except Exception as e:
        return f"Error: {str(e)}"

python_repl_tool = Tool(
    name="Python_REPL",
    description="""Execute Python/Pandas code on CSV data.
    DataFrame available as 'df'. Store output in 'result' variable.
    Example: result = df.groupby('Category')['Sales'].sum()""",
    func=run_python_code
)