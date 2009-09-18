#!/usr/bin/env python

# scan.py
# 



import sys, os, serial, threading, getopt, time




#print a short help message
def usage():
    sys.stderr.write("""
  -------------------------------------------------------
  Scan - Scan for Spectroscopy boards.
  -------------------------------------------------------
  Tim Browning 16/05/2008



""" % (sys.argv[0], ))

if __name__ == '__main__':
    #initialize with defaults
    port  = 0
    baudrate = 115200
    echo = 0
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
    #print "good"

    #open the port
    try:
         s = serial.Serial(port, baudrate, rtscts=rtscts, xonxoff=xonxoff, timeout=0.1)
    except:
        sys.stderr.write("Could not open port\n")
        sys.exit(1)

    for i in range(0,85):
        s.flushInput()
        s.flushOutput()
        #print i
        addr=i
        data1=143
        data2=data3=0
        
        addrhex = hex(int(addr))[2:]
        data1hex = hex(int(data1))[2:]
        data2hex = hex(int(data2))[2:]
        data3hex = hex(int(data3))[2:]
        #print type(data1hex)
        #print addrhex, data1hex, data2hex, data3hex
        checksum = (int(addrhex,16) + int(data1hex,16)
                     + int(data2hex,16) + int(data3hex,16)) %256
        #print hex(checksum)

            
        
        s.write(chr(int(addrhex, 16)))
        s.write(chr(int(data1hex, 16)))
        s.write(chr(int(data2hex, 16)))
        s.write(chr(int(data3hex, 16)))
        s.write(chr(checksum))

        print
        print '>>>Reply: ',

        data1 = s.read()
        #print data1
        if data1 !='':
            data1dec=(repr(data1)[1:-1])[2:]
            #print data1
            print int(data1dec,16),

            data2 = s.read()
            #print data2
            if data2 !='':
                data2dec=(repr(data2)[1:-1])[2:]
                print int(data2dec,16),

                data3 = s.read()
                #print data3
                if data3 !='':
                    data3dec=(repr(data3)[1:-1])[2:]
                    print int(data3dec,16),

                    data4 = s.read()
                    #print data4
                    if data4 !='':
                        data4dec=(repr(data4)[1:-1])[2:]
                        print int(data4dec,16),

        else:
            print 'NONE'


s.close()


def another dummy()
    """Another attempt at a dummy function"""
        
