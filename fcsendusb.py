#!/usr/bin/env python

# fcsendusb.py
# 

import sys, os, getopt

import d2xx


#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  FCsendusb - Send firmware commands to Spectroscopy boards.
  -->-->--> Via USB!!
  -------------------------------------------------------
  Tim Browning 16/05/2009


  USAGE: %s <Address> <Command> <Data1> <Data2>

  Use decimal numbers.


""" % (sys.argv[0], ))

if __name__ == '__main__':
    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",)
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    if  len(args) == 4:
        addr = int(args[0])
        cmd = int(args[1])
        dat1 = int(args[2])
        dat2 = int(args[3])
        cksum = (addr + cmd + dat1 + dat2) %256
        wbuffer = chr(0) + chr(0) + chr(addr) + chr(cmd) + chr(dat1) + chr(dat2) + chr(cksum) + chr(0) # filled out to 8 bytes
        
        #open the port
        try:
            h=d2xx.openEx('SEMSCA', d2xx.OPEN_BY_DESCRIPTION)
            h.setTimeouts(500, 500)
            h.setLatencyTimer(2)
            
        except:
            sys.stderr.write("Could not open port\n")
            sys.exit(1)

        h.write(wbuffer)

        print
        print '>>>Reply: ',

        returneddata = h.read(8)
        if returneddata[1] == '\x00': # If the second byte sent is not x00 then an error has occurred - see Firmware command list for details
            print [ord(byte) for byte in returneddata][2:6]
        else:
            print 'Board Address not found'
        
        h.close()

    else:
        usage()
        sys.exit(2)
        
