# Literature_downloader
This is a part of project "Literature_analyzer"
It loads common information about good authors from site "https://royallib.com"
using wikipedia (such as birthday and death...day date, age, genre, e.t.c.),
understanding if it is a popular author, and actually, if it is an author, 
but not a politician, for example and the main part (but not the hardest at all..)
of its work is downloading their artworks.

#Here is an example of information about one very famous author got by this parser...
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