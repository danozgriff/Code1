import scraperwiki
import mechanize
import re
import csv
import time
from datetime import datetime, date, timedelta
from time import gmtime, strftime
from math import sqrt
import datetime, base64
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import random
import urllib2
from urllib2 import HTTPError


##################################################      
#Load Prices from shareprices.com
##################################################
#

def ScrapeLivePrices():

    #Sleep the process while day is still open
    #time.sleep(sleeptime)
    
    #print "Start rerunflag: %d" % (rerunflag)
    
    #scraperwiki.sqlite.execute("drop table if exists company")
    #scraperwiki.sqlite.execute("create table company (`TIDM` string, `Company` string, `Yesterday Price` real, `FTSE` string, `Date` date NOT NULL)")

    todaydate=datetime.date.today()
    todaydate=todaydate.strftime("%Y-%m-%d") 
    
    datecheck = scraperwiki.sqlite.execute("select max(`Date`) from company")
    
    for x in datecheck["data"]:
       if x[0] == None:
         tdate = datetime.date.today() - datetime.timedelta(days=1)
         tdate = tdate.strftime("%Y-%m-%d")
       else:
         tdate=datetime.datetime.strptime(x[0], "%Y-%m-%d")
         tdate=tdate.strftime("%Y-%m-%d") 

    #if todaydate > tdate:
             
    dtnow = datetime.datetime.utcnow()
    #print now
    ftseopen = dtnow.replace(hour=0, minute=1, second=0, microsecond=0)
    ftseclosed = dtnow.replace(hour=13, minute=15, second=0, microsecond=0)
    wkday = datetime.datetime.today().weekday()
    #timetilclose = (ftseclosed - dtnow).total_seconds()
    #if timetilclose < 0:
    #    timetilclose = 0

    #if rerunflag == 1:
      #print "timetilclose: %d" % (timetilclose)
    #  time.sleep(timetilclose)  
      # Trading should be closed
    #  print "In First"
    #  tradingopen = "N"
    #  runagainflag = 0
    if dtnow >= ftseopen and dtnow <= ftseclosed and wkday < 5:
       tradingopen = "Y"
       #runagainflag = 1
       #print "In Second"
       #print "ftse open"
    else:
       #print "ftse closed"
       tradingopen = "N"
       #runagainflag = 0
       #print "In Third"
        
    #print "mid rerunflag: %d" % (rerunflag)

    #ftses = ['FTSE 100', 'FTSE 250',  'FTSE Small Cap']
    ftses = ['FTSE 100']

    for ftse in ftses:        

        if ftse == 'FTSE 100':
            url = 'http://shareprices.com/ftse100'
        ##elif ftse == 'FTSE 250':
        ##    url = 'http://shareprices.com/ftse250'
        ##elif ftse == 'FTSE Small Cap':
        ##    url = 'http://shareprices.com/ftsesmallcap'

        br = mechanize.Browser()
        br.set_handle_robots(False)

          # sometimes the server is sensitive to this information
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        #scraperwiki.sqlite.commit()

        response = br.open(url)

        #for pagenum in range(1):
        html = response.read()
        test1 = re.search(r'Day\'s Volume(.*?)<br \/><\/div>', html).group()
        #tuples = re.findall(r'((\">|\'>)(.*?)<\/))', str(test1.replace(" ", "")).replace("><", ""))
        tuples = re.findall(r'(\">|\'>|img\/)(.*?)(<\/|\.gif)', str(test1.replace(" ", "")).replace("><", ""))
        count = 0
        tidm = ""
        company = ""
        price = 0
        change = 0
        poscnt = 0
        overallcnt = 0

        for tuple in tuples:
            if poscnt == 1:
                company = tuple[1].replace("amp;", "")
            if poscnt == 2:
                price = float(tuple[1].replace(",", "").replace("p", ""))
            if poscnt == 3:
                change = float(tuple[1][:tuple[1].find("&")].replace(",", ""))
                if tuple[1][-2:] == 'up':
                    change = change * -1
            if poscnt == 4:
                if tradingopen == "Y":
                    "Trading Started"
                    price = price+change
                    #if tidm == "3IN":
                      #print change
                      #print price
                      #print price+change

                #+timedelta(days=-1)
                #"Volume":tuple[1].replace(",", "")
                scraperwiki.sqlite.execute("insert into Company values (?, ?, ?, ?, ?)",  [tidm+'.L', company, round(price,2), ftse, datetime.date.today()]) 
                #scraperwiki.sqlite.save(["TIDM", "Date"], data={"TIDM":tidm+'.L', "Company":company, "Yesterday Price":round(price,2), "FTSE":ftse, "Date":datetime.date.today()-timedelta(days=-1)}, table_name='company')
                scraperwiki.sqlite.commit()
            if len(tuple[1]) <= 4 and tuple[1][-1:].isalpha() and tuple[1][-1:].isupper() and tuple[1]!=tidm and poscnt!=1:
                count = count+1
                tidm = tuple[1]
                poscnt = 1
            else:
                poscnt = poscnt + 1    

        #if overallcnt > 9:
         #    return;
        #print "%s ftse records were loaded" % (count)
    #print "end rerunflag: %d" % (rerunflag)
    
    return;

####################################################
#Load Main Page from British Bulls ===NOT USED===
####################################################

