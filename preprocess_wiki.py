"""Scrape_wiki
- Scrape a wikipedia page into .txt or .md
- encodes url in the file name
- parses out the "See also", "References", "External links" sections
"""


import wikipediaapi
import re
import html2text
from _global import path_to_resources
from bs4 import BeautifulSoup, SoupStrainer


def remove_sections(page):
    """dont include references, see also, external links"""
    sections_to_remove = ["See also", "References", "External links"]
    for i in range(len(page.sections)-1, -1, -1):
        if page.sections[i].title in sections_to_remove:
            del page.sections[i]



def parser(page):
    """parse html file into md"""
    # remove unessary content: see also, references, external links
    remove_sections(page)

    # conver to .md
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = False
    text_maker.escape_snob = True # escape special characters
    text_maker.ignore_emphasis = True
    text_maker.ignore_images = True
    text_maker.body_width = 0 # dont wrap lines

    soup = BeautifulSoup(page.text, "html.parser")
    
    return text_maker.handle(str(soup))



def get_pages_in_cat_md(category, path):
    """get all pages in first level of a category, in .md format"""
    agent = wikipediaapi.Wikipedia(
                user_agent = "WikiMedDB (test@gmail.com)", 
                language = "en",
                extract_format = wikipediaapi.ExtractFormat.HTML
            )

    i = 0
    cat_page = agent.page(f"Category:{category}")
    for page in cat_page.categorymembers.values():
        if page.ns == wikipediaapi.Namespace.MAIN:
            print(f"downloading {page.title}")

            # parse into .md
            content = parser(page)

            # encode url in filename
            url = page.canonicalurl
            filename = url.replace('https://', '').replace('http://', '').replace('/', '.').strip()

            with open(f"{path}/{filename}.md", "w") as f:
                f.write(f"# {page.title}\n\n") # add title
                f.write(f"## Introduction\n\n") # add heading for introduction
                f.write(content)
                f.write(f"\n\n ## Source \n\n {page.canonicalurl}") 
        i += 1

    print(f"total {i} pages downloaded")



def get_pages_in_cat_txt(category, path):
    """get all pages in first level of a category and parsed them, in .txt format"""
    agent = wikipediaapi.Wikipedia("WikiMedDB (test@gmail.com)", "en")

    i = 0
    cat_page = agent.page(f"Category:{category}")
    for page in cat_page.categorymembers.values():
        if page.ns == wikipediaapi.Namespace.MAIN:
            print(f"downloading {page.title}")

            # remove unessary content: see also, references, external links
            remove_sections(page)

            # encode url in filename
            url = page.canonicalurl
            filename = url.replace('https://', '').replace('http://', '').replace('/', '.').strip()

            with open(f"{path}/{filename}.txt", "w") as f:
                f.write(page.text)

            i += 1

    print(f"total {i} pages downloaded")


if __name__ == '__main__':
    get_pages_in_cat_md("Pediatrics", f"{path_to_resources}/wiki")
    get_pages_in_cat_md("Human diseases and disorders", f"{path_to_resources}/wiki")
    get_pages_in_cat_md("Disorders originating in the perinatal period", f"{path_to_resources}/wiki")
    get_pages_in_cat_md("Medical_emergencies", f"{path_to_resources}/wiki")


    #get_pages_in_cat_txt("Pediatrics", f"{path_to_resources}/wiki")
    #get_pages_in_cat_txt("Human diseases and disorders", f"{path_to_resources}/wiki")
    #get_pages_in_cat_txt("Disorders originating in the perinatal period", f"{path_to_resources}/wiki")
    #get_pages_in_cat_txt("Medical_emergencies", f"{path_to_resources}/wiki")
