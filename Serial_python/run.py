from main import Wiegand
valid_facility_codes = [ '123']
valid_cards = [ '12345' ]

wiegand_zero = 0  # Pin number here
wiegand_one = 1   # Pin number here

def on_card(card_number, facility_code, cards_read):
	if (card_number in valid_cards) and (facility_code in valid_facility_codes):
		print('succes')

Wiegand(wiegand_zero, wiegand_one, on_card)