
# Olympic Athlete Data: The O.A.D.
#### Intro
This program allows a user to query data using a custom query language to retreive results from a dataset of Olympic Athletes and Sports, compiled using data from the 2014 Winter Olympics in Sochi, Russia and the 2016 Summer Olympics in Rio de Janeiro, Brazil. This program was created by Jackson Hall, Jake Walburger, Lauren Paicopolis, and Sarah O'Brien for the CS 205 Software Engineering warmup project.

#### Setup
To run this program you need to make sure you have the [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html) package installed. With `pip`, you can do `pip install pandas`.

#### Using the Program
There are four types of commands:
* `select` - filter and pull records from the database (more info below)
* `load data` - load data from `tblAthlete.csv` and `tblSport.csv` (these are hard-coded so filenames must be identical and located in the same directory as `main.py`)
* `help` - displays a help message explaining command usage
* `quit` - quits the program

#### `Select` Commands
Formally, here is the general form for user `select` queries (everything is case insensitive):
`select [athlete|sport] [<intField> = <value>|<stringField> = "<value>"][, <intField> = <value>|, <stringField> = "<value>"]*`

Every user query must start with `select`, `help`, `load`. From here you can choose to filter by any combination of the fields 
relating to athletes or sports, listed below. If you would like to select fields from both athlete and sport you should enter:
select athlete <field_name> = "<value>" sport <field_name> = "<info>"

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

#### Example Queries
* select athlete age = 30 - This will return all the athletes who are of age 30.
* select sport type = "team" age = 17 - This will get all the sports where an anthlete of age 17 has competed in.
* select athlete team = “Russia” event = “Archery” - This will return all of the Russian athletes who competed in Archery.
