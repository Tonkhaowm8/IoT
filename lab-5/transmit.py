import time
from SX127x.LoRa import *
from SX127x.board_config import Board

BOARD.setup()
BOARD.reset()

class mylora(LoRa):

    def __init__(self, verbose = False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.val = 0

    def on_rx_done(self):
        self.clear_irq_flags(RxDone = True)
        payload = self.read_payload(nocheck = True)
        mens = bytes(payload).decode("utf-8", 'ignore')
        print("Receive from LoRa 2: " + mens + "\n")

        time.sleep(2)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def start(self):

        while True:
            info = "Hello From LoRa1 No." + str(self.val)
            self.val = self.val + 1
            print("Send to LoRa 2: " + info)

            word1 = list(into)
            word2 = []
            
            for f in word1: word2.append(ord(f))
            data = [0, 0] + word2 + [0]
            self.write_payload(data) # Send INF
            self.set_mode(MODE.TX)
            time.sleep(3)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCOUNT)
            time.sleep(10)

lora = mylora(verbose = False)

lora.set_pa_config(pa_select = 1, max_power = 21, output_power = 15)
lora.set_freq(433.2)
lora.set_bw(BW.BW250)
lora.set_coding_rate(CODE_RATE.CR4_8)
lora.set_spreading_factor(7)
lora.set_rx_crc(True)
lora.set_low_data_rate_optim(True)

assert(lora.get_agc_auto_on() == 1)

try:
    print("START Loral \n")
    lora.start()

except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")

finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
