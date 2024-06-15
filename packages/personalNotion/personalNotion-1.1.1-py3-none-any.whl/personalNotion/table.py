from custom_development_standardisation import *
# outcome = extract_core_data_from_all_blocks(outcome["results"])


def extract_core_table_data(raw):
    results = raw["results"]
    
    if not isinstance(results, list):
        return generate_outcome_message("error",f'Expected array type, but type(${type(results)}) was received',the_type="custom")
    
    table_row_data = []
    for i in results:
        current_row = []
        if i["type"] != "table_row":
            return generate_outcome_message("error",f'non-table row identified. Expect all items in array of be of type table row...',the_type="custom")

        table_row = i["table_row"]
        row_cell_array = table_row["cells"]
        if row_cell_array == None:
            return generate_outcome_message("error",'Expect cells key, but there is none...',the_type="")

        

        for cell in row_cell_array:
            
            if len(cell) == 0:
                current_row.append("")
                continue

            core_obj = cell[0]
            the_type = core_obj["type"]
            content = core_obj[the_type]["content"]
            current_row.append(content)
        
        table_row_data.append(current_row)

    return generate_outcome_message("success",table_row_data)

    # if results["table"]
    # # Display page content
    # if i["type"] == "table":
    #     for key,value in i.items():
    #         print(key,":",value)
    # Display table items
        # for j,value in i["table_row"].items():
        #     for k in value:
        #         print(k)




# id = "cd4f57fe-a769-4385-a71a-e09a82f99ed6"       # table id
# # id = "2e03a285ec5b48808dc8f212770b5902"             # page
# outcome = extract_all_blocks_from_page(id)
# # print("HERE: ",outcome["results"])
# print(extract_core_table_data(outcome))
# for i in outcome["results"]:
#     print(i)
    # # Display page content
    # if i["type"] == "table":
    #     for key,value in i.items():
    #         print(key,":",value)
    # Display table items
    # for j,value in i["table_row"].items():
    #     for k in value:
    #         print(k)



# print(generate_outcome_message("error","something",the_type="others"))

# def get_table_data(table_id):
    