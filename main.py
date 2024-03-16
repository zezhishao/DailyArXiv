import time
from utils import get_daily_papers_by_keyword, generate_table, back_up_files, restore_files, remove_backups


keywords = ["Time Series"] # TODO add more keywords

max_result = 100 # maximum query results from arXiv API for each keyword
issues_result = 15 # maximum papers to be included in the issue

# all columns: Title, Authors, Abstract, Link, Tags, Comment, Date
# fixed_columns = ["Title", "Link", "Date"]

column_names = ["Title", "Link", "Abstract", "Date", "Comment"]

back_up_files() # back up README.md and ISSUE_TEMPLATE.md

# write to README.md
f_rm = open("README.md", "w") # file for README.md
f_rm.write("# Daily Papers\n")
f_rm.write("This project only retains the latest papers, with a maximum of 100 papers.\n\nYou can click the 'Watch' button to receive daily email notifications.\n\n")

# write to ISSUE_TEMPLATE.md
f_is = open(".github/ISSUE_TEMPLATE.md", "w") # file for ISSUE_TEMPLATE.md
f_is.write("---\n")
f_is.write("title: Latest {0} Papers - {{{{ date | date('MMMM D, YYYY') }}}}\n".format(issues_result))
f_is.write("labels: documentation\n")
f_is.write("---\n")
f_is.write("**Please check the [Github](https://github.com/zezhishao/MTS_Daily_ArXiv) page for a better reading experience and compatibility.**\n\n")

for keyword in keywords:
    f_rm.write("## {0}\n".format(keyword))
    f_is.write("## {0}\n".format(keyword))
    papers = get_daily_papers_by_keyword(keyword, column_names, max_result)
    if len(papers) == 0:
        print("ArXiv API Limit Exceeded!\n")
        f_rm.close()
        f_is.close()
        restore_files() # restore README.md and ISSUE_TEMPLATE.md
        exit(-1)
    rm_table = generate_table(papers)
    is_table = generate_table(papers[:issues_result])
    f_rm.write(rm_table)
    f_rm.write("\n\n")
    f_is.write(is_table)
    f_is.write("\n\n")
    time.sleep(30) # avoid being blocked by arXiv API

f_rm.close()
f_is.close()
remove_backups()
