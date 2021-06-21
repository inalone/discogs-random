from bs4 import BeautifulSoup
import random
import requests
import sys

def display_genres(genreList):
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

def format_output(response, count):
    output = ""
    data_format = ["ID: ", "Artist: ", "Title: ", "Released: ", "Genres: ", "Link: "]
    data = ["id", "artists_sort", "title", "released", "genres", "uri"]
    
    print(f"Release #{count + 1}:")

    for i in range(0, 6):
        try:
            response_data = response[data[i]]

            if i == 4:
                response_data = display_genres(response_data)
            
            output += data_format[i] + str(response_data) + "\n"
        except KeyError:
            pass
    
    return output

# if an ID isn't valid, discogs will just send JSON response with the message key
def check_valid_id(response):
    if 'message' in response:
        return False
    return True

def get_discogs_release_amount():
    discogs_page = requests.get("https://www.discogs.com/search/?ev=em_rs")
    soup = BeautifulSoup(discogs_page.text, features="html5lib")

    amount_text = soup.find(class_="pagination_total").text
    amount_text = amount_text.split("of", 1)[1].strip()
    amount = int(amount_text.replace(',', ''))

    return amount

if __name__ == "__main__":
    releases = 1
    if len(sys.argv) > 1:
        try:
            releases = int(sys.argv[1])
        except:
            pass
    
    discogs_release_amount = get_discogs_release_amount()

    count = 0
    explicit_no_singles = True
    while count < releases:
        rand = str(random.randint(0, discogs_release_amount))
        response = requests.get("https://api.discogs.com/releases/" + rand).json()

        if explicit_no_singles:
            try:
                descriptions = response["formats"][0]["descriptions"]
                if "Single" in descriptions or ("7\"" in descriptions and "EP" not in descriptions):
                    continue
            except:
                continue

        if check_valid_id(response):
            print(format_output(response, count))
        else:
            continue
        
        count += 1