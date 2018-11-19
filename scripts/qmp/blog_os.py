import fault_injection
import sys
import random

inj = None

def main():
    # The injection framework will parse the command line automatically
    # (eg: the qmp socket/port.. etc)
    sys.stdout.write('Fault Injection for blog_os\n')
    global inj
    inj = fault_injection.FaultInjectionFramework(sys.argv[1], 0)

    inj.notify(1 * 1000 * 1000 * 1000, corrupt_random_bit)

    inj.run()

    sys.exit(1)

def corrupt_random_bit():
    #print 'corrupt_random_bit()'
    byte_number = random.randint(0, 20 * 1024 * 1024)
    bit_number = random.randint(0, 7);
    byte = inj.read(byte_number, 1, 0)["value"]

    #print ("corrupting byte " + hex(byte_number) + ":" + str(bit_number))
    #print ("original value: " + hex(byte))

    if byte & (1 << bit_number) == 0:
        byte |= (1 << bit_number)
    else:
        byte &= not (1 << bit_number)

    #print ("corrupted value: " + hex(byte))
    inj.write(byte_number, byte, 1, 0)

    inj.notify(1 * 1000 * 1000, corrupt_random_bit) # every millisecond

def virt_to_phys(addr):
    # Translate a virtual to a physical address
    p4_index = (addr >> 12 >> 9 >> 9 >> 9) & 0x1ff;
    p3_index = (addr >> 12 >> 9 >> 9) & 0x1ff;
    p2_index = (addr >> 12 >> 9) & 0x1ff;
    p1_index = (addr >> 12) & 0x1ff;
    page_offset = addr & 0xfff;

    p4_addr = 0x1000;
    print hex(inj.read(p4_addr, 8, 0)["value"])

if __name__ == '__main__':
    main()
