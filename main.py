import sys
import time

from utils import get_daily_papers_by_keyword, generate_table, back_up_files,\
    restore_files, remove_backups, get_daily_date


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
f_rm.write("The project automatically fetches the latest papers from arXiv based on keywords.\n\nThe subheadings in the README file represent the search keywords.\n\nOnly the most recent articles for each keyword are retained, up to a maximum of 100 papers.\n\nYou can click the 'Watch' button to receive daily email notifications.\n\n")

# write to ISSUE_TEMPLATE.md
f_is = open(".github/ISSUE_TEMPLATE.md", "w") # file for ISSUE_TEMPLATE.md
f_is.write("---\n")
f_is.write("title: Latest {0} Papers - {1}\n".format(issues_result, get_daily_date()))
f_is.write("labels: documentation\n")
f_is.write("---\n")
f_is.write("**Please check the [Github](https://github.com/zezhishao/MTS_Daily_ArXiv) page for a better reading experience and more papers.**\n\n")

for keyword in keywords:
    f_rm.write("## {0}\n".format(keyword))
    f_is.write("## {0}\n".format(keyword))
    papers = get_daily_papers_by_keyword(keyword, column_names, max_result)
    if len(papers) == 0:
        print("ArXiv API Limit Exceeded!\n")
        f_rm.close()
        f_is.close()
        restore_files() # restore README.md and ISSUE_TEMPLATE.md
        sys.exit("ArXiv API Limit Exceeded!")
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
