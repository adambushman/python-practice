# type: ignore
# flake8: noqa
#
#
#
#
#
#

import pandas as pd
import numpy as np
import datetime as dt
from pandas.tseries import offsets
import random as rand
import matplotlib.pyplot as plt
import seaborn as sns

#
#
#
#
#
#
#
#
#
#
#
#
#

# Reading Google Sheet data
url = 'https://docs.google.com/spreadsheets/d/10h1G4q9YbCLUZ5aCymr1emezeHw6C51JdW5wO4y7nwE/export?gid=1759582157&format=csv'
data_0621 = pd.read_csv(url)

#
#
#

grouped = (data_0621
    .assign(
        exityear = lambda dfx: pd.to_datetime(dfx['enddate']).dt.year, 
        exitbin = lambda dfy: pd.cut(dfy['exityear'], range(1870, 2020, 15))
    )
    .groupby(['exitcode', 'exitbin'])
    .agg(freq = ('leadid', 'count'))
    .reset_index()
    .pivot_table(
        values="freq", index="exitbin", columns="exitcode", aggfunc="sum"
    )
)

#
#
#
#

grouped.plot(kind="bar", legend = False)

#
#
#
#
#

sns.set_theme()

sns.barplot(grouped, x="exitbin", y="freq", ci=False)

plt.xticks(rotation=45)
plt.xlabel('Year Leadership Ended')
plt.ylabel('Count of Leaders')
plt.title('The Reign of National Leaders')
plt.legend([], [], frameon=False)
plt.show()

#
#
#
#
#
#
#

url = 'https://raw.githubusercontent.com/erood/interviewqs.com_code_snippets/master/Datasets/online_retail.csv'

data_0531 = pd.read_csv(url)

#
#
#

table = (data_0531
    .assign(
        real_date = lambda dfx: pd.to_datetime(dfx["InvoiceDate"]).dt.date, 
        month_end = lambda dfy: dfy["real_date"] + offsets.MonthEnd(), 
        signup_month = lambda dfz: (dfz.groupby("CustomerID")
            ["month_end"]
            .transform("min")), 
        periods_af = lambda dfa: (dfa["month_end"].dt.to_period("M").view(dtype='int64') - dfa["signup_month"].dt.to_period("M").view(dtype='int64'))
    )
    .groupby(["signup_month", "periods_af"])
    .agg(
        users = ("CustomerID", "nunique")
    )
    .reset_index()
    .assign(
        new_users = lambda dfb: (dfb.groupby("signup_month")
            ["users"]
            .transform("max"))
    )
    .query("periods_af > 0")
    .assign(
        retention = lambda dfc: dfc["users"] / dfc["new_users"], 
        signup_month = lambda dfd: dfd["signup_month"]#.dt.strftime('%b %d,%Y')
    )
    .pivot_table(
        values = "retention", 
        index = ["signup_month", "new_users"], 
        columns = "periods_af", 
    )
    .reset_index()
    .rename_axis(None, axis=1)
)

#
#
#

(table
    .style
    .background_gradient(subset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], axis = 1)
    .applymap(lambda x: 'background-color: transparent; color: transparent;' if pd.isnull(x) else '')
    .format({
        "signup_month": "{:%b %d, %Y}", 
        1: "{:,.0%}", 2: "{:,.0%}", 3: "{:,.0%}", 4: "{:,.0%}", 5: "{:,.0%}", 6: "{:,.0%}", 
        7: "{:,.0%}", 8: "{:,.0%}", 9: "{:,.0%}", 10: "{:,.0%}", 11: "{:,.0%}", 12: "{:,.0%}"
    })
)

#
#
#
#
#
#
#
#
#
#

def calc_earnings(wage, hours):
    if(wage * hours >= 2000):
        rate = 0.3
    else:
        rate = 0.15
    
    print(f'Pre-tax earnings: {round(wage * hours, 2)}\nPost-tax earnings: {round(wage * hours * (1-rate), 2)}')

calc_earnings(40, 35) # Below 2000
calc_earnings(79, 41) # Above 2000

#
#
#
#
#
#
#
#

