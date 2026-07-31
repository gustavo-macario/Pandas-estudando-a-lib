# %%
# 595. Big Countries
import pandas as pd

def big_countries(world: pd.DataFrame) -> pd.DataFrame:
    world = world[(world['area'] >= 3000000) | (world['population'] >= 25000000)][['name', 'population', 'area']]
    return world

# %%
# 1757. Recyclable and Low Fat Products
import pandas as pd

def find_products(products: pd.DataFrame) -> pd.DataFrame:
    products = products[(products['low_fats'] == 'Y') & (products['recyclable'] == 'Y')][['product_id']]
    return products

# %%
# 183. Customers Who Never Order
import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    semid = customers.merge(right=orders, how='left', left_on='id', right_on='customerId')
    semid = semid[semid['customerId'].isna()][['name']].rename(columns={'name': 'Customers'})
    return semid

# %%
# 1148. Article Views I
import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:
    views = views[views['author_id'] == views['viewer_id']]
    views = views[['author_id']].drop_duplicates().rename(columns={'author_id': 'id'}).sort_values(by='id')
    return views

# %%
# 1683. Invalid Tweets
import pandas as pd

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    tweets = tweets[tweets['content'].str.len() > 15]
    return tweets[['tweet_id']]

# %%
# 1873. Calculate Special Bonus
import pandas as pd
import numpy as np

def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    condicao = (employees['employee_id'] % 2 != 0) & (~employees['name'].str.startswith('M'))
    employees['bonus'] = np.where(condicao, employees['salary'], 0)
    return employees[['employee_id', 'bonus']].sort_values(by='employee_id')

# %%
# 1667. Fix Names in a Table
import pandas as pd

def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    users['name'] = users['name'].str.lower()
    users['name'] = users['name'].str[0].str.upper() + users['name'].str[1:]
    return users.sort_values(by='user_id')

# %%
# 1527. Patients With a Condition
import pandas as pd

def find_patients(patients: pd.DataFrame) -> pd.DataFrame:
    patients = patients[patients['conditions'].str.contains(r'\bDIAB1', na=False)]
    return patients

# %%
# 176. Second Highest Salary
import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    salarios_unicos = employee[['salary']].drop_duplicates().sort_values(by='salary', ascending=False)

    if len(salarios_unicos) < 2:
        return pd.DataFrame({'SecondHighestSalary': [None]})

    second = salarios_unicos.iloc[[1]]
    return second.rename(columns={'salary': 'SecondHighestSalary'})


# %%
# 184. Department Highest Salary
import pandas as pd

def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    top_employees = employee.merge(right=department, how='inner', left_on='departmentId', right_on='id')
    top_employees['max_salary'] = top_employees.groupby('departmentId')['salary'].transform('max')
    top_employees = top_employees[top_employees['salary'] == top_employees['max_salary']]
    top_employees = top_employees[['name_y', 'name_x', 'salary']]
    return top_employees.rename(columns={
        'name_y': 'Department', 
        'name_x': 'Employee', 
        'salary': 'Salary'
    })

# %%
# 178. Rank Scores
import pandas as pd

def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    scores = scores.sort_values(by='score', ascending=False)
    scores['rank'] = scores['score'].rank(method='dense', ascending=False)
    return scores[['score', 'rank']]

# %%
# 196. Delete Duplicate Emails
import pandas as pd

def delete_duplicate_emails(person: pd.DataFrame) -> None:
    person.sort_values(by='id', inplace=True)
    person.drop_duplicates(subset=['email'], keep='first', inplace=True)

# %%
# 1795. Rearrange Products Table
import pandas as pd

def rearrange_products_table(products: pd.DataFrame) -> pd.DataFrame:
    df = products.melt(
        id_vars='product_id',
        value_vars=['store1', 'store2', 'store3'],
        var_name='store',
        value_name='price'
    ).dropna()
    return df

# %%
# 1907. Count Salary Categories
import pandas as pd

def count_salary_categories(accounts: pd.DataFrame) -> pd.DataFrame:
    low_count = len(accounts[accounts['income'] < 20000])
    avg_count = len(accounts[(accounts['income'] >= 20000) & (accounts['income'] <= 50000)])
    high_count = len(accounts[accounts['income'] > 50000])
    
    resultado = pd.DataFrame({
        'category': ['Low Salary', 'Average Salary', 'High Salary'],
        'accounts_count': [low_count, avg_count, high_count]
    })
    
    return resultado


