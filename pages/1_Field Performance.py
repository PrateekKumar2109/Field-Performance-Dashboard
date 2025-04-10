import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
st.title("""Field Level  Performance Dashboard Page """)

st.header("Upload the  Production  data file here ")
st.markdown(" The file format is  standard Excel File")

data_uploader = st.file_uploader("upload file", type={"csv", "txt",'xlsx'})
if data_uploader is not None:
    try:
          data_df=pd.read_csv(data_uploader)
          data_df=data_df[['Platform','Well No','Date','Days','YEAR','Ql, blpd', 'Qo, bopd', 'Qw, bopd','RecOil, bbls   ',
                  'Qg (Assoc. Gas), m3/d','Moil, MMt', 'RecGas, m3']]  
    except:      
          data_df=pd.read_excel(data_uploader)

          data_df=data_df[['Platform','Well No','Date','Days','YEAR','Ql, blpd', 'Qo, bopd', 'Qw, bopd','RecOil, bbls   ',
                  'Qg (Assoc. Gas), m3/d','Moil, MMt', 'RecGas, m3']]
    
    
st.header("The  Production Data ")
st.sidebar.header("User input parameter")

years=st.sidebar.multiselect("Select the year",options=data_df['YEAR'].unique(),default=data_df['YEAR'].unique()[-5:-1])
years=np.array(years)
from datetime import datetime
#start_time = st.sidebar.slider(
#     "When do you want plot to start?",
#     value=datetime(2016, 1),
#     format="Mth-yy")
st.dataframe(data_df.head())
df=data_df.copy()


platform=df['Platform'].unique()
year_list=df['YEAR'].unique()
def dataframe_list_conv(data):
    df_platform=data.groupby(['Platform','Date']).sum()

    data_frame_list=[]
    for i in range(len(platform)):
        temp_df=df_platform.loc[platform[i]]
        data_frame_list.append(temp_df)
    return data_frame_list
def data_frame_for_plot(data_frame_list_d):
  
   field_data_plot=pd.concat( data_frame_list_d)
   field_data_plot=field_data_plot.groupby('Date').sum()
   field_data_plot=field_data_plot.reset_index()
   field_data_plot['W/C']=field_data_plot['Qw, bopd']*100/field_data_plot['Ql, blpd']
   field_data_plot['GOR']=field_data_plot['Qg (Assoc. Gas), m3/d']*6.28/field_data_plot['Qo, bopd']
   return field_data_plot

