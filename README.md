# Literature downloader
This is a part of project "Literature_analyzer"
It loads common information about good authors from site "https://royallib.com"
using wikipedia (such as birthday and death...day date, age, genre, e.t.c.),
understanding if it is a popular author, and actually, if it is an author, 
but not a politician, for example and the main part (but not the hardest at all..)
of its work is downloading their artworks.


## Steps
The site is highly nested. 
So, there are several steps in it, the next one is always significantly longer, than the previous one.
1) Get the list of pages with links to authors. 
This operation is pretty fast, the result is situated in "res/author_pages.json"
2) Scrape the links to author pages from the pages of links from the previous step. 
The result of this operation is in file 
3) From each of 86000 authors\` pages: get artwork names and links to their pages. 
The result of this operation is in file 
4) Scrape all of the pages of artworks in order to get their sizes, names and links for downloading.
5) The final step: download all the artworks to corresponding directories

## Results:
As the result, there are nearly 32 GB of different artworks. 
(There is no guarantee, that they don\`t repeat each other, Moreover, there are really much duplicates)

There are still some things to do:
1) During downloading, there were several errors, for example, with internet connection, not handled properly...
So, nearly 20 % of all data were lost during the long way mentioned above. 
I`m going to modify and rerun all that steps with modernized error handling.
2) We have to much artworks written by authors such as "Абазидзе Гуссейн" and "Абдулаева Сахиба".
They will be used for learning Word2Vec model, because they are still valid russian texts, but I\`m going to use only famous authors for training classification model.
I chose having an article in Wikipedia about this author to be the criteria of being famous.
 

#### Here is an example of information about one very famous author got by this parser from Wikipedia - free encyclopedia...
`{
    "life": {
        "alive": false,
        "birth_day": 1799,
        "death_day": 1837,
        "age": 38,
        "precision": true
    },
    "raw_title": "Пушкин, Александр Сергеевич",
    "title": "Пушкин Александр Сергеевич",
    "additional_properties": {
        "Имя при рождении": "Александр Сергеевич Пушкин",
        "Псевдонимы": "Александр НКШП, Иван Петрович Белкин,Феофилакт Косичкин (журнальный), P., Ст. Арз. (Старый Арзамасец), А. Б.[1]",
        "Дата рождения": "26 мая (6 июня) 1799(1799-06-06)",
        "Место рождения": "Москва, Российская империя",
        "Дата смерти": "29 января (10 февраля) 1837(1837-02-10) (37 лет)",
        "Место смерти": "Санкт-Петербург, Российская империя",
        "Род деятельности": "поэт, прозаик, драматург, литературный критик, переводчик, публицист, историк",
        "Годы творчества": "1814—1837",
        "Направление": "романтизм, реализм",
        "Жанр": "поэма, роман (исторический роман, роман в стихах, разбойничий роман), пьеса, повесть, сказка",
        "Язык произведений": "русский, французский[~ 1]",
        "Дебют": "К другу стихотворцу (1814)"
    },
    "load": true
}`