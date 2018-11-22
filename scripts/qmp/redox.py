import fault_injection
import sys
import random

inj = None

def main():
    # The injection framework will parse the command line automatically
    # (eg: the qmp socket/port.. etc)
    sys.stdout.write('Fault Injection for redox os\n')
    global inj
    inj = fault_injection.FaultInjectionFramework(sys.argv[1], 0)

    inj.notify(1 * 1000 * 1000 * 1000, corrupt_random_bit)

    inj.run()

    sys.exit(1)

def corrupt_random_bit():
    #print 'corrupt_random_bit()'
    byte_number = random.randint(0, 2048 * 1024 * 1024)
    bit_number = random.randint(0, 7);
    byte = inj.read(byte_number, 1, 0)["value"]

    #print ("corrupting byte " + hex(byte_number) + ":" + str(bit_number))
    #print ("original value: " + hex(byte))

    if byte & (1 << bit_number) == 0:
        byte |= (1 << bit_number)
    else:
        byte &= ~(1 << bit_number)

    #print ("corrupted value: " + hex(byte))
    inj.write(byte_number, byte, 1, 0)

    inj.notify(1 * 1000 * 1000 * 1000, corrupt_random_bit) # every second

if __name__ == '__main__':
    main()
