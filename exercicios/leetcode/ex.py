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