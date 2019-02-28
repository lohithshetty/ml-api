from api.ml.common_utils import *


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    _, indices = nbrs.kneighbors(table)
    return indices


def get_similar_states(id, attribute, num=2):
    if id not in state_id_name_map.keys():
        return {"ERROR": "State id unknown"}, 404
    if attribute not in supported_attributes:
        return {"ERROR": "Attribute is not supported"}, 400
    features = ['Year', 'ID']
    features.append(attribute)
    _df = state_df[features]
    pivoted = _df.pivot_table(index='ID', columns='Year', values=attribute)
    pivoted = pivoted.sort_index()
    indices = getNearest(pivoted, num+1)
    id_ = pivoted.index.tolist().index(id)

    neighbors = indices[id_]
    similar_states = pivoted.index[neighbors].tolist()[1:]
    response = []
    for state in similar_states:
        data = {}
        data["attribute_name"] = state_id_name_map[state][0]
        data["state_id"] = state
        response.append(data)
    return response, 200