def ScrapeBritishMain():

    url = 'https://www.britishbulls.com/Default.aspx?lang=en'
    
    
    #scraperwiki.sqlite.execute("drop table if exists Signal_History")  
    #scraperwiki.sqlite.execute("create table Company_Recommendations (`Date` date NOT NULL, `TIDM` varchar2(8) NOT NULL, `Signal` varchar2(15) NOT NULL, `Avg Price` real NOT NULL, `EOD Signal` varchar2(15) NOT NULL, `EOD Pattern` varchar2(30) NOT NULL, `EOD Last Price` real NOT NULL, `EOD %Change` real NOT NULL, `Refresh Date` date, UNIQUE (`Date`, `TIDM`))")
    
    
    #lselist = scraperwiki.sqlite.execute("select `TIDM` from company")
    
    #for x in lselist["data"]:
        
        #tidm = str(x)[3:-2]
        
        #siglist = scraperwiki.sqlite.execute("select count(*) from Signal_History where tidm = '%s' and (Signal IN ('SELL',  'SHORT',  'STAY IN CASH',  'STAY SHORT') OR (Signal IN ('BUY, 'STAY LONG') AND ))" % (tidm, d1date))

    br = mechanize.Browser()

    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    #response = br.open(url + tidm)
    response = br.open(url)

    for pagenum in range(1):
        html = response.read()

        publishdate = re.search(r'MARKET STATUS REPORT, (..........)', html).group(0)[22:]

        test1 = re.search(r'MainContent_SignalListGrid1_DXDataRow0((.|\n)+)MainContent_SignalListGrid1_IADD', html)

        if test1:
            test1 = test1.group(0)

            test3 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))

            while len(test3) >= 5:
    
                recdate = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
                rectidm = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                recsignal = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                recavgprice = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                eodsignal = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(",", "")).group(0)
                eodpattern = re.search(r'title="((.|\n)+)" src=', str(test3.pop(0))).group(0)[7:-6]
                eodprice = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                eodchange = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                
                #scraperwiki.sqlite.execute("insert or ignore into Company_Recommendations values (?, ?, ?, ?, ?, ?, ?, ?, ?)",  [recdate, rectidm, recsignal, recavgprice, eodsignal, eodpattern, eodprice, eodchange, publishdate]) 
                #scraperwiki.sqlite.commit()

                #scraperwiki.sqlite.execute("drop table if exists trades")

    

                #scraperwiki.sqlite.execute("create table trades (`TIDM` string, `OpenDate` date, `OpenSignal` string, `OpenPrice` real, `Direction` string, `LastPrice` real, `LastDate` date, `LastChange` real, `LastSignal` string, `Position` string)")
                scraperwiki.sqlite.execute("insert or ignore into Trades values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  [rectidm, publishdate, eodsignal, eodprice, recsignal, eodprice, publishdate, eodchange, eodsignal, 'Open']) 
                scraperwiki.sqlite.commit()
                
    return;

def gvars():

    global cGFzc3dvcmQ, cGFdc2evcmQ, cGFyc3vdcmF, cPFyc4dvcvF

    cGFzc3dvcmQ = base64.b64decode("ZnRzZXBhc3M=")
    cGFdc2evcmQ = base64.b64decode("c210cC5nbWFpbC5jb20=")
    cGFyc3vdcmF = base64.b64decode("ZGFub3pncmlmZkBnbWFpbC5jb20=")
    cPFyc4dvcvF = base64.b64decode("ZGFuZS5ncmlmZkBnbWFpbC5jb20=")

    return;

####################################################
#Update Open Trades
####################################################

def UpdateOpenTrades():

    #scraperwiki.sqlite.execute("delete from trades")  
    #scraperwiki.sqlite.execute("drop table if exists trades")
    #scraperwiki.sqlite.execute("create table trades (`TIDM` string, `OpenDate` date, `OpenSignal` string, `EntryDate` date, `EntryPrice` real, `Size` real, `LastPrice` real, `LastDate` date, `LastChange` real, `LastSignal` string, `Position` string, `CloseDate` Date, `CloseSignal` string, `ClosePrice` real, `Earnings` real) UNIQUE (`TIDM`, `OpenDate`) ON CONFLICT IGNORE")
    
    lastchange = None

    openlist = scraperwiki.sqlite.execute("select `TIDM`, `EntryDate`, `EntryPrice`, `AlertSignal` from Trades where CloseSignal is null")
    
    for x in openlist["data"]:
        
        tidm = x[0]
        entrydate = datetime.datetime.strptime(x[1], "%Y-%m-%d").date()
        entryprice = x[2] 
        entrysignal = x[3]

        #print "open tidm: %s open price %f open signal: %s" % (tidm, entryprice, entrysignal)
        #print "tidm length: %d" % len(tidm)
        
        currprices = scraperwiki.sqlite.execute("select `Yesterday Price`, `Date` from Company where tidm = '%s'" % (tidm))
        
        for z in currprices["data"]:
            currprice = z[0]
            currdate = datetime.datetime.strptime(z[1], "%Y-%m-%d").date()
            
        #print "live tidm: %s live date: %s live price: %s" % (tidm, currdate, currprice)
            
        if (entrysignal=='BUY' or entrysignal=='STAY LONG'): #and (currsignal=='SELL' or entrysignal=='SHORT' or currsignal=='STAY SHORT' or currsignal=='STAY SHORT' or currsignal=='STAY IN CASH'):
          lastchange = round((currprice - entryprice) / entryprice,3)
        #elif (entrysignal=='SELL' or entrysignal=='SHORT' or entrysignal=='STAY SHORT' or entrysignal=='STAY SHORT' or entrysignal=='STAY IN CASH') and (currsignal=='BUY' or currsignal=='STAY LONG'):
        else:  
          lastchange = round((entryprice - currprice) / entryprice,3)
        
        #print "lastchange: %f" % (lastchange)

        siglist = scraperwiki.sqlite.execute("select `TIDM`, `Date`, `Signal` from Signal_History where tidm = '%s' and Date >= '%s' order by Date" % (tidm, entrydate))
        
        for y in siglist["data"]:
            currtidm = y[0]
            currsignaldate = datetime.datetime.strptime(y[1], "%Y-%m-%d").date()
            currsignal = y[2]

            #if currdate > opendate: 

            #print "open tidm: %s current date: %s current signal: %s" % (currtidm, currsignaldate, currsignal)

            if currsignaldate <= entrydate:
              #print "In FIRST"
              scraperwiki.sqlite.execute("update Trades set LastPrice = '%f', LastDate = '%s', LastChange = '%f' where tidm = '%s'" % (currprice, currdate, lastchange, tidm))
            else:
              #print "in Second"
              #print "currprice: %f, currdate: %s, lastchange: %f, currsignal: %s, currsignaldate: %s, tidm: %s"  % (currprice, currdate, lastchange, currsignal, currsignaldate, tidm)
              scraperwiki.sqlite.execute("update Trades set LastPrice = '%f', LastDate = '%s', LastChange = '%f', LastSignal = '%s', LastSignalDate = '%s', Position = NULL where tidm = '%s'" % (currprice, currdate, lastchange, currsignal, currsignaldate, tidm))
              #print "tidm: %s entrysignal: %s  currsignal: %s" % (tidm, entrysignal, currsignal)
              if ((entrysignal=='BUY' or entrysignal=='STAY LONG') and (currsignal=='SELL' or currsignal=='SHORT' or currsignal=='STAY SHORT' or currsignal=='STAY SHORT' or currsignal=='STAY IN CASH')) or ((entrysignal=='SELL' or entrysignal=='SHORT' or entrysignal=='STAY SHORT' or entrysignal=='STAY SHORT' or entrysignal=='STAY IN CASH') and (currsignal=='BUY' or currsignal=='STAY LONG')):
                #print "In third"
                scraperwiki.sqlite.execute("update Trades set Position = 'CLOSE OUT' where tidm = '%s' and CloseDate is null" % (tidm))
                scraperwiki.sqlite.commit()      
            

            currsignal = None
            currsignaldate = None
            
        currprice = None 
        currdate = None
    
            #elif direction=='SELL':
             #   scraperwiki.sqlite.execute("update Trades set Position = 'Closing' where tidm = '%s'") % (tidm)
            #    scraperwiki.sqlite.commit()
           
    return;

####################################################
#Find New Stocks ===NOT USED===
####################################################

def FindNewTrades():
    
    opencnt = scraperwiki.sqlite.execute("select count(*) from Trades where Postion = 'Closing'")
    for x in opencnt["data"]:
        closecnt = x[0]
    
    #recommlist = scraperwiki.sqlite.execute("select `TIDM` from Company_Recommendations
    
    return;

####################################################
#Load Price History For Each Company (Called from Signal History Function)
####################################################

def ScrapePriceHistory(tidm):

  #scraperwiki.sqlite.execute("create table Company_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Open` real NOT NULL, `High` real NOT NULL, `Low` real NOT NULL, `Close` real NOT NULL, `Volume` integer NOT NULL, UNIQUE (`TIDM`, `Date`))")

  pricehistidm = 'z'
  pricehiscnt = 0
    
  p_enddate = datetime.date.today()
  p_startdate = p_enddate - datetime.timedelta(days=365)

  csvurl = "http://chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%s&c=%s&d=%d&e=%s&f=%s&g=d&ignore=.csv" % (tidm, int(p_startdate.strftime("%-m"))-1, p_startdate.strftime("%d"), p_startdate.strftime("%Y"), int(p_enddate.strftime("%-m"))-1, p_enddate.strftime("%d"), p_enddate.strftime("%Y"))  
  if pricehistidm == tidm:
    pricehistcnt = pricehiscnt + 1
    #print "Signal History TIDM: %s Count: %d" % (pricehistidm, pricehiscnt)
  elif pricehistidm != tidm:
    pricehistidm = tidm
    pricehiscnt = 0
  headercnt = 0

  try:
    #print tidm
    data = scraperwiki.scrape(csvurl)
    reader = csv.reader(data.splitlines()) 

    for row in reader:     
      if headercnt > 0:      
        cdate = row[0]
        copen = float(row[1])
        chigh = float(row[2])
        clow = float(row[3])
        cclose = float(row[4])
        cvolume = row[5]
        
        #if headercnt == 2:  
        #  print "tidm: %s, cdate: %s, copen: %f, chigh: %f, clow: %f, cclose: %f, cvolume: %s" % (tidm, cdate, copen, chigh, clow, cclose, cvolume)

        scraperwiki.sqlite.execute("insert or ignore into Company_History values (?, ?, ?, ?, ?, ?, ?)",  [tidm, cdate, copen, chigh, clow, cclose, cvolume])   

      headercnt+=1
 
  except HTTPError, e:
    print "%s HTTPError: " % (tidm), e.code

  scraperwiki.sqlite.commit()

  return;  


####################################################
#Load Signal History from British Bulls
####################################################

def ScrapeSignalHistory(runno):
    
    #scraperwiki.sqlite.execute("drop table if exists Signal_History")  
    #scraperwiki.sqlite.execute("create table Signal_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Price` real NOT NULL, `Signal` varchar2(15) NOT NULL, `Confirmation` char(1) NOT NULL, `GBP 100` real NOT NULL, `Last Updated` date NOT NULL,  UNIQUE (`TIDM`, `Date`))")
    
    #scraperwiki.sqlite.execute("create table Company_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Open` real NOT NULL, `High` real NOT NULL, `Low` real NOT NULL, `Close` real NOT NULL, `Volume` integer NOT NULL, UNIQUE (`TIDM`, `Date`))")


    #CoreSQL = "select distinct `TIDM` from Trades where CloseDate is null UNION select `tidm` from (select distinct `tidm` from Company_Performance where StdDev <= 12 and SignalAccuracy >= .6 limit 30)"
    AllSQL = "select distinct `TIDM` from company"
    CoreSQL = "select distinct `TIDM` from Trades where CloseDate is null"
    
    url = 'https://www.britishbulls.com/SignalPage.aspx?lang=en&Ticker='
    weekday = datetime.datetime.today().weekday()
    rundate = datetime.datetime.now().date()
    
    ### DEBUGGGING ###
    debugcnt = 0
    
    
    #Determine how much history to scan for, based on the day of week and the run number
    # 0=Monday, 6=Sunday
    if runno == 0:
        # All Companies
        lselist = scraperwiki.sqlite.execute(AllSQL)
    if runno == 1:
        # Trades Only
        lselist = scraperwiki.sqlite.execute(CoreSQL)
    elif runno == 2:
      if weekday == 0:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('A', 'H', 'O') and tidm not in ('%s')" % (CoreSQL))
      elif weekday == 1:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('B', 'I', 'P', 'W') and tidm not in ('%s')" % (CoreSQL))        
      elif weekday == 2:
        #lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('C', 'J', 'L', 'Q', 'X') and tidm not in ('%s')" % (CoreSQL))  
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('A', 'H', 'O', 'F', 'M', 'T', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'G', 'N', 'U', 'V', 'A', 'H', 'O', 'C', 'J', 'L', 'Q', 'X', 'B', 'I', 'P', 'W') and tidm not in ('%s')" % (CoreSQL))
        #lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where tidm not in ('%s')" % (CoreSQL))    
      elif weekday == 3:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('D', 'K', 'R', 'Y') and tidm not in ('%s')" % (CoreSQL))  
      elif weekday == 4:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('E', 'S', 'Z') and tidm not in ('%s')" % (CoreSQL))  
      elif weekday == 5:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('F', 'M', 'T', '1', '2', '3', '4', '5', '6', '7', '8', '9') and tidm not in ('%s')" % (CoreSQL))  
      #Must be Sunday..
      else:
        lselist = scraperwiki.sqlite.execute("select distinct `tidm` from company where substr(tidm,1,1) in ('G', 'N', 'U', 'V') and tidm not in ('%s')" % (CoreSQL))  
        
        
   

    #lselist = scraperwiki.sqlite.execute("select distinct `TIDM` from company")
    
    random.shuffle(lselist["data"])
    
    for x in lselist["data"]:
        
        tidm = str(x)[3:-2]
        #tidm = str(x)
        #print tidm
        
        ##siglist = scraperwiki.sqlite.execute("select count(*) from Signal_History where tidm = '%s' and (Signal IN ('SELL',  'SHORT',  'STAY IN CASH',  'STAY SHORT') OR (Signal IN ('BUY, 'STAY LONG') AND ))" % (tidm, d1date))

        br = mechanize.Browser()
    
        # sometimes the server is sensitive to this information
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        #pause before calling the URL
        if runno <= 1:
          time.sleep(random.uniform(5, 10))
        elif runno == 2:
          time.sleep(random.uniform(10, 45))
          ### CALL PRICE HISTORY FUNCTION ####
          ScrapePriceHistory(tidm)

        sighistidm = 'z'
        sighistcnt = 0

        response = br.open(url + tidm)
        if sighistidm == tidm:
          sighistcnt = sighiscnt + 1
          #print "Price History TIDM: %s Count: %d" % (sighistidm, sighiscnt)
        elif sighistidm != tidm:
          sighistidm = tidm
          sighiscnt = 0
        #debugcnt = debugcnt + 1
    
    #for pagenum in range(1):
        html = response.read()

        test1 = re.search(r'MainContent_signalpagehistory_PatternHistory24_DXDataRow0((.|\n)+)MainContent_signalpagehistory_PatternHistory24_IADD', html)

        if test1:
            test1 = test1.group(0)

            test3 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))

            while len(test3) >= 5:

                sh_Date = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
                sh_Date = date(int(sh_Date[6:10]),int(sh_Date[3:5]),int(sh_Date[:2]))
                #print "Date: %s" % (sh_Date)
                sh_Price = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                #print "Price: %s" % (sh_Price)
                sh_Signal = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)
                #print "Signal: %s" % (sh_Signal)
                sh_Confirmation = ((re.search("[Uncheck|Check]", str(test3.pop(0)).replace(" ", "")).group(0).lower()).replace("u","N")).replace("c", "Y")
                #print "Confirmation: %s" % (sh_Confirmation)
                sh_GBP100 = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "").replace(",", "")).group(0)
                #print "GDP100: %s" % (sh_GBP100)
                #print "Rundate: %s" % rundate

                scraperwiki.sqlite.execute("insert or ignore into Signal_History values (?, ?, ?, ?, ?, ?, ?)",  [tidm, sh_Date, sh_Price, sh_Signal, sh_Confirmation, sh_GBP100, rundate]) 

                scraperwiki.sqlite.commit()

                    
    #print "debugcnt: %d" % (debugcnt)
    return;