def find_perimeter(matrix):
    perim = 0

    for r in range(0, len(matrix)):
        for c in range(0, len(matrix[r])):
            # Not a bank
            if(matrix[r][c] != 0):
                # Left
                if(r == 0):
                    perim = perim + 1
                else:
                    perim = perim + 1 if matrix[r-1][c] == 0 else perim
                
                # Right
                if(r == len(matrix) - 1):
                    perim = perim + 1
                else:
                    perim = perim + 1 if matrix[r+1][c] == 0 else perim
                
                # Top
                if(c == 0):
                    perim = perim + 1
                else:
                    perim = perim + 1 if matrix[r][c-1] == 0 else perim

                # Bottom
                if(c == len(matrix[r]) - 1):
                    perim = perim + 1
                else:
                    perim = perim + 1 if matrix[r][c+1] == 0 else perim
    
    return(perim)

#
#
#
#
#

my_matrix = ([
    [1, 0, 1], 
    [1, 1, 1]
])

print(find_perimeter(my_matrix))

#
#
#
#
#

my_matrix2 = ([
    [1, 0]
])

print(find_perimeter(my_matrix2))

#
#
#
#
#

my_matrix3 = ([
    [1,1,1,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0],
    [0,1,1,0,0,0,0,0,0],
    [0,1,0,0,1,1,1,0,0],
    [0,1,0,0,1,1,1,1,0],
    [0,1,1,1,1,0,0,1,1],
    [0,0,0,0,0,0,0,0,0]
])

print(find_perimeter(my_matrix3))

#
#
#
#
#
#
#
#
#
#
#
#

url = 'https://raw.githubusercontent.com/erood/interviewqs.com_code_snippets/master/Datasets/ddi_baby_names.csv'

data_0512 = pd.read_csv(url)

#
#
#
#
#

(data_0512
    .groupby("gender")
    .agg(uniq_num = ("name", "nunique"))
    .reset_index()
)

#
#
#
#
#

(data_0512
    .groupby(["gender", "name"])
    .agg(freq = ("count", "sum"))
    .sort_values(["gender", "freq"], ascending = [False, False])
    .groupby("gender")
    .head(10)
    .reset_index()
)

#
#
#
#
#

(data_0512
    .merge(
        (data_0512
            .query("year >= 2010")
            .groupby(["gender", "name"])
            .agg(freq = ("count", "sum"))
            .sort_values(["gender", "freq"], ascending = [False, False])
            .groupby("gender")
            .head(10)
            .reset_index()
        ), 
        how = 'inner', 
        on = ["gender", "name"]
    )
    .query("year >= 2010")
    [["year", "name", "gender", "count"]]
)

#
#
#
#
#
#
#
#

def LargestSubArray(my_arr, my_A):
    for i in range(A, len(my_arr) + 1):
        sub = my_arr[i-my_A:i]
        sub_chr = ",".join(str(a) for a in sub)
        maxx = max(sub_chr)

        print("In [" + sub_chr + "], max is " + maxx)

#
#
#

my_array = [1, 2, 3, 1, 4, 5, 2, 3, 6]
A = 3

LargestSubArray(my_array, A)

#
#
#
#
#
#
#
#

def SmallestMissingNumber(arr, n, m):
    def present(array, x):
        try:
            array.index(x)
            return True
        except:
            return False

    reals = list(range(0, m))

    for r in reals:
        if not(present(arr, r)): return r

#
#
#

SmallestMissingNumber([0, 1, 3, 4, 8, 9], 5, 10)
SmallestMissingNumber([4, 7, 9, 11], 4, 12)

#
#
#
#
#
#
#
#

data_1209 = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5], 
    "channel": ['online', 'online', 'in_store', 'in_store', 'online'], 
    "date": ['2018-09-01', '2018-09-03', '2018-10-11', '2018-08-21', '2018-08-13'], 
    "month": ['09', '09', '10', '08', '08'], 
    "revenue": [100, 125, 200, 80, 200]
})

#
#
#

(data_1209
    .groupby(['month', 'channel'])
    .agg(
        avg_rev = ('revenue', 'mean')
    )
    .reset_index()
    .rename(columns={'month': 'Month', 'channel': 'Channel', 'avg_rev': 'Avg. Revenue'})
)

#
#
#
#
#
#
#
#
#

def count_words(allreviews):
    uWords = []

    for r in allreviews:
        allwords = r.split()
        for a in allwords:
            if not(uWords.__contains__(a)): uWords.append(a)
    
    return len(uWords)

#
#
#

reviews = ['app is good, but forced updates are too frequent', 'love this app, use it daily to log calories', 'free version of this app has way too many ads', 'app doesn\'t load, 0/10'] 

count_words(reviews)

#
#
#
#
#
#
#

def normalize(vec):
    norm_vec = (vec - vec.mean()) / vec.std()
    return(norm_vec)

#
#
#

