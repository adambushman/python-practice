import pandas as pd
import numpy as np



# -----------------------
# Interview Q: 11/30/2022
# Normalizing student grades
    # The dataframe is showing information about students. Write code using Python Pandas to select the rows where the students' favorite color is blue or yellow and their grade is above 90.

df_1130 = pd.DataFrame({
    "Age": [20, 19, 22, 21], 
    "Favorite Color": ["blue", "blue", "yellow", "green"], 
    "Grade": [88, 95, 92, 70], 
    "Name": ["Willard Morris", "Al Jennings", "Omar Mullins", "Spencer McDaniel"]
})

# Answer
def normalize(vec):
    norm_vec = (vec - vec.mean()) / vec.std()
    return(norm_vec)

(df_1130
    .assign(norm_Grade = lambda a_df: normalize(a_df['Grade']))
)


# -----------------------
# Interview Q: 11/28/2022
# Calculating earnings
    # Suppose an individual is taxed 30% if earnings for a given week are > = $2,000. If earnings land < $2,000 for the week, the individual is taxed at a lower rate of 15%.
    # Write a function using Python to calculate both the pre-tax and post-tax earnings for a given individual, with the ability to feed in the hourly wage and the weekly hours as inputs.

def calc_earnings(hourly_wage, weekly_hours):
    t_earnings = hourly_wage * weekly_hours
    
    tax = 0.3 if t_earnings >= 2000 else 0.15
    n_earnings = t_earnings * (1 - tax)

    print("Pre-tax earnings: " + "${:,.2f}".format(t_earnings) + "\nPost-tax earnings: " + "${:.2f}".format(n_earnings) + ", at rate of " + "{:0%}".format(tax))
    return t_earnings, n_earnings


calc_earnings(55, 35)
calc_earnings(70, 40)


# -----------------------
# Interview Q: 11/21/2022
# Filtering student info
    # The dataframe is showing information about students. Write code using Python Pandas to select the rows where the students' favorite color is blue or yellow and their grade is above 90.

df_1121 = pd.DataFrame({
    "Age": [20, 19, 22, 21], 
    "Favorite Color": ["blue", "blue", "yellow", "green"], 
    "Grade": [88, 95, 92, 70], 
    "Name": ["Willard Morris", "Al Jennings", "Omar Mullins", "Spencer McDaniel"]
})

# Answer
(df_1121
    .loc[(df_1121["Favorite Color"] == "blue") & (df_1121["Grade"] > 90)]
)


# -----------------------
# Interview Q: 11/18/2022
# Identifying prime numbers
    # Given a single #, n, write a function using Python to return whether or not the # is prime. Additionally, if the inputted # is prime, save it into an array, a. 

# Answer
a = []

def is_prime(n):
    if (n < 2):
        result = False
    elif(n == 2 | n == 3):
        result = True
    else:
        i = 2
        while i <= n:
            if (n % i == 0):
                result = False
                break
            i = i + 1
        result = True if i == n else result
        if result == True:
            a.append(n)

    return result

is_prime(101)
is_prime(71)
is_prime(5)

print(a)


# -----------------------
# Interview Q: 11/09/2022
# Assigning grades
    # You need to assign the following letter grades based on final_grade_pct in a new column named "final_grade_letter":
    # >90: A, 81-90: B, 71-80: C, <70: D
    # Write a function using Python to loop through the table and assign the appropriate letter grades to each student, adding a new column to the existing dataframe, df.

df_1109 = pd.DataFrame({
    "student_name": ["Leon Rose", "Jamal Mosley", "Michael Malone", "Mike Brown", "Nick Nurse"], 
    "student_id": [1904839, 3824892, 4920940, 2849284, 4824242], 
    "class": ["Business 101", "Communication 210", "Optimization 440", "Tactics 310", "Strategy 550"], 
    "final_grade_pct": [67, 80, 92, 88, 79]
})

# Answer
def add_letter_grades(df):
    def letter_logic(vec):
        l = []
        for v in vec:
            if(v > 90):
                letter = "A"
            elif(v > 80):
                letter = "B"
            elif(v > 70):
                letter = "C"
            else:
                letter = "D"
            
            l.append(letter)
        
        return l

    return (
        df_1109
        .assign(
            final_grade_letter = lambda a_df: letter_logic(a_df["final_grade_pct"])
        )
    )
    

add_letter_grades(df_1109)


# -----------------------
# Interview Q: 11/07/2022
    # There are a few ways we can score in American Football:
    # Given a score value, can you write a function that lists the possible ways the score could have been achieved?

# Answer

def possibilities(score):
    vals = [8, 7, 6, 3, 2]
    poss = ['TD+2P', 'TD+PA', 'TD', 'FG', 'SF']

    def check(c, s):
        for i in range(0, len(vals)):
            if (s - vals[i]) > 1:
                c.append(poss[i])
                check(c, s - vals[i])
            elif (s - vals[i]) == 0:
                c.append(poss[i])
                print(' ... '.join(r for r in c))
                c.pop(len(c)-1)
        
        if len(c) != 0: c.pop(len(c)-1)
    
    check([], score)
    

# Possible ways print to the console
possibilities(8)


# -----------------------
# Interview Q: 10/28/2022
    #  A Product Manager asked you to give an update 
    #  on how the Alpha Launch is going. You decide to '
    #  aggregate (e.g. pivot) the events by each app to provide '
    # a quick summary. Write the aggregation using Python (Pandas).

data_1028 = pd.DataFrame({
    "time": [1625642764, 1625640152, 1625640161, 1625640161, 1625642754, 1625642753, 1625640153, 1625599912, 1625599929, 1625642767, 1625640154, 
        1625599917, 1625640156, 1625642763, 1614724387, 1625642764, 1614724383, 1625640150, 1625642769, 1614724388, 1614724378, 
        1625599928, 1625640155, 1625640146, 1614724388, 1625599928, 1614724377, 1625640154, 1625599915, 1625640150], 
    "user_id": [849839, 102912, 849839, 540394, 1019291, 540394, 428495, 428495, 540394, 647564, 
        865849, 849839, 849839, 102912, 250938, 102912, 540394, 250938, 865849, 865849, 
        102912, 102912, 250938, 428495, 865849, 849839, 102912, 428495, 250938, 647564], 
    "app_id": ['PayPal', 'PayPal', 'Venmo', 'Cashapp', 'Venmo', 'PayPal', 'Venmo', 'PayPal', 'Cashapp', 'PayPal', 
        'Venmo', 'Venmo', 'Cashapp', 'Venmo', 'Cashapp', 'Cashapp', 'Cashapp', 'Venmo', 'Cashapp', 'PayPal', 
        'PayPal', 'Cashapp', 'Cashapp', 'PayPal', 'Venmo', 'PayPal', 'Cashapp', 'Cashapp', 'Cashapp', 'Cashapp'], 
    "event": ['No', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 
        'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'Yes', 
        'Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No']
})

# Answer

(data_1028
    .pivot_table(
        values = 'user_id', 
        index = 'app_id', 
        columns = 'event', 
        aggfunc = np.count_nonzero
    )
)