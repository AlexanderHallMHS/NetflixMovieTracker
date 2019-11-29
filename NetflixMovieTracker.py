# File: NetflixMovieTracker.py
# Author: Alexander Hall, Mayra Hernandez, Tanvi Vishwanath
# Date: 12/01/2019
# E-mail: hallale22howdy@tamu.edu, mhdz@tamu.edu, tanvivishwanath@tamu.edu
# Description: The Netflix Movie Tracker, This program will analyze Netflix movie
# data from a file and plot said data in different types of charts.
# Section: 505

import csv
import matplotlib.pyplot as plt

printOrNot = True

def retrieveDataFromFile():
    """This function takes all the data from the file and stores it in 
    dictionaries and lists."""
    # added Fathom Events to The Met: Live in HD - Manon Lescaut
    with open("2016_movie_data.csv", "r") as movieDataFile:
        movieDataFile.readline()
        data = csv.reader(movieDataFile)
        numMovies = 0
        numTicketsSold = 0
        distributorsAndTickets = {}
        totalMoviesAndTicketsInMonths = {}
        dramaMonths = [0 for n in range(12)]
        horrorMonths = [0 for n in range(12)]
        actionMonths = [0 for n in range(12)]
        comedyMonths = [0 for n in range(12)]
        genres = []
        MPAAs = []
        global printOrNot
        for line in data:
            # if ticket number has commas and can't be cast as an int vs not
            try:
                line[5] = int(line[5])
            except:
                formatTickets = ""
                iterator = 0
                while iterator < len(line[5]):
                    if line[5][iterator] != ",":
                        formatTickets += line[5][iterator]
                    iterator += 1                        
                line[5] = int(formatTickets)
            if line[1].split("/")[0] not in totalMoviesAndTicketsInMonths:
                totalMoviesAndTicketsInMonths[line[1].split("/")[0]] = [0, int(line[5])]
            else:
                totalMoviesAndTicketsInMonths[line[1].split("/")[0]][0] += 1
                totalMoviesAndTicketsInMonths[line[1].split("/")[0]][1] += int(line[5])
            if line[2] not in distributorsAndTickets:
                distributorsAndTickets[line[2]] = int(line[5])
            else:
                distributorsAndTickets[line[2]] += int(line[5])

            for month in range(1, 13):
                if int(line[1][0]) == month or line[1][0:2] == str(month):
                    if line[3] == "Drama":
                        dramaMonths[month - 1] += 1
                    elif line[3] == "Horror":
                        horrorMonths[month - 1] += 1
                    elif line[3] == "Action":
                        actionMonths[month - 1] += 1
                    elif line[3] == "Comedy":
                        comedyMonths[month - 1] += 1
            if line[3] not in genres:
                genres.append(line[3])
            if line[4] not in MPAAs:
                MPAAs.append(line[4])
            numTicketsSold += int(line[5])
            numMovies += 1
        if printOrNot:
            print("========Dataset details========\n")
            print(f"Number of Movies: {numMovies}")
            print(f"Number of different genres: {len(genres)}")
            print(f"Number of different MPAA: {len(MPAAs)}")
            print(f"Number of different distributors: {len(distributorsAndTickets)}")
            print(f"Total number of tickets sold: {numTicketsSold}\n")
            print("================================\n")
        totalMoviesAndTicketsInMonths["January"] = totalMoviesAndTicketsInMonths.pop("1")
        totalMoviesAndTicketsInMonths["February"] = totalMoviesAndTicketsInMonths.pop("2")
        totalMoviesAndTicketsInMonths["March"] = totalMoviesAndTicketsInMonths.pop("3")
        totalMoviesAndTicketsInMonths["April"] = totalMoviesAndTicketsInMonths.pop("4")
        totalMoviesAndTicketsInMonths["May"] = totalMoviesAndTicketsInMonths.pop("5")
        totalMoviesAndTicketsInMonths["June"] = totalMoviesAndTicketsInMonths.pop("6")
        totalMoviesAndTicketsInMonths["July"] = totalMoviesAndTicketsInMonths.pop("7")
        totalMoviesAndTicketsInMonths["August"] = totalMoviesAndTicketsInMonths.pop("8")
        totalMoviesAndTicketsInMonths["September"] = totalMoviesAndTicketsInMonths.pop("9")
        totalMoviesAndTicketsInMonths["October"] = totalMoviesAndTicketsInMonths.pop("10")
        totalMoviesAndTicketsInMonths["November"] = totalMoviesAndTicketsInMonths.pop("11")
        totalMoviesAndTicketsInMonths["December"] = totalMoviesAndTicketsInMonths.pop("12")
        mostMovies = totalMoviesAndTicketsInMonths["January"][0]
        mostTickets = totalMoviesAndTicketsInMonths["January"][1]
        mostMoviesMonth = ""
        mostTicketsMonth = ""
        for key, value in totalMoviesAndTicketsInMonths.items():
            if value[0] > mostMovies:
                mostMovies = value[0]
                mostMoviesMonth = key
            if value[1] > mostTickets:
                mostTickets = value[1]
                mostTicketsMonth = key
        if printOrNot:
            print(f"Most number of movies released ({mostMovies}) in {mostMoviesMonth}")
            print(f"Most number of tickets sold ({mostTickets}) in {mostTicketsMonth}")
            print("\n================================\n")
            print("========Tickets sold by distributors========\n")
        for key, value in distributorsAndTickets.items():
            distributorsAndTickets[key] = (distributorsAndTickets[key] / numTicketsSold) * 100
        others = 0
        percentTickets = []
        trueDistributorsAndTickets = {}
        for key, value in distributorsAndTickets.items():
            if value < 1:
                others += value
            else:
                percentTickets.append(value)
                trueDistributorsAndTickets[key] = value
        trueDistributorsAndTickets["Others"] = others
        percentTickets.append(others)
        percentTickets.sort(reverse=True)

        percentTicketDistributors = []
        trueDistributorsAndTicketsKeys = list(trueDistributorsAndTickets.keys())
        trueDistributorsAndTicketsValues = list(trueDistributorsAndTickets.values())
        for percentage in percentTickets:
            if percentage in trueDistributorsAndTicketsValues:
                percentTicketDistributors.append(trueDistributorsAndTicketsKeys[trueDistributorsAndTicketsValues.index(percentage)])
            else:
                percentTicketDistributors.append("Others")
        for i in range(0,len(percentTickets)):
            percentTickets[i] = round(percentTickets[i], 2)
            if printOrNot:
                print(f"{percentTicketDistributors[i]}: {percentTickets[i]}%")
        if printOrNot:
            print("\n===================")
        printOrNot = False
    return totalMoviesAndTicketsInMonths, percentTicketDistributors, percentTickets, dramaMonths, horrorMonths, actionMonths, comedyMonths