########################################################
# Return Signal Accuracy
########################################################

 
def signal_accuracy(tidm, d1date, todaydate):
    """Calculates the signal accuracy for Signal History from British Bulls"""

    complist = scraperwiki.sqlite.execute("select Sum(case `Confirmation` when 'Y' then 1 Else 0 end), Count(*) from Signal_History where tidm = '%s' and date between '%s' and '%s'" % (tidm, d1date, todaydate))
    
    #signalscore = 0

    for x in complist["data"]:
      signalscore = x[0]
      num_items = x[1]

    #for x in complist["data"]:
    #  if x[0] = 'Y' 
    #    signalscore = signalscore + 1;

    #num_items = len(complist["data"])

    #accuracy = signalscore / num_items
    if signalscore == 0 or signalscore == None or num_items < 10:
      accuracy = 0.0
    else:
      #print ("tidm: %s" % (tidm))
      #print ("SignalScore: %i" % (signalscore))
      #print ("num_items: %i" % (num_items))  
      accuracy = float(signalscore) / num_items

    #if tidm == "III.L":
    #  print ("Accuracy: %f" % (accuracy))
    #  print ("SignalScore: %i" % (signalscore))
    #  print ("num_items: %i" % (num_items))

    return accuracy

########################################################
# Return Standard Deviation
########################################################

 
def standard_deviation(tidm, d1date, todaydate):
    """Calculates the standard deviation for a list of numbers."""

    #print "tidm %s  d1date %s  todaydate %s" % (tidm, d1date, todaydate)
    #complist = scraperwiki.sqlite.execute("select (`High` - `Low`)/`High` from Company_History where tidm = '%s' and date between '%s' and '%s'" % (tidm, d1date, todaydate))
    ###complist = scraperwiki.sqlite.execute("select `Open`, `High`, `Low` from Company_History where tidm = '%s' and date between '%s' and '%s'" % (tidm, d1date, todaydate))
    complist = scraperwiki.sqlite.execute("select `High`-`Open` from Company_History where tidm = '%s' and date between '%s' and '%s'" % (tidm, d1date, todaydate))

    lstlength = len(complist["data"])
    
    if lstlength >= 10:
    
      lst = []
        
      for x in complist["data"]:
        lst.append(x[0])
       
      mean = sum(lst) / lstlength     

      ###for x in complist["data"]:
      ###  lst.append(x[0])
      ###  lst.append(x[1])
      ###  lst.append(x[2])
        #print "high-low: %f" % (x[0])
    
      ###mean = sum(lst) / lstlength
      ###differences = [y - mean for y in lst]
      ###sq_differences = [d ** 2 for d in differences]
      ###ssd = sum(sq_differences)
 
      #print('This is SAMPLE standard deviation.')
      #print "tidm: %s  numitems: %d  ssd: %f" % (tidm, num_items, ssd)
    
    
      ###variance = ssd / (lstlength - 1)
      ###sd = sqrt(variance)
    else:
      mean = 0
    # You could `return sd` here.

    return mean
 
    #print('The mean of {} is {}.'.format(lst, mean))
    #print('The differences are {}.'.format(differences))
    #print('The sum of squared differences is {}.'.format(ssd))
    #print('The variance is {}.'.format(variance))
    #print('The standard deviation is {}.'.format(sd))
    #print('--------------------------')
    
    
    ########################################################
