from main import Wiegand
VALID_FACILITY_CODES = [ '123']
VALID_CARDS = [ '12345' ]

GREEN_LED = Pin(0)
RED_LED = Pin(1)

WIEGAND_ZERO = 0  # Pin number here
WIEGAND_ONE = 1   # Pin number here

def on_card(card_number, facility_code, cards_read):
	if (card_number in VALID_CARDS) and (facility_code in VALID_FACILITY_CODES):
		GREEN_LED.high()
		RED_LED.low()
	else:
		RED_LED.high()
		GREEN_LED.low()


Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)