df_1130 = pd.DataFrame({
    "Age": [20, 19, 22, 21], 
    "Favorite Color": ["blue", "blue", "yellow", "green"], 
    "Grade": [88, 95, 92, 70], 
    "Name": ["Willard Morris", "Al Jennings", "Omar Mullins", "Spencer McDaniel"]
})

(df_1130
    .assign(norm_Grade = lambda a_df: normalize(a_df['Grade']))
)

#
#
#
#
#
#
#
#
#
#

def calc_earnings(hourly_wage, weekly_hours):
    t_earnings = hourly_wage * weekly_hours
    
    tax = 0.3 if t_earnings >= 2000 else 0.15
    n_earnings = t_earnings * (1 - tax)

    print("Pre-tax earnings: " + "${:,.2f}".format(t_earnings) + "\nPost-tax earnings: " + "${:.2f}".format(n_earnings) + ", at rate of " + "{:0%}".format(tax))
    return t_earnings, n_earnings

#
#
#

calc_earnings(55, 35)
calc_earnings(70, 40)

#
#
#
#
#
#
#
#

df_1121 = pd.DataFrame({
    "Age": [20, 19, 22, 21], 
    "Favorite Color": ["blue", "blue", "yellow", "green"], 
    "Grade": [88, 95, 92, 70], 
    "Name": ["Willard Morris", "Al Jennings", "Omar Mullins", "Spencer McDaniel"]
})

(df_1121
    .loc[(df_1121["Favorite Color"] == "blue") & (df_1121["Grade"] > 90)]
)

#
#
#
#
#
#
#
#

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

#
#
#

a = []

is_prime(101)
is_prime(71)
is_prime(5)

print(a)

#
#
#
#
#
#
#
#
#
#
#
#

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

#
#
#

df_1109 = pd.DataFrame({
    "student_name": ["Leon Rose", "Jamal Mosley", "Michael Malone", "Mike Brown", "Nick Nurse"], 
    "student_id": [1904839, 3824892, 4920940, 2849284, 4824242], 
    "class": ["Business 101", "Communication 210", "Optimization 440", "Tactics 310", "Strategy 550"], 
    "final_grade_pct": [67, 80, 92, 88, 79]
})

add_letter_grades(df_1109)

#
#
#
#
#
#
#
#

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

#
#
#

possibilities(8)

#
#
#
#
#
#
#
#

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

(data_1028
    .pivot_table(
        values = 'user_id', 
        index = 'app_id', 
        columns = 'event', 
        aggfunc = np.count_nonzero
    )
)

#
#
#
#
#
#
#
#
#
#

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

#
#
#

print_num(15)

#
#
#
#
#
#
#
#
#
#

data_1019 = pd.DataFrame({
    "Month": [1, 2, 3], 
    "Revenue": [300, 330, 390]
})

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

#
#
#
#
#
#
#
#
#
#

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

#
#
#

oneEditAway("pea", "pea")
oneEditAway("pea", "lea")
oneEditAway("pea", "seas")

#
#
#
#
#
#
#
#

def assign_buckets(ser):
    m = int(np.ceil(max(ser) / 5) + 1)

    r = list(range(0, m * 5, 5))

    return pd.cut(ser, r)

#
#
#

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

#
#
#
#
#
#
#
#
#
#

def count_overlap(P, z):
    n = 0
    for p in P:
        n = (n + 1) if (p[0] <= z and p[1] >= z) else n
    return n

#
#
#

ivals = [[0, 2], [3, 7], [4, 6], [7, 8], [1, 5]]

count_overlap(ivals, 5)
count_overlap(ivals, 10)

#
#
#
#
#
#
#
#
#
#
#
#

df_0930 = pd.DataFrame({
    "employee_name": ['Andy', 'Beth', 'Cindy', 'Dale', 'Sebastian Andrade', 'Sebastian Andrade', 'Cruz Ellis', 'Andy', 'Sebastian Andrade', 'Judy Vaughan', 'Sebastian Andrade', 'Santiago', 'Cruz Ellis', 'Judy Vaughan', 'Sebastian Andrade', 'Judy Vaughan', 'Santiago', 'Judy Vaughan', 'Sebastian Andrade', 'Sebastian Andrade'], 
    "employee_id": [123456, 789456, 654123, 963852, 858382, 858382, 103030, 123456, 858382, 294902, 858382, 393929, 103030, 294902, 858382, 294902, 393929, 294902, 858382, 858382], 
    "date_joined": ['2015-02-15', np.nan, '2017-05-16', '2018-01-15', '2018-07-14', '2018-07-14', '2013-09-30', '2015-02-15', '2018-07-14', '2020-02-03', '2018-07-14', np.nan, '2013-09-30', '2020-02-03', '2018-07-14', '2020-02-03', np.nan, '2020-02-03', '2018-07-14', '2018-07-14'], 
    "age": [45, 36, 34, 25, 52, 52, 36, 45, 52, 49, 52, 21, 36, 49, 52, 49, 21, 49, 52, 52], 
    "yrs_of_experience": [24, 15, 14, 4, 26, 26, 14, 24, 26, 20, 26, 1, 14, 20, 26, 20, 1, 20, 26, 26]
})

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

