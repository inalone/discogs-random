import requests
import random

def displayGenres(genreList):
    first = True
    genres = ""

    for each in genreList:
        genre = ""

        if not first:
            genre += ", "
        
        genre += each
        genres += genre
        first = False
    
    return genres

def formatOutput(response):
    output = ""
    data_format = ["ID: ", "Artist: ", "Title: ", "Released: ", "Genres: ", "Link: "]
    data = ["id", "artists_sort", "title", "released", "genres", "uri"]
    
    for i in range(0, 6):
        try:
            response_data = response[data[i]]

            if i == 4:
                response_data = displayGenres(response_data)
            
            output += data_format[i] + str(response_data) + "\n"
        except KeyError:
            pass
    
    return output

# if an ID isn't valid, discogs will just send JSON response with the message key
def checkValid(response):
    if 'message' in response:
        return False
    return True

def main():
    # TODO: Make number dynamic with Discogs API
    rand = str(random.randint(0, 25000000))
    response = requests.get("https://api.discogs.com/releases/" + rand).json()

    if checkValid(response):
        print(formatOutput(response))
    else:
        print("Something went wrong - try again")

main()