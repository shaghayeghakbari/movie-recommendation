##################### calculations ####################
# Taste Compatibility Index
def calculate_TCI(userID):
    user_TCI_list[userID][0]=0
    for i in range (userID+1,user_count):
        temp_list=[]
        for k in (user_rating_list[userID]):
            for z in (hashed_rating_list[i][k[0]%200]):
                if (k[0]==z[0]):
                    temp_list.append(abs(k[1]-z[1]))
        if (len(temp_list)>1):
            this_TCI=0
            for j in (temp_list):
                this_TCI += j
            this_TCI=float(this_TCI)/len(temp_list)
            user_TCI_list[userID][i]=this_TCI
            user_TCI_list[i][userID]=this_TCI
    """ calculate top 100 TCI """
    temp_list=[]
    for i in range(user_count):
        temp_list.append(user_TCI_list[userID][i])
    for i in range(bestCount):
        conti=False
        for k in (temp_list):
            if (k!="#"):
                conti=True
        if(conti):
            min_TCI=100
            min_index=-1
            for k in range(len(temp_list)):
                if (temp_list[k]!="#"):
                    if(temp_list[k]<min_TCI):
                        min_TCI=temp_list[k]
                        min_index=k
            best_user_TCI[userID].append([min_index,min_TCI])
            temp_list[min_index]="#"
        else:
            break
        
"""  Probable Score Indicator """   #changed        
def calculate_PSI(userID,movieID,a,b,c,d,e):
    if(user_TCI_list[userID][0]=="#"):
        calculate_TCI(userID)
    temp_list=[]
    for i in (best_user_TCI[userID]):
        for j in (hashed_rating_list[i[0]][movieID%200]):
            if(j[0]==movieID):
                temp_list.append(j[1])
                break
    this_PSI=0
    min_to_cal=5                       
    if(len(temp_list)<min_to_cal):
        return "not enough data"
    else:
        for i in range(min_to_cal):
            this_PSI += temp_list[i]
        this_PSI=float(temp_list[0]*a+temp_list[1]*b+temp_list[2]*c+temp_list[3]*d+temp_list[4]*e)/(a+b+c+d+e)
        return int('%.0f'%this_PSI)

##################### testing functions ####################
def test_difference_result(userID,a,b,c,d,e):
    if(user_TCI_list[userID][0]=="#"):
        calculate_TCI(userID)
    rating_list=user_rating_list[userID]
    best_TCI=best_user_TCI[userID]
    total_results=0
    total_dif=0
    for i in (rating_list):
        ans=calculate_PSI(userID,i[0],a,b,c,d,e)
        if(ans!="not enough data"):
            total_dif +=abs(int(ans)-i[1])
            total_results += 1
    return "%.2f"%((20.0*total_dif)/total_results)

def total_difference_test(userCount,a,b,c,d,e):
    total=0
    for i in range(1,userCount):
        print "User "+str(i)+" ::",
        ans=test_difference_result(i,a,b,c,d,e)
        print ans
        total += float(ans)
    print total/user_count

def print_TCI(userID):
    print calculate_TCI(userID)

def print_PSI(userID,movieID,a,b,c,d,e):
    print calculate_PSI(userID,movieID,a,b,c,d,e)
    
############################################################ Added

def addScore(userID,movieID,score):
    user_rating_list[userID].append(score)
    hashed_rating_list[userID][movieID%200].append([movieID,score])
    if (user_TCI_list[userID][0]=="#"):
        user_TCI_list[userID][0]=1
    elif (user_TCI_list[userID][0]>=0 and user_TCI_list[userID][0]<5):
        user_TCI_list[userID][0]=user_TCI_list[userID][0]+1
    elif (user_TCI_list[userID][0]==5):
        user_TCI_list[userID][0]="#"
        update_TCI(userID)

def update_TCI(userID):
    if (user_TCI_list[userID][0]=="#"):
        best_user_TCI[userID]=[]
        calculate_TCI(userID)

############################################################
    
rating_file=open('Ratings.txt','r')
rating_list=rating_file.readlines()
user_rating_list=[[]]
hashed_rating_list=[[]]
user_TCI_list=[[]]
best_user_TCI=[[]]
bestCount=100                                         
user_count=0
""" Enter data in user rating list """
for i in range (len(rating_list)):                  
    rating_list[i]=rating_list[i].split()           
    rating_list[i][0]=int(rating_list[i][0])
    rating_list[i][1]=int(rating_list[i][1])
    rating_list[i][2]=int(rating_list[i][2])
user_count=rating_list[-1][0]+1     #list is sorted by userID
print user_count
""" Extending arrays """
for i in range (user_count):
    user_rating_list.append([])
    user_TCI_list.append([])
    best_user_TCI.append([])
    hashed_rating_list.append([])
    for j in range(user_count):
        user_TCI_list[i].append("#")
    for j in range(200):
        hashed_rating_list[i].append([])
"""adding score to user rating lists"""
for i in (rating_list):
    user_rating_list[i[0]].append([i[1],i[2]])
    hashed_rating_list[i[0]][i[1]%200].append([i[1],i[2]])
