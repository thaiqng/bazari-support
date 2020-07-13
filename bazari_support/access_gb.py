import csv

import anvil.server
anvil.server.connect("NCQHRMRGTCNNGLUUUUKQIM2M-LHKZF6QGOHJTJ32F")

@anvil.server.callable
def uplink_access_data():
  data=[]
  with open('index.csv') as file:
    reader=csv.reader(file, delimiter=',')
    for row in reader:
      data.append((row[0], row[1], row[2]))

    return data

anvil.server.wait_forever()