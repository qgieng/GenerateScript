##Generate Script sql scripts

import os
import csv

TABLE_NAME = ""
TO_DATE = "to_date({},'DD-MON-RR')"

DATE_MAP = {
    '01': 'JAN', 
    '02':'FEB',
    '03': 'MAR',
    '04': 'APR',
    '05': 'MAY',
    '06': 'JUN',
    '07': 'JUL',
    '08': 'AUG',
    '09': 'SEP',
    '10': 'OCT',
    '11': 'NOV',
    '12': 'DEC'}
    


def add_headers():
    ALTER = "ALTER SESSION SET CURRENT_SCHEMA = REFERENCES; \n"
    REMINSERT = "REM INSERTING into " + TABLE_NAME + " \n" 
    DEFINE = "SET DEFINE OFF; \n"
    return ALTER + REMINSERT+ DEFINE

def combine_schema(schema, values):
    result  = schema + values + ';\n'
    
    return result

def generate_insert_schema(columns:str):
    result = "Insert into "  + TABLE_NAME + "("
    for i in range(len(columns)):
        if i == (len(columns)-1):
            result+= columns[i] + ") values "
        else:
            result += columns[i] + ","
    
    
    return result
    
def format_date(date_str):
    if date_str == 'null':
        return date_str
    beginning  = date_str.split(' ')[0].split('/')

    DATE_FORMAT = "'{DATE}-{MONTH}-{YEAR}'".format(DATE = beginning[1], 
                                                    MONTH = DATE_MAP[beginning[0]],
                                                    YEAR = beginning[2][2:])
    
    return TO_DATE.format(DATE_FORMAT)


def generate_value_format(columns:str , indexes, str_line):
    result = "( " 
    for i in range(len(columns)):
        
        if i == (len(columns)-1):
            result+= "\'{" + columns[i]+ "}\')"
        elif i == 32  or i == 52:
            result+= "{" + columns[i]+ "},"
        elif str_line[i] == 'null':
            result+= "{" + columns[i]+ "},"
        else:
            result+= "\'{" + columns[i]+ "}\',"
    
    return result
    
def generate_format_body(columns:str):
    result = ""
    for i in range(len(columns)):
        if i == (len(columns)-1):
            result+= columns[i] + "= str_line[{c}]\n".format(c=i) 
        else:
            result+= columns[i] + "= str_line[{c}] ,\n".format(c=i) 

    return result
    

def generate_schema(columns, str_line):
    for i,values in enumerate(str_line):
        #print(i, values)
        if values == '':
            str_line[i] = 'null'
    DATE_INDEXES = [32,52],
    VALUE_COLUMN_FORMAT = generate_value_format(columns, DATE_INDEXES, str_line);
    #print(VALUE_COLUMN_FORMAT)
    FORMAT_BODY = generate_format_body(columns);
    #print(FORMAT_BODY)
    
           
    return VALUE_COLUMN_FORMAT.format(...)
    
    

def runScript():
    PATH_TO_DIRECTORY = os.getcwd()
    FILE_NAME = "NAME.csv"
    
    PATH_TO_FILE =PATH_TO_DIRECTORY+"\\" +FILE_NAME
    file = open(PATH_TO_FILE, "r")
    csvfile = csv.reader(file)
    columns = next(csvfile)
    INSERT_INTO_SCHEMA = generate_insert_schema(columns)
    WRITE_FILE_NAME = 'OUTPUTNAME.sql'
    
    WRITE_FILE = open(WRITE_FILE_NAME, 'w')
    WRITE_FILE.write(add_headers())
    
    c= 0
    
    
    for row in csvfile:
        WRITE_FILE.write(combine_schema(INSERT_INTO_SCHEMA, generate_schema(columns,row)))
        #if(c<20):
        #    print((combine_schema(INSERT_INTO_SCHEMA, generate_schema(columns,row))))
        #    c+=1
    
    WRITE_FILE.write('\n\ncommit;\n')
    WRITE_FILE.close()
            
if __name__ == "__main__":
	runScript();
    
    