# Return Standard Deviation
########################################################

 
def standard_deviation1(tidm, d1date, todaydate):
    """Calculates the standard deviation for a list of numbers."""

    complist = scraperwiki.sqlite.execute("select `Open`-`Low` from Company_History where tidm = '%s' and date between '%s' and '%s'" % (tidm, d1date, todaydate))

    lstlength = len(complist["data"])
    
    if lstlength >= 10:
    
      lst = []
        
      for x in complist["data"]:
        lst.append(x[0])
       
      mean = sum(lst) / lstlength     

    else:
      mean = 0

    return mean


########################################################
# Obtain User Input from Google Sheets
########################################################

def ScrapeUserInput():
  
  #scraperwiki.sqlite.execute("create table Trades (`TIDM` string, `3D` real, `10D` real, `30D` real, `90D` real, `180D` real, `6mthProfit` real, `6mthProfit_Rank` integer, `StdDev` real, `StdDev_Rank` integer, `SignalAccuracy` real, `SignalAccuracy_Rank` integer, `Overall_Score` integer, `Overall_Rank` integer, `Date` date) UNIQUE (col_name1, col_name2) ON CONFLICT IGNORE")

  #scraperwiki.sqlite.execute("drop table if exists trades")
  #scraperwiki.sqlite.execute("create table trades (`TXID` integer PRIMARY KEY, `TIDM` string, `OpenDate` date, `OpenSignal` string, `OpenPrice` real, `Stake` string, `LastDate` date, `LastPrice` real, `LastChange` real, `LastSignal` string, `LastSignalDate` date, `Position` string, `CloseDate` Date, `CloseSignal` string, `ClosePrice` real, `Earnings` real)")

  maxTXID = scraperwiki.sqlite.execute("select max(TXID) from trades")

  #for x in complist["data"]:
  #    signalscore = x[0]  

  br = mechanize.Browser()
  br.set_handle_robots(False)
  br.set_handle_equiv(False)
        
  csvurl = 'https://docs.google.com/spreadsheets/d/1HehMfkCV3uVEu4dgsVl1MTpZ891MGTTJaSNErxKIaiE/export?format=csv'
  #csvurl = 'https://drive.google.com/open?id=0B5StQm74mIseeE9pb09Qb1lPNDQ'
        
    # sometimes the server is sensitive to this information
  br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; AskTB5.6)')]
  response = br.open(csvurl, timeout=120.0)
        
        
  for pagenum in range(1):
    html = response.read()
    #html = urllib2.urlopen(csvurl)
    #reader = csv.DictReader(html)
    #for record  in reader["data"]:

    #print html
    #test1 = re.search(r'content=\"Sheet1(.*?)\"><meta name=\"google\" content=\"notranslate\">', html).group()
    #test1 = re.search(r'Earnings((.|\n)+)\"><meta name=\"google\"', html).group()
    #test1 = re.search(r'ltr\">EOF((.|\n)+)TX_LOCALE', html).group()
    test2 = re.search(r'EOF((.|\n)+),', html).group()
    #test2a = test2.replace(". ", ".").replace("/ ", "/")
    #print test2
    test3 = re.findall(r'(.*?)","', test2)
    #print test3

    #print test3.pop(0)
    #print test3.pop(0)
    #print "len: %i" % (len(test3)) 
    
    #words = test3.pop(0).split(',',1)
    
    while len(test3) > 0:   
      words = test3.pop(0).split(",")
    
      txid=words[0]
      tidm=words[1].strip()
      AlertDate=datetime.datetime.strptime(words[2].strip(), "%d/%m/%y")
      AlertDate=AlertDate.strftime("%Y-%m-%d") 
      AlertSignal=words[3].strip().upper()
      AlertPrice=words[4]
      EntryDate=datetime.datetime.strptime(words[5].strip(), "%d/%m/%y")
      EntryDate=EntryDate.strftime("%Y-%m-%d") 
      EntryPrice=words[6]
      Size=words[7]
      if len(words[8].strip()) == 0:
        CloseDate = None
      else:
        CloseDate=datetime.datetime.strptime(words[8].strip(), "%d/%m/%y")
        CloseDate=CloseDate.strftime("%Y-%m-%d") 
      CloseSignal=words[9].strip().upper()
      ClosePrice=words[10]
      Earnings=words[11]
    
      scraperwiki.sqlite.execute("insert or replace into trades values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  [txid, tidm, AlertDate, AlertSignal, AlertPrice, EntryDate, EntryPrice, Size, None, None, None, None, None, None, CloseDate, CloseSignal, ClosePrice, Earnings])  
   
    scraperwiki.sqlite.commit()
    #      print txid
    #    if cnt==2:
    #      tidm=test3.pop(0).strip()
    #      print tidm
    #      print " "
    #    if cnt==3:
    #      OpenDate=datetime.datetime.strptime(test3.pop(0).strip(), "%d/%m/%y")
    #      OpenDate=OpenDate.strftime("%Y-%m-%d") 
    #   if cnt==4:
    #      OpenSignal=test3.pop(0).strip().upper()
    #    if cnt==5:
    #      OpenPrice=test3.pop(0)
    #    if cnt==6:
    #      Stake=test3.pop(0)
    #    if cnt==7:
    #      CloseDate=test3.pop(0).strip()
    #    if cnt==8:
    #      CloseSignal=test3.pop(0).strip().upper()
    #    if cnt==9:
    #      ClosePrice=test3.pop(0)  
    #    if cnt==10:
    #      Earnings=test3.pop(0)

    # for each word in the line:
    #for word in words:

        # print the word
        #print(word)

    #cnt=1
    #while len(test3) > 0:
    #  CloseDate=None
    #  CloseSignal=None
    #  ClosePrice=None
    #  Earnings=None
    #  while test3[0] != "":
    #    if cnt==1:
    #      txid=test3.pop(0)
    #      print txid
    #    if cnt==2:
    #      tidm=test3.pop(0).strip()
    #      print tidm
    #      print " "
    #    if cnt==3:
    #      OpenDate=datetime.datetime.strptime(test3.pop(0).strip(), "%d/%m/%y")
    #      OpenDate=OpenDate.strftime("%Y-%m-%d") 
    #   if cnt==4:
    #      OpenSignal=test3.pop(0).strip().upper()
    #    if cnt==5:
    #      OpenPrice=test3.pop(0)
    #    if cnt==6:
    #      Stake=test3.pop(0)
    #    if cnt==7:
    #      CloseDate=test3.pop(0).strip()
    #    if cnt==8:
    #      CloseSignal=test3.pop(0).strip().upper()
    #    if cnt==9:
    #      ClosePrice=test3.pop(0)  
    #    if cnt==10:
    #      Earnings=test3.pop(0)
    #    cnt+=1
    #  if txid > maxTXID:
    #    scraperwiki.sqlite.execute("insert or replace into trades values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  [txid, tidm, OpenDate, OpenSignal, OpenPrice, Stake, None, None, None, None, None, None, CloseDate, CloseSignal, ClosePrice, Earnings])  
      
    #  test3.pop(0)
    #  cnt=1

    #scraperwiki.sqlite.commit()
 
  return;

########################################################
# Calculate Signal Performance
########################################################

def SignalPerformance(): 
           
   
   complist = scraperwiki.sqlite.execute("select `TIDM`, `Yesterday Price`, `Date` from company where TIDM in (select distinct TIDM from Signal_History) and Date in (select max(`Date`) from company)")
   #complist = scraperwiki.sqlite.execute("select `TIDM`, `Yesterday Price`, `Date` from company where tidm = 'III.L'")

   #scraperwiki.sqlite.execute("drop table if exists Company_Performance")   
   #scraperwiki.sqlite.execute("create table Company_Performance (`TIDM` string, `3D` real, `10D` real, `30D` real, `90D` real, `180D` real, `6mthProfit` real, `6mthProfit_Rank` integer, `StdDev` real, `StdDev_Rank` integer, `SignalAccuracy` real, `SignalAccuracy_Rank` integer, `Overall_Score` integer, `Overall_Rank` integer, `Date` date)")
   scraperwiki.sqlite.execute("delete from Company_Performance") 
   
   for x in complist["data"]:
       tidm=x[0]
       nprice=x[1]
       tdate=datetime.datetime.strptime(x[2], "%Y-%m-%d").date()
       todaydate=datetime.date.today()
       
       Commission=0.994

# Find Today GDP100

       ldata = scraperwiki.sqlite.execute("select `GBP 100` from Signal_History where tidm = '%s' and Date = '%s'" % (tidm, tdate))
       if len(ldata["data"]) != 0:
           for c in ldata["data"]:
              #print "first tprice: %s tidm: %s date: %s" % (tprice, tidm, tdate) 
              tprice = c[0]
              #print "second tprice: %s" % (tprice) 
           
       else:
        
           ldata = scraperwiki.sqlite.execute("select `GBP 100`, `Price`, `Signal` from Signal_History where tidm = '%s' and Date in (select max(`Date`) from Signal_History where tidm = '%s')" % (tidm, tidm))
           if len(ldata["data"]) == 0:
               tprice = 0
    
           else: 
               for b in ldata["data"]:
                   LatestGDP100 = b[0]
                   LatestPrice = b[1]
                   LatestSignal = b[2]
       
                   ldiff = (nprice - LatestPrice) / LatestPrice
           
                   if LatestSignal == 'BUY':
                       tprice = (LatestGDP100 + (LatestGDP100*ldiff))*Commission
                   elif LatestSignal == 'SHORT':
                       tprice = (LatestGDP100 + (LatestGDP100*(ldiff*-1)))*Commission
                   #SELL etc
                   else:
                       tprice = LatestGDP100*.994
               #print "Latest: %s: $%s" % (tdate, round(tprice,2))      
       

#Calculate Performance for the various intervals   
#-----------------------------------------------

       timeintervals = [3, 10, 30, 90, 180];
       
       for timeint in timeintervals:
       
          #print "Starting interval: %d" , (timeint)
           d1date=todaydate - datetime.timedelta(days=timeint)

           #print "TimeInt: %i" , (timeint)
           #print "d1date: %d" , (d1date)
    
           d1list = scraperwiki.sqlite.execute("select `GBP 100` from Signal_History where tidm = '%s' and Date = '%s'" % (tidm, d1date))
           
           if len(d1list["data"]) != 0:
               for a in d1list["data"]: 
                   CalcPrice = a[0]
    
           else:        
               d1mindate = scraperwiki.sqlite.execute("select `Date`, `GBP 100` from Signal_History where tidm = '%s' and Date in (select max(`Date`) from Signal_History where tidm = '%s' and Date < '%s')" % (tidm, tidm, d1date))
               
               if len(d1mindate["data"]) == 0:
                   #MinDate = '1900-01-01' #datetime.datetime.strptime(y[0], "%Y-%m-%d").date()
                   MinDate = datetime.datetime.strptime('1900-01-01', "%Y-%m-%d").date()
                   MinPrice = 0.0
               else: 
                   for y in d1mindate["data"]:
                        MinDate = datetime.datetime.strptime(y[0], "%Y-%m-%d").date()
                        MinPrice = y[1]

                        #print "MinDate: %d" , (MinDate)
                        #print "MinPrice: %f" , (MinPrice)
               
           d1maxdate = scraperwiki.sqlite.execute("select `Date`, `GBP 100` from Signal_History where tidm = '%s' and Date in (select min(`Date`) from Signal_History where tidm = '%s' and Date > '%s')" % (tidm, tidm, d1date))
                   
           #print "tprice: %s" % (tprice)
                
           if len(d1maxdate["data"]) == 0:
                #print "in first"
                MaxDate=tdate
                MaxPrice=tprice

                       #print "MaxDate: %d" , (MaxDate)
                       #print "MaxPrice: %f" , (MaxPrice)

           else:
               #print "in second"
               #print "MaxDate: %d" , (MaxDate)
               #print "d1date: %d" , (d1date)                       
               for z in d1maxdate["data"]:
                    #print "in secondp2"
                    MaxDate = datetime.datetime.strptime(z[0], "%Y-%m-%d").date()
                    #print "z1 is :%s" % (z[1]) 
                    MaxPrice = z[1]
          
           Abovedelta = MaxDate - d1date
           Belowdelta = d1date - MinDate

           MinMaxDelta = MaxDate - MinDate
           #print "tidm: %s" % (tidm)
           #print "timeint: %s" % (timeint)
           #print "maxPrice: %s" % (MaxPrice) 
           #print "minPrice: %s" % (MinPrice) 
           PriceDelta = MaxPrice - MinPrice
           if PriceDelta == 0 or MinMaxDelta.days == 0:
               PriceInterval=0
           else:
               PriceInterval = PriceDelta / MinMaxDelta.days

           if abs(Abovedelta.days) >= Belowdelta.days:
               CalcPrice = MinPrice+Belowdelta.days*PriceInterval
           else:
               CalcPrice = MaxPrice-Abovedelta.days*PriceInterval
                   
           D1PC = (tprice - CalcPrice) / CalcPrice


           #print "MaxPrice: %f" , (MaxPrice)
           #print "MixPrice: %f" , (MinPrice)
           #print "PriceDelta: %f" , (PriceDelta)
               
           if timeint == 3:
               T3D = round(D1PC,3)
           elif timeint == 10:
               T10D = round(D1PC,3)
           elif timeint == 30:
               T30D = round(D1PC,3)
           elif timeint == 90:
               T90D = round(D1PC,3)  
               stddev = standard_deviation(tidm, d1date, todaydate)
               sigacc = signal_accuracy(tidm, d1date, todaydate)
               #T90Earnings = ((tprice - CalcPrice)/CalcPrice+1)*100
               T90Earnings = standard_deviation1(tidm, d1date, todaydate)
           elif timeint == 180:
               T180D = round(D1PC,3)
               total = T3D + T10D + T30D + T90D + T180D
               #T180Earnings = ((tprice - CalcPrice)/CalcPrice+1)*100
               #if tidm == "KWE.L":
               #  print "tidm: %s  tprice: %f  calc price: %f"  % (tidm, tprice, CalcPrice)
               tprice=0.0
               scraperwiki.sqlite.execute("insert into Company_Performance values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  [tidm, round(T3D,3), round(T10D,3), round(T30D,3), round(T90D,3), round(T180D,3), round(T90Earnings,2), 0, round(stddev,3), 0, round(sigacc,3), 0, 0, 0, tdate]) 
               scraperwiki.sqlite.commit()
       #return;
 


#Calculate Rankings
#-----------------------------------------------

       #Update StdDev Ranking
       scraperwiki.sqlite.execute("delete from tmptbl_rank")
       scraperwiki.sqlite.execute("INSERT into tmptbl_rank (TIDM, Rank) SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance" )
       scraperwiki.sqlite.execute("Update Company_Performance SET StdDev_Rank = (select rank from tmptbl_rank where tidm = Company_Performance.tidm)")

       #Update 6mthProfit_Rank Ranking
       scraperwiki.sqlite.execute("delete from tmptbl_rank")
       scraperwiki.sqlite.execute("INSERT into tmptbl_rank (TIDM, Rank) SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT `6mthProfit` FROM Company_Performance AS t WHERE `6mthProfit` > Company_Performance.`6mthProfit` order by `6mthProfit` desc )) AS Rank FROM Company_Performance" )
       scraperwiki.sqlite.execute("Update Company_Performance SET `6mthProfit_Rank` = (select rank from tmptbl_rank where tidm = Company_Performance.tidm)")

       #Update SignalAccuracy Ranking
       scraperwiki.sqlite.execute("delete from tmptbl_rank")
       scraperwiki.sqlite.execute("INSERT into tmptbl_rank (TIDM, Rank) SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT SignalAccuracy FROM Company_Performance AS t WHERE SignalAccuracy > Company_Performance.SignalAccuracy)) AS Rank FROM Company_Performance" )
       scraperwiki.sqlite.execute("Update Company_Performance SET SignalAccuracy_Rank = (select rank from tmptbl_rank where tidm = Company_Performance.tidm)")

       #Update Company_Performance Ranking
       scraperwiki.sqlite.execute("Update Company_Performance SET Overall_Score = StdDev_Rank * `6mthProfit_Rank` * SignalAccuracy_Rank")
       scraperwiki.sqlite.execute("delete from tmptbl_rank")
       scraperwiki.sqlite.execute("INSERT into tmptbl_rank (TIDM, Rank) SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT Overall_Score FROM Company_Performance AS t WHERE Overall_Score < Company_Performance.Overall_Score)) AS Rank FROM Company_Performance" )
       scraperwiki.sqlite.execute("Update Company_Performance SET Overall_Rank = (select rank from tmptbl_rank where tidm = Company_Performance.tidm)")
       scraperwiki.sqlite.commit()
              
        
   return;     

#-----------------------------#
#-----------------------------#
def Notify(rundt):

  #if rerunflag == 0:  
    
      openlist = scraperwiki.sqlite.execute("select TXID, TIDM, AlertDate, AlertSignal, AlertPrice, EntryDate, EntryPrice, Size, LastDate, LastPrice, LastChange, LastSignal, LastSignalDate, Position, CloseDate, CloseSignal, ClosePrice, Earnings from Trades")

      Performance_Out = " TXID     TIDM     AlertDate    AlertSignal     AlertPrice     EntryDate     EntryPrice     Size      LastDate     LastPrice     LastChange     LastSignal     LastSignalDate     Position     CloseDate     CloseSignal     ClosePrice     Earnings<br>"
      Performance_Out = Performance_Out + "-----------------------------------------------------------------------------------------------------------------------------<br>"

      for x in openlist["data"]:
         txid = x[0]
         tidm = x[1]
         alertdate = x[2]
         alertsignal = x[3]
         alertprice = x[4]
         entrydate = x[5]
         entryprice = x[6]
         size = x[7]
         lastdate = x[8]
         lastprice = x[9]
         lastchange = x[10]
         lastsignal = x[11]
         lastsignaldate = x[12]
         position = x[13]
         closedate = x[14]
         closesignal = x[15]
         closeprice = x[16]
         earnings = x[17]       
         Performance_Out = Performance_Out + '{:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6}<br>'.format(txid, tidm, alertdate, alertsignal, alertprice, entrydate, entryprice, size, lastdate, lastprice, lastchange, lastsignal, lastsignaldate, position, closedate, closesignal, closeprice, earnings)
    
    #closecnt = scraperwiki.sqlite.execute("select count(*) from Trades where position = 'Closing'")
    
    #if closecnt > 0:
      
      Performance_Out = Performance_Out + "<br><br>Please close off the required trades. Here are your options for new trades:<br><br>"
    
      # New Options
      #ranklist = scraperwiki.sqlite.execute("select tidm, `3d`, `10d`, `30d`, `90d`, `180d`, `6mthProfit`, `6mthProfit_Rank`, StdDev, StdDev_Rank, SignalAccuracy, SignalAccuracy_Rank, Overall_Score, Overall_Rank from Company_Performance where `6mthProfit_Rank` < 150 and StdDev_Rank < 150 and SignalAccuracy >= .6 and tidm not in (select distinct tidm from Trades where CloseDate is null) and tidm not in (select distinct tidm from (select tidm, count(*) from Signal_History group by tidm having count(*) < 10)) order by Overall_Rank LIMIT 20")
      #ranklist = scraperwiki.sqlite.execute("select tidm, `3d`, `10d`, `30d`, `90d`, `180d`, `6mthProfit`, `6mthProfit_Rank`, StdDev, StdDev_Rank, SignalAccuracy, SignalAccuracy_Rank, Overall_Score, Overall_Rank from (select tidm, `3d`, `10d`, `30d`, `90d`, `180d`, `6mthProfit`, `6mthProfit_Rank`, StdDev, StdDev_Rank, SignalAccuracy, SignalAccuracy_Rank, Overall_Score, Overall_Rank from Company_Performance order by StdDev_Rank limit 50 intersect select tidm, `3d`, `10d`, `30d`, `90d`, `180d`, `6mthProfit`, `6mthProfit_Rank`, StdDev, StdDev_Rank, SignalAccuracy, SignalAccuracy_Rank, Overall_Score, Overall_Rank from Company_Performance order by SignalAccuracy_Rank limit 50) order by Overall_Rank")
      #ranklist = scraperwiki.sqlite.execute("select * from (select * from Company_Performance where StdDev_Rank <= 50 intersect select * from Company_Performance where SignalAccuracy_Rank <= 50) order by Overall_Rank")  
      #ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`3d`, A.`10d`, A.`30d`, A.`90d`, A.`180d`, A.`6mthProfit`, A.`6mthProfit_Rank`, A.StdDev, A.StdDev_Rank, A.SignalAccuracy, A.SignalAccuracy_Rank, A.Overall_Score, A.Overall_Rank from (select * from Company_Performance where StdDev_Rank <= 50 intersect select * from Company_Performance where SignalAccuracy_Rank <= 50) as A inner join company as B on A.tidm = B.tidm order by A.Overall_Rank")
      #ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`3d`, A.`10d`, A.`30d`, A.`90d`, A.`180d`, A.`6mthProfit`, A.`6mthProfit_Rank`, A.StdDev, A.StdDev_Rank, A.SignalAccuracy, A.SignalAccuracy_Rank, A.Overall_Score, A.Overall_Rank, C.Signal, C.Date AS "Signal Date" from (select * from Company_Performance where StdDev_Rank <= 50 intersect select * from Company_Performance where SignalAccuracy_Rank <= 50) as A inner join company as B on A.tidm = B.tidm INNER JOIN Signal_History as C on A.tidm = C.tidm where c.date >= %s order by A.Overall_Rank" % (datetime.datetime.strptime(datetime.date.today() - datetime.timedelta(days=7), "%Y-%m-%d").date()))
      #ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`3d`, A.`10d`, A.`30d`, A.`90d`, A.`180d`, A.`6mthProfit`, A.`6mthProfit_Rank`, A.StdDev, A.StdDev_Rank, A.SignalAccuracy, A.SignalAccuracy_Rank, A.Overall_Score, A.Overall_Rank, C.Signal, C.Date AS "Signal Date" from (select * from Company_Performance where StdDev_Rank <= 50 intersect select * from Company_Performance where SignalAccuracy_Rank <= 50) as A inner join company as B on A.tidm = B.tidm INNER JOIN Signal_History as C on B.tidm = C.tidm where c.date >= %s order by A.Overall_Rank" % (datetime.datetime.strptime(datetime.date.today() - datetime.timedelta(days=7), "%Y-%m-%d").date()))
      SignalDate = datetime.date.today() - datetime.timedelta(days=7)
      #SignalDate = SignalDate.strftime("%Y-%m-%d")

      #ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`3d`, A.`10d`, A.`30d`, A.`90d`, A.`180d`, A.`6mthProfit`, A.`6mthProfit_Rank`, A.StdDev, A.StdDev_Rank, A.SignalAccuracy, A.SignalAccuracy_Rank, A.Overall_Score, A.Overall_Rank, C.Signal, C.Date AS 'Signal Date' from (select * from Company_Performance intersect select * from Company_Performance ) as A inner join company as B on A.tidm = B.tidm LEFT JOIN (select distinct IA.tidm, IA.signal, IB.date from Signal_History as IA inner join (select tidm, max(date) as date from Signal_History where cast(substr(date,1,4) || substr(date,6,2) || substr(date,9,2) as integer) > %i group by tidm) as IB on IA.tidm = IB.tidm and IA.date = IB.date) as C on A.tidm = C.tidm where B.FTSE in ('FTSE 100') and C.Date is not null order by A.Overall_Rank LIMIT 50" % (int(SignalDate.strftime("%Y%m%d"))))
      ###ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`3d`, A.`10d`, A.`30d`, A.`90d`, A.`180d`, A.`6mthProfit`, A.`6mthProfit_Rank`, A.StdDev, A.StdDev_Rank, A.SignalAccuracy, A.SignalAccuracy_Rank, A.Overall_Score, A.Overall_Rank, C.Signal, C.Date AS 'Signal Date' from (select * from Company_Performance) as A inner join company as B on A.tidm = B.tidm LEFT JOIN (select distinct IA.tidm, IA.signal, IB.date from Signal_History as IA inner join (select tidm, max(date) as date from Signal_History where cast(substr(date,1,4) || substr(date,6,2) || substr(date,9,2) as integer) > %i group by tidm) as IB on IA.tidm = IB.tidm and IA.date = IB.date) as C on A.tidm = C.tidm where B.FTSE in ('FTSE 100') and C.Date is not null order by C.Date desc, A.SignalAccuracy desc" % (int(SignalDate.strftime("%Y%m%d"))))
      
      ranklist = scraperwiki.sqlite.execute("select distinct A.tidm, B.FTSE, A.`6mthProfit`, A.StdDev, A.SignalAccuracy, C.Signal, C.Date AS 'Signal Date' from (select * from Company_Performance) as A inner join company as B on A.tidm = B.tidm LEFT JOIN (select distinct IA.tidm, IA.signal, IB.date from Signal_History as IA inner join (select tidm, max(date) as date from Signal_History where cast(substr(date,1,4) || substr(date,6,2) || substr(date,9,2) as integer) > %i group by tidm) as IB on IA.tidm = IB.tidm and IA.date = IB.date) as C on A.tidm = C.tidm where B.FTSE in ('FTSE 100') and C.Date is not null order by C.Date desc, A.SignalAccuracy desc" % (int(SignalDate.strftime("%Y%m%d"))))
      
    
      #print SignalDate
      #ranklist = scraperwiki.sqlite.execute("select distinct tidm, max(date) from Signal_History where cast(substr(date,1,4) || substr(date,6,2) || substr(date,9,2) as integer) > %i and tidm = 'FXPO.L'" % (int(SignalDate.strftime("%Y%m%d"))))

      #for x in ranklist["data"]:
      #   print "%s  %s" % (x[0],x[1]) 

      Performance_Out = Performance_Out + "  TIDM  FTSE            Low Margin   High Margin   Sig Accuracy   Signal   Date<br>"
      Performance_Out = Performance_Out + "-------------------------------------------------------------------------------<br>"

      ###Performance_Out = Performance_Out + "  TIDM  FTSE            3D     10D     30D    90D   180D    6MthProfit   Rank   Stddev    Rank   Sig Accuracy  Rank    Overall Score  Rank     Signal   Date<br>"
      ###Performance_Out = Performance_Out + "------------------------------------------------------------------------------------------------------------------------------------------------------------<br>"

        #                                    LWDB.L FTSE Small Cap -0.029 -0.009  0.028  0.062  0.083     108.31       48     7.115     14      0.889        3         2016      5   SELL 2017-02-23

      for x in ranklist["data"]:
         tidm = x[0]
         ftse = x[1]    
         ###d3 = x[2]
         ###d10 = x[3]
         ###d30 = x[4]
         ###d90 = x[5]
         ###d180 = x[6]
         profit6mth = x[2]
         ###profit6mth_rank = x[8]
         stddev = x[3]
         ###stddev_rank = x[10]
         signalaccuracy = x[4]
         ###signalaccuracy_rank = x[12]
         ###overall_score = x[13]
         ###overall_rank = x[14]
         signal = x[5]
         signaldate = x[6]
    
         ###Performance_Out = Performance_Out + '{:>6} {:>8} {:>6} {:>6} {:>6} {:>6} {:>6} {:>10} {:>8} {:>9} {:>6} {:>10} {:>8} {:>15} {:>6} {:>11} {:>10}<br>'.format(tidm, ftse.ljust(14), d3, d10, d30, d90, d180, profit6mth, profit6mth_rank, stddev, stddev_rank, signalaccuracy, signalaccuracy_rank, overall_score, overall_rank, signal, signaldate)
         Performance_Out = Performance_Out + '{:>6} {:>8} {:>10} {:>9} {:>6} {:>11} {:>10}<br>'.format(tidm, ftse.ljust(14), profit6mth, stddev, signalaccuracy, signal, signaldate)

    

      msg = MIMEMultipart()
      msg['From'] = cGFyc3vdcmF
      msg['To'] = cPFyc4dvcvF
      msg['Subject'] = "List"

      body = "<pre><font face='Consolas'>" + Performance_Out + "</font></pre>"

      msg.attach(MIMEText(body, 'html'))
 
      server = smtplib.SMTP(cGFdc2evcmQ, 587)
      server.starttls()
      server.login(cGFyc3vdcmF, cGFzc3dvcmQ)
      text = msg.as_string()
      server.sendmail(cGFyc3vdcmF, cPFyc4dvcvF, text)
      server.quit()
      
      return;

#-----------------------------#
#-----------------------------#
def Logger(rundt, fname, status):
    
    #scraperwiki.sqlite.execute("create table RunLog (`Rundate` date, `RunDateTime` date, `Proc` string, `status` string)") 
    
    if status == 'Starting':
      scraperwiki.sqlite.execute("insert into RunLog values (?,?,?,?)", [rundt.date(), rundt, fname, status])
    elif status == 'Complete':
      scraperwiki.sqlite.execute("update RunLog set proc = '%s', status = '%s' where rundatetime = '%s'" % (fname, status, rundt))
    else:
      scraperwiki.sqlite.execute("update RunLog set proc = '%s', status = '%s' where rundatetime = '%s'" % (fname, 'Incomplete', rundt))                      
    
    scraperwiki.sqlite.commit()
    return;

            
########################################################
# MAIN
########################################################
if __name__ == '__main__':
                      
    rundt = datetime.datetime.utcnow()
    gvars()

    ###scraperwiki.sqlite.execute("delete from company")
    ###scraperwiki.sqlite.execute("delete from Signal_History")

    #openlist = scraperwiki.sqlite.execute("select `tidm`, `OpenDate` from Trades where CloseDate is null")

    #for x in openlist["data"]:
        
    #    tidm = x[0]
    #    opendate = datetime.datetime.strptime(x[1], "%Y-%m-%d").date()
        #openprice = x[2]

    #siglist = scraperwiki.sqlite.execute("select `TIDM`, `Date`, `Signal` from Signal_History where Date >= '%s' order by Date" % (opendate))

    #for x in siglist["data"]:
    #  print "%s  %s  %s" % (x[0],x[1], x[2]) 

    #scraperwiki.sqlite.execute("create table RunLog (`Rundate` date, `RunDateTime` date, `Proc` string, `status` string)") 
    #scraperwiki.sqlite.execute("create table Company_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Open` real NOT NULL, `High` real NOT NULL, `Low` real NOT NULL, `Close` real NOT NULL, `Volume` integer NOT NULL, UNIQUE (`TIDM`, `Date`))")
    #scraperwiki.sqlite.execute("create table tmptbl_rank (`TIDM` string, `Rank` integer)")
    #scraperwiki.sqlite.execute("create table trades (`TXID` integer PRIMARY KEY, `TIDM` string, `OpenDate` date, `OpenSignal` string, `OpenPrice` real, `Stake` string, `LastDate` date, `LastPrice` real, `LastChange` real, `LastSignal` string, `LastSignalDate` date, `Position` string, `CloseDate` Date, `CloseSignal` string, `ClosePrice` real, `Earnings` real)")

    #scraperwiki.sqlite.execute("drop table if exists Signal_History")  
    #scraperwiki.sqlite.execute("create table Signal_History (`TIDM` varchar2(8) NOT NULL, `Date` date NOT NULL, `Price` real NOT NULL, `Signal` varchar2(15) NOT NULL, `Confirmation` char(1) NOT NULL, `GBP 100` real NOT NULL, `Last Updated` date NOT NULL,  UNIQUE (`TIDM`, `Date`))")
    
    #scraperwiki.sqlite.execute("drop table if exists Company_Performance")   
    #scraperwiki.sqlite.execute("create table Company_Performance (`TIDM` string, `3D` real, `10D` real, `30D` real, `90D` real, `180D` real, `6mthProfit` real, `6mthProfit_Rank` integer, `StdDev` real, `StdDev_Rank` integer, `SignalAccuracy` real, `SignalAccuracy_Rank` integer, `Overall_Score` integer, `Overall_Rank` integer, `Date` date)")
   
    
    #scraperwiki.sqlite.execute("drop table company_recommendations")
    #scraperwiki.sqlite.execute("drop table company1")
    
    #scraperwiki.sqlite.execute("drop table if exists trades")
    #scraperwiki.sqlite.execute("create table trades (`TXID` integer PRIMARY KEY, `TIDM` string, `AlertDate` date, `AlertSignal` string, `AlertPrice` real, `EntryDate` date, `EntryPrice` real, `Size` real, `LastDate` date, `LastPrice` real, `LastChange` real, `LastSignal` string, `LastSignalDate` date, `Position` string, `CloseDate` Date, `CloseSignal` string, `ClosePrice` real, `Earnings` real)")
    #scraperwiki.sqlite.execute("create table trades (`TIDM` string, `OpenDate` date, `OpenSignal` string, `EntryDate` date, `EntryPrice` real, `Size` real, `LastPrice` real, `LastDate` date, `LastChange` real, `LastSignal` string, `Position` string, `CloseDate` Date, `CloseSignal` string, `ClosePrice` real, `Earnings` real) UNIQUE (`TIDM`, `OpenDate`) ON CONFLICT IGNORE")
    
                                             
    #Logger(rundt, 'Main', 'Starting')
    #print "%s Started.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    
    #Logger(rundt, 'ScrapeUserInput', None)
    #print "%s Scraping User Input.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #ScrapeUserInput()

    #Logger(rundt, 'ScrapeLivePrices', None)
    #print "%s Scraping Live Prices.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #ScrapeLivePrices()

    #Logger(rundt, 'ScrapeSignalHistory_Core', None)
    #print "%s Scraping Signal History (Core).." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #ScrapeSignalHistory(0)

    #Logger(rundt, 'UpdateOpenTrades', None)
    #print "%s Updating Open Trades.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #UpdateOpenTrades()

    #Logger(rundt, 'SignalPerformance', None)
    #print "%s Calculating Signal Performance.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #SignalPerformance()

    Logger(rundt, 'Notify', None)
    print "%s Sending Email Notification.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    Notify(rundt)

    #Logger(rundt, 'ScrapeSignalHistory_Ext', None)
    #print "%s Scraping Signal History Ext.." % (datetime.datetime.utcnow() + timedelta(hours=8))
    #ScrapeSignalHistory(1)

    Logger(rundt, 'Main', 'Complete')
    print "%s Complete." % (datetime.datetime.utcnow() + timedelta(hours=8))


    #`6mthProfit` real, `6mthProfit_Rank` integer, `StdDev` real, `StdDev_Rank` integer, `SignalAccuracy`
    #scraperwiki.sqlite.execute("create table tmptbl_rank (`TIDM` string, `Rank` integer)")

    #scraperwiki.sqlite.execute("delete from tmptbl_rank")
    #scraperwiki.sqlite.execute("INSERT into tmptbl_rank (TIDM, Rank) SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance" )

    #scraperwiki.sqlite.execute("UPDATE Company_Performance SET Company_Performance.StdDev_Rank = (select rank from tmptbl_rank) where tidm = Company_Performance.tidm")

    #scraperwiki.sqlite.execute("UPDATE Company_Performance dest, (SELECT tidm, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance) src SET dest.StdDev_Rank = src.Rank where dest.tidm = src.tidm" )


    #scraperwiki.sqlite.execute( \
    #+ "Update Company_Performance CP Set StdDev_Rank = SELECT RANK FROM (SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance) where tidm = CP.tidm" ) 
    #+ "SET StdDev_Rank = " \
    #+ "(select rank from (SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev))" \
    #+ " AS Rank FROM Company_Performance) as A)" \
    #+ " where tidm = A.tidm" ) 

    #scraperwiki.sqlite.execute(
    #+ "Update Company_Performance "
    #+ "SET StdDev_Rank = " \
    #+ "(select rank from (SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < t.StdDev)) " \
    #+ "AS Rank FROM Company_Performance) as A) " \
    #+ "where tidm = Company_Performance.tidm" ) 

    #scraperwiki.sqlite.execute("Update Company_Performance SET StdDev_Rank = (select rank from (SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance) as A) where tidm = Company_Performance.tidm")
    
    #scraperwiki.sqlite.execute("Update Company_Performance SET StdDev_Rank = (select rank from (SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance AS t WHERE StdDev < t.StdDev)) AS Rank FROM Company_Performance) where tidm = Company_Performance.tidm)")
    #scraperwiki.sqlite.execute("Update Company_Performance SET StdDev_Rank = (select rank from tmptbl_rank where tidm = Company_Performance.tidm)")


    #scraperwiki.sqlite.commit()

    #ranklist = scraperwiki.sqlite.execute( \
    #"SELECT TIDM, 3D, 10D, 30D, 90D, 180D, 6mthProfit, StdDev, SignalAccuracy, Date, from Company_Performance_tmp order by tidm" \
    #+ "UNION" \
    #+ "SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance " \
    #+  "AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance order by tidm")

    #ranklist = scraperwiki.sqlite.execute("SELECT tidm, StdDev, (SELECT COUNT()+1 FROM (SELECT DISTINCT StdDev FROM Company_Performance " \
    #+  "AS t WHERE StdDev < Company_Performance.StdDev)) AS Rank FROM Company_Performance order by rank")
          
    #data = scraperwiki.scrape("https://drive.google.com/open?id=1HehMfkCV3uVEu4dgsVl1MTpZ891MGTTJaSNErxKIaiE")
      
    #reader = csv.reader(data.splitlines())

    #for row in reader:           
    #    print row[1]




          #print test3.pop(0)
          #print test3.pop(0)
          #print test3.pop(0)

        #test3 = re.findall('(\">|img\/)(.*?)(<\/|\.gif)', test1.replace("\B", ""))

         #       while len(test3) >= 5:
        
          #          sh_Date = re.search("(\w|\d)(.*)(\w|\d)", str(test3.pop(0)).replace(" ", "")).group(0)

    #reader = csv.DictReader(data.splitlines()) 
    
    #for row in reader:           qqw
    #if row['Transaction Number']:
    #   row['Amount'] = float(row['Amount'])
    #   scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)

    #Notify(Performance_Out)
    #print strftime("%Y-%m-%d %H:%M:%S", gmtime())

