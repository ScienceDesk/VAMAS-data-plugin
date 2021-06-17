##  Required imports
import matplotlib; matplotlib.use('Agg')
from sdesk.proc import io
from VAMAS import parseVAMAS
##


def extract_vamas_data_and_meta(block):
    jHeader = dict()
    jInfo = dict()
    column_names = []; units = []
    for key in list(block.keys())[:-1]: # except last key which is the numerical data
        jHeader[key] = block[key]

    if block['scan_mode'] == 'REGULAR':
        columnX = block['abscissa_label']
        column_names.append(columnX) # if a column X was created, add its label
        units.append(block['abscissa_units'])
        
    column_names += (block['corresponding_variables'])  
    units.append(block['corresponding_variables_units']) 
    data = block['data_values']

    jInfo['columnNames'] = column_names
    jInfo['columnX'] = columnX
    jInfo['units'] = units
    return jHeader, jInfo, data


def json_to_text(json_data):
    text = "HEADER\n"
    for key in json_data:
        text += "{0}: {1}\n".format(key, json_data[key])
    text += "\n"
    return text


# Define your method main()
def main():
    # Load input file
    input_metadata = io.get_input_metadata()
    files = io.get_input_files(input_metadata)
    sdesk_input_file = files[0]
    file_metadata = input_metadata[0]

    # Process input file and produces results
    output_files = []
    with open(sdesk_input_file.path(),'r') as fp:
        vamas_data = parseVAMAS(fp)
        for dict_data in vamas_data['blocks']:
            jHeader, jInfo, data = extract_vamas_data_and_meta(dict_data)
            output_files.append({"name": '{}.txt'.format(dict_data['block_identifier']),
                                 "columns": jInfo['columnNames'],
                                 "data": data,
                                 "header": json_to_text(jHeader)
                                 })

    # Create output files derived from the processing of input file
    for out_file in output_files:
        sdesk_output_file = io.create_output_file(out_file["name"])
        io.write_tsv_file(sdesk_output_file.path(), out_file['columns'], out_file['data'],  out_file['header'])


# Call method main()
main()
