import re


def is_passport_number(text: str):
	return True if re.fullmatch(r'[A-Z]{2}\d{5}', text) else False


def is_ipn(text: str):
	return True if re.fullmatch(r'\d{10}', text) else False


def is_car_number_dnipro(text: str):
	return True if re.fullmatch(r'(AE|KE)\d{4}[A-Z]{2}', text) else False


def is_car_number_kharkiv(text: str):
	return True if re.fullmatch(r'(AX|KX)\d{4}[A-Z]{2}', text) else False
