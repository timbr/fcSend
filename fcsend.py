#!/usr/bin/env python

# fcsend.py
# 

# Input characters are sent directly (only LF -> CR/LF/CRLF translation is
# done), received characters are displayed as is (or as trough pythons
# repr, useful for debug purposes)
# Baudrate and echo configuartion is done through globals


import sys, os, serial, threading, getopt

import msvcrt

CONVERT_CRLF = 2
CONVERT_CR   = 1
CONVERT_LF   = 0

#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  FCsend - Send firmware commands to Spectroscopy boards.
  -------------------------------------------------------
  Tim Browning 16/05/2008


  USAGE: %s <Address> <Data1> <Data2> <Data3>

  Use decimal numbers for Address and Data.


""" % (sys.argv[0], ))

if __name__ == '__main__':
    #initialize with defaults
    port  = 0
    baudrate = 115200
    echo = 0
    convert_outgoing = CONVERT_CRLF
    rtscts = 0
    xonxoff = 0
    repr_mode = 0
    
    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",)
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    #print args
    #print len(args)
    if  len(args) == 4:
        #print "good"
        addrhex = hex(int(args[0]))[2:]
        data1hex = hex(int(args[1]))[2:]
        data2hex = hex(int(args[2]))[2:]
        data3hex = hex(int(args[3]))[2:]
        #print type(data1hex)
        #print addrhex, data1hex, data2hex, data3hex
        checksum = (int(addrhex,16) + int(data1hex,16)
                    + int(data2hex,16) + int(data3hex,16)) %256
        #print hex(checksum)

        
        #open the port
        try:
            s = serial.Serial(port, baudrate, rtscts=rtscts, xonxoff=xonxoff, timeout=0.1)
        except:
            sys.stderr.write("Could not open port\n")
            sys.exit(1)

        s.write(chr(int(addrhex, 16)))
        s.write(chr(int(data1hex, 16)))
        s.write(chr(int(data2hex, 16)))
        s.write(chr(int(data3hex, 16)))
        s.write(chr(checksum))

        print
        print '>>>Reply: ',

        data1 = s.read()
        if data1 !='':
            data1dec=(repr(data1)[1:-1])[2:]
            print int(data1dec,16),

            data2 = s.read()
            if data2 !='':
                data2dec=(repr(data2)[1:-1])[2:]
                print int(data2dec,16),

                data3 = s.read()
                if data3 !='':
                    data3dec=(repr(data3)[1:-1])[2:]
                    print int(data3dec,16),

                    data4 = s.read()
                    if data4 !='':
                        data4dec=(repr(data4)[1:-1])[2:]
                        print int(data4dec,16),

        else:
            print 'NONE'



    else:
        usage()
        sys.exit(2)
        