#
#
#
#
#
#
#
#

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

#
#
#

QQ = [1, -1, -5, 2, 4, -2, 1]
jj = 3

closest(QQ, jj)

#
#
#
#
#
#
#
#
#
#

data_0921 = pd.DataFrame({
    "date": ['2012-05-11', '2012-05-10', '2012-05-10', '2012-05-07', '2012-05-09', '2012-05-08', '2012-05-11', '2012-05-09', '2012-05-07', '2012-05-07', '2012-05-07', '2012-05-09', '2012-05-07', '2012-05-09', '2012-05-10', '2012-05-08', '2012-05-10', '2012-05-07', '2012-05-08', '2012-05-11', '2012-05-10', '2012-05-09', '2012-05-08', '2012-05-09', '2012-05-07', '2012-05-10', '2012-05-07', '2012-05-09', '2012-05-08', '2012-05-09'], 
    "timestamp": [461860, 518496, 518401, 465793, 518619, 517357, 540481, 461597, 465551, 517524, 465739, 518631, 518581, 461788, 461786, 517347, 461561, 517258, 461651, 540417, 465394, 461668, 540448, 461755, 518391, 461803, 461827, 465481, 465582, 517609], 
    "sender_id": [3739274, 1183813, 1183813, 3739274, 2920404, 2948292, 2920404, 2948292, 2948292, 2920404, 2920404, 5839587, 8484948, 2948292, 2948292, 2948292, 3739274, 5839587, 8484948, 3739274, 2920404, 2920404, 1183813, 2948292, 3739274, 2920404, 3739274, 8484948, 1183813, 5839587], 
    "receiver_id": [1183813, 2948292, 5839587, 2920404, 3739274, 5839587, 3739274, 3739274, 1183813, 3739274, 2948292, 2948292, 2920404, 5839587, 3739274, 2920404, 2948292, 2920404, 2948292, 2920404, 3739274, 8484948, 2948292, 2920404, 2920404, 3739274, 2948292, 2948292, 5839587, 8484948]
})

def create_var(df, name):
    globals()[name] = data_0921
    return df

#
#
#

(data_0921
    .assign(
        date = lambda df1: pd.to_datetime(df1['date'])
    )
    .sort_values(
        ['date', 'timestamp', 'sender_id', 'receiver_id'], 
        ascending = [True, True, True, True]
    )
    .pipe(create_var, 'sorted')
    .merge(
        sorted, 
        how = 'inner', 
        left_on = ['sender_id', 'receiver_id'], 
        right_on = ['receiver_id', 'sender_id']
    )
    .assign(
        prior = lambda df1: (
            df1['date_x'] <= df1['date_y']) & (df1['timestamp_x'] <= df1['timestamp_y']
        ), 
        within_5 = lambda df1: (df1['timestamp_x'] - df1['timestamp_y']) <= 60 * 5
    )
    .pipe(create_var, 'evaled')
    .query('prior == True & within_5 == True')
    .shape[0] / evaled.shape[0]
)

#
#
#
#
#
#
#
#
#
#

def madeEqual(arr):
    def scenario(arr, m):
        eval = []
        test = False
        for i in arr:
            if i != m:
                eval.append(((m / i) % 2) == 0 or ((m / i) % 7) == 0)

        if not(all(eval)):
            scenario(arr, m * 2)
            scenario(arr, m * 7)
            if test != True: return test
        else:
            test = True
            return test
    
    return scenario(arr, max(arr))

#
#
#

madeEqual([128, 4, 2])
madeEqual([65, 4, 2])

#
#
#
#
#
#
#
#
#
#