# %%
# 1741. Find Total Time Spent by Each Employee
import pandas as pd

def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    employees['total_time'] = employees['out_time'] - employees['in_time'] 
    df = employees.groupby(['event_day', 'emp_id'])['total_time'].sum().reset_index()
    return df.rename(columns={'event_day': 'day'})

# %%
# 511. Game Play Analysis I
import pandas as pd

def game_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    activity = activity.sort_values(by='event_date', ascending=True)
    activity['rank'] = activity.groupby('player_id')['event_date'].rank(method='dense', ascending=True)
    primeiros = activity[activity['rank'] == 1]
    primeiros = primeiros.rename(columns={'event_date': 'first_login'})
    return primeiros[['player_id', 'first_login']]

# %%
# 2356. Number of Unique Subjects Taught by Each Teacher
import pandas as pd

def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    df = teacher.groupby('teacher_id')['subject_id'].nunique().reset_index()
    return df.rename(columns={'subject_id': 'cnt'})

# %%
# 596. Classes With at Least 5 Students
import pandas as pd

def find_classes(courses: pd.DataFrame) -> pd.DataFrame:
    df = courses.groupby('class')['student'].count().reset_index()
    df = df[df['student'] >= 5]
    return df[['class']]

# %%
# 586. Customer Placing the Largest Number of Orders
import pandas as pd

def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.groupby('customer_number')['order_number'].count().sort_values(ascending=False).reset_index()
    return df[['customer_number']].head(1)

# %%
# 1484. Group Sold Products By The Date
import pandas as pd

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    df = activities.groupby('sell_date')['product'].agg(
        num_sold='nunique',
        products=lambda x: ','.join(sorted(x.unique()))
    ).reset_index()
    return df

# %%
# 1693. Daily Leads and Partners
import pandas as pd

def daily_leads_and_partners(daily_sales: pd.DataFrame) -> pd.DataFrame:
    df = daily_sales.groupby(['date_id', 'make_name'])[['lead_id', 'partner_id']].nunique().reset_index()
    return df.rename(columns={
        'lead_id': 'unique_leads',
        'partner_id': 'unique_partners'
    })

# %%
# 1050. Actors and Directors Who Cooperated At Least Three Times
import pandas as pd

def actors_and_directors(actor_director: pd.DataFrame) -> pd.DataFrame:
    df = actor_director.groupby(['actor_id', 'director_id']).count().reset_index()
    df = df[df['timestamp'] >= 3]
    return df[['actor_id', 'director_id']]

# %%
# 1378. Replace Employee ID With The Unique Identifier
import pandas as pd

def replace_employee_id(employees: pd.DataFrame, employee_uni: pd.DataFrame) -> pd.DataFrame:
    df = employees.merge(right=employee_uni, how='left', on='id')
    return df[['unique_id', 'name']]

# %%
# 1280. Students and Examinations
import pandas as pd

def students_and_examinations(students: pd.DataFrame, subjects: pd.DataFrame, examinations: pd.DataFrame) -> pd.DataFrame:
    df = students.merge(right=subjects, how='cross')
    examinations['attended_exams'] = 1
    df = df.merge(right=examinations, how='left', on=['student_id', 'subject_name'])
    df = df.groupby(['student_id', 'student_name', 'subject_name'], dropna=False)['attended_exams'].count().reset_index()
    return df.sort_values(by=['student_id', 'subject_name'])

# %%
# 570. Managers with at Least 5 Direct Reports
import pandas as pd

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    df = employee.merge(right=employee, how='left', left_on='id', right_on='managerId')
    df = df.groupby(['id_x', 'name_x'], dropna=False)['managerId_y'].count().reset_index()
    df = df[df['managerId_y'] >= 5]
    df = df.rename(columns={'name_x': 'name'})
    return df[['name']]

# %%
# 607. Sales Person
import pandas as pd

def sales_person(sales_person: pd.DataFrame, company: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    red_company = company[company['name'] == 'RED']  
    red_orders = orders.merge(red_company, on='com_id')
    red_sales_ids = red_orders['sales_id'].unique()   
    return sales_person[~sales_person['sales_id'].isin(red_sales_ids)][['name']]