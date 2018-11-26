import os
import re
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats
import calendar
import sys



sizeList=np.zeros((100,100))
sizeListWeekdays=np.zeros((100,100))
sizeListWeekends=np.zeros((100,100))
resultSizeList=np.zeros((100,100))
tmpList=np.zeros(100)



def passing_perHour():
    if os.path.isfile("2015_07//2015_07_01_ResponseSizePerHour.csv")==False:
        for date in range(1,32):
            if date<10:
                date=str("0"+str(date))
            f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+".request.log",'r')
            f_out_1=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+"_ResponseSizePerHour.csv",'w')
            lines=f_in.readlines()
            now_hour_str="00"
            now_hour=0
            size_hour=list(range(25))

            # initializing list
            for j in range(25):
                size_hour[j]=0


            p=re.compile('\d+\/\w+\/\d+\:\d+\:\d+\:\d+\s+\+\d+')
            q=re.compile('"\s+\d+\s+(\d+)')

            for line in lines:
            
                iterator_size=q.finditer(line)
                iterator_time=p.finditer(line)

                # iterator
                for match in iterator_time:
                    # Getting only hours in data
                    if now_hour_str!=match.group()[12:14]:
                        now_hour_str=match.group()[12:14]
                        now_hour+=1

                for match in iterator_size:
                    size_hour[now_hour]+=int(match.group(1))

            # This is for 00:00:00
            size_hour[23]=size_hour[23]+size_hour[24]
            for i in range(0,24):
                f_out_1.write(str(size_hour[i])+"\n")
        
        f_in.close()
        f_out_1.close()
        print("Session 1 complete")
    
    else:
        print("Session 1 complete(already done)")

            

def passing_perHalfHour():
    if os.path.isfile("2015_07//2015_07_01_ResponseSizePerHalfHour.csv")==False:
        for date in range(1,32):
            if date<10:
                date=str("0"+str(date))
    
            f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+".request.log",'r')
            f_out_1=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+"_ResponseSizePerHalfHour.csv",'w')
            lines=f_in.readlines()
            flag=1
            now_hour_str="00"
            now_hour=0
            size_hour=list(range(100))


            # initializing list
            for j in range(100):
                size_hour[j]=0


            p=re.compile('\d+\/\w+\/\d+\:\d+\:\d+\:\d+\s+\+\d+')
            q=re.compile('"\s+\d+\s+(\d+)')


            for line in lines:
        
                iterator_size=q.finditer(line)
                iterator_time=p.finditer(line)
        
                for match in iterator_time:
                    if flag==0 and (str(match.group()[15:17])=="00" or str(match.group()[15:17])=="30"):
                        now_hour+=1
                        flag=1
    
                    if str(match.group()[15:17])!="00" and str(match.group()[15:17])!="30":
                        flag=0

                for match in iterator_size:
                    size_hour[now_hour]+=int(match.group(1))

            size_hour[47]+=size_hour[48]

            for i in range(0,48):
                f_out_1.write(str(size_hour[i])+"\n")
        
        f_in.close()
        f_out_1.close()

        print("Session 1 complete")
    
    else:
        print("Session 1 complete(already done)")



def fileOpening(r, Choice_2):
    f_in_list=list(range(r+1))
    time=0
    d=0

    for date in range(1,r+1):
        if Choice_2==1:
            if date<10:
                f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_0"+str(date)+"_ResponseSizePerHour.csv",'r')
            else:
                f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+"_ResponseSizePerHour.csv",'r')
        elif Choice_2==2:
            if date<10:
                f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_0"+str(date)+"_ResponseSizePerHalfHour.csv",'r')
            else:
                f_in=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//2015_07_"+str(date)+"_ResponseSizePerHalfHour.csv",'r')
    
        f_in_list[date]=f_in


    for i in range(1,r+1):
        lines=f_in_list[i].readlines()
        for line in lines:
            sizeList[d,time]=line
            #print(str(d)+" "+str(time)+" "+str(line))
            time+=1
        d+=1
        time=0



