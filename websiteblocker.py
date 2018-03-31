import sqlite3
import os
import sys
import socket

redirect="127.0.0.1"
website_list = []
host_path = "/etc/hosts"
hostname = socket.gethostname()
misc_text = ("""\n127.0.0.1	localhost
127.0.1.1	"""+ hostname +"""\n
The following lines are desirable for IPv6 capable hosts
#::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters""")

database = "websiteblocker.db"
conn=sqlite3.connect(database)
cur=conn.cursor()
#Save all of this in a DATABASE.

def connect():
    cur.execute("CREATE TABLE IF NOT EXISTS websites (id INTEGER PRIMARY KEY, wSite text)")
    conn.commit()

def getSites():
	cur.execute("SELECT wSite FROM websites")
	rows = cur.fetchall()
	return rows

def insert(wSite):
	delete(wSite)
	cur.execute("INSERT INTO websites VALUES (NULL,?)",(wSite,))
	conn.commit()

def delete(wSite):
    cur.execute("DELETE FROM websites WHERE wSite=?",(wSite,))
    conn.commit()

def show():
    print("\nBlocked Websites:\n")
    for item in getSites():
        print(str(item[0]))

def write():
	siteCol = getSites()
	for item in siteCol:
		website_list.append(item[0])
	open(host_path, 'w')
	with open(host_path, 'r+') as file:
		content = file.read()
		for website in website_list:
			file.write(redirect + "        " + website + "\n")
		file.write(misc_text)

def runCode():
    while True:
        inp = input("\nAdd [a], Delete [d], Show [s], Exit [x]: ")
        if (inp == "x" or inp == "X"):
    	    write()
    	    conn.close()
    	    break
        elif (inp == "s" or inp == "S"):
            show()
            continue
        site = input("Website: ")
        if (not checkWebsiteFormat(site)):
            print("Invalid Input.")
            break
        if (inp == "a" or inp == "A"):
            insert(site)
        elif (inp == "d" or inp == "D"):
            delete(site)

def checkWebsiteFormat(site):
    siteSplit = site.split(".")
    if len(siteSplit) >= 3 and siteSplit[0] == "www":
        if siteSplit[1] != "" and siteSplit[2] != "":
            return True
    else:
        return False

def main():
    if os.getuid() == 0:
        connect()
        runCode()
    else:
        print("Script needs to be run as a root!")

main()
