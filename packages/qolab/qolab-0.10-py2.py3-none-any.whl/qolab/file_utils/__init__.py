import platform
import re
import os
from datetime import date

def filename2os_fname( fname ):
    # filename2os_fname translate Win or Linux fname to OS dependent style
    # takes in account the notion of 'Z:' drive on different systems
    # Z:\dir1\dir2\file   <==> /mnt/qol_grp_data/dir1/dir2/file
    if platform.system() == 'Windows':
        fname = re.sub('/mnt/qol_grp_data', 'Z:', fname)
    else:
        fname = re.sub('Z:', '/mnt/qol_grp_data', fname)
        fname = re.sub(r'\\', '/', fname)

    fname = os.path.normpath(fname)
    return (fname)


def get_runnum(data_dir):
    # For the provided data_dir:
    #  reads, increments data counter and saves it back.
    # If nesessary creates counter file and full path to it.
    # example
    #  get_runnum('Z:\Ramsi_EIT\data\')
    #  get_runnum('/mnt/qol_grp_data/data')
    data_dir = filename2os_fname( data_dir );
    if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    if not os.path.isdir(data_dir):
        print(f"ERROR: cannot create directory for data: {data_dir}")
        print("Will use current dir for storage")
        data_dir = "."

    runnumpath = os.path.join(data_dir, 'autofile')
    # convert to OS dependent way
    runnumpath = filename2os_fname( runnumpath );

    if not os.path.exists(runnumpath):
            os.mkdir(runnumpath)
    runnum_file = os.path.join(runnumpath, 'runnum.dat');
    runnum_file = filename2os_fname( runnum_file );

    run_number = 0
    if os.path.isfile(runnum_file):
        with open(runnum_file, 'r') as f:
            content = f.readlines()
            run_number = int(content[0])
            f.close()

    # Increment it and fold if needed
    run_number = run_number + 1;
    # Important: we are using five digit counters to synchronize
    # with qol_get_next_data_file.m
    if run_number > 99999:
        run_number = 0

    with open(runnum_file, 'w') as f:
        f.write(f'{run_number}')
        f.close()
    return(run_number)

def get_next_data_file(prefix, savepath, run_number=None, datestr=None, date_format='%Y%m%d', extention='dat'):
    if run_number is None:
        run_number = get_runnum( savepath )
    today = date.today()
    if datestr is None:
        datestr = today.strftime(date_format)
    fname = os.path.join(savepath, f'{prefix}_{datestr}_{run_number:05d}.{extention}')
    return(fname)

def save_table_with_header(fname, data, header='', comment_symbol='%', skip_headers_if_file_exist=False, item_format='e', item_separator='\t'):
    # itemFormat examples: 'e', '.15e', 'f'
    fname = filename2os_fname(fname)
    file_exist_flag = os.path.exists(fname)
    item_format=str.join('', ['{', f':{item_format}', '}'])
    with open(fname, 'a') as f:
        if not (file_exist_flag and skip_headers_if_file_exist):
            for l in header:
                f.write(f'{comment_symbol} {l}\n')
        if data is not None:
            for r in data:
                l=item_separator.join( map(item_format.format, r))
                f.write(l)
                f.write('\n')
        f.close()
    return(fname)

