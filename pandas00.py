import datetime as dt
import numpy as np
import pandas as pd

##############
# Point of this script is a reference for a lot of the ordinary manipulations
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
npc = np.concatenate((names, nco)).reshape(-1, 2)
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
nba.iloc[:, 2:].head()

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
nba.sort_values(by="Salary", ascending=False)

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
mask = employees_format["Team"].isin(["Marketing", "Finance"])

mkfin = employees_format[mask]
mkfin.shape

mask = employees_format["Team"].isnull()  # or notnull

#### Filtering: Use .between()
mask = employees_format["Salary"].between(50000, 80000)
employees_format[mask]

#### Exclude duplicates with .duplicated()
employees = pd.read_csv("./ignoreland/employees.csv")
employees.columns = [x.replace(" ", "_") for x in employees.columns]  # no need for lambda function
dups = employees["First_Name"].duplicated(keep="first")  # note the keep=False will clobber every row that is not unique
employees["First_Name"].nunique(dropna=False)  # need to handle NAs if triangulating this.
sum(dups == False)
sum(dups == True)
employees["First_Name"].fillna("Zeus", inplace=True)
dups = employees["First_Name"].duplicated(keep="first")
fnames = employees.loc[dups == False, "First_Name"].squeeze()
len(fnames)
fnameset = set(employees["First_Name"].squeeze())
len(fnameset)
fnames = set(pd.concat([fnames, pd.Series("ApolloCreed")], axis=0))

fnameset ^ fnames  # show the set difference
len(fnameset & fnames)
fnameset.difference(fnames)
fnames.difference(fnameset)
# take highest-salaried individual
employees = pd.read_csv("./ignoreland/employees.csv")
employees.columns = [x.replace(" ", "_") for x in employees.columns]
employees.sort_values(by=["First_Name", "Salary"], ascending=[True, False], inplace=True)
highest_salary = employees.drop_duplicates(subset=["First_Name"], keep="first")

employees.sort_values(by=["First_Name", "Salary"], ascending=[True, True], inplace=True)
lowest_salary = employees.drop_duplicates(subset=["First_Name"], keep="first")
len(highest_salary)
len(lowest_salary)

#### Count distinct values
# straightforward, except don't forget the na action.
jb = pd.read_csv("./ignoreland/jamesbond.csv")  # index_col= is an option

#### set_index, reset index. We can shuffle indices and columns around
jb.set_index(keys="Film", inplace=True)  # requires the inplace.
jb.reset_index(drop=False, inplace=True)  # we don't want to lose the film column

jb.set_index(keys="Film", inplace=True)
jb.reset_index(inplace=True)
jb.set_index("Year", inplace=True)

#### .loc[] accessor
jb = pd.read_csv("./ignoreland/jamesbond.csv", index_col="Film")
jb.columns = [x.replace(" ", "_") for x in jb.columns]
# easier to search when dataset is sorted by index. Like R data.table
jb.sort_index(inplace=True)
# Check whether a label is in the index first:
"Tuxedo" in jb.index
# use second label to correspond to second dimension.

jb.loc["Moonraker", "Actor" : "Box_Office"]

#### .iloc reflects whatever index is in place.
# iloc can take a tuple, I think.

#### both loc and iloc can be used to identify values that get overwritten
jb
#### renaming values
mapper = {"Skyfall":"bschool",
          "Casino Royale":"gradschool",
          "Die Another Day":"college",
          "Tomorrow Never Dies":"highschool"}

jb.rename(mapper=mapper, axis=0)  # renaming  based on index
# can do same with columns.
# << dataframe.rename(mapper=, axis=) >>

#### drop rows if we want
jb.drop("Dr. No", axis=0)
actor = jb.pop("Actor")  # Removes from the df, truly popping it.
del jb["Director"]  # this deletes the column.

#### Random sampling:
jb = pd.read_csv("./ignoreland/jamesbond.csv", index_col="Film")
jb.columns = [x.replace(" ", "_") for x in jb.columns]
asample = jb.sample(n=8, replace=True, axis=0).sort_index()  # Note that the axis is an arg.
asample = jb.sample(n=8, replace=True, axis=0)

#### .nsmallest() and .nlargest(); they work on df or series
jb.nsmallest(4, columns="Budget")

#### Filtering df with query method.
jb.query("Actor == 'Sean Connery'").sort_index()
jb.query("Budget > 50").sort_values(by="Year")
jb.query("Actor not in ['Sean Connery', 'Timothy Dalton']")
jb.query("Actor in ['Sean Connery', 'Timothy Dalton']")

#### Apply function
def string_money(numeric):
    return str(numeric) + " pounds sterling!"

