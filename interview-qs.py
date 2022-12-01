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

def score_possibilities(point_total):
    def combos(point_total):
        c = []
        total = 0
        if point_total >= 6: 
            c.append("TD")
            total = total - 6
        if point_total >= 7: c.append("PA")
        if point_total >= 8: c.append("2P")
        if ((point_total % 3 == 0) or (np.floor(point_total / 3) > 0 and (point_total % 3 > 1))): c.append("FG")
        if ((point_total % 2 == 0) or (np.floor(point_total / 2) > 0 and (point_total % 2 > 1))): c.append("SF")

        return c, total

    points = [1, 2, 3, 6]

    for p in points:
        print("Raw Division: " + str(np.floor(point_total / p)))
        print(" -> Left Over: " + str(point_total % p))



new_point_total = 15
def possible(c, new_point_total, i):
    deduct = -1
    if np.floor(new_point_total / 8) > 0: # TD+2P
        deduct = 8
        c = c + "TD-" + "2P-"
    elif np.floor(new_point_total / 7) > 0: # TD+PA
        deduct = 7
        c = c + "TD-" + "PA-"
    elif np.floor(new_point_total / 6) > 0: # TD+MPA
        deduct = 6
        c = c + "TD-" + "MPA-"
    elif np.floor(new_point_total / 3) > 0 and new_point_total % 3 > 1: # FG
        deduct = 3
        c = c + "FG-"
    elif np.floor(new_point_total / 2) > 0 and new_point_total % 2 > 1: # FG
        deduct = 6
        c = c + "SF-"
    else:
        c = ""
    
    if new_point_total - deduct == 0:
        return c, 0, i
    elif deduct > -1:
        possible(c, new_point_total - deduct)
    else: 
        return c, -1


def avenues(point_total):
    c = ""
    i = []
    possible(c, point_total, i)





x = "TD-PA-FG-SF"
x.split(sep="-")