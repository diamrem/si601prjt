import sqlite3 as sqlite
import time
from collections import OrderedDict


def count_revision_per_hour(rows):	
	data = []
	for row in rows:
		data.append([time.strptime(row[0],"%Y-%m-%d %H:%M:%S"),row[1]])
	hour_list={}
	for d in data:
		hour = d[0][3]
		if hour_list.has_key(hour):
			hour_list[hour] += 1
		else:
			hour_list[hour] = 1
	#print hour_list
	count_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[1], reverse=True))
	hour_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[0]))
	with open('2_output_count_sorted.txt','wb') as f:
		f.writelines('Count\tHour\n')
		for l in count_ordered_list.keys():
			f.writelines(str(count_ordered_list[l])+'\t'+str(l)+ '\n')
	with open('2_output_hour_sorted.txt','wb') as f:
		f.writelines('Hour\tCount\n')
		for l in hour_ordered_list.keys():
			f.writelines(str(l)+'\t'+str(hour_ordered_list[l])+ '\n')

def count_revision_per_hour_weekday(rows):
	data = []
	for row in rows:
		data.append([time.strptime(row[0],"%Y-%m-%d %H:%M:%S"),row[1]])
	hour_list={}
	for d in data:
		hour = d[0][3]
		week = d[0][6]
		if week < 5:	
			if hour_list.has_key(hour):
				hour_list[hour] += 1
			else:
				hour_list[hour] = 1
	#print hour_list
	hour_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[0]))
	with open('2_output_weekday.txt','wb') as f:
		f.writelines('Hour\tCount per day\n')
		for l in hour_ordered_list.keys():
			f.writelines(str(l)+'\t'+str(hour_ordered_list[l]/5)+ '\n')

def count_revision_per_hour_weekend(rows):
	data = []
	for row in rows:
		data.append([time.strptime(row[0],"%Y-%m-%d %H:%M:%S"),row[1]])
	hour_list={}
	for d in data:
		hour = d[0][3]
		week = d[0][6]
		if week > 4:	
			if hour_list.has_key(hour):
				hour_list[hour] += 1
			else:
				hour_list[hour] = 1
	#print hour_list
	hour_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[0]))
	with open('2_output_weekend.txt','wb') as f:
		f.writelines('Hour\tCount per day\n')
		for l in hour_ordered_list.keys():
			f.writelines(str(l)+'\t'+str(hour_ordered_list[l]/2)+ '\n')

def count_revision_per_hour_wdays_wends(rows):
	data = []
	for row in rows:
		data.append([time.strptime(row[0],"%Y-%m-%d %H:%M:%S"),row[1]])
	hour_list={}
	for d in data:
		hour = d[0][3]
		week = d[0][6]	
		if hour_list.has_key(hour):
			if week<5:
				hour_list[hour][0] += 1
			else:
				hour_list[hour][1] += 1
		else:
			hour_list[hour] = [0,0]
	#print hour_list

	hour_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[0]))
	with open('2_output_wdays_wends.txt','wb') as f:
		f.writelines('Hour\tWeekdays\tWeekends\n')
		for i in hour_ordered_list:
			f.writelines(str(i)+'\t'+str(hour_ordered_list[i][0]/5)+'\t'+str(hour_ordered_list[i][1]/2)+'\n')


def count_revision_per_hour_wdays(rows):
	data = []
	for row in rows:
		data.append([time.strptime(row[0],"%Y-%m-%d %H:%M:%S"),row[1]])
	hour_list={}
	for d in data:
		hour = d[0][3]
		week = d[0][6]	
		if hour_list.has_key(hour):
			if hour_list[hour].has_key(week):
				hour_list[hour][week] += 1
			else:
				hour_list[hour][week] = 1
		else:
			hour_list[hour] = {}
	#print hour_list

	hour_ordered_list = OrderedDict(sorted(hour_list.items(), key=lambda t: t[0]))
	with open('2_output_wdays.txt','wb') as f:
		f.writelines('Hour\tMon\tTue\tWed\tThu\tFri\tSat\tSun\n')
		for i in hour_ordered_list:
			str_wr =''
			for j in OrderedDict(sorted(hour_ordered_list[i].items(), key=lambda t: t[0])):
				str_wr += '\t'+str(hour_ordered_list[i][j])
			f.writelines(str(i)+str_wr+'\n')

def main():
	with sqlite.connect('wiki.db') as con:
		cur = con.cursor()
		cur.execute("SELECT timestamp, revision_id FROM wiki ORDER BY timestamp desc")
		rows = cur.fetchall()
	count_revision_per_hour(rows)
	#count_revision_per_hour_weekday(rows)
	#count_revision_per_hour_weekend(rows)
	count_revision_per_hour_wdays(rows)
	count_revision_per_hour_wdays_wends(rows)

  	

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()