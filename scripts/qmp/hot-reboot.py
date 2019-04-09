import fault_injection
import sys
import random

inj = None

def main():
    # The injection framework will parse the command line automatically
    # (eg: the qmp socket/port.. etc)
    global inj
    inj = fault_injection.FaultInjectionFramework(sys.argv[1], 0)

    inj.cont()

    qmpcmd = {'execute': 'system_reset'}
    sys.stdout.write('Provoking hot reboot in Redox OS:  ')
    print "Response:", inj.send(qmpcmd)

if __name__ == '__main__':
    main()
