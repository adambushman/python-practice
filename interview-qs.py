import pandas as pd
import numpy as np
import sys


# -----------------------
# Interview Q: 12/07/2022
    # You are given reviews for a popular iOS app below:

data_1209 = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5], 
    "channel": ['online', 'online', 'in_store', 'in_store', 'online'], 
    "date": ['2018-09-01', '2018-09-03', '2018-10-11', '2018-08-21', '2018-08-13'], 
    "month": ['09', '09', '10', '08', '08'], 
    "revenue": [100, 125, 200, 80, 200]
})

# Answer

(data_1209
    .groupby(['month', 'channel'])
    .agg(
        avg_rev = ('revenue', 'mean')
    )
    .reset_index()
    .rename(columns={'month': 'Month', 'channel': 'Channel', 'avg_rev': 'Avg. Revenue'})
)


# -----------------------
# Interview Q: 12/07/2022
    # You are given reviews for a popular iOS app below:
    # Your task is to determine sentiment from the reviews above. To do this you first decide to write code to find the count of individual words across all the reviews -- write this code using Python.

reviews = ['app is good, but forced updates are too frequent', 'love this app, use it daily to log calories', 'free version of this app has way too many ads', 'app doesn\'t load, 0/10'] 

# Answer

def count_words(allreviews):
    uWords = []

    for r in allreviews:
        allwords = r.split()
        for a in allwords:
            if not(uWords.__contains__(a)): uWords.append(a)
    
    return len(uWords)

count_words(reviews)


# -----------------------
# Interview Q: 11/30/2022
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


# -----------------------
# Interview Q: 10/26/2022
    #  Write a function that takes in an integer n, and prints out integers from 1 to n inclusive.
    #  Additionally, if %3 == 0 then print "foo" in place of the integer, 
    #  if %5 == 0 then print "ie" in place of the integer, 
    #  and if both conditions are true then print "foo-ie" in place of the integer.

# Answer

def print_num(n):
    for r in range(1, n+1):
        if ((r % 3) == 0 and (r % 5) == 0):
            print("foo-ie")
        elif (r % 3) == 0:
            print("foo")
        elif (r % 5) == 0:
            print("ie")
        else:
            print(str(r))

print_num(15)


# -----------------------
# Interview Q: 10/19/2022
    #  You're given a set of data that is aggregated on a monthly basis (as illustrated in Table A).
    #  Can you write code that can expand this monthly table into a daily table which spreads revenue across the 30 day period (as shown in Table B)? 

data_1019 = pd.DataFrame({
    "Month": [1, 2, 3], 
    "Revenue": [300, 330, 390]
})

# Answer

(
    pd.DataFrame({
        "Month": np.repeat(data_1019['Month'].unique(), [30, 30, 30]).tolist()
    })
    .assign(Day = [*range(1, 31)] + [*range(1, 31)] + [*range(1, 31)])
    .merge(
        data_1019, 
        how = 'left', 
        on = 'Month'
    )
    .assign(R = lambda x: x['Revenue'] / 30)
    .drop(['Revenue'], axis = 1)
    .rename(columns = {'R': 'Revenue'})
)


# -----------------------
# Interview Q: 10/17/2022
    #  Write a function to return a boolean that indicates if two strings are one edit away from being identical.
    #  The definition of an "edit" is as follows: Insert one character, Remove one character, Replace one character

# Answer

def oneEditAway(str1, str2):
    if(str1 == str2):
        return True
    else:
        str1 = list(list(zip(*str1))[0])
        str2 = list(list(zip(*str2))[0])

        c = []
        for i in range(0, min(len(str1), len(str2))):
            c.append(1 if str1[i] == str2[i] else 0)

        t = len(c) - sum(c) + (1 if len(str1) != len(str2) else 0)
        return t == 1


oneEditAway("pea", "pea")
oneEditAway("pea", "lea")
oneEditAway("pea", "seas")


# -----------------------
# Interview Q: 10/10/2022
    #  Can you pull the average, median, minimum, maximum, and standard deviations for salary across 5 year experience buckets at Company XYZ?

df_1010 = pd.DataFrame({
    "employee_name": ([
        'Esther Dixon', 'Molly Bird', 'Gabriel Fowler', 'Cruz Ellis', 'Ollie Santiago', 'Judy Vaughan', 'Sebastian Andrade', 'Mohamed Howard', 'Riya Kane', 'Joan Henry', 
        'Kamil Hogan', 'Willard Mayer', 'Grayson Bradley', 'Davina Schaefer', 'Alexia Gallegos', 'Teresa Simpson', 'Allen Davis', 'Idris Blanchard', 'Owain Lowery', 'Esha Love', 
        'Zara Lawrence', 'Sebastien Rowland', 'Moshe Delacruz', 'Abdul Rush', 'Kelly Norman', 'Terry Lewis', 'Otto Jennings', 'Macy Moyer', 'Sumaiya Cooke', 'Omari Gill'
    ]), 
    "employee_id": ([
        986719, 316904, 317045, 181254, 387226, 316961, 181042, 119970, 316782, 386879, 
        181111, 120002, 986837, 119945, 119810, 180859, 317101, 119995, 119999, 387173, 
        120099, 181000, 181080, 387110, 387220, 316966, 387143, 180794, 180978, 180862
    ]), 
    "yrs_of_experience": ([
        4, 1, 4, 13, 3, 1, 15, 6, 2, 4, 1, 1, 13, 5, 6, 3, 1, 6, 5, 9, 3, 1, 1, 4, 3, 5, 2, 5, 2, 4
    ]), 
    "yrs_at_company": ([
        2, 1, 1, 6, 1, 1, 4, 2, 2, 1, 3, 1, 1, 2, 1, 3, 3, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 2
    ]), 
    "compensation": ([
        95206.71, 82433.77, 72149.85, 105361.12, 97243.93, 134557.55, 124501.72, 96949.17, 71891.63, 120495.23, 
        98712.27, 71560.75, 101382.74, 116620.68, 160333.08, 94146.18, 113638.03, 94368.48, 100548.31, 128403.32, 
        123583.45, 99533.72, 98481.03, 94969.71, 120027.67, 144925.92, 78430.78, 106169.62, 88842.7, 95882.39
    ]), 
    "career_track": ([
        'technical', 'executive', 'non-technical', 'executive', 'executive', 'technical', 'executive', 'technical', 'technical', 'executive', 
        'non-technical', 'executive', 'non-technical', 'executive', 'executive', 'technical', 'technical', 'technical', 'non-technical', 'executive', 
        'non-technical', 'technical', 'technical', 'technical', 'non-technical', 'executive', 'non-technical', 'executive', 'technical', 'executive'
    ])
})