def graphData():
    """This function takes all the data from the file that is saved in data 
    structures and graphs it into different plots"""

    months = list(retrieveDataFromFile()[0].keys())
    numMovies = []
    numTickets = []
    for value in retrieveDataFromFile()[0].values():
        numMovies.append(value[0])
        numTickets.append(value[1])
    plt.figure(1)
    plt.bar(months, numMovies)
    plt.title("Number of movies released in different months of 2016")
    plt.xticks(fontsize="12", rotation=90)
    plt.xlabel("Month")
    plt.ylabel("Number of movies")
    plt.show()

    plt.figure(2)
    plt.plot(months, numTickets)
    plt.title("Tickets sold in different months of 2016")
    plt.xticks(fontsize="12", rotation=90)
    plt.xlabel("Month")
    plt.ylabel("Number of tickets sold")
    plt.show()

    pieChartTitles = list(retrieveDataFromFile()[1])
    pieChartPercentages = [int(n) for n in list(retrieveDataFromFile()[2])]
    plt.figure(3)
    plt.pie(pieChartPercentages, labels=pieChartTitles, textprops={'fontsize': 8}, autopct='%.2f%%', pctdistance=0.83)
    plt.title("Percentage of tickets sold by different distributors")
    plt.show()

    dramaMovies = retrieveDataFromFile()[3]
    horrorMovies = retrieveDataFromFile()[4]
    actionMovies = retrieveDataFromFile()[5]
    comedyMovies = retrieveDataFromFile()[6]

    plt.figure(4)
    plt.plot(months, dramaMovies, color="b")
    plt.plot(months, horrorMovies, color="y")
    plt.plot(months, actionMovies, color="g")
    plt.plot(months, comedyMovies, color="r")
    plt.title("Number of movies released in different months of 2016")
    plt.xlabel("Number of movies")
    plt.ylabel("Month")
    plt.legend(["Drama", "Horror", "Action", "Comedy"])
    plt.xticks(fontSize="12", rotation=90)
    plt.show()

def main():
    """This function runs acts as a way to call every other function in the file
    all at once."""
    retrieveDataFromFile()
    graphData()
    
main()