# staffs-timetable
A very hacky python script that extrapolates what a Staffordshire University timetable will be from the first week from the Beacon website and then makes an ics file so you can import it into Outlook/wherever. 

# Catherine's very hacky ics export for Staffs Beacon timetable. Best not to use unless you are vaguely familiar with python. 
Apologies, this is terrible hacky code and yes, it is terrible hacky code. OK no apologies, it works. 
How to use:
1. You will need to run this separately for each term. 
2. Change the first/last week commencing dates below for each "term". I've used the first term for 24/25 as an example.
3. If there are any half terms/breaks etc. put those in the week_breaks list. This will take an entire week from the date commencing right now, it's bad, I'm sorry
4. You'll need python (obviously) in your path, and the modules lxml and icalendar which you might need to install with pip separately (pip install icalendar, for example)
5. Navigate to the beacon timetable website and click the first week of your timetable. 
6. Download (right click, Save As) each day of the first week of the timetable as YYYY-MM-DD.htm and put it into the folder with the script. e.g. if you have timetabled items Mon, Wed, Thurs there should be 3 files with the dates of the days of the first week of term as their names (with a .htm).
7. Run "python timetable.py" and it will parse the html file and create duplicates for each week so long as it isn't in the break list and isn't past the last week of term.
8. Double click the generated .ics file and it will open in Outlook. I suggest adding it as a new calendar instead of importing!
9. Good luck. This is a couple of hours bad coding and itch scratching. You'll need to rerun it if your timetable updates.

# DOES NOT SUPPORT: one off lectures etc. or anything that doesn't run weekly basically. It also doesn't support any sort of changes of rooms etc. during the term. 
I mean it's basically probably not much more work to add everything repeating manually, so idk, if this doesn't work for you, don't waste time on it :)

Use at your own risk, I'm happy to review pull requests but please don't ask me for support - this is a thing I did for myself and which I have put up here for anyone else interested to fiddle with. 
Microsoft OAuth is used by Beacon to do authentication, hence my choice of manual bad ways to do this rather than banging my head against forces that are beyond my comprehension. 