# Answer

def assign_buckets(ser):
    m = int(np.ceil(max(ser) / 5) + 1)

    r = list(range(0, m * 5, 5))

    return pd.cut(ser, r)


(df_1010
    .assign(bucket = lambda x: assign_buckets(x['yrs_of_experience']))
    .groupby('bucket')
    .agg(
        mean_sal = ('compensation', 'mean'), 
        med_sal = ('compensation', 'median'), 
        min_sal = ('compensation', 'min'), 
        max_sal = ('compensation', 'max'), 
        std_sal = ('compensation', 'std')
    )
)


# -----------------------
# Interview Q: 10/7/2022
    #  Suppose you are given P, which is list of j integer intervals, where j is the number of intervals. The intervals are in a format [a, b]. 
    #  Given an integer z, can you return the number of overlapping intervals for point z?

# Answer

def count_overlap(P, z):
    n = 0
    for p in P:
        n = (n + 1) if (p[0] <= z and p[1] >= z) else n
    return n


ivals = [[0, 2], [3, 7], [4, 6], [7, 8], [1, 5]]

count_overlap(ivals, 5)
count_overlap(ivals, 10)


# -----------------------
# Interview Q: 9/30/2022
    #  Below is a snippet from a table that contains information about employees that work at Company XYZ:
    #  Company XYZ recently migrated database systems causing some of the date_joined records to be NULL. 
    #  You're told by an analyst in human resources NULL records for the date_joined field indicates the employees joined prior to 2010. 
    #  You also find out there are multiple employees with the same name and duplicate records for some employees.

df_0930 = pd.DataFrame({
    "employee_name": ['Andy', 'Beth', 'Cindy', 'Dale', 'Sebastian Andrade', 'Sebastian Andrade', 'Cruz Ellis', 'Andy', 'Sebastian Andrade', 'Judy Vaughan', 'Sebastian Andrade', 'Santiago', 'Cruz Ellis', 'Judy Vaughan', 'Sebastian Andrade', 'Judy Vaughan', 'Santiago', 'Judy Vaughan', 'Sebastian Andrade', 'Sebastian Andrade'], 
    "employee_id": [123456, 789456, 654123, 963852, 858382, 858382, 103030, 123456, 858382, 294902, 858382, 393929, 103030, 294902, 858382, 294902, 393929, 294902, 858382, 858382], 
    "date_joined": ['2015-02-15', np.nan, '2017-05-16', '2018-01-15', '2018-07-14', '2018-07-14', '2013-09-30', '2015-02-15', '2018-07-14', '2020-02-03', '2018-07-14', np.nan, '2013-09-30', '2020-02-03', '2018-07-14', '2020-02-03', np.nan, '2020-02-03', '2018-07-14', '2018-07-14'], 
    "age": [45, 36, 34, 25, 52, 52, 36, 45, 52, 49, 52, 21, 36, 49, 52, 49, 21, 49, 52, 52], 
    "yrs_of_experience": [24, 15, 14, 4, 26, 26, 14, 24, 26, 20, 26, 1, 14, 20, 26, 20, 1, 20, 26, 26]
})

df_0930.head()

# Answer

(df_0930
    .drop_duplicates()
    .assign(
        date_joined = lambda x: x['date_joined'].fillna('2009-12-01')
    )
    .assign(
        month_joined = lambda x: pd.DatetimeIndex(x['date_joined']).month
    )
    .groupby('month_joined')
    .size()
    .reset_index(name = 'count')
)


# -----------------------
# Interview Q: 9/28/2022
    #  Suppose you are given a list of Q 1D points. 
    #  Write code to return the value in Q that is the closest to value j. 
    #  If two values are equally close to j, return the smaller value. 

# Answer

def closest(Q, j):
    Z = []
    for q in Q:
        Z.append(abs(q - j))
        m = min(Z)
    Y = []
    for i in range(1, len(Z)):
        if m == Z[i]:
            Y.append(Q[i]) 
    
    return min(Y)


QQ = [1, -1, -5, 2, 4, -2, 1]
jj = 3

closest(QQ, jj)


# -----------------------
# Interview Q: 9/21/2022
    #  Suppose you are given a list of Q 1D points. 
    #  Write code to return the value in Q that is the closest to value j. 
    #  If two values are equally close to j, return the smaller value. 

data_0921 = pd.DataFrame({
    "date": []
})

# Answer