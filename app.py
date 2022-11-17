import pandas as pd
import numpy as np

df = pd.read_csv("final_ML_data.csv",sep=",", encoding='cp1252')

df['location']=df['location'].str.replace(', Bangalore','')

list_1=[]
for i in df['cusines']:
    list_1.append(len([x for x in i if "," in x])+1)

df['new']=1
for i in df.index:
    df['new'][i]=list_1[i]

someDF=df
someDF["RepeatIndex"] = someDF["new"].fillna(value=0).apply(lambda x: list(range(int(x))) if x > 0 else [])
superDF = someDF.explode("RepeatIndex").dropna(subset="RepeatIndex")

abss = [val.strip() for sublist in df.cusines.dropna().str.split(",").tolist() for val in sublist]

superDF['cuisine']=abss

superDF.drop(['cusines','new'],axis=1,inplace=True)

superDF.drop(superDF[superDF['cuisine']==''].index,inplace=True)

loc=superDF['location'].unique()

loc1=[]
for i in loc:
    loc1.append(i)
loc1.sort()
start=0
dict_1={}
for i in range(len(loc1)):
    dict_1[start]=loc1[i]
    start+=1

Cu_Li=superDF['cuisine'].unique()
Cu_Li
Cu_Li1=[]
for i in Cu_Li:
    Cu_Li1.append(i)
Cu_Li1.sort()   
Cu_Li1
start1=0
dict_2={}
for i in range(len(Cu_Li1)):
    dict_2[start1]=Cu_Li1[i]
    start1+=1



# #--------------------------

from flask import Flask,render_template,request,redirect
import pickle

model=pickle.load(open('model.pkl','rb'))
model2=pickle.load(open('model2.pkl','rb'))

app = Flask(__name__)
@app.route('/')  
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    #for the area selected, display the popular cuisine
    abc=[x for x in request.form.values()]
    pop_cu=superDF[superDF['location']==abc[1]]
    output=pop_cu['cuisine'].mode().values[0]

    #average price for 1

    Avg_price=superDF[superDF['location']==abc[1]]
    Avg1=Avg_price['price_for_one'].mean()

    #Display the most popular Restaurant and Cuisine they are serving
    
    Most_popu=superDF[superDF['location']==abc[1]]
    Most_popu=Most_popu.sort_values(by=['delivery_review_number'],ascending=False).Name.head(1).values[0]
    Cui_by_popu=superDF[(superDF['Name']==Most_popu) & (superDF['location']==abc[1])]['cuisine'].values
    
    # Display the most popular restaurant that is serving the same cuisine as user provided cuisine
    Same_Serving_cusine=superDF[superDF['cuisine']==abc[0]]
    SSC=Same_Serving_cusine.sort_values(by=['delivery_review_number'],ascending=False).Name.head(1).values[0]
 
    #encoding Location based on dictionary1
    key_list1 = list(dict_1.keys())
    val_list1 = list(dict_1.values())
    position = val_list1.index(abc[1])
    encoded_loc=key_list1[position]

    #encoding Cuisine based on dictionary2
    key_list2 = list(dict_2.keys())
    val_list2 = list(dict_2.values())
    position2 = val_list2.index(abc[0])
    encoded_Cui=key_list2[position2]

    
    #model prediction 1
    prediction1 = model.predict([[encoded_loc]])
    

    #model prediction 2
    encoded_prediction2=model2.predict([[encoded_Cui,int(abc[2])]])
    prediction_2=dict_1.get(encoded_prediction2[0])



    return render_template('index.html', prediction_text='Popular cuisine is {}'.format(output), Avgfor1='Average Price for one is Rs.{}'.format(int(Avg1)),Q3='Most popular restaurant is {} and they are serving {}'.format(Most_popu,str(Cui_by_popu).strip("[]")),Q4='The most popular restaurant that is serving the same cuisine as you provided: {}'.format(SSC),Q2_1='Recommended price :{} Rs'.format(prediction1[0]),Q2_2='Recommended location is :{}'.format(prediction_2))



if __name__=='__main__':
    app.run(debug=True)