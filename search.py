from newspaper import Article
import openai
import requests
from googlesearch import search
from dotenv import load_dotenv
import os
import prompts

load_dotenv()


def search_google(query, num_results=2):
    # Searches Google for the given query and returns up to num_results links found.
    
    responses = search(query, stop=num_results, verify_ssl=True, lang="en")
    

    # Raises:
    # Exception: If the request fails.
    if responses == 200:
        raise Exception("Request failed with code {}".format(responses.status_code))
    
    # Returns:
    # A list of result links.
    links = [response for response in responses]
    
    return links


def get_article_from_url(url):
    # Loads the article from the url
    article = Article(url)

    # Downloads the article from the given URL, parses it, 
    article.download()
    article.parse()

    # and returns the article text.
    article_text = article.text
    return article_text


openai.api_key = os.getenv("OPENAI_API_KEY")


def summerize_article(promt, model="gpt-3.5-turbo-0301",temperature=0):
    messages = [{"role": "user", "content":promt}]
    response = openai.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Main entry point for the search script.
    # Asks the user for query
    query = input("Enter query: ")

    # generate search results and returns links
    search_results = search_google(query, 3)

    # for each result, get article text and summarize it
    for result in search_results:
        print(f"Summary For: {result}")
        print("-----------------------")


        # retrieves each result article using get_article_from_url()
        transcript = get_article_from_url(result)

        prompt = prompts.prompt.format(transcript)

        # text using summarize_article(), and prints the summary.
        response = summerize_article(prompt)

        print(response)
        print('-------------------------')