def field_perf_plot(field_data_plot):
   field_data_plot.dropna(inplace=True)
   field_data_plot['Date']=pd.to_datetime(field_data_plot['Date'])
   field_data_plot['Date']=field_data_plot['Date'].dt.strftime("%b-%y")
   fig=plt.figure(figsize=(20,14),dpi=90)
   ax = fig.add_subplot(211)
   ax.set_title('  Offshore  Field Performance plot ',fontsize=32)
   #ax.set_title('  Ratna & R-Series Field Performance plot ',fontsize=32)
   ax.plot(field_data_plot['Date'],field_data_plot['Ql, blpd'],color='brown',lw=3.5,label='Liquid Rate')
   ax.plot(field_data_plot['Date'],field_data_plot['Qo, bopd'],color='green',marker='o',lw=3.5,label='Oil Rate')
   ax.legend(loc=1,fontsize='x-large')
   ax.set_ylim([0, (int(field_data_plot['Ql, blpd'].values.max())+10000)])

 
   ax.set_xlabel("Date",fontsize=26,labelpad=10)
   ax.tick_params( axis='y',labelsize=16,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
   ax.set_xticklabels(field_data_plot['Date'],fontsize=14,rotation=45)
   
    #ax.tick_params(axis='both', which='both', length=0)
   ax.set_ylabel("Ql & Qo in bpd",color="green",fontsize=22)
   ax2=ax.twinx()
   ax2.plot(field_data_plot['Date'], field_data_plot['W/C'],color="blue",marker="o",lw=3.5,label='Water Cut')
   ax2.set_yticks(np.round(np.linspace(0, 100, 16), 0))
   ax2.set_ylim([0, 100])
   ax2.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.99, 0.85))
   ax2.tick_params( axis='y',labelsize=16,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
   ax2.set_ylabel("Water Cut ",color="blue",fontsize=26)
   ax.xaxis.grid(color='black', linestyle='--', linewidth=1.5)
   ax.yaxis.grid(color='black', linestyle='--', linewidth=1.5)

   ax3 = fig.add_subplot(212)
   #ax.set_title(platform[k]+'  Performance plot Allocation',fontsize=20)
   ax3.plot(field_data_plot['Date'],field_data_plot['Qg (Assoc. Gas), m3/d'],color='brown',lw=3.5,label='Gas Rate in m3/d')

   ax3.legend(loc=1,fontsize='x-large')
   ax3.set_ylim([0, (int(field_data_plot['Qg (Assoc. Gas), m3/d'].values.max())+20000)])
   #ax3.set_xlim(['Aug-18', 'Jun-22'])
   ax3.set_xlabel("Date",fontsize=26,labelpad=10)
   ax3.tick_params( axis='y',labelsize=16,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
   ax3.set_xticklabels(field_data_plot['Date'],fontsize=18,rotation=45)
   ax3.tick_params(axis='both', which='both', length=0)
   ax3.set_ylabel("Gas Rate in m3/d",color="brown",fontsize=26)
   ax4=ax3.twinx()
   ax4.plot(field_data_plot['Date'], field_data_plot['GOR'],color="orange",marker="o",lw=2.5,label='GOR (v/v)')
   ax4.set_ylim([0, (int(field_data_plot['GOR'].values.max())+200)])
   ax4.legend(loc='upper right', fontsize='x-large',bbox_to_anchor=(0.99, 0.9))
   ax4.tick_params( axis='y',labelsize=16,direction='out', length=6, width=2, colors='black',
               grid_color='r', grid_alpha=0.5)
   ax4.set_ylabel("GOR (v/v)",color="orange",fontsize=22)
   ax3.xaxis.grid(color='black', linestyle='--', linewidth=1.5)
   ax3.yaxis.grid(color='black', linestyle='--', linewidth=1.5)
   #plt.show()
   #plt.savefig("Performance plot Allocation. pdf", format="pdf", bbox_inches="tight")
   plt.setp(ax.get_yticklabels(), visible=False)
   plt.setp(ax3.get_yticklabels(), visible=False)
   #plt.setp(ax3.get_yticklabels(), visible=False)
   #plt.setp(ax2.get_yticklabels(), visible=False)
   return fig
data_frame_list1=dataframe_list_conv(df)
df_field_dta_plot=data_frame_for_plot(data_frame_list1)
st.dataframe(df_field_dta_plot)
fig1=field_perf_plot(df_field_dta_plot)
st.text('Field Performance Since Inception')
st.pyplot(fig1)

df_filtered=df[df['YEAR'].isin(years)]

data_frame_list2=dataframe_list_conv(df_filtered)
df_data_filtered=data_frame_for_plot(data_frame_list2)
st.dataframe(df_filtered)
fig2=field_perf_plot(df_data_filtered)
st.text('Field Performannce on Selected year by User')
st.pyplot(fig2,width=25)

# create two columns for charts
fig_col1, fig_col2 = st.columns(2)
with fig_col1:
            st.markdown("### Density Heatmap for flowing days")
            fig_1 = px.density_heatmap(
                data_frame=df_filtered, y='Days', x='Well No'
            )
            st.write(fig_1)
            
with fig_col2:
            st.markdown("### Field Production Histogram")
            fig_2 = px.histogram(data_frame=df_data_filtered, x="Qo, bopd")
            st.write(fig_2)

