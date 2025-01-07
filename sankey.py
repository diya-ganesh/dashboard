import plotly.graph_objects as go
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)

def _code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers """
    df[src] = df[src].astype(str)
    df[targ] = df[targ].astype(str)

    # Get distinct labels
    list(set(list(df[src]) + list(df[targ])))
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Get integer codes
    codes = list(range(len(labels)))

    # Create label to code mapping
    lc_map = dict(zip(labels, codes))

    # Substitute names for codes in dataframe
    df = df.replace({src: lc_map, targ: lc_map})
    return df, labels       

def make_sankey(df, *cols, vals=None, title='Winter Sports Diagram', **kwargs):
    """ Generate a sankey diagram
    df - Dataframe
    src - Source column
    targ - Target column
    vals - Values column (optional)
    optional params: pad, thickness, line_color, line_width """
    # create list
    stack_list = []

    # iterate through list of columns (minus 1 to prevent being out of index)
    # creating source and target for a column and the column after it and
    # appending it to the stack list
    for i in (range(len(cols) - 1)):
        curr_stack = df[[cols[i], cols[i + 1]]]
        curr_stack.columns = ['src', 'targ']
        stack_list.append(curr_stack)

    # concatenate the entire stack list as rows
    stacked = pd.concat(stack_list, axis=0)

    if vals:
        values = stacked[vals]
    else:
        values = [1] * len(stacked['src'])  # all 1

    stacked, labels = _code_mapping(stacked, 'src', 'targ')
    link = {'source': stacked['src'], 'target': stacked['targ'], 'value': values}

    pad = kwargs.get('pad', 50)
    thickness = kwargs.get('thickness', 50)
    line_color = kwargs.get('line_color', 'black')
    line_width = kwargs.get('line_width', 1)

    node = {'label': labels, 'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': line_width}}
    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    width = kwargs.get('width', 800)
    height = kwargs.get('height', 400)
    fig.update_layout(
        autosize=False,
        title=kwargs.get('title', title),
        width=width,
        height=height)
    return fig

def show_sankey(df, *cols, vals=None, **kwargs):
    fig = make_sankey(df, cols, vals, **kwargs)
    fig.show()