## MEDICAL INTENT RECOGNIZE

### Deadline
28 May 2021

### Task
+ Reproduce QA system from HHH repository which using pattern matching for user's intent.

### Step
+ Install DBMS Neo4j follow link: https://www.liquidweb.com/kb/how-to-install-neo4j-on-ubuntu-20-04/
+ Custom password and port to connecting DBMS
+ Build KG & Import into DBMS: run file build_medicalgraph.py
+ Testing query DBMS: run file answer_search.py
+ System testing with command line: run file chatbot_graph.py
+ Using chatbot with GUI: run file GUI.py