"""
Created on Fri Feb 10 15:08:27 2017

@author: Hiu
"""
#Lecture 2

######### PROBLEM SET 2 ####################################################################################
######### PART A: HOUSE HUNTING ############################################################################
def PartA_HouseHunting():
    '''
    Calculates how many months it will take user to save enough money to make a down payment on a house.
    User enters the following variables:  1) starting annual salary, 2) portion of salary to be saved, and 3) cost of dream home
    Assumptions:  Down payment = 25%, Current savings = $0, Annual return (r) = 4%.
    '''
    annual_salary = float(input("Enter your annual salary: "))
    portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))
    portion_down_payment = 0.25  #Assumes portion down payment is 25%
    current_savings = float(0)  # initial savings of $0
    r = 0.04  # annual return rate (4%)
    months = 0
    downpayment = total_cost * portion_down_payment

    while (current_savings < downpayment):
        current_savings = current_savings + ((current_savings * r / 12) + (
        annual_salary / 12 * portion_saved))  # Add monthly_return + monthly_savings to current_savings
        months += 1

    print("Number of months:", months)


#UNCOMMENT PartA_HouseHunting() TO RUN CODE
#PartA_HouseHunting()


######### PART B: SAVINGS WITH A RAISE ######################################################################
def PartB_SavingsWithRaise():
    '''
    Extension of PartA_HouseHunting().
    Calculates how many months it will take user to save enough money to make a down payment on a house, assuming a semi-annual raise
    User inputs an additional variable (semi-annual raise, as a decimal percent)
    '''
    annual_salary = float(input("Enter your annual salary: "))
    portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))
    semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))  # Semi-annual raise
    portion_down_payment = 0.25  #Assumes portion down payment is 25%
    current_savings = float(0)  # initial savings
    r = 0.04  # annual return rate (4%)
    months = 0
    downpayment = total_cost * portion_down_payment

    while (current_savings < downpayment):
        current_savings = current_savings + ((current_savings * r / 12) + (annual_salary / 12 * portion_saved))
        months += 1
        if months % 6 == 0:  # Semi-annual raise
            annual_salary = annual_salary * (1 + semi_annual_raise)

    print("Number of months:", months)

#UNCOMMENT PartB_SavingsWithRaise() TO RUN CODE
#PartB_SavingsWithRaise()


######### PART C: RIGHT AMT TO SAVE ###########################################################################
def PartC_RightAmtToSave():
    '''
    Calculates how much (percent) of salary user needs to save to afford a down payment in 36 months.
    Assumptions:  Semi-annual raise = 7%, Annual return (r) = 4%, Down payment = 25%, Cost of house = $1M
    Implements bisectional search to calculate best savings rate to 2 decimals of accuracy (eg. 7.04%), to achieve savings within $100 of down payment.
    '''
    semi_annual_raise = float(0.07)
    r = float(0.04)  # annual return rate
    portion_down_payment = float(0.25)
    total_cost = float(1000000)
    total_months = int(36)
    current_savings = float(0)
    saving_rate = int(5000)  # Initialize at 50.00% (0.5000).  Values are between 0.00% (0.0000) o 100.00% (1.0000)
    # Divide by 100 to get percent to 2 decimal place
    # Start test at 50% and do bisection search between 0-100% (0-10000)
    saving_rate_max = int(10000)
    saving_rate_min = int(0)
    steps = int(0)
    annual_salary_input = float(input("Enter the starting salary: "))
    total_savings = float(0)  # max savings possible if saving 100% of salary

    downpayment = total_cost * portion_down_payment

    for current_month in range(1, total_months + 1):  # Maximum savings possible if saving 100% of salary
        annual_salary = annual_salary_input
        current_savings += (current_savings * r / 12) + (annual_salary / 12)  # Assuming saving_rate = 100%
        if current_month % 6 == 0:  # Semi-annual raise
            annual_salary = annual_salary * (
            1 + semi_annual_raise)  # Semi-annual raise
        if (current_month == total_months):
            total_savings = current_savings

    if total_savings < (downpayment - 100):
        print("It is not possible to pay the down payment in three years.")

    else:  #Bisectional search
        while (current_savings < (downpayment - 100) or current_savings > (downpayment + 100)):
            current_savings = 0  #resets current_savings to 0
            annual_salary = annual_salary_input  #resets annual_salary to user input

            for current_month in range(1, total_months + 1):  #Total income in in 36 months given saving_rate x
                current_savings += (current_savings * r / 12) + (annual_salary * (saving_rate / 10000) / 12)
                if current_month % 6 == 0:  #Semi-annual raise
                    annual_salary = annual_salary * (1 + semi_annual_raise)

            if current_savings > (downpayment - 100) and current_savings < (
                downpayment + 100):  #Current_savings = downpayment
                steps += 1
                print("Best savings rate: ", saving_rate / 10000)
                print("Steps in bisection search: ", steps)
                break

            elif current_savings > downpayment:  #Current_savings > downpayment
                saving_rate_max = saving_rate
                saving_rate = int((saving_rate_max + saving_rate_min) / 2)
                steps += 1

            else:  #Current_savings < downpayment
                saving_rate_min = saving_rate
                saving_rate = int((saving_rate_max + saving_rate_min) / 2)
                steps += 1

#UNCOMMENT PartC_RightAmtToSave() TO RUN CODE
#PartC_RightAmtToSave()