def estimation(Choice_1,Choice_2,confidence=95):
    wdIndex=0
    weIndex=0
    tmpList=np.zeros(100)

    if Choice_2==1:
        passingIndex=24
    elif Choice_2==2:
        passingIndex=48

    if Choice_1==1:
        for date in range(1,31):
            if calendar.weekday(2015,7,date)<5:
                sizeListWeekdays[wdIndex]=sizeList[date]
                wdIndex+=1
            else:
                sizeListWeekends[weIndex]=sizeList[date]
                weIndex+=1
        
        for i in range(0,passingIndex):
            tmpList=np.resize(tmpList,100)
            for j in range(0,wdIndex):
                tmpList[j]=sizeListWeekdays[j,i]

            tmpList=np.resize(tmpList,wdIndex)
            m=np.mean(tmpList)
            se=scipy.stats.sem(tmpList)
            h=se*sp.stats.t._ppf((1+(confidence/100))/2.,24)

            resultSizeList[0,i]=m
            resultSizeList[1,i]=m+h
            resultSizeList[2,i]=m-h

            for k in range(0,weIndex):
                tmpList[k]=sizeListWeekends[k,i]

            tmpList=np.resize(tmpList,(weIndex))
            m=np.mean(tmpList)
            se=scipy.stats.sem(tmpList)
            h=se*sp.stats.t._ppf((1+(confidence/100))/2.,24)

            resultSizeList[3,i]=m
            resultSizeList[4,i]=m+h
            resultSizeList[5,i]=m-h

        ##############################
        ## Graph visualization
        num_plots = 6
        colormap = plt.cm.gist_ncar
        plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))

        labels = []

        plt.axis([0, 24, 0, 100000000])
        #modify axis range

        plt.plot(resultSizeList[0])
        labels.append(r'$weekday$')

        plt.plot(resultSizeList[1], 'o')
        # labels.append(r'$%ith +$' % (0))
        labels.append(r'$weekday+$')

        plt.plot(resultSizeList[2], 'x')
        labels.append(r'$weekday-$')

        plt.plot(resultSizeList[3])
        labels.append(r'$weekend$')

        plt.plot(resultSizeList[4], 'o')
        labels.append(r'$weekend+$')

        plt.plot(resultSizeList[5], 'x')
        labels.append(r'$weekend-$')

        plt.ylabel('Response Size')
        plt.xlabel('Hour')
        
        plt.legend(labels, ncol=2, loc='upper center', bbox_to_anchor=[0.5, 1.1], columnspacing=1.0, labelspacing=0.0, handletextpad=0.0, handlelength=1.5, fancybox=True, shadow=True)

        plt.show()

        ##
        #######################################################
    elif Choice_1==2:
        for now in range(1,8):
            nowDate=calendar.weekday(2015,7,now)

            while(True):   
                if now>30:
                    break
                else:
                    sizeListWeekdays[wdIndex]=sizeList[now]
                    wdIndex+=1
                    now+=7
            
            for i in range(0,passingIndex):
                for j in range(0,wdIndex):
                    tmpList[j]=sizeListWeekdays[j,i]

                tmpList=np.resize(tmpList,wdIndex)
                m=np.mean(tmpList)
                se=scipy.stats.sem(tmpList)
                h=se*sp.stats.t._ppf((1+(confidence/100))/2.,24)

                resultSizeList[nowDate*3,i]=m
                resultSizeList[nowDate*3+1,i]=m+h
                resultSizeList[nowDate*3+2,i]=m-h

            wdIndex=0


    
    elif Choice_1==3:
        nowDate=int(SpecificDate[8:10])
        tmpList=np.zeros(int(nowDate/7))
        while(True):   
            nowDate-=7
            if nowDate<1:
                break
            else:
                sizeListWeekdays[wdIndex]=sizeList[nowDate]
                wdIndex+=1

        for i in range(0,passingIndex):
            for j in range(0,wdIndex):
                tmpList[j]=sizeListWeekdays[j,i]

            m=np.mean(tmpList)
            se=scipy.stats.sem(tmpList)
            h=se*sp.stats.t._ppf((1+(confidence/100))/2.,24)

            resultSizeList[0,i]=m
            resultSizeList[1,i]=m+h
            resultSizeList[2,i]=m-h



def outputCsv(Choice_1, Choice_2):
    if Choice_2==1:
        passingIndex=24
    elif Choice_2==2:
        passingIndex=48

    outputFileName=input("Enter the output file name: ")
    f_out_2=open(os.path.dirname(os.path.realpath(__file__))+"//2015_07//"+outputFileName,'w')

    if Choice_1==1:
        for i in range(0,6):
            for j in range(0,passingIndex):
                f_out_2.write(str(resultSizeList[i,j])+",")
            f_out_2.write("\n")
    
    elif Choice_1==2:
        for i in range(0,21):
            for j in range(0,passingIndex):
                f_out_2.write(str(resultSizeList[i,j])+",")
            f_out_2.write("\n")

    elif Choice_1==3:
        for i in range(0,3):
            for j in range(0,passingIndex):
                f_out_2.write(str(resultSizeList[i,j])+",")
            f_out_2.write("\n")




    
# Main Function


print("#                                            #")
print("#   This program is data estimating program  #")
print("#   for auto-scaling for cloud computing     #")
print("#                                            #\n")


    # For Mode Selecting
while(True):
    print(" 1) Mode Selecting")
    print("     1. Estimating Object\n")
    print("(1) With 3 weeks' data, estimate weekdays and weekends")
    print("(2) With 3 weeks' data, estimate by day of the week")
    print("(3) Specific date, with previous data")

    Choice_1=int(input("Select: "))
    if Choice_1==1 or Choice_1==2:
        break
    elif Choice_1==3:
        print("Enter the date [ex)2015_07_01]")
        SpecificDate=input("Date should be over 2015_07_14:")
        if int(SpecificDate[8:10])<15:
            print("Date is too small\n")
        else:
            break
    else:
        print("Wrong input, plz try again\n\n")


    # For Time Unit Selecting
while(True):
    print("\n     2. Time Unit\n")
    print("(1) 1 hour")
    print("(2) a half hour")

    Choice_2=int(input("Select: "))
    if (Choice_2==1) or (Choice_2==2):
        break
    else:
        print("Wrong input, plz try again\n\n")


    # For Reliability
while(True):
    print("\n     3. Reliability\n")
    Choice_3=int(input("Enter Reliability(0~100): "))

    if(Choice_3>0) and (Choice_3<100):
        break
    else:
        print("Wrong input, plz try again\n\n")


    # For Output Style
    '''
while(True):
    print("\n     4. Output Style\n")
    print("(1) Graph")
    print("(2) csv file")
    print("(3) 1 and 2")

    Choice_4=int(input("Select: "))
    if (Choice_4==1) or (Choice_4==2) or (Choice_4==3):
        break
    else:
        print("Wrong input, plz try again\n\n")
        '''


    # Processing with input
if Choice_2==1:
    passing_perHour()
elif Choice_2==2:
    passing_perHalfHour()

if Choice_1==1 or Choice_1==2:
    fileOpening(30,Choice_2)
elif Choice_1==3:
    fileOpening(int(SpecificDate[8:10]),Choice_2)

estimation(Choice_1,Choice_2,Choice_3)
outputCsv(Choice_1,Choice_2)
