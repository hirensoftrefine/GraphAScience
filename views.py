## This file contains Routes
## API developemtn goes here
from flaskapp import app
from flask import Flask, request, jsonify, Response
import flask
from flask import render_template, make_response
from datetime import datetime
import json, os
import pyodbc,csv
import itertools


# Default Route
@app.route('/')
def index():
	return render_template('index.html')

# API for upload database 
# API will return Case Combos, File Location and ETAB Version
@app.route('/regions',methods=['POST','GET'])
def none():
        if request.method == 'POST':
               #print('Hello')
        # check if the post request has the file part

                db_file = request.files['file1']
                db_file.save(os.path.join(app.config['UPLOAD_FOLDER'], db_file.filename)) 
                file_path = app.config['UPLOAD_FOLDER']+'\\'+db_file.filename
                file_path = os.path.abspath(file_path)
                conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
                cursor = conn.cursor()
                cursor.execute('select DISTINCT [Output Case] from [Story Drifts]')

              
                data = []
                rows = cursor.fetchall()
                for row in rows:
                        data.append([x for x in row])

        query = cursor.execute('select Version, CurrUnits as Units from [Program Control]')
        rows = cursor.fetchall()
        for row in rows:
                version = row.Version
                units = row.Units

        if version != '18.1.0' or units != 'kip, in, F':
                if version != '18.1.0':
                        #print('Verion is'+version)
                        return Response('Please confirm Version in ETABS Database match to 18.1.0', 201)
                if units != 'kip, in, F':
                        return Response('Please confirm units in ETABS Database match kip, in, F', 201)
                        

                
        # or units is not 'kip, in, F':
                

        data = {'file-location':file_path, 'combos': data,'version':version}

        # Returning File Location, Case Combos and ETAB Drift Version
        return jsonify(data)


## API for generating X Chart
@app.route('/graph',methods=['POST','GET'])
def getGraph(chartID = 'chart_ID_X', chart_type = 'line', chart_height = 930):


        cutoff = float(request.form.getlist('cutoff')[0])
        drift_status = request.form.getlist('drift-status')[0]
        db_file = request.files['file1']
        file_path = app.config['UPLOAD_FOLDER']+'\\'+db_file.filename

        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
        cursor = conn.cursor()

        max_drift = 0
        x_max_drift = 0
        
        a = request.form.getlist('cdemos[]')
        b = [i.split(',') for i in a]
        flatList = [ item for elem in b for item in elem]
      
        data = []
        series = []
        load_cases_drift = []
        for combo in flatList:
                cursor.execute("select [Output Case] as Case,Direction,Drift,Z from [Story Drifts] where [Output Case]='%s' and Direction='X'" % combo)
                
                rows = cursor.fetchall()
                data = []
               
                for row in rows:

                        load_cases_drift.append(row.Drift)
                        graph_points = [float("{:.4f}".format(row.Drift)),row.Z/12]
                        data.append(graph_points)
        
                series.append({'name': combo, 'data': data})
                
        conn.close()

        #print(load_cases_drift)
        if len(load_cases_drift) != 0:
                max_drift = max(load_cases_drift)
                x_max_drift = float("{:.5f}".format(max_drift))
                if max_drift < 0.0025:
                        max_drift = 0.0025
                if cutoff > max_drift:
                        cutoff = max_drift

                

             
        ## Data for generating Chart with HighChart.JS Library

        #chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "events": {"click": "function() { console.log('XXX Graph Clicked'); this.update({ chart: { width: 800  } }) };"}}
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
        title = {"text": 'Drift-X'}
        pageType = 'graph'
        xAxis = {"title": {"text": 'INTERSTORY DRIFTS (IN. /IN.)'}}
        yAxis = {"title": {"text": 'HEIGHT  (FEET)'}, "lineWidth": '1', "lineColor": '#FF0000'}
        
        return render_template('graph.html', chartID=chartID, chart=chart, marDrift=max_drift, maxDriftVal=x_max_drift, direction='X', pageType=pageType, series=series, title=title, xAxis=xAxis, yAxis=yAxis, cutoff = cutoff, type="drift")



