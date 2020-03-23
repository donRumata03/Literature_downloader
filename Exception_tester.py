from mylang import *
import random
import royal_parser
import thread_parser

text = json.loads("""

{
        "name": [
            "Аникеев",
            "Владимир"
        ],
        "link": "https://royallib.com/author/anikeev_vladimir.html",
        "artworks": [
            {
                "name": "Армейские байки (сборник)",
                "link": "https://royallib.com/book/anikeev_vladimir/armeyskie_bayki_sbornik.html"
            },
            {
                "name": "Научная фантастика Польши",
                "link": "https://royallib.com/book/anikeev_vladimir/nauchnaya_fantastika_polshi.html"
            }
        ]
    }

""")

processor = thread_parser.Art_parser(text, Vova())
res = processor.do_work()
print_good_info("Ready!")
print_as_json(res)




#
# string = "(Размер: 24    sdkjhsdfguilhsdfghjil Мб)"
#
# print(print_as_json(thread_parser.Art_parser(
#     {
#         "name": "Божий контрабандист",
#         "link": "https://royallib.com/book/brat_andrey/bogiy_kontrabandist.html"
#     },
#     Vova()
# ).do_work()))
