# CS205-Warmup
Custom query language for a dataset of Olympic Athletes and Sports.

To run this program you need to make sure you have pandas installed.

Examples user queries:
select athlete age = 30 - This will return all the athletes who are of age 30.
select sport type = "team" age = 17 - This will get all the sports where an anthlete of age 17 has competed in.
select athlete team = “Russia” event = “Archery” - This will return all of the Russian athletes who competed in Archery.

How to query:
Any query will start with the word select followed by athlete or sport. From here you can choose any of the athlete fields or sport fields described below.

Athlete Fields:
- fullname
- age
- sex
- team
- event

Sport Fields:
- name
- season
- type

You can use these by saying field_name = "*info*"
If you would like to select fields from both athlete and sport you should enter: select athlete field_name = "*info*" sport field_name = "*info*"
