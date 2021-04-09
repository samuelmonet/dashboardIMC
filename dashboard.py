import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor

st.title('IMC GBV South Sudan')
st.write('Dashboard to generate bivariate graphics')
st.sidebar.title('Questions Selector')


@st.cache
def load_data():
   data = pd.read_csv('../../visualizations.csv')
   correl= pd.read_csv('correl.csv')
   return data,correl

data=load_data()[0]
correl=load_data()[1]


def main():
	#Selection de la question principale
	main_question = st.sidebar.selectbox('Main question:', [None]+data.columns.tolist())
	if main_question != None:
			
		if st.sidebar.checkbox('Display potentially correlated questions'):	
			fig=bivariate(main_question)
		else: 
			fig=px.histogram(data, x=main_question)
	else:
		fig=px.histogram(data, x=main_question)
	st.plotly_chart(fig)
		
def bivariate(main_question):
	
		#Selection de la seconde question
	second_question = st.sidebar.selectbox('Second question:', correl[main_question].tolist())

	if second_question!= None:
	
		agg=data[[second_question,main_question]].groupby(by=[main_question,second_question])\
			.aggregate({main_question:'count'}).unstack()
		agg=agg/agg.sum()
		agg=agg.T
		agg
		x=[i[1] for i in agg.index]
		fig = go.Figure(go.Bar(x=x, y=agg.iloc[:,0], name=agg.columns.tolist()[0],marker_color='green'))
		for i in range(len(agg.columns)-1):
			fig.add_trace(go.Bar(x=x, y=agg.iloc[:,i+1], name=agg.columns.tolist()[i+1]))
		fig.update_layout(barmode='relative', title_text='{} vs {}'.format(main_question,second_question), \
	        	         xaxis={'title':second_question},\
	        	         yaxis={'title':None}, legend_title_text=main_question)
	
	else:
		fig=px.histogram(data, x=main_question)
	return fig

if __name__== '__main__':
    main()
    
