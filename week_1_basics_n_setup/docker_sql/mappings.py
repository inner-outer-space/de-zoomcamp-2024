# DEFINE MAPPING DICTIONARY
# For analysis purposes the 'store and forward flag' will be converted from Y/N to 1/2  
# a mapping is added here to convert back 

mapping_dict = {
    "vendor_id": {
        1: "Creative Mobile Technologies",
        2: "VeriFone"
    },
    "rate_code": {
        1: "Standard rate",
        2: "JFK",
        3: "Newark",
        4: "Nassau or Westchester",
        5: "Negotiated fare",
        6: "Group ride"
    },
    "store_and_fwd_flag": {
        True: "Yes",
        False: "No"
    },
    "payment_type": {
        1: "Credit card",
        2: "Cash",
        3: "No charge",
        4: "Dispute",
        5: "Unknown",
        6: "Voided trip"
    }
    "day_of_week": {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
}

# Example usage:
# print(mapping_dict["vendor_id"].get(1, "Unknown"))
# print(mapping_dict["vendor_id"][2])
# print(mapping_dict["payment_type"][3])  