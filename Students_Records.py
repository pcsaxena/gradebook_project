import pandas

df1=pandas.read_csv("hw_exam_grades.csv")
df2=pandas.read_csv("roster.csv")

df4=pandas.read_csv('quiz_1_grades.csv')
df5=pandas.read_csv('quiz_2_grades.csv')
df6=pandas.read_csv('quiz_3_grades.csv')
df7=pandas.read_csv('quiz_4_grades.csv')
df8=pandas.read_csv('quiz_5_grades.csv')

#loop for creation of 3 files(section_1, section_2, section_3)
for x in range(1,4):
    section = df2.loc[df2['Section']==x]    # variable to store data from df2 where Section coumn ==x
    section=section.rename(columns={'Section':'Grade', 'NetID':'SID'})
    section['SID']=section['SID'].str.lower()
    print(section)
    section=pandas.merge(df1,section[["SID","Email Address","Grade"]],on="SID",how="inner")
    list_of_pop_items=["Email Address","Grade"]    #list for columns to be placed forward
    for item in list_of_pop_items:          #  column is popped and inserted using above list
        items_pop=section.pop(item)
        section.insert(3, item, items_pop)

    section=section.rename(columns={'Grade':'Section'})    
    section['Email Address']=section['Email Address'].str.lower()

    for y in range(1,6):    # inner merging and adding 5 quiz columns in each section table
        section=pandas.merge(section,df4[["Grade","Email"]],left_on="Email Address", right_on="Email", how="inner")
        Quiz = "Quiz" + str(y)
        section=section.rename(columns={'Grade':Quiz})
        section=section.drop(['Email'], axis =1)
    section=section.fillna(0)          # filling each section table's empty value with 0
   
    values=section.loc[:,['Exam 1', 'Exam 2', 'Exam 3']].mean(axis=1)      # assigning mean of all 3 columns for each row to variable
    section['Exam_Mean']= values                                           # assigning above variable data to section's Exam_Mean column
    list1= section['Exam_Mean'].tolist()           # converting column to list
    list1.sort(reverse=True)                       # sorting in desc.. order
    dataframe_data=[]
    #length= len(list1)
    var_rank=1
    for idx,z in enumerate(list1):          #data to create new dataframe which will have Rank and sorted (Exam_Mean) column data
        
        list_item_x=[] 
        length_dataframe_data=len(dataframe_data)
        if length_dataframe_data > 0 and dataframe_data[length_dataframe_data-1][0]==z:    # if length of new variable(to be used for new dataframe) is more than 0 and last exam_mean is equal to current z value
            list_item_x.append(z)
            list_item_x.append(dataframe_data[length_dataframe_data-1][1])
        else:
            list_item_x.append(z)
            list_item_x.append(var_rank)
            var_rank=var_rank+1
                                     
        dataframe_data.append(list_item_x)         # data is appended in the variable(to be used for new dataframe) in each sequence
    
    Rank_Dataframe=pandas.DataFrame(dataframe_data, columns=['Exam_Mean', 'Rank'])        # creation of dataframe
    section=pandas.merge(section,Rank_Dataframe,on='Exam_Mean')                           # final merging of section table with new dataframe 
    file_name = "section_" + str(x) + ".csv"                                               # assigning text to variable to be used for naming the final table
    section.to_csv(file_name)                                                              #converting section table into csv file using above variable 
    








