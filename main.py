import threading
import time
import serial  # type: ignore # Replace pygsm with pyserial for modem communication
from send_sms import send_silent_sms
from receive_sms import process_received_sms

def main():
    # Set up the GSM modem
    modem = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=1)
    if not modem.is_open:
        modem.open()

    # Start a thread for processing received messages
    receive_thread = threading.Thread(target=process_received_sms, args=(modem,))
    receive_thread.start()

    # Main loop for sending Silent SMS and performing triangulation
    shutdown_flag = threading.Event()

    def send_sms_loop():
        while not shutdown_flag.is_set():
            target_number = "+1234567890"  # Replace with actual target number
            send_silent_sms(target_number)
            time.sleep(60)  # Wait for 60 seconds before next ping

    sms_thread = threading.Thread(target=send_sms_loop)
    sms_thread.start()

    try:
        while not shutdown_flag.is_set():
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutdown signal received. Cleaning up...")
        shutdown_flag.set()

    sms_thread.join()

        # Perform triangulation (assuming you have the necessary data)
        # estimated_location = triangulate(tower1, tower2, tower3, dist1, dist2, dist3)
        # print(f"Estimated location: {estimated_location}")

    # Clean up
    shutdown_flag.set()
    receive_thread.join()
    modem.close()
    print("Resources cleaned up successfully.")

if __name__ == "__main__":
    main()
