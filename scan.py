from notion_client import Client
import os

notion = Client(auth=os.environ["NOTION_API_KEY"])
db = notion.databases.query(database_id=os.environ["NOTION_DATABASE_ID"]).get("results")

# do something with the query results, such as:
for result in db:
  print(result)
