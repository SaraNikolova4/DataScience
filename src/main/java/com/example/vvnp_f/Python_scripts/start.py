import pandas as pd
from sklearn.preprocessing import LabelEncoder
from neo4j import GraphDatabase
import pandas as pd
import pandas as pd
from neo4j import GraphDatabase
import networkx as nx
from py2neo import Graph


# read the datasets
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\Data_set\eurovision_1957-2021.csv')
winner = pd.read_csv(r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\Data_set\eurovision_winners.csv')
finals = pd.read_csv(r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\Data_set\eurovision_song_contest_1975_2019.csv')

# convert a data in number
df['Points_type'] = df['Points type'].apply(lambda x: 1 if x == 'Points given by televoters' else 0)

# remove a columns
df = df.drop(columns=['Unnamed: 0', 'Edition'])
winner = winner.drop(columns=['Runner-up', 'Margin', 'Host City', 'Date', 'index'])
finals = finals.drop(columns=['Duplicate', 'Points      ', 'To country', 	'Jury or Televoting', 'Edition'])

#remove a duplicates rows
finals = finals.drop_duplicates()

#add other columns
pom = pd.DataFrame(columns=['Country', 'Finals', 'Finals_Count', '1_Semi', '1_Semi_Count', '2_Semi', '2_Semi_Count'])

#select unique from country in one list
countriess = finals['From country'].unique()




#for every country FROM
for country in countriess:
    final = []  # years when participated in final
    one_semi = [] #years when participated in semi1_final
    two_semi = [] # years when participated in semi2_final
    final_c = 0  # how many times he participated in the final
    one_semi_c = 0 # how many times he participated in the semi1_final
    two_semi_c = 0 # how many times he participated in the semi2_final

    for index, row in finals.iterrows():
        if country == row['From country']:
            if row['(semi-) final'] == 'f':
                final.append(row['Year'])
                final_c += 1
            if row['(semi-) final'] == 'sf' or row['(semi-) final'] == 'sf1':
                one_semi.append(row['Year'])
                one_semi_c += 1
            if row['(semi-) final'] == 'sf2':
                two_semi.append(row['Year'])
                two_semi_c += 1


    pom.loc[len(pom)] = [country, final, final_c, one_semi, one_semi_c, two_semi, two_semi_c]


finals = pom

#Trasform
df['From'] = df['From'].str.strip().str.lower()
finals['Country'] = finals['Country'].str.strip().str.lower()

#add columns in original data sets
df['Finals'] = None
df['Finals_Count'] = 0
df['Semi_1'] = None
df['Semi_Count_1'] = 0
df['Semi_2'] = None
df['Semi_Count_2'] = 0

for index, row in df.iterrows():
    for index_f, finale in finals.iterrows():
        if row['From'] == finale['Country']:
            df.at[index, 'Finals'] = finale['Finals']
            df.at[index, 'Finals_Count'] = finale['Finals_Count']
            df.at[index, 'Semi_1'] = finale['1_Semi']
            df.at[index, 'Semi_Count_1'] = finale['1_Semi_Count']
            df.at[index, 'Semi_2'] = finale['2_Semi']
            df.at[index, 'Semi_Count_2'] = finale['2_Semi_Count']



# Save df
df = pd.DataFrame(df)
import os

# Патека до фајлот
file_path = r'C:/Users/Lenovo/Desktop/VVNP_F/src/main/java/com/example/vvnp_f/New_DataSet/full_data_set.csv'

# Создајте ги недостасувачките директориуми
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Зачувајте ја DataFrame-от
df.to_csv(file_path, index=False)
print(df.head())


# Конекција на Neo4j
uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_nodes(tx, data):
    # Create nodes for 'From' column
    from_query = """
    UNWIND $rows AS row
    MERGE (f:Country {name: row.From})
    SET f.finals = row.Finals,
        f.finals_count = row.Finals_Count,
        f.semi_1 = row.Semi_1,
        f.semi_count_1 = row.Semi_Count_1,
        f.semi_2 = row.Semi_2,
        f.semi_count_2 = row.Semi_Count_2
    """

    # Create nodes for 'To' column
    to_query = """
    UNWIND $rows AS row
    MERGE (t:Country {name: row.To})
    SET t.finals = row.Finals,
        t.finals_count = row.Finals_Count,
        t.semi_1 = row.Semi_1,
        t.semi_count_1 = row.Semi_Count_1,
        t.semi_2 = row.Semi_2,
        t.semi_count_2 = row.Semi_Count_2
    """


    # Execute both queries
    tx.run(from_query, rows=data.to_dict('records'))
    tx.run(to_query, rows=data.to_dict('records'))

def create_relationships(tx, data):
    query = """
    UNWIND $rows AS row
    MERGE (f:Country {name: row.From})
    MERGE (t:Country {name: row.To})
    MERGE (f)-[r:CONNECTED_TO]->(t)
    WITH r, row
    SET r.year = 
        CASE 
            WHEN r.year IS NOT NULL THEN r.year + [row.Year]
            ELSE [row.Year]
        END,
    r.points = 
        CASE 
            WHEN r.points IS NOT NULL THEN r.points + [row.Points]
            ELSE [row.Points]
        END,
    r.points_type = 
        CASE 
            WHEN r.points_type IS NOT NULL THEN r.points_type + [row.Points_type]
            ELSE [row.Points_type]
        END
    RETURN r
    """
    tx.run(query, rows=data.to_dict('records'))

def main():
    # Читање на CSV
    df = pd.read_csv(r'C:/Users/Lenovo/Desktop/VVNP_F/src/main/java/com/example/vvnp_f/New_DataSet/full_data_set.csv')


    # Внесување на податоците во Neo4j
    with driver.session() as session:
        session.write_transaction(create_nodes, df)
        session.write_transaction(create_relationships, df)

    driver.close()

if __name__ == "__main__":
    main()

