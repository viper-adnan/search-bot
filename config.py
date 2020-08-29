import os

config = """
  BOT_TOKEN = "{}"
  OWNER_ID = {}
  """.format(
          os.environ.get("BOT_TOKEN"),
          os.environ.get("OWNER_ID"))

with open('config.env', 'w') as conf:
  print(config, file=conf)

drive_index = os.environ.get("DRIVE_INDEX", "")

with open('drive_index.txt', 'w') as di:
  print(drive_index, file=di)
