from api.ml.common_utils import *

# TODO: Add these to config file and read at the startup
supported = ['Total_Revenue', 'Total_Taxes', 'Total_Income_Taxes', 'Total_Hospital_Total_Exp', 'Total_Highways_Tot_Exp',
             'Libraries_Total_Expend', 'Sewerage_Total_Expend', 'Unemp_Comp_Total_Exp,Total_Util_Total_Exp', 'Total_Cash___Securities']


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    distances, indices = nbrs.kneighbors(table)

    return indices


def get_similar_states(id, attribute, num=2):
    if id not in state_id_name_map.keys():
        return {"ERROR": "State id unknown"}
    features = ['Year', 'ID']
    features.append(attribute)
    _df = df[features]
    pivoted = _df.pivot_table(index='ID', columns='Year', values=attribute)
    pivoted = pivoted.sort_index()
    indices = getNearest(pivoted, num+1)
    id_ = pivoted.index.tolist().index(id)

    neighbors = indices[id_]
    similar_states = pivoted.index[neighbors].tolist()[1:]
    response = []
    for state in similar_states:
        data = {}
        data["name"] = state_id_name_map[state][0]
        data["id"] = state
        response.append(data)
    # plot_info = plot_similar_states(id, similar_states, attribute)
    return {"similar_states ": response}
