import requests
from bs4 import BeautifulSoup
import MeCab
import re

def get_wikipedia_page(search_word):
    url = f"https://ja.wikipedia.org/wiki/{search_word}"
    response = requests.get(url)
    return response.text if response.status_code == 200 else None

def extract_summary(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    summary = soup.find("div", {"id": "bodyContent"}).find("p")
    return summary

def extract_keywords(summary, html_content):
    tagger = MeCab.Tagger()
    parsed_summary = tagger.parse(summary.text)
    noun_candidates = []

    for line in parsed_summary.split('\n'):
        if "名詞" in line:
            noun_candidates.append(line.split('\t')[0])

    soup = BeautifulSoup(html_content, "html.parser")
    keywords = []

    for candidate in noun_candidates:
        if len(re.findall(r'[\u4e00-\u9fff\u30a0-\u30ff]{5,}', candidate)) > 0:
            keywords.append(candidate)

    return keywords[:7]

if __name__ == "__main__":
    search_word = input("検索したい単語を入力してください: ")
    parent_page_html = get_wikipedia_page(search_word)
    parent_summary = extract_summary(parent_page_html)

    print("親ワードの検索結果:")
    print(parent_summary.text)

    child_keywords = extract_keywords(parent_summary, parent_page_html)

    print("\n子ワードの検索結果:")
    for keyword in child_keywords:
        child_page_html = get_wikipedia_page(keyword)
        child_summary = extract_summary(child_page_html)
        print(f"{keyword}:")
        print(child_summary.text if child_summary else "概要が見つかりませんでした。")
        print()
