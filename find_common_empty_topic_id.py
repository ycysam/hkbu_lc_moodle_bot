from moodle import Moodle
from activity import Activity

def main_process(section):
    global common_empty_topics
    global all_empty_topics
    a = Activity()
    tids = a.find_all_empty_topic_ids()
    common_empty_topics = list(set(common_empty_topics).intersection(tids))
    for t in tids:
        all_empty_topics.add(t)

if __name__ == '__main__':
    common_empty_topics = []
    all_empty_topics = set()
    m = Moodle("UCLC1008", "2021", "S1")
    m.start_iteration(main_process)
    if common_empty_topics != []:
        print(f"The smallest common empty topic is { min(common_empty_topics) }.")
    else:
        print(f"No smallest common empty topic found, the max empty topic is { max(list(all_empty_topics)) }")