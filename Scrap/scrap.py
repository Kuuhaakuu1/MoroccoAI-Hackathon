import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url_list = ["https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/97f3970e-ce36-4f3c-a45c-6ba42ab1f46e",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/2db5b721-b4c4-4e5c-b724-909eab57ca40",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/b695f263-6807-4ff2-b0c0-2c74b625aef1",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/7c7617ce-2024-4d58-8b47-a75a6fce6ef1",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/5ad0ba3b-34c1-48c7-8e2f-9d68bde3b51f",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/0f6816f5-0b9e-47d7-be1b-7df6f7427953",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/26542a50-068b-4d07-bf56-88b4785f83fd",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/6986fd3a-051d-44a5-ade4-7c3af1f94f59",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/e7a1dc28-e27f-4d68-b63d-7024e28c4390",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/efc643c6-4dff-4382-9e08-1ad6b73c8a42",
            "https://www.idarati.ma/informationnel/ar/thematique/f098d7d4-2268-4f82-b23f-d742deb398c2/6d8919c7-30e8-49ed-8556-9b0847587c22"]
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode, without a visible browser window
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
driver.get(url_list[5])#10
WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, "//h1[@class='sc-eWVKcp fMRhjG']"))
)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
driver.quit()
print(soup.prettify())

title = soup.find('h1', class_='sc-eWVKcp fMRhjG')
print(title)
print(title.text)

valid_title = re.sub(r'[<>:"/\\|?*]', '', title.text)

file_path = "D:\\MoroccanAI\\Hackathon1\\المقاولة والأعمال\\الصفقات العمومية\\" + valid_title + ".txt"
file_path = os.path.normpath(file_path)
cleaned_file_path = file_path.replace('\t', '')

text_output = open(cleaned_file_path, "a", encoding="utf-8")
# text_output = open("D:\MoroccanAI\Hackathon1\المقاولة والأعمال\الصفقات العمومية\\" + title.text + ".txt", "a",encoding="utf-8")
meta_content = soup.find('meta', {'name': 'keywords'})

# Get the content and keywords attributes
content = meta_content.get('content', '')
keywords = content.split(', ')

print("Content:", content)
print("Keywords:", keywords)

text_output.write(title.text + "\n")
text_output.write("Content: " + content + "\n")
text_output.write("Keywords: " + str(keywords) + "\n")

administrationType = soup.find('h3', class_='sc-iGctRS egEZgc')
print(administrationType.text)

text_output.write("نوع الإدارة: " + administrationType.text + "\n")

resume = soup.find('p', class_='sc-dwcuIR hBmVMu')
print(resume.text)

text_output.write("ملخص: " + resume.text + "\n")
necessaryDocuments = soup.findAll('span', class_='sc-iWFSnp kIZzT')

text_output.write("الوثائق اللازمة: ")
for i in range(len(necessaryDocuments)):
    text_output.write(necessaryDocuments[i].text + ", ")
text_output.write("\n")
target_divs = soup.findAll('div', class_='sc-jtHMlw kQYoxi')

# Iterate through each target div
for target_div in target_divs:
    
    smallTitle = target_div.find('div', class_='sc-eltcbb eQzHCE')
    # Find the div with the class "sc-iIEYCM dQOubi" within the current target_div
    inner_divv = target_div.find('div', class_='sc-kmASHI kIRTbX')

    # Find all divs with the class "sc-fmlJLJ eyMhHH" within the inner_div
    inner_divs = inner_divv.findAll('div', class_='sc-fmlJLJ eyMhHH')
    print("Title : " + smallTitle.text)
    text_output.write(smallTitle.text + " : ")
    if(len(inner_divs) > 0):
        for i in range(len(inner_divs)):
            print("Content : " + inner_divs[i].text )
            text_output.write(inner_divs[i].text + ", ")
        text_output.write("\n")
    else:
        print("Content : " + inner_divv.text )
        text_output.write(inner_divv.text + ", \n")
