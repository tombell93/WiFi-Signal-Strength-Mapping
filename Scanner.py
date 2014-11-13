#!/usr/bin/env python
# Based on an example by Hugo Chargois

'''''''''''''''
Authored by Tom Bell
MWR InfoSecurity
'''''''''''''''

import sys
import subprocess 

def get_name(cell):
    return matching_line(cell,"ESSID:")[1:-1]

def get_quality(cell):
    quality = matching_line(cell,"Quality=").split()[0].split('/')
    return str(int(round(float(quality[0]) / float(quality[1]) * 100))).rjust(3) + " %"

def get_power(cell):
    power = matching_line(cell,"Quality=").split()[2].split('=')[1]
    return power

def get_channel(cell):
    return matching_line(cell,"Channel:")

def get_encryption(cell):
    enc=""
    if matching_line(cell,"Encryption key:") == "off":
        enc="Open"
    else:
        for line in cell:
            matching = match(line,"IE:")
            if matching!=None:
                wpa=match(matching,"WPA Version ")
                if wpa!=None:
                    enc="WPA v."+wpa
                wpa2=match(matching,"IEEE 802.11i/WPA2 Version ")
                if wpa2!=None:
                    #enc="WPA2 v."+wpa2
                    enc="WPA2"
        if enc=="":
            enc="WEP"
    return enc

def get_bssid(cell):
    return matching_line(cell,"Address: ")

def get_essid(cell):
    essid = matching_line(cell,"ESSID:")
    essid = essid.replace('"','')
    return essid

'''
Dictionary of rules that will be applied to the description of each cell. 
The key is a function defined above.
'''

rules={"Name":get_name,
       "Quality":get_quality,
       "Power":get_power,
       "Channel":get_channel,
       "Encryption":get_encryption,
       "ESSID":get_essid,
       "BSSID":get_bssid,
       }

''' 
Choose how to sort the table
'''

def sort_cells(cells):
    sortby = "Quality" # Can be changed to column to be sorted by 
    reverse = True
    cells.sort(None, lambda el:el[sortby], reverse)

'''
Here choose which columns to display when printing
'''

columns=["Name","ESSID", "BSSID","Quality","Power", "Channel","Encryption"]

def matching_line(lines, keyword):
    """Returns the first matching line in a list of lines. See match()"""
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    """If the first part of line (modulo blanks) matches keyword,
    returns the end of that line. Otherwise returns None"""
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

def parse_cell(cell):
    """Applies the rules to the bunch of text describing a cell and returns the
    corresponding dictionary"""
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

def print_table(table):
    widths=map(max,map(lambda l:map(len,l),zip(*table))) #functional magic

    justified_table = []
    for line in table:
        justified_line=[]
        for i,el in enumerate(line):
            justified_line.append(el.ljust(widths[i]+2))
        justified_table.append(justified_line)
    
    for line in justified_table:
        for el in line:
            print el,
        print

def print_cells(cells):
    table=[columns]
    for cell in cells:
        cell_properties=[]
        for column in columns:
            cell_properties.append(cell[column])
        table.append(cell_properties)
    print_table(table)

def scan(printData = False, sort = True):

    proc = subprocess.Popen('iwlist scan 2>/dev/null', shell=True, stdout=subprocess.PIPE, ) 
    stdout_str = proc.communicate()[0] 

    """Pretty prints the output of iwlist scan into a table"""
    cells=[[]]
    parsed_cells=[]

    stdout_list=stdout_str.split('\n') 

    for line in stdout_list:
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())

    cells=cells[1:]

    for cell in cells:
        parsed_cells.append(parse_cell(cell))

    if sort:
        sort_cells(parsed_cells)
    
    if printData:
        print_cells(parsed_cells)

    return parsed_cells

if __name__ == '__main__':
    scan()