jb["Box_Office"] = jb["Box_Office"].apply(string_money)
colhere = ["Box_Office", "Budget", "Bond_Actor_Salary"]

#### Can also use applymap after using series selection to pull out column names
colhere = list(jb.dtypes[jb.dtypes=="float64"].keys())
jb[colhere] = jb[colhere].applymap(string_money, na_action='ignore')

#### String methods
chi = pd.read_csv("./ignoreland/chicago.csv")
chi.iloc[:,1:].head()
chi.info()
chi[["Position Title", "Department"]] = chi[["Position Title", "Department"]].apply(lambda x: x.astype("category"))

chi["Department"].str.len()
# chi["Department"] = chi["Department"].str.replace("O","E")
mask = chi["Position Title"].str.lower().str.contains("water")
# str.startswith()

#### Splitting strings and getting the right element (this is vectorized):
chi["Name"].str.split(",").str.get(0)  # get the element by position.
# get the first name cleanly and tabulate:
chi["Name"].str.split(",").str.get(1).str.strip().str.split(" ").str.get(0).value_counts(ascending=False).head()

#### expand and n params for str.split()
chi[["title1","titlerest"]] = chi["Position Title"].str.split(" ", expand=True, n=1)
# expand takes it across multiple columns
"Hi the point is to take from the right".str.rpartition(" ", )[-1]
chi["Position Title"].str.rpartition(" ", expand=True).get(2)

#### Get the index values level
bigmac = pd.read_csv("./ignoreland/bigmac.csv", parse_dates=["Date"], index_col = ["Date","Country"])
bigmac.info()
aa = bigmac.index.get_level_values("Date")  # get the values (not necessarily distinct)
len(aa)
aa.nunique()  # index is not a set.
## Sort by the index (typical op):
bigmac.sort_index(inplace=True)
bigmac.index.set_names(names="Day",level=0,inplace=True)
bigmac.index

#### Sort on multiindex.  Default is to sort outer to inner
bigmac.sort_index(ascending=[True,False], inplace=True)
bigmac

#### Sort stably:
bigmac.sort_index(level=0, ascending=False, inplace=True)  # only sort on that level of the index


#### Risk: using .loc['',''], the second argument could be index value or column label.
# avoid this bug using a tuple to encapsulate all row-indexing information
bigmac.loc[("2010-01-01",)]

# iloc is unchanged: rows are rows; there is no counting within-index.

#### Transpose method.
bigmac = bigmac.transpose()  # no inplace param

#### Pivoting
sales = pd.read_csv("./ignoreland/salesmen.csv", parse_dates=["Date"])
sales["Salesman"] = sales["Salesman"].astype("category")
## index is what's in the rows; columns obviously are columns; values -- is there a default aggregate function?
sales.pivot(index = "Date", columns = "Salesman", values = "Revenue")

# count unique combinations of two columns.  Use set_index, not group_by().
# https://stackoverflow.com/questions/35268817/unique-combinations-of-values-in-selected-columns-in-pandas-data-frame-and-count
sales.groupby(["Date","Salesman"]).size()
sales.set_index(["Date","Salesman"]).index.size  # scalar with the length of the index
sales.set_index(["Date","Salesman"]).index.nunique()  # scalar with length of the deduplicated index
sales["Salesman"].nunique() * sales["Date"].nunique()

#### pivot_table()
foods = pd.read_csv("./ignoreland/foods.csv")
foods.info()
aa = foods.pivot_table(values="Spend", index="Gender", aggfunc="sum")
type(aa)  # it returns a data frame
aa.info()
aa = foods.pivot_table(values="Spend", index=["Gender","Item"], aggfunc="sum")
# Factor it out by city
aa = foods.pivot_table(values="Spend", index=["Gender","Item"], columns=["City"], aggfunc="sum", fill_value=0)
aa

#### Melting
sales = pd.read_csv("./ignoreland/quarters.csv")
sales.melt(id_vars="Salesman", var_name=["QuarterMelted"], value_name="Revenue")

#### Groupby
ft = pd.read_csv("./ignoreland/fortune1000.csv")
ft.info()
sectors = ft.groupby("Sector")  # placeholder, not useful until used. does not have an .info method
type(ft), type(sectors)
len(sectors)
sectors.size()  # sorts alpha
# what can we do with groupby object:
sectors.first()
aa = sectors.max()
aa = sectors.sum()  # restricts to the columns that are amenable to that function.
# look at a specific group, plucked from the groupby object:
sectors.get_group("Apparel")["Revenue"].sum()  # get (only one) specific group
sectors["Revenue"].sum()  # look just at a single column and apply a function

