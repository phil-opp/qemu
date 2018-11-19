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

    # inj.notify(1 * 1000 * 1000 * 1000, corrupt_random_bit)
    inj.notify(1 * 1000 * 1000 * 1000, test)

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
        byte &= ~(1 << bit_number)

    #print ("corrupted value: " + hex(byte))
    inj.write(byte_number, byte, 1, 0)

    inj.notify(100 * 1000 * 1000, corrupt_random_bit) # every millisecond

def test():
    phys = virt_to_phys(0xb8100)
    current = inj.read(phys, 8, 0)["value"]
    print hex(current)
    print inj.write(phys, 0xfffffffffffffff, 8, 0)
    current = inj.read(phys, 8, 0)["value"]
    print hex(current)

    phys = virt_to_phys(0x2094e0)
    current = inj.read(phys, 1, 0)["value"]
    print inj.write(phys, 0xcccc, 2, 0) # 2 times int3 opcode
    print hex(current)

def virt_to_phys(addr):
    # Translate a virtual to a physical address
    p4_index = (addr >> 12 >> 9 >> 9 >> 9) & 0x1ff;
    p3_index = (addr >> 12 >> 9 >> 9) & 0x1ff;
    p2_index = (addr >> 12 >> 9) & 0x1ff;
    p1_index = (addr >> 12) & 0x1ff;
    page_offset = addr & 0xfff;

    p4_addr = 0x1000;

    p4_entry = inj.read(p4_addr + p4_index * 8, 8, 0)["value"]
    p3_addr = p4_entry & (~0xfff)

    p3_entry = inj.read(p3_addr + p3_index * 8, 8, 0)["value"]
    p2_addr = p3_entry & (~0xfff)

    p2_entry = inj.read(p2_addr + p2_index * 8, 8, 0)["value"]
    p1_addr = p2_entry & (~0xfff)

    p1_entry = inj.read(p1_addr + p1_index * 8, 8, 0)["value"]
    phys_page_addr = p1_entry & (~0xfff)

    phys_addr = phys_page_addr + page_offset

    return phys_addr

if __name__ == '__main__':
    main()
