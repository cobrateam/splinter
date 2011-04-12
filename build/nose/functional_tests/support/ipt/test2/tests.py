import sys

print 'ipthelp', sys.modules.get('ipthelp')
import ipthelp
print ipthelp

def test2():
    ipthelp.help(1)
