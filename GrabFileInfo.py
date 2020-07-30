import MySQLdb
import paramiko as paramiko
import pandas as pd


def connect_to_server():
    '''It is used to connect to Database'''
    # create SSH obj
    ssh = paramiko.SSHClient()
    # allow to connect the server which is not in know_hosts
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connect to server
    ssh.connect(hostname='server.acemap.cn', password='readonly', username='readonly', port=10001)
    # execute some commands
    command = ''
    stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    res, err = stdout.read(), stderr.read()
    print(res)
    stdout.close()
    stdin.close()
    ssh.close()

def extract_Index():
    '''
    It is used to extract relative information from database am_paper
    including paperID and pdfPath
    '''
    # database connection
    db = MySQLdb.connect(host="server.acemap.cn", user="readonly", passwd="readonly", port=13306)
    # set cursor for query
    cursor = db.cursor()
    # venueID is used to store the data retrieved from am_paper.am_paper_category
    venueID = []
    # paperID is used to store the data retrieved from am_paper.am_paper
    paperID=[]
    #paperInfo: paperID:pdfPath
    paperInfo={}

    # sql operations
    sql1="SELECT t.venue_id FROM am_paper.am_venue_category t WHERE field = 'Geoscience';"
    sql2="SELECT t.paper_id FROM am_paper.am_paper t WHERE journal_id = "
    sql3="SELECT t.pdfpath FROM am_paper.am_paper_pdfpath t WHERE paper_id = "

    cursor.execute(sql1)
    for data in cursor:
        venueID.append(data[0])

    print(len(venueID))

    for vID in venueID:
        tmpsql = sql2+str(vID)+";"
        cursor.execute(tmpsql)
        for data in cursor:
            paperID.append(data[0])
    print(len(paperID))
    # print(paperID)

    for pID in paperID:

        tmpsql = sql3+str(pID)+";"
        cursor.execute(tmpsql)
        for data in cursor:
            paperInfo[pID]=data[0]

    print(len(paperInfo))

    pd.DataFrame.from_dict(paperInfo, orient='index').to_csv('paperInfo.csv')
    db.close()

    # with open('data/paperInfo.txt', 'w') as f:
    #     for p in paperInfo:
    #         f.write(p)
    #         f.write('\n')


extract_Index()