sector_indust = ft.groupby(["Sector","Industry"])
aa = sector_indust["Revenue"].mean()
aa.index.size
type(aa.index[0])  # series of tuples.
type(aa.index)  # type is multiindex.

#### Using agg:
sector_indust.agg({"Revenue":["sum","mean"]})

#### Iterating through groupby to build out a summary dataframe
ft = pd.read_csv("./ignoreland/fortune1000.csv", index_col="Rank")
df = pd.DataFrame(columns=ft.columns)
df  # (blank)

for sector, data in sectors:
    """ data is the 'value' for the key of sector"""
    highest_rev_by_group = data.nlargest(1, "Revenue")
    df = df.append(highest_rev_by_group)  # no inplace

cities = ft.groupby("Location")
df = pd.DataFrame(columns=ft.columns)  # new blank df
for city, data in cities:
    highest_rev_by_city = data.nlargest(1, "Revenue")
    df = df.append(highest_rev_by_city)

#### Joining/concatenating
week1  = pd.read_csv("./ignoreland/Restaurant - Week 1 Sales.csv")
week2  = pd.read_csv("./ignoreland/Restaurant - Week 2 Sales.csv")
customers = pd.read_csv("./ignoreland/Restaurant - Customers.csv")
foods = pd.read_csv("./ignoreland/Restaurant - Foods.csv")

aa = pd.concat(objs=[week1, week2])
bb = pd.concat(objs=[week1, week2], ignore_index=False)
cc = pd.concat(objs=[week1, week2], ignore_index=True)  # creates a new index
bb.index.size
bb.index.nunique()
cc.index.nunique()

dd = week1.append(other=week2)
dd.equals(aa)
bb.equals(dd)
cc.equals(dd)  # False

aa = pd.concat(objs=[week1, week2], keys=["Week_1", "Week_2"])
bb = aa.loc[("Week_1",), ["Customer ID", "Food ID"]]
type(bb)  # dataframe if more than one column is selected.

#### Inner join

joinkey = "Customer ID"  # we can pass this as a variable
week1.sort_values(by=joinkey, inplace=True)
week2.sort_values(by=joinkey, inplace=True)
len(week1), len(week2)
aa = week1.merge(week2, how="inner", left_on=joinkey, right_on=joinkey, suffixes=["_left","_right"],
                 sort=True, indicator=True)
len(aa)

#### Inner join (compound key)
joinkey = ["Customer ID","Food ID"]  # we can pass this as a variable
aa = week1.merge(week2, how="inner", left_on=joinkey, right_on=joinkey, suffixes=["_left","_right"])

#### Outer join
joinkey = "Customer ID"  # we can pass this as a variable
aa = week1.merge(week2, how="outer", left_on=joinkey, right_on=joinkey, suffixes=["_left","_right"],
                 indicator=True, sort=True)
aa.shape
# use aa["_merge"].value_counts() to summarize the provenance of each row
aa["_merge"].value_counts()
## and we can remove the intersection by
mask_aa_xor = aa["_merge"].isin(["left_only","right_only"])  #this only creates a mask
aa_xor = aa[mask_aa_xor]

#### Leftjoin
joinkey = "Food ID"  # we can pass this as a variable
aa = week1.merge(foods, how="left", left_on=joinkey, right_on=joinkey, suffixes=["_left","_right"],
                 sort=True)
len(foods)
len(week1)
len(aa)
aa.index.size
aa.index.nunique()
# use .drop(right_on, axis=1) after confirming the join worked.

bb = week2.merge(customers, how="left", left_on="Customer ID", right_on="ID", suffixes=["_left","_right"],
                 sort=True, indicator=True)

#### use indexes so that we do not need to drop the column:
customers = pd.read_csv("./ignoreland/Restaurant - Customers.csv")
cc = week1.merge(customers, how="left", left_on="Customer ID", right_on="ID", suffixes=["_left","_right"],
                 sort=True, indicator=True).drop("ID", axis=1)
customers = pd.read_csv("./ignoreland/Restaurant - Customers.csv", index_col="ID")
dd = week1.merge(customers, how="left", left_on="Customer ID", right_index=True, suffixes=["_left","_right"],
                 sort=True, indicator=True, )
cc.equals(dd)  # false at first
dd.reset_index(drop=True, inplace=True)  # it becomes equivalent only after we reindex
cc.equals(dd)  # true now.

#### To do a join just "on" indexes, use .join()
week1 = pd.read_csv("./ignoreland/Restaurant - Week 1 Sales.csv")
satisf = pd.read_csv("./ignoreland/Restaurant - Week 1 Satisfaction.csv")
len(satisf)
joined = week1.join(satisf)   # fast.


