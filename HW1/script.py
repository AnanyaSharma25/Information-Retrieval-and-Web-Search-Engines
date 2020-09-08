from bs4 import BeautifulSoup
import time
import requests
import json
from random import randint
from html.parser import HTMLParser
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
class SearchEngine:
    @staticmethod
    def SearchEngine(query, sleep=True):
        if sleep: # Prevents loading too many pages too soon
            time.sleep(randint(10, 100))
        temp_url = '+'.join(query.split()) #for adding + between words for the query
        url = 'https://www.ask.com/web?q=' + temp_url
        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        if len(new_results)<10:
            temp_url = '+'.join(query.split())
            url = 'https://www.ask.com/web?q=testn&page=2' + temp_url
            soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
            new_result = SearchEngine.scrape_search_result(soup)
            new_results.extend(new_result)
        return new_results
    
    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("div", attrs = {"class" : "PartialSearchResults-item-title"})
        results = []
#implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            if len(results)==10:
               break
            link = result.find('a').get('href')
            if link not in results:
                results.append(link)
        return results

queries = """How is the spinning mule fuelled ?
What are two properties or characteristics of cotton fibers ?
Information needed to locate a nonfiction book ?
What is a non-chordates ?
Which team won the 2006 Stanley Cup ?
What bands are there in folk music ?
What invented by persian ?
Where was the place of origin for Taoism ?
How many seats does usc stadium hold ?
What is one of selena gomez top hit ?
Sidney crosby live in pittburgh ?
What is a normal 8year olds blood presure ?
The capital city of the pennsylvannia colony was ?
How many cups is 1 pounds of almond ?
What parts make up the chloroplast ?
What do crocodiles do to survive ?
What is the name of the dog in Garfield ' ?
Are paris hilton and icole richie friends ?
What is yur ideal job ?
What are some cheats for pets on barbiegirlscom ?
What are five obstacles to prayer ?
How many chriss are in the world ?
What year did john cabot return to England from canada ?
What is the brown and white myepet 's code ?
How much moneydoes a coach of soccer earn ?
What is prospecting and what does prospector do ?
How do you calculate load pressure ?
2001 walking liberty silver dollar ?
What is the number one adaptation for a sea anemone ?
How much is the average yearly wage for an EMT intermediate in Georgia ?
What kind of galleys is the milky way ?
The name of ernest hemingway parents ?
What is the hackcode to stick rpg complete ?
What is the scientific name of the tail bone ?
What kind of places do '' tourists visit when they travel to Poland ?
How did Carolus Linaaeus classify organisms ?
Infection of the skin on the lower leg unknown origin found icd-9cm ?
What is the standard size for a billiards table in cm ?
Do glaciers vreate mountains ?
Who discovered x-rays and radiation therapy ?
Some sentences of possessive adjectives in french ?
Milage Frankfurt am Mainz to Vienna ?
What do christians believe about healthy living ?
How did telegraph change ?
What do playboy girls do ?
What is photoynthesis ?
In which do you want to improve ?
How do you replace a motor starter on a 1985 thunderbird ?
Where does sperm can be found ?
How do you access a routers settings ?
The fundamental unit for measuring distance ?
How many lines are there in a limerick ?
How many black 6 in a deck ?
How many bean seeds are in a pound ?
What religon 's does russia have ?
How many species of panda 's ?
What is a model 1878 colt shotgun worth ?
What temperature should a snake ?
When was the first Radar used in weather observation ?
What are the important religious celebrations of the Islam ?
The ar code for the pokemon modifier ?
Massachusetts age to be left alone ?
What is spring like in the alps ?
What is the popolarion of your London ?
What is the order of british nobility ?
What do you call a testable prediction about a possible solution to a problem ?
You hear chreeing noises on your Nissian Altima ?
What is neo-confuciansim ?
How can you solve this issue in transporting ?
Why does co curicullar activities bother studies ?
What temperture do you cook a chicken at ?
What does the proper left turn signal look like ?
What are the main two motions of earth ?
At what level does leafeon learn it final move ?
What is 1921 wheat penny worth ?
What causes a person to be fat or thin ?
Replacing wiper blades on a 98 chevy s 10 ?
How many stitchs does a baseball have ?
What is postive externality ?
How many calories in 1 teaspoon of white sugar ?
Is cloth heavier than paper ?
Peter pan dog name ?
What is the process the army uses for risk management ?
What is the runaway growth of the bodys own cells ?
How would you test sugar ?
How do you heal pink eye ?
What is the meaning of the word mariam ?
How much does it cost for 1 gram of iron ?
What is the theme in Cirque du Freak ?
Who are daniel radcliffe is parents ?
How do capitalize the letter f in cursive ?
What is the value of a 1935 series f one dollar silver certificate ?
What si the offical language of somalia ?
Measurements of the field ?
What is the name of the leader of columbia ?
When was potassium discovered in ?
What size is 34 inch waist ?
The island future Singapore is ?
What did schindler see ?
How do you get rid of permanet marker ?
"""

output = dict()
for query in queries.split("\n"):
    result = SearchEngine.SearchEngine(query)
    output.update({query: result[:10]})
with open("final.json", 'w') as fp:
    json.dump(output, fp,indent=2)





    