## API for generating Y Chart
@app.route('/ygraph',methods=['POST','GET'])
def getGraphY(chartID = 'chart_ID_Y', chart_type = 'line', chart_height = 930):

        db_file = request.files['file1']
        cutoff = float(request.form.getlist('cutoff')[0])
        file_path = app.config['UPLOAD_FOLDER']+'\\'+db_file.filename
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
        cursor = conn.cursor()

        max_drift = 0
        y_max_drift = 0
        
        a = request.form.getlist('cdemos[]')
        b = [i.split(',') for i in a]
        flatList = [ item for elem in b for item in elem]

        data = []
        series = []
        load_cases_drift = []
        for combo in flatList:
                cursor.execute("select [Output Case] as Case,Direction,Drift,Z from [Story Drifts] where [Output Case]='%s' and Direction='Y'" % combo)
                rows = cursor.fetchall()
                data = []
                for row in rows:

                        load_cases_drift.append(row.Drift)
                        graph_points = [float("{:.4f}".format(row.Drift)),row.Z/12]
                        data.append(graph_points)
                        
                series.append({'name': combo, 'data': data})

        conn.close()

        #print(load_cases_drift)
        if len(load_cases_drift) != 0:
                max_drift = max(load_cases_drift)

                if max_drift < 0.0025:
                        max_drift = 0.0025
                if cutoff > max_drift:
                        cutoff = max_drift

                y_max_drift = float("{:.5f}".format(max(load_cases_drift)))

 
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "events": {"click": "function() { console.log('XXX Graph Clicked'); this.update({ chart: { width: 800  } }) };"}}
        title = {"text": 'Drift-Y'}
        pageType = 'graph'
        xAxis = {"title": {"text": 'INTERSTORY DRIFT (IN. /IN.)'}}
        yAxis = {"title": {"text": 'HEIGHT (FEET)'}, "lineWidth": "1", "lineColor": '#FF0000'}
        
        return render_template('graph.html', chartID=chartID, chart=chart,marDrift=max_drift,maxDriftVal=y_max_drift, direction='Y', pageType=pageType, series=series, title=title, xAxis=xAxis, yAxis=yAxis, cutoff = cutoff, type="drift")

@app.route('/inversegraph',methods=['POST','GET'])
def getInverseGraph(chartID = 'chart_ID_X', chart_type = 'line', chart_height = 930):


        cutoff = float(request.form.getlist('cutoff')[0])
        drift_status = request.form.getlist('drift-status')[0]
        db_file = request.files['file1']
        file_path = app.config['UPLOAD_FOLDER']+'\\'+db_file.filename
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
        cursor = conn.cursor()

        max_drift = 0
        x_max_drift = 0
        
        a = request.form.getlist('cdemos[]')
        b = [i.split(',') for i in a]
        flatList = [ item for elem in b for item in elem]
      
        data = []
        series = []
        load_cases_drift = []
        for combo in flatList:

                cursor.execute("select [Output Case] as Case,Direction,Drift,Z from [Story Drifts] where [Output Case]='%s' and Direction='X'" % combo)
                rows = cursor.fetchall()
                data = []
                for row in rows:
                        load_cases_drift.append(int(1/row.Drift))
                        graph_points = [int(1/row.Drift),row.Z/12]
                        data.append(graph_points)
                        
                series.append({'name': combo, 'data': data})
        
         
        conn.close()


        if len(load_cases_drift) != 0:
                x_max_drift = min(load_cases_drift)
                max_drift = x_max_drift

        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "events": {"click": "function() { console.log('XXX Graph Clicked'); this.update({ chart: { width: 800  } }) };"}}
        title = {"text": 'Drift-X'}
        pageType = 'graph'
        xAxis = {"title": {"text": 'INTERSTORY DRIFTS (IN. /IN.)'}}
        yAxis = {"title": {"text": 'HEIGHT  (FEET)'}, "lineWidth": "1", "lineColor": '#FF0000'}
        
        return render_template('graph.html', chartID=chartID, chart=chart, marDrift=max_drift, maxDriftVal=x_max_drift, direction='X', pageType=pageType, series=series, title=title, xAxis=xAxis, yAxis=yAxis, cutoff = cutoff,type="inverse-drift")



## API for generating Y Chart
@app.route('/yinversegraph',methods=['POST','GET'])
def getInverseGraphY(chartID = 'chart_ID_Y', chart_type = 'line', chart_height = 930):


        db_file = request.files['file1']
        cutoff = float(request.form.getlist('cutoff')[0])
        drift_status = request.form.getlist('drift-status')[0]

        file_path = app.config['UPLOAD_FOLDER']+'\\'+db_file.filename
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
        cursor = conn.cursor()

        max_drift = 0
        y_max_drift = 0
        
        a = request.form.getlist('cdemos[]')
        b = [i.split(',') for i in a]
        flatList = [ item for elem in b for item in elem]

        data = []
        series = []
        load_cases_drift = []
        for combo in flatList:
                cursor.execute("select [Output Case] as Case,Direction,Drift,Z from [Story Drifts] where [Output Case]='%s' and Direction='Y'" % combo)
                rows = cursor.fetchall()
                data = []
                for row in rows:

                        load_cases_drift.append(int(1/row.Drift))
                        graph_points = [int(1/row.Drift),row.Z/12]
                        data.append(graph_points)
                        
                series.append({'name': combo, 'data': data})

               
        conn.close()

        if len(load_cases_drift) != 0:
                y_max_drift = min(load_cases_drift)
                max_drift = y_max_drift

        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "events": {"click": "function() { console.log('XXX Graph Clicked'); this.update({ chart: { width: 800  } }) };"}}
        title = {"text": 'Drift-Y'}
        pageType = 'graph'
        xAxis = {"title": {"text": 'INTERSTORY DRIFT (IN. /IN.)'}}
        yAxis = {"title": {"text": 'HEIGHT (FEET)'}, "lineWidth": "1", "lineColor": '#FF0000'}
        
        return render_template('graph.html', chartID=chartID, chart=chart,marDrift=max_drift, maxDriftVal=y_max_drift, direction='Y', pageType=pageType, series=series, title=title, xAxis=xAxis, yAxis=yAxis, cutoff = cutoff, type="inverse-drift")