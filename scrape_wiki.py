"""Scrape_wiki
- Scrape a wikipedia page 
- encodes url in the file name
- parses out the "See also", "References", "External links" sections
"""


import wikipediaapi
import re


def get_pages_in_cat(category, agent, path):
    i = 0
    cat_page = agent.page(f"Category:{category}")
    for page in cat_page.categorymembers.values():
        if page.ns == wikipediaapi.Namespace.MAIN:
            print(f"downloading {page.title}")

            # remove unessary content: see also, references, external links
            match = re.search(r"See also", page.text) or \
                    re.search(r"References", page.text) or \
                    re.search(r"External links", page.text)
            if match is not None:
                start = match.start()
            else:
                start = -1

            # encode url in filename
            url = page.canonicalurl
            filename = url.replace('https://', '').replace('http://', '').replace('/', '.').strip()

            with open(f"{path}/{filename}.txt", "w") as f:
                f.write(page.text[:start])

            i += 1

    print(f"total {i} pages downloaded")


if __name__ == '__main__':
    wiki = wikipediaapi.Wikipedia("WikiMedDB (a.wei.william.0513@gmail.com)", "en")
    #get_pages_in_cat("Pediatrics", wiki, "./resources/wiki")
    #get_pages_in_cat("Human diseases and disorders", wiki, "./resources/wiki")
    get_pages_in_cat("Disorders originating in the perinatal period", wiki, "./resources/wiki")
    get_pages_in_cat("Medical_emergencies", wiki, "./resources/wiki")
