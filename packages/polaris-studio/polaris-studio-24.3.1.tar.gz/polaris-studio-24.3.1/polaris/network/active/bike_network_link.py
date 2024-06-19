get_bike_links_qry = """Select bike_link, from_node, to_node, "length", ref_link, asbinary(geo) from Transit_Bike
                       where ref_link>0 AND ref_link not NULL"""
