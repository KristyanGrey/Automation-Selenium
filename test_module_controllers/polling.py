import requests
import time
import xml.etree.ElementTree as ET
import logging
import threading
import os
import glob


class Poll:
    def __init__(self, id, url, frequency):
        self.url = url
        self.orders_received = []
        self.frequency = frequency
        self.cleanup('../logs/*')
        self.cleanup('../orders/*')
        self.log = logging.getLogger(f"poll-{id}")
        self.log.setLevel(level=logging.DEBUG)
        file_handler = logging.FileHandler(f"logs/poll-{id}.txt", mode='w')
        file_handler.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)
        self.stopper = self.finish = threading.Event()

    def start(self):
        self.log.debug("Starting polling.")
        self.poll_thread = threading.Thread(target=self.poll)
        self.poll_thread.start()

    def stop(self):
        self.stopper.set()

    def poll(self):
        self.endpoint = f"{self.url}/api/get_order.php"
        self.log.debug(f"Polling {self.endpoint}")
        while True:
            try:
                response = requests.get(self.endpoint)
                response.raise_for_status()

                # Parse the XML response
                xml_response = response.text.strip()  # Remove leading/trailing whitespace
                if xml_response.startswith('<?xml') and '<metadata>' not in xml_response:
                    self.log.debug("Polling: Item received.")
                    order = self.parse_xml(xml_response)
                    if order['rec_id'] is not None:
                        self.log.debug(f"Polling: RecId {order['rec_id']}")
                        self.orders_received.append(order)
                        # Save the XML response to a file
                        filename = f"order_{order['rec_id']}.xml"
                        self.save_xml_response(xml_response, f"../orders/{filename}")
                        self.log.debug(f"Polling: XML response saved to {filename}")

                        # Call the update endpoint with the RecID
                        update_url = f"{self.url}/api/update_order.php?status=Accepted&orderID={order['rec_id']}"
                        update_response = requests.get(update_url)
                        update_response.raise_for_status()
                        self.log.debug(f"Polling: Update response: {update_response.text}")
                    else:
                        self.log.error("Polling: RecId not found in XML response.")
                else:
                    self.log.debug("Polling: Poll retrieved nothing.")

            except requests.exceptions.RequestException as e:
                self.log.error(f"Polling: Error occurred: {e}")
            
            if self.stopper.is_set():
                self.log.debug("Polling: Finish event received, stopping polling.")
                break

            time.sleep(self.frequency)

    def verify_order_received(self, order_id):
        order_id = str(order_id).replace("-", "")
        for order in self.orders_received:
            if order_id == order['order_notes']:
                return True
        return False

    def cleanup(self, directory):
        files = glob.glob(directory)
        for f in files:
            os.remove(f)

    def parse_xml(self, order_xml):
        root = ET.fromstring(order_xml)
        rec_id_element = root.find('.//RecId')
        notes_element = root.find('.//OrderNotes')
        order = {
            "rec_id": rec_id_element.text,
            "order_notes": notes_element.text
        }
        return order

    def save_xml_response(self, xml_response, filename):
        with open(filename, 'w') as file:
            file.write(xml_response)