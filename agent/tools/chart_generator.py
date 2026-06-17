import plotly.express as px
import pandas as pd
from langchain.tools import Tool

_dataframe = None
_last_chart = None

def reset_chart():
    global _last_chart
    _last_chart = None

def set_dataframe(df: pd.DataFrame):
    global _dataframe
    _dataframe = df

def get_last_chart():
    return _last_chart

def generate_chart(instruction: str) -> str:
    global _dataframe, _last_chart
    
    if _dataframe is None:
        return "Error: Koi CSV upload nahi hua."
    
    try:
        df = _dataframe
        instruction_lower = instruction.lower()
        num_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
        cat_cols = [c for c in df.columns if df[c].dtype == 'object']

        # Column names extract karo instruction se
        x_col = None
        y_col = None
        
        for col in df.columns:
            if col.lower() in instruction_lower:
                if df[col].dtype == 'object' and x_col is None:
                    x_col = col
                elif df[col].dtype in ['int64', 'float64'] and y_col is None:
                    y_col = col

        if "bar" in instruction_lower:
            if x_col and y_col:
                agg_df = df.groupby(x_col)[y_col].mean().reset_index()
                fig = px.bar(agg_df, x=x_col, y=y_col,
                           title=f"Average {y_col} by {x_col}",
                           color=x_col)
            elif x_col and num_cols:
                agg_df = df.groupby(x_col)[num_cols[0]].mean().reset_index()
                fig = px.bar(agg_df, x=x_col, y=num_cols[0],
                           title=f"Average {num_cols[0]} by {x_col}",
                           color=x_col)
            elif cat_cols and num_cols:
                agg_df = df.groupby(cat_cols[0])[num_cols[0]].mean().reset_index()
                fig = px.bar(agg_df, x=cat_cols[0], y=num_cols[0],
                           title=f"Average {num_cols[0]} by {cat_cols[0]}",
                           color=cat_cols[0])
            else:
                return "Bar chart ke liye column names specify karo."

        elif "pie" in instruction_lower:
            if x_col and y_col:
                agg_df = df.groupby(x_col)[y_col].sum().reset_index()
                fig = px.pie(agg_df, names=x_col, values=y_col,
                           title=f"{y_col} distribution by {x_col}")
            elif cat_cols and num_cols:
                agg_df = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
                fig = px.pie(agg_df, names=cat_cols[0], values=num_cols[0],
                           title=f"{num_cols[0]} distribution")
            else:
                return "Pie chart ke liye column names specify karo."

        elif "line" in instruction_lower:
            if y_col:
                fig = px.line(df, y=y_col, title=f"{y_col} trend")
            elif num_cols:
                fig = px.line(df, y=num_cols[0], title=f"{num_cols[0]} trend")
            else:
                return "Line chart ke liye numeric column specify karo."

        elif "scatter" in instruction_lower:
            if len(num_cols) >= 2:
                fig = px.scatter(df, x=num_cols[0], y=num_cols[1],
                               title=f"{num_cols[0]} vs {num_cols[1]}")
            else:
                return "Scatter plot ke liye 2 numeric columns chahiye."

        else:
            if cat_cols and num_cols:
                agg_df = df.groupby(cat_cols[0])[num_cols[0]].mean().reset_index()
                fig = px.bar(agg_df, x=cat_cols[0], y=num_cols[0],
                           title=f"Average {num_cols[0]} by {cat_cols[0]}",
                           color=cat_cols[0])
            else:
                return "Chart type specify karo: bar, pie, line, scatter."

        _last_chart = fig
        return f"Chart successfully created!"

    except Exception as e:
        return f"Chart Error: {str(e)}"

chart_tool = Tool(
    name="Chart_Generator",
    description="""Create visual charts from CSV data.
    Specify chart type (bar/pie/line/scatter) and column names.
    Examples:
    - "bar chart of Purchase Amount by Category"
    - "pie chart of Sales by Region"
    - "line chart of Revenue"
    """,
    func=generate_chart
)