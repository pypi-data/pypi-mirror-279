"""
Provide basic method to process data describing tables
Created by Eugeniy E. Mikhailov 2024/05/27

The basic idea that we will have an *input* table
with data description and we (re)generate *output* table
based on the input table with processed rows.

If output table already have processed rows with entries different from NA
such rows are skipped.

Super handy for bulk processing data files where only a few parameters changed.
"""

import pandas as pd
import warnings

def loadInOutTables(inputFileName=None, outputFileName=None, comment=None):
    if not inputFileName:
        return None, None

    if not comment:
        comment = '#'

    tIn = pd.read_csv(inputFileName, comment=comment)
    tIn.columns = tIn.columns.str.removeprefix(' '); # clean up leading white space in columns names

    try:
        tOut=pd.read_csv(outputFileName, comment=comment)
    except Exception:
        tOut=tIn.copy(deep=True)

    return tIn, tOut

def ilocRowOrAdd(tbl, row):
    # Find similar 'row' in 'tbl', NA in both set treated as a hit.
    # if similar row not found, insert it.
    tSub = tbl[row.keys()]
    res = (tSub == row) | (tSub.isna() & row.isna() )
    res = res.all(axis=1) # which rows coincide
    if res.any():
        # we have a similar row
        i = res[res].index[0]
    else:
        # we need to create new row since tbl does not has it
        i=len(tbl)
        updateTblRowAt(tbl, i, row)
    return i

def updateTblRowAt(tbl, i, row):
    for k in row.keys():
        tbl.at[i, k] = row[k]
    return

def isRedoNeeded(row, cols2check):
    # redo is required if *all* required entries in cols2check are NA
    # or we are missing columns in cols2check list
    for c in cols2check:
        if c not in row.keys():
            return True
    if row[cols2check].isna().all():
        return True
    return False

def reflowTable(tIn, tOut, process_row_func=None, postProcessedColums=None, extraInfo=None, redo=False):
    # update tOut in place based on the inputs specified in tIn
    # effectively maps unprocess rows in to process_row_func
    # - postProcessedColums is a list of column names which need to be generated
    # - extraInfo is dictionary of additional parameter supplied to process_row_func
    # - process_row_func expected to behave like:
    #   rowOut = process_row_func(rowIn, extraInfo=userInfo)
    # - redo controls if reflow is needed unconditionally (i.e. force reflow)
    if not process_row_func:
        warnings.warn("process_row_func is not provided, exiting reflowTable")
        return
    if not postProcessedColums:
        warnings.warn("postProcessedColums are not provided, exiting reflowTable")
        return

    for index, rowIn in tIn.iterrows():
        iOut = ilocRowOrAdd(tOut, rowIn)
        rowOutBefore = tOut.iloc[iOut]

        if not (redo or isRedoNeeded(rowOutBefore, postProcessedColums) ):
            continue

        # processing data describing row
        rowOut = process_row_func(rowOutBefore, extraInfo=extraInfo)
        updateTblRowAt(tOut, iOut, rowOut)

