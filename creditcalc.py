import argparse
import math


def calculate_loan_principal(a, i, n):
    return a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1))


def calculate_number_of_months(a, i, p):
    return math.ceil(math.log((a / (a - i * p)), 1 + i))


def calculate_monthly_payment(i, n, p):
    return math.ceil(p * (i * (1 + i) ** n) / ((1 + i) ** n - 1))


def calculate_normal_interest_rate(i):
    return (i / 100) / 12


def calculate_differentiated_payment(p, n, i, m):
    return math.ceil(p / n + i * (p - (p * (m - 1) / n)))


parse = argparse.ArgumentParser()
parse.add_argument('--type', choices=['annuity', 'diff'])
parse.add_argument('--payment')
parse.add_argument('--principal')
parse.add_argument('--periods')
parse.add_argument('--interest')
args = parse.parse_args()

if args.type == 'annuity':
    if args.interest is None:
        print('Incorrect parameters')
    else:
        if not args.periods and float(args.payment) >= 0 and float(args.interest) >= 0 and float(args.principal) >= 0:
            interest = calculate_normal_interest_rate(float(args.interest))
            months = calculate_number_of_months(float(args.payment), interest, float(args.principal))
            years = int(months / 12)
            remaining_months = months % 12
            if years > 0 and remaining_months > 0:
                print(
                    f"It will take {years} year{'s' if years > 1 else ''}{' and ' if remaining_months > 0 else ''}"
                    f"{remaining_months}"
                    f"{'s' if remaining_months > 1 else ''} to repay this loan!")
            elif years > 0 and remaining_months == 0:
                print(
                    f"It will take {years} year{'s' if years > 1 else ''} to repay this loan!")
            else:
                print(f"It will take {months} month{'s' if months > 1 else ''} to repay this loan!")
            print(f'Overpayment = {math.ceil((months * float(args.payment)) - float(args.principal))}')
        elif not args.payment and float(args.interest) >= 0 and float(args.periods) >= 0 and float(args.principal) >= 0:
            interest = calculate_normal_interest_rate(float(args.interest))
            monthly_payment = calculate_monthly_payment(interest, float(args.periods), float(args.principal))
            print(f'Your annuity payment = {monthly_payment}!')
            print(f'Overpayment = {math.ceil(monthly_payment * float(args.periods) - float(args.principal))}')
        elif not args.principal and float(args.payment) >= 0 and float(args.interest) >= 0 and float(args.periods) >= 0:
            interest = calculate_normal_interest_rate(float(args.interest))
            loan_principal = calculate_loan_principal(float(args.payment), interest, float(args.periods))
            print(f'Your loan principal = {int(loan_principal)}!')
            print(f'Overpayment = {math.ceil((float(args.payment) * float(args.periods)) - loan_principal)}')
        else:
            print('Incorrect parameters')
elif args.type == 'diff':
    if not args.payment and float(args.interest) >= 0 and float(args.periods) >= 0 and float(args.principal) >= 0:
        interest = calculate_normal_interest_rate(float(args.interest))
        total_payment = 0
        for i in range(int(args.periods)):
            monthly_payment = calculate_differentiated_payment(float(args.principal),
                                                               float(args.periods), interest, i + 1)
            print(f'Month {i + 1}: payment is {monthly_payment}')
            total_payment += monthly_payment
        print(f'\nOverpayment = {math.ceil(total_payment - float(args.principal))}')
    else:
        print('Incorrect parameters')
else:
    print('Incorrect parameters')
