from neo4j import GraphDatabase
import pandas as pd

uri = "bolt://localhost:7687"  # Replace with your Neo4j server URI
username = "..."  # Replace with your Neo4j username
password = "..."  # Replace with your Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

# Read the TSV files into pandas DataFrames
df1 = pd.read_csv('mooc_actions.tsv', sep='\t')
df2 = pd.read_csv('mooc_action_features.tsv', sep='\t')
df3 = pd.read_csv('mooc_action_labels.tsv', sep='\t')

# Concatenate the DataFrames vertically
combined_df = pd.concat([df1, df2, df3], axis=1)

# Remove duplicate columns, if any
combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

# Convert the Dataframe to a table
combined_list = combined_df.values.tolist()
combined_list.remove(combined_list[0])
print(combined_list[-1])

# Create a Neo4j session
with driver.session() as session:
    for rows in combined_list:
        # Create a node for each unique user
        session.run("MERGE (u:User {user_id: $user_id})", user_id=rows[1])
        # Create a node for each unique target
        session.run("MERGE (t:Target {target_id: $target_id})", target_id=rows[2])
    for rows in combined_list:
        # Create an edge between the user and the target for each action
        session.run("""
                   MATCH (u:User {user_id: $user_id})
                   MATCH (t:Target {target_id: $target_id})
                   CREATE (u)-[:ACTION {action_id: $action_id, action_timestamp: $action_timestamp,
                   action_feature0: $action_feature0, action_feature1: $action_feature1, action_feature2:
                   $action_feature2, action_feature3: $action_feature3, action_label: $action_label}]->(t)
                   """,
                    user_id=rows[1], target_id=rows[2], action_id=rows[0], action_timestamp=rows[3],
                    action_feature0=rows[4], action_feature1=rows[5], action_feature2=rows[6],
                    action_feature3=rows[7], action_label=rows[8])
