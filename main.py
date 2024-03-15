import time
from utils import get_daily_papers_by_keyword, generate_table


keywords = ["Time Series"] # TODO add more keywords

max_result = 100 # NOTE this project only retains the latest 100 papers

# all columns: Title, Authors, Abstract, Link, Tags, Comment, Date
# fixed_columns = ["Title", "Link", "Date"]

column_names = ["Title", "Link", "Abstract", "Date", "Comment"]

top_desc = "This project only retains the latest 100 papers."

with open("README.md", "w") as f:
    f.write("# Daily Papers\n")
    f.write("{0}\n".format(top_desc))
    for keyword in keywords:
        f.write("## {0}\n".format(keyword))
        papers = get_daily_papers_by_keyword(keyword, column_names, max_result)
        if len(papers) == 0:
            print("ArXiv API Limit Exceeded!\n")
            break
        table = generate_table(papers)
        f.write(table)
        f.write("\n\n")
        time.sleep(310) # avoid being blocked by arXiv API
