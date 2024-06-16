import re

import numpy as np

from quakeio.core import QuakeSeries
from quakeio.utils.parseutils import open_quake

RE_TIME_STEP = re.compile(r"DT=\s+(.*)SEC")

def ReadRecordAT2(inFilename):
    """
    A procedure which parses a ground motion record from the PEER
    strong motion database by finding dt in the record header, then
    echoing data values to the output file.

    Formal arguments
       inFilename -- file which contains PEER strong motion record
       outFilename -- file to be written in format G3 can read
    Return values
       dt -- time step determined from file header
       nPts -- number of data points from file header

    Assumptions
       The header in the PEER record is, e.g., formatted as 1 of following:
     1) new PGA database
        PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
         IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230
         ACCELERATION TIME HISTORY IN UNITS OF G
         3930 0.00500 NPTS, DT

      2) old SMD database
        PACIFIC ENGINEERING AND ANALYSIS STRONG-MOTION DATA
         IMPERIAL VALLEY 10/15/79 2319, EL CENTRO ARRAY 6, 230
         ACCELERATION TIME HISTORY IN UNITS OF G
         NPTS=  3930, DT= .00500 SEC
    """


    dt = 0.0
    npts = 0

    # Open the input file and catch the error if it can't be read
    inFileID = open(inFilename, 'r')

    # Container for acceleration values
    data = []

    # Flag indicating dt is found and that ground motion
    # values should be read -- ASSUMES dt is on last line
    # of header
    flag = 0

    # Look at each line in the file
    for line in inFileID:
        if line == '\n':
            # Blank line --> do nothing
            continue

        elif flag == 1:
            if "end" in line.lower():
                break

            # collect values
            data.extend(map(float, line.split()))


        else:
            # Search header lines for dt
            words = line.split()
            lengthLine = len(words)

            if lengthLine >= 4:

                if words[0] == 'NPTS=':
                    # old SMD format
                    for word in words:
                        if word == '':
                            continue

                        # Read in the time step
                        if flag == 1:
                            dt = float(word)
                            break

                        if flag == 2:
                            npts = int(word.strip(','))
                            flag = 0

                        # Find the desired token and set the flag
                        if word == 'DT=' or word == 'dt':
                            flag = 1

                        if word == 'NPTS=':
                            flag = 2


                elif words[-1] == 'DT':
                    # new NGA format
                    count = 0
                    for word in words:
                        if word == '':
                            continue
                        if count == 0:
                            npts = int(word)
                        elif count == 1:
                            dt = float(word)
                        elif word == 'DT':
                            flag = 1
                            break

                        count += 1


    inFileID.close()

    return dt, npts, np.array(data)


def read_nga(read_file, *args, **kwds):
    with open_quake(read_file, "r") as f:
        match = RE_TIME_STEP.search(next(f))
        header = [""]
        while RE_TIME_STEP.search(header[-1]) is None:
            header.append(next(f))

        #header = [next(f) for _ in range(4)]
    dt = float(RE_TIME_STEP.search(header[-1]).group(1).strip())
    #dt = float(match.group(1).strip())
    series_type = header[-2][:5].lower()
    accel = np.genfromtxt(read_file, skip_header=4, skip_footer=1).flatten()
    return QuakeSeries(
        accel, dt, meta=dict(series_type=series_type, units="g")
    )


FILE_TYPES = {
    "nga.at2": {
        "read": read_nga,
        "type": QuakeSeries,
    }
}
