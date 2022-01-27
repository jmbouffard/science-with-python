#!/usr/bin/env python3
#
#   Based on picrunch.py  -  by Don Cross
#
#   Use Machin's Formula
#   pi = 4*(4*arctan(1/5) - arctan(1/239))
#   to calculate pi to one million places after the decimal.
#
#####
#
#   Adapted for quicker execution  -  by Jean-Michel Bouffard
#
import sys
from datetime import datetime
from multiprocessing import Process, Manager

def ArctanDenom(d, ndigits, lst, verbose):
    # Calculates arctan(1/d) = 1/d - 1/(3*d^3) + 1/(5*d^5) - 1/(7*d^7) + ...
    total = term = (10**ndigits) // d
    n = 0
    fixed = -d*d
    #print('total = term = {}'.format(total))
    while term != 0:
        n += 1
        term //= fixed
        total += term // (2*n + 1)
        if verbose and n % 10000 == 0:
            print('Iteration #{}'.format(n))
    print('ArctanDenom({}) took {} iterations'.format(d, n))
    lst.append(total)
    #print('ArctanDenom({}) stored {} result of len={} in queue.'.format(d, type(total), len(str(total))))
    #print('ArctanDenom({}) stored {} result of len={} in queue.'.format(d, type(lst[0]), len(str(lst[0]))))
    return

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('USAGE: picrunch.py ndigits outfile')
        sys.exit(1)

    xdigits = 10  # Extra digits to reduce trailing error
    ndigits = int(sys.argv[1])
    outFileName = sys.argv[2]

    now = datetime.now()
    print('Computing pi with {} digits'.format(ndigits))
    print('Started at {}'.format(now))

    # Multiprocessing 
    # List data structure used to move data between processes
    manager = Manager()
    shared_list_1 = manager.list()
    shared_list_2 = manager.list()
    
    # Create processes
    p1 = Process(target=ArctanDenom, args=(5,ndigits+xdigits,shared_list_1,True))
    p2 = Process(target=ArctanDenom, args=(239,ndigits+xdigits,shared_list_2,False))
    
    # Start processes in parallele
    p1.start()
    p2.start()
    
    print('Waiting for processes execution')
    p1.join()
    p2.join()
    print('Processes completed')
    
    # Use Machin's Formula to calculate pi.
    #pi = 4 * (4*ArctanDenom(5,ndigits+xdigits) - ArctanDenom(239,ndigits+xdigits))
    pi = 4 * (4*shared_list_1[0] - shared_list_2[0])

    # We calculated extra digits to compensate for roundoff error.
    # Chop off the extra digits now.
    pi //= 10**xdigits

    # Write the result to a text file.
    with open(outFileName, 'wt') as outfile:
        # Insert the decimal point after the first digit '3'.
        text = str(pi)
        outfile.write(text[0] + '.' + text[1:] + '\n')

    print('Wrote to file {}'.format(outFileName))
    now = datetime.now()
    print('Completed at {}'.format(now))
    sys.exit(0)