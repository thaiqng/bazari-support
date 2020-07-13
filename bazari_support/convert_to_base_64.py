import csv
import base64
from datetime import datetime
from os import walk

folder=input('Enter the folder path: ')

files=[]
pictures_b64=[]

for dirpath, dirnames, filenames in walk(folder):
  files.extend(filenames)

print("[IN PROGRESS] Converting pictures to base_64. Please wait...")
for file in files:
  print("Converting picture " + str(files.index(file) + 1) + "/" + str(len(files)) + "...")
  picture_dir=folder + "/" + file
  with open(picture_dir, 'rb') as img_file:
    picture_b64="data:image/png;base64,"+base64.b64encode(img_file.read()).decode('utf-8')
    pictures_b64.append(picture_b64)

print("[IN PROGRESS] Writing data to 'index.csv'. Please wait...")
# Open a csv file with append instead of erasing.
csv_dir=folder + "/" + 'index.csv'
with open(csv_dir, 'a') as csv_file:
  writer = csv.writer(csv_file)
  for picture_b64 in pictures_b64:
    writer.writerow([file, picture_b64, datetime.now()])

print("[DONE] Finish converting " + str(len(files)) + " pictures to base_64.")
