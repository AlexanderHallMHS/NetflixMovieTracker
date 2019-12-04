import matplotlib.pyplot as plt
import csv

# Returns the index of i in list l, but only if i is in l
def getIndex(l, i):
    if i in l:
        return l.index(i)
    return 0

# Returns a list of all unique values in list l
def getUnique(l):
    out = []
    for i in l:
        if i not in out:
            out.append(i)
    return out

# Returns the month of the cooresponding date string
def getMonth(date):
    return int(date.split('/')[0])

# Returns a list of only a specific attribute, i.e. returning list of only ticket sales
def getByAttribute(data, attr):
    idx = getIndex(attributes, attr)
    return [mov[idx] for mov in data]

# Returns list of values in data that match filter attribute and mask
def filterByAttribute(data, attr, mask):
    idx = getIndex(attributes, attr)
    return [mov for mov in data if mov[idx].casefold() == mask.casefold()]

# Returns list of values in data that matchs month input
def filterByMonth(data, month):
    return [mov for mov in data if month == getMonth(mov[1])]

# Returns total amount of tickets sold in data
def countTickets(data):
    tickets = 0
    for num in getByAttribute(data, 'tickets'):
        tickets += int(num.replace(',',''))
    return tickets
    
attributes = [
    'movie',
    'date',
    'distributor',
    'genre',
    'rating',
    'tickets'
    ]

months_text = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
    ]

months = range(1,13)

# Opens file and saves data
with open('2016_movie_data.csv') as file:
    data = list(csv.reader(file))[1:]

# Calculates number of unique values
NumOfMovies = len(getUnique(getByAttribute(data, 'movie')))
NumOfGenres = len(getUnique(getByAttribute(data, 'genre')))
NumOfRatings = len(getUnique(getByAttribute(data, 'rating')))
NumOfDistros = len(getUnique(getByAttribute(data, 'distributor')))

# Calculates total number of ticket sales
NumOfTickets = countTickets(data)

# Prints info
print('Total number of movies:', NumOfMovies)
print('Number of different genres:', NumOfGenres)
print('Number of different ratings:', NumOfRatings)
print('Number of different distributors:', NumOfDistros)
print('Total number of tickets sold:', NumOfTickets)

# Calculates movies released per month and tickets sold per month
MoviesPerMonth = [len(filterByMonth(data, i)) for i in months]
TicketsPerMonth = [countTickets(filterByMonth(data, i)) for i in months]

# Calculate months with most movies and most tickets
MonthWithMostMovies = MoviesPerMonth.index(max(MoviesPerMonth))
MonthWithMostTickets = TicketsPerMonth.index(max(TicketsPerMonth))

# Prints info
print('Most number of movies released (' + str(max(MoviesPerMonth)) + ') in ' + months_text[MonthWithMostMovies] + '.')
print('Most number of tickets sold (' + str(max(TicketsPerMonth)) + ') in ' + months_text[MonthWithMostTickets] + '.')

# Calculates the percent of total sales by distributor
SalesPcts = {'Other' : 0}
for distro in getUnique(getByAttribute(data, 'distributor')):
    tickets = countTickets(filterByAttribute(data, 'distributor', distro))
    pct = tickets / NumOfTickets * 100
    if pct >= 1:
        SalesPcts[distro] = pct
    else:
        SalesPcts['Other'] += pct

# Prints info
print(SalesPcts)

# Calculates number of movies released per month by genre
DramaPerMonth = [len(filterByMonth(filterByAttribute(data, 'genre', 'drama'), i)) for i in months]
ComedyPerMonth = [len(filterByMonth(filterByAttribute(data, 'genre', 'comedy'), i)) for i in months]
ActionPerMonth = [len(filterByMonth(filterByAttribute(data, 'genre', 'action'), i)) for i in months]
HorrorPerMonth = [len(filterByMonth(filterByAttribute(data, 'genre', 'horror'), i)) for i in months]

# Plots bar chart of movies released per month
plt.bar(months_text, MoviesPerMonth)
plt.title("Movies Released Per Month In 2016")
plt.xlabel("Month")
plt.ylabel("Movies released")
plt.show()

# Plots line chart of tickets sold per month
plt.plot(months_text, TicketsPerMonth)
plt.title("Tickets Sold Per Month In 2016")
plt.xlabel("Month")
plt.ylabel("Tickets sold")
plt.show()

# Generates pie chart labels with percentages on next line
pie_labels = [k + '\n' + str(round(v,2)) + '%' for k, v in SalesPcts.items()]

# Generates pie chart of percent of tickets sold per distributor
plt.pie(SalesPcts.values(), labels = pie_labels)
plt.title("Percent Of Total Tickets Sold Per Distributor")
plt.show()

# Plots line chart of movies released per month by genre
plt.plot(months_text, DramaPerMonth)
plt.plot(months_text, ComedyPerMonth)
plt.plot(months_text, ActionPerMonth)
plt.plot(months_text, HorrorPerMonth)
plt.title("Movies Released In 2016 By Genre")
plt.xlabel("Month")
plt.ylabel("Movies released")
plt.legend(['Drama', 'Comedy', 'Action', 'Horror'])
plt.show()
