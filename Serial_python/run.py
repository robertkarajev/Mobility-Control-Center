from main import Wiegand
VALID_FACILITY_CODES = [ '123']
VALID_CARDS = [ '12345' ]

WIEGAND_ZERO = 0  # Pin number here
WIEGAND_ONE = 1   # Pin number here

def on_card(card_number, facility_code, cards_read):
	if (card_number in VALID_CARDS) and (facility_code in VALID_FACILITY_CODES):
		print('succes')


Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)