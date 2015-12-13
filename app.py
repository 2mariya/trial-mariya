from flask import Flask, render_template, request, redirect
import requests
import pandas as pnds
from bokeh.plotting import figure
from bokeh.embed import components
import datetime

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/show_graph', methods=['POST'])
def show_graph():
    try:
        app.vars['ticker_symbol'] = request.form['ticker_symbol']
        app.vars['date_range'] = request.form['date_range']
    
        ticker=app.vars['ticker_symbol']
        r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'.json?api_key=EFJs6hiBgqzxkVEzmhN2')
        fp=r.json()
        
        column_names_list=fp['dataset']['column_names']
        data_list=fp['dataset']['data']
        df=pnds.DataFrame(data_list, columns=column_names_list) 
        df['Date']=pnds.to_datetime(df['Date'])
        df=df.set_index('Date')
        df=df.sort_index()
        
        if app.vars['date_range']!='all':
            from_date= datetime.date.today() + datetime.timedelta(-30)  
            to_date=datetime.date.today()
            start = df.index.searchsorted(from_date)
            end=df.index.searchsorted(to_date)
            df=df[start:end]        
     
    
        p = figure(title="Closing rate",
            x_axis_label="Date", y_axis_label="Rate", x_axis_type="datetime")
        p.line(df.index.values,df['Close'],color='blue',legend='Closing Price')
        script, div = components(p)
    
        return render_template('plot.html',script=script, div=div)
        #return "getting there"
    except:
        return render_template('error.html')

if __name__ == '__main__':
  app.run(port=33507)
