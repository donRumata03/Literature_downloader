from lib.mylang import *

def collect_wiki_res() -> List[dict]:
    prev_res_path = "/res/last_res.json"
    prev_res = from_utf8_json_file(prev_res_path)

    thread_res_dir = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp"
    thread_res_paths = [i for i in full_lsdir(thread_res_dir) if "result" in i]

    thread_reses = make_json_from_files(thread_res_paths)

    print_good_info(f"From thread reses: {len(thread_reses)} \nFrom previous result: {len(prev_res)}")

    all_res = sorted(prev_res + thread_reses, key = lambda x: x["name"])

    return all_res

def cong_wiki_res():
    to_utf8_json_file(collect_wiki_res(), "D:\\Projects\\Literature_downloading\\res\\wiki_data.json")

if __name__ == '__main__':

    print(len(from_utf8_json_file("/res/last_processed.json")))

    data = collect_wiki_res()
    print(len(data))

    cong_wiki_res()
