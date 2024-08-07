# -*- coding: utf-8 -*-

from lxml import etree
import sys
import os
from datetime import datetime, timedelta
import re 
from icalendar import Calendar, Event


##### Catherine's very hacky ics export for Staffs Beacon timetable. Best not to use unless you are vaguely familiar with python. 
# Apologies, this is terrible hacky code and yes, it is terrible hacky code. OK no apologies, it works. 
# How to use:
# 1. You will need to run this separately for each term. 
# 2. Change the first/last week commencing dates below for each "term". I've used the first term for 24/25 as an example.
# 3. If there are any half terms/breaks etc. put those in the week_breaks list. This will take an entire week from the date commencing right now, it's bad, I'm sorry
# 4. You'll need python (obviously) in your path, and the modules lxml and icalendar which you might need to install with pip separately (pip install icalendar, for example)
# 5. Navigate to the beacon timetable website and click the first week of your timetable. 
# 6. Download (right click, Save As) each day of the first week of the timetable as YYYY-MM-DD.htm and put it into the folder with the script. e.g. if you have timetabled items 
# Mon, Wed, Thurs there should be 3 files with the dates of the days of the first week of term as their names (with a .htm).
# 7. Run "python timetable.py" and it will parse the html file and create duplicates for each week so long as it isn't in the break list and isn't past the last week of term.
# 8. Double click the generated .ics file and it will open in Outlook. I suggest adding it as a new calendar instead of importing!
# 9. Good luck. This is a couple of hours bad coding and itch scratching. You'll need to rerun it if your timetable updates.
# DOES NOT SUPPORT: one off lectures etc. or anything that doesn't run weekly basically. It also doesn't support any sort of changes of rooms etc. during the term. 
# I mean it's basically probably not much more work to add everything repeating manually, so idk, if this doesn't work for you, don't waste time on it :)



first_week_date = '2024-09-30'
last_week_date = '2024-11-19'
week_breaks = [] #week_breaks = ['2024-11-04'] - week commencing these dates. this is a bit of a cludge, sorry
download_folder = '.' # . means current folder, you can change this if you like but the script will always make the ics file in the same directory as the script
cal = Calendar()

def process_files(download_folder):
	timetable_items = []
	date_format = "%Y-%m-%d"
	lwd=datetime.strptime(last_week_date, date_format)

	for f in os.listdir(download_folder):
			if os.path.isfile(f):
				#print(f)
				if f.endswith('.htm'):
					#print (f)
					file_path = f
					with open(file_path, 'r', encoding='utf-8') as file:
						html_content = file.read()

					# Parse the HTML content
					parser = etree.HTMLParser()
					tree = etree.fromstring(html_content, parser)

					# Define the XPath
					xpath_location = '/html/body/div/div/div/div[2]/div/div[3]/div/div/div[1]/div/div[2]/div/div/div[2]'

				
					# Extract the text from the specified XPath
					elements = tree.xpath(xpath_location)
					
					event = {}
					ele_counter = 1

					if elements:
						# Extract and join all text content from the elements and their children
						for element in (elements[0].itertext()): 
							# Normalise spaces and hyphens
							element = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015\u00AD]', '', element)  # Replace different types of hyphens with a regular hyphen
							element = re.sub(r'[\u00A0\u202F\u2007]', ' ', element)  # Replace non-breaking spaces with a regular space
							element = re.sub(r'[\u200B-\u200D\u2060\uFEFF]', '', element)  # Remove zero-width spaces
							event['date'] = datetime.strptime((os.path.splitext(f)[0]), date_format)


							if element == "MANDATORY":
								#reset things
								timetable_items.append(event)
								event = {}
								ele_counter = 1
							elif ele_counter == 1:
								event['title'] = element
								ele_counter+=1
							elif ele_counter == 2:
								#strip out the time and duration
								start_time_str, end_time_str = element.split(' - ')
								time_format = "%H:%M"
								start_time = datetime.strptime(start_time_str, time_format)
								end_time = datetime.strptime(end_time_str, time_format)
								duration = end_time - start_time
								

								event['time'] = start_time
								event['duration'] = duration
								ele_counter+=1
							elif ele_counter == 3:
								event['location'] = element
								ele_counter+=1

							else:
								print("No text found at the specified XPath location.")
					#print(timetable_items)

	break_dates = []
	for week_start in week_breaks:
		week_start_date = datetime.strptime(week_start, date_format)
		break_dates.append(week_start_date)
		for i in range(6):
			add_days=timedelta(days=i+1)
			break_dates.append(week_start_date+add_days)
	
	complete_timetable_items = timetable_items.copy()
	#print (timetable_items)
	for event in timetable_items:
		#print(event)

		existing_time = event['date']
		#print(existing_time)
		sevendays = timedelta(days=7)
		new_time = existing_time+sevendays


		
		if (new_time <= lwd):
			new_event = {}
			new_event['date'] = new_time
			new_event['title'] = event['title']
			new_event['time'] = event['time']				
			new_event['duration'] = event['duration']
			new_event['location'] = event['location'] 
			if new_time not in break_dates:
				#print("skipped this date")
				complete_timetable_items.append(new_event) # got to add a new event to the end of the list for checking the next time around
			timetable_items.append(new_event)	
	
	#print(complete_timetable_items)

	return complete_timetable_items

def make_ical(c_timetable_items):
	# Add events to the calendar
	for event in c_timetable_items:
		#print(event)
		cal_event = Event()
		start_datetime = datetime.combine(event['date'], event['time'].time())
		end_datetime = start_datetime + event["duration"]
		cal_event.add('summary', event['title'])
		cal_event.add('dtstart', start_datetime)
		cal_event.add('dtend', end_datetime)
		cal_event.add('location', event['location'])

		cal.add_component(cal_event)

	# Write to an .ics file
	with open('events.ics', 'wb') as f:
		f.write(cal.to_ical())

	print("iCalendar file created successfully.")




complete_timetable_items = process_files(download_folder)
make_ical(complete_timetable_items)