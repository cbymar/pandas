import datetime as dt
import numpy as np
import pandas as pd

##############
# from here:
# https://www.udemy.com/course/data-analysis-with-pandas/learn/lecture/5931596#overview
# Lec32:
webster = {'aardvark': 'animal',
           'banana': 'fruit',
           'cyan': 'color'}

pd.Series(webster)  # no numeric index.  Series labels do not have to be unique.
alist = ["id", "title", "tagline", "release_date", "genres", "belongs_to_collection"]
s = pd.Series(alist)
## show attributes
s.values, s.index, s.keys()
## Do same with numeric series
s = pd.Series([2.99, 4.45, 1.36])
s.mean()  # basic functions
s.get(1)  # get a single value by position

## pandas read in, but as a series
pk = pd.read_csv("./ignoreland/pokemon.csv", usecols=["Pokemon"], squeeze=True)
type(pk)
pk.is_unique
pk.sort_values(inplace=True)
pk.get(key=[0, 4])
pk.get([0, 4])  # pass a list to get arbitrary values by position

#### c-bind numpy arrays into a dataframe:
pkbs = np.random.choice(pk, size=5000, replace=True)
names, nco = np.unique(pkbs, return_counts=True)  # 2 ndarrays
npc = np.concatenate((names,nco)).reshape(-1,2)
npc.ndim
npc.shape
pdc = pd.DataFrame(npc, columns=['Name', 'n_occurrences'])
pdc.info()

#### Math on series
google = pd.read_csv("./ignoreland/google_stock_price.csv", squeeze=True)
google.count()  # excludes null or nan values
len(google)  # does not exclude
google.idxmax()  # index of largest value
google[google.idxmin()]  # get the smallest value; same as below
google.min()

#### functions can be .applied to series

#### map a function to a series
pk_types = pd.read_csv("./ignoreland/pokemon.csv", index_col="Pokemon", squeeze=True)
pk.head(10)
pk.map(pk_types)  # maps the type to each name. map doesn't require a function, just k:v pairs
## demonstrate using an actual dict
pk_types = pd.read_csv("./ignoreland/pokemon.csv", index_col="Pokemon", squeeze=True).to_dict()
pk.map(pk_types)

#### Dataframes
nba = pd.read_csv("./ignoreland/nba.csv")
nba.shape
nba.info()
nba.dtypes  # returns a series
nba.columns  # returns an index object
nba.axes  # list of two objects: a range index and ordinary index.

rev = pd.read_csv("./ignoreland/revenue.csv", index_col="Date")
rev.head()
rev.sum(axis=1)  # sum over columns

#### Extract or add column
nba.Salary.sum()  # unpreferred; better to use bracket syntax.  Returns series.
nba[["Name", "Team"]]  # returns df.  Must list column names in a list.

nba["Sport"] = "Basketball"  # broadcasts. Can also try:
nba.insert(3, column="Sport2", value="bball")  # puts in the specified position
nba.iloc[:,2:].head()

#### broadcasting operations
# straightforward.

#### Dropping rows with nulls
nba.dropna(axis=0, how="any", inplace=True)  #
nba.dropna(axis=0, how="any", subset=["Salary"])  # remove rows where the value is missing from those columns

#### Fillna
# better to use on individual series
nba["Salary"].value_counts(ascending=False)
nba["Salary"].fillna(0, inplace=True)
nba["College"].fillna("Nocollege", inplace=True)

#### Convert types using .astype()  -- there's no inplace option
nba["Salary"] = nba["Salary"].astype("int")
nba.dtypes
nba["Age"] = nba["Age"].astype("int", errors="ignore")

# best to use category datatype for 'factors' -- pandas internally normalizes
nba["Position"] = nba["Position"].astype("category")
nba.info()  # watch for memory use reductions
nba["Team"] = nba["Team"].astype("category")

#### Sorting dataframes
nba.sort_values("Age", ascending=False).head(30)  # nan values are default last

nba.sort_values(["Age", "Salary"], ascending=[True, False], inplace=True)
nba.head()
# .sort_index() method
nba.sort_index(inplace=True)  # puts it right back

#### Rank series values
nba = pd.read_csv("./ignoreland/nba.csv")
nba["Salary"] = nba["Salary"].fillna(0).astype("int")  # can't use inplace=True in chained methods

nba["Salary"].rank(ascending=False).astype("int")
nba["SalaryRank"] = nba["Salary"].rank(ascending=False).astype("int")  # it's a dense rank
nba.sort_values(by="Salary",ascending=False)

#### Memory management
employees = pd.read_csv("./ignoreland/employees.csv")
employees.info()
employees["Start Date"] = pd.to_datetime(employees["Start Date"])
employees.columns = [x.replace(" ", "_") for x in employees.columns]  # no need for lambda function
# If I'm using a lambda function on a list, need to map it
employees["Senior_Management"] = employees["Senior_Management"].astype("bool")  # save space
employees["Gender"] = employees["Gender"].astype("category")  # save space

employees_format = pd.read_csv("./ignoreland/employees.csv", parse_dates=["Start Date"])
employees_format.info()

#### Filtering: assign a boolean series to a mask
mask = employees_format["Gender"] == "Male"
mask2 = employees_format["Team"] == "Marketing"
men = employees_format[mask]
men.shape
employees_format[mask & mask2]

#### Filtering: use .isin()
mask = employees_format["Team"].isin(["Marketing","Finance"])

mkfin = employees_format[mask]
mkfin.shape

mask = employees_format["Team"].isnull()  # or notnull

#### Filtering: Use .between()
mask = employees_format["Salary"].between(50000, 80000)
employees_format[mask]

#### Exclude duplicates with .duplicated()