def getPowerSet(set):
    def find(arr, x):
            try:
                arr.index(x)
                return True
            except:
                return False
    
    def numCombo(r, n):
        def factorial(num):
            f = 1
            for n in range(2, num + 1):
                f = f * n
            return f

        return int(factorial(n) / (factorial(r) * factorial(n - r)))
        
    def sampl(x, n, replace = False):
        arr = []
        
        for i in range(0, n):
            j = rand.randint(0, len(x)-1)
            while not(replace) and find(arr, x[j]):
                j = rand.randint(0, len(x)-1)

            arr.append(x[j])

        return arr

    full = list(set)
    lvl = list(range(2, len(set)))

    power = []
    power.append([])
    
    for l in lvl:
        for i in range(0, numCombo(l, len(full))):
            t = sampl(full, l)
            t.sort()
            while find(power, t):
                t = sampl(full, l)
                t.sort()
            power.append(t)

    power.append(full)

    return power

#
#
#

s1 = {1, 2, 3}
s2 = {4, 5, 6, 7}

getPowerSet(s1)
getPowerSet(s2)

#
#
#
#
#
#
#
#
#
#

df_0909 = pd.DataFrame({
    'date': ['2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-01', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02', '2018-03-02'], 
    'sender_id': [87642, 62684, 17492, 84882, 87642, 49372, 38274, 38274, 10938, 84882, 87642, 62684, 62684, 62684, 38274, 10938, 38274, 17492, 62684, 38274, 17492, 49372, 87642, 10938, 87642, 38274, 87642, 49372, 87642, 84882], 
    'receiver_id': [84882, 49372, 84882, 38274, 62684, 84882, 10938, 17492, 87642, 62684, 38274, 49372, 87642, 10938, 62684, 38274, 17492, 62684, 87642, 84882, 38274, 84882, 84882, 49372, 38274, 87642, 38274, 38274, 38274, 10938]
})

(df_0909
    .loc[df_0909['date'] == '2018-03-01']
    .groupby(['sender_id', 'receiver_id'])
    .count()
    .reset_index()
    [['sender_id', 'receiver_id']]
    .groupby('sender_id')
    .count()
    .reset_index()
    .rename(columns = {'sender_id': 'sender_id', 'receiver_id': 'count'})
)

#
#
#
#
#
#
#
#
#
#

def movingAvg(J, p):
    ma = []

    for i in list(range(0, len(J) - p + 1)):
        j = i + p
        ma.append(np.mean(J[i:j]))
    
    print('[Min, Max]')
    return min(ma), max(ma)

#
#
#

movingAvg([4, 4, 4, 9, 10, 11, 12], 3)

#
#
#
#
#
#
#
#
#
#
#
#

def tallyup(df):
    new_df = (df
        .groupby('date')
        .count()
        ['store_id']
        .reset_index()
        .rename(columns = {'date': 'date', 'store_id': 'count'})
    )

    return new_df

#
#
#

df_0902 = pd.DataFrame({
    'store_id': ['392840', '839284', '882722', '646463', '248274', '994827', '392840', '839284', '882722', '646463', '248274', '994827', '392840', '839284', '882722', '646463', '248274', '994827', '392840', '839284', '882722', '646463', '248274', '994827', '392840', '839284', '882722', '646463', '248274', '994827'], 
    'date': ['2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05', '2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05', '2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05', '2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05', '2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05', '2022-12-01', '2022-12-02', '2022-12-03', '2022-12-04', '2022-12-05'], 
    'status': ['open', 'open', 'open', 'open', 'open', 'open', 'open', 'open', 'fraud', 'open', 'open', 'open', 'closed', 'open', 'fraud', 'open', 'open', 'open', 'closed', 'fraud', 'fraud', 'fraud', 'open', 'fraud', 'closed', 'closed', 'closed', 'fraud', 'open', 'closed'], 
    'revenue': [1946.5, 2300.72, 2013.87, 1795.87, 1502.03, 2322.77, 2265.76, 1938.45, 1934.63, 2547.55, 2089.72, 1767.5, 0, 2148.14, 1853.98, 2398.07, 2605.37, 1990.49, 0, 1119.34, 1866.7, 2033.86, 2377.66, 2843.75, 0, 0, 0, 1657.41, 1543.57, 0]
})

(tallyup(df_0902)
    .merge(
        right = (
            tallyup(df_0902
                .query("revenue > 0 & status == 'fraud'")
            )
        ), 
        how = 'inner', 
        on = 'date'
    )
    .assign(
        percent = lambda dfx: (1.0 * dfx['count_y']) / dfx['count_x']
    )
    [['date', 'percent']]
)

#
#
#
