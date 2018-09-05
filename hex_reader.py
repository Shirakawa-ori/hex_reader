#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

class getsizeERRO(Exception):
    pass

def table_print(s):
    print ''
    l = s.split(' ')
    print '{:^8}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|'.format('','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
    print '-'*90
    pl = [l[i:i+16] for i in xrange(0,len(l),16)]
    row = 0
    for p in pl :
        p.insert(0,'0x%s0' %str.upper(str(hex(row)).replace('0x', '')))
        if len(p)<17 :
            for i in xrange(17-len(p)):
                p.append('')
        #print '{:^8}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|'.format(p)
        print '{:^8}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|{:^4}|'.format(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13],p[14],p[15],p[16])
        row += 1

def str_to_hex(s):
    l = []
    for c in s:
        h = hex(ord(c)).replace('0x', '')
        if (len(h) == 1):
            h = '0'+h
        l.append(str.upper(h))
    return ' '.join(l)

def read_file(file_name,read_interval):
    print '* Read interval:%s' % str(read_interval)
    f = open(file_name,'r')
    data = ''
    f.seek(read_interval[0], 1)
    for i in xrange(read_interval[1]-read_interval[0]):
        data = data + f.read(1)
    f.close()
    print '* Read done.\n* Datalen:%s' % len(data)
    #print data
    #exit()
    return data

def get_file_size(file_name):
    s = os.path.getsize(file_name)
    if s == 0:
        raise getsizeERRO('File Size value 0')
    else :
       return s

if __name__ == '__main__' :
    if len(sys.argv) > 1 :
        for a in sys.argv:
            al = a.split('=')
            if al[0] == 'file':
                file_name = al[1]
            elif al[0] == 'start_byte' :
                start_byte = int(al[1])
            elif  al[0] == 'stop_byte' :
                stop_byte = int(al[1])
            else :
                pass
    else :
        print 'hex_reader.py file=/dev/sda start_byte=0 stop_byte=512'
        exit(0)

    try :
        file_size = get_file_size(file_name)
    except getsizeERRO as e:
        print '*' ,e ,', getFilesizeERRO block device?'
        file_size = 512
        file_size = stop_byte
    except Exception as e:
        print e
        exit()
    if start_byte > file_size :
        print '* ERROR start_byte > file_size'
        exit(0)
    elif stop_byte > file_size :
        print '* Warning stop_byte > file_size'
    elif start_byte > stop_byte :
        print '* ERROR start_byte > stop_byte'
        exit(0)
    else :
        file_size = stop_byte
    print ''
    table_print(str_to_hex(read_file(file_name,[start_byte,file_size])))
