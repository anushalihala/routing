from search import *
from calculate_distance import *

def get_graph_from_json_string(json, mode="bike", metadata=None):
    if(mode=="bike"):
        (locations_dict, edges_dict) = get_graph_from_bikes_json(json, metadata)
    elif(mode=="bus"):
        print("Processing bus routes")
        (locations_dict, edges_dict) = get_graph_from_buses_json(json, metadata)
    else:
        print("Please send valid mode")
        
    return (locations_dict, edges_dict)

def get_graph_from_bikes_json(json, metadata=None):
    if(metadata is None):
        print("meta data is none")
        metadata = dict()
        metadata["id"] = "number"
        print("Using default metadata object")
    
    locations_dict = {}
    for bike_stand in json:
        id = bike_stand[metadata["id"]]
        locations_dict[id] = (bike_stand["position"]["lat"], bike_stand["position"]["lng"])

    edges_dict = get_mesh_edges(locations_dict)
    return (locations_dict, edges_dict)
    

def get_graph_from_buses_json(json, metadata=None):
    if(metadata is None):
        print("meta data is none")
        metadata = dict()
        metadata["id"] = "stopid"
        print("Using default metadata object")
    
    locations_dict = {}
    for bus_stand in json:
        id = bus_stand[metadata["id"]]
        locations_dict[id] = (bus_stand["latitude"], bus_stand["longitude"])

    edges_dict = get_bus_edges(locations_dict, json, metadata)
    return (locations_dict, edges_dict)
    
def get_bus_edges(locations_dict, json, metadata):
    bus_routes = {}
    
    print("Computing bus routes")
    for bus_stop in json:
        id = bus_stop[metadata["id"]]
        for op_obj in bus_stop["operators"]:
            op_name = op_obj["name"]
            for route_name in op_obj["routes"]:
                route_id = op_name+route_name
                bus_routes[route_id] = bus_routes.get(route_id, []) + [str(id)]
                
    # print(bus_routes)
   
    print("Computing bus route edges")   
    edges_dict = {}
    for id, bus_route_list in bus_routes.items():
        print(id)
        # print(bus_route_list)
        for stop_id in bus_route_list:
            try:
                edges_dict[stop_id]
            except KeyError:
                edges_dict[stop_id] = {}
                
            for other_stop_id in bus_route_list:
                if(other_stop_id==stop_id):
                    continue
                    
                edges_dict[stop_id][other_stop_id] = get_distance(locations_dict[stop_id], locations_dict[other_stop_id])
                     
    return edges_dict
    
    
    
def get_mesh_edges(locations_dict):
    # Parameters
    # locations_dict is a dictionary of location tuples 
    # edges_dict is a dictionary of dictionaries of distances.
    
    print("Computing mesh edges")
        
    edges_dict = {}
    for k1,v1 in locations_dict.items():
        for k2,v2 in locations_dict.items():
            if(str(k1)==str(k2)):
                continue
            # print(k1,v1,k2,v2)
            k1 = str(k1)
            k2 = str(k2)
            try:
                # if edge exists already
                edges_dict[k2][k1]
                continue
            except KeyError:
                try: 
                    # if node exists already
                    edges_dict[k1]
                except KeyError:
                    edges_dict[k1] = dict()
                finally:
                    edges_dict[k1][k2] = get_distance(v1, v2)
           
    # print(edges_dict)
    return edges_dict

    





    