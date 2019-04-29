from flask import Flask, redirect, url_for, request, render_template,jsonify, flash
import mysql.connector
import os
app = Flask(__name__)

def showTable(name):
   mydb = mysql.connector.connect(
      host="localhost",
      user="administrator",
      passwd="Ujju@8860",
      database="ERP"
   )

   mycursor = mydb.cursor()

   try:
        query = "SELECT * from "+name+";"
        mycursor.execute(query)

        data = mycursor.fetchall()

        return data

   except Exception as e:
        return (str(e))

def addinventory(form) :
   mydb = mysql.connector.connect(
      host="localhost",
      user="administrator",
      passwd="Ujju@8860",
      database="ERP"
   )

   mycursor = mydb.cursor()

   rid = form['RawID'][0]
   name = form["ProductName"][0]
   cat = form['Category'][0]
   desc = form['Desc'][0]
   qnt = form['Quantity'][0]
   price = form['Price'][0]
   intime = form['InTime'][0]
   print(rid,name,cat,price,qnt,intime)

   master = 'insert into Master values('+rid+', "'+name+'", "'+desc+'");'
   transaction = 'insert into Transaction values('+rid+', "'+name+'", "'+cat+'", '+price+', "'+intime+'", "",'+qnt+');'
   print(master,transaction)
   try :
      mycursor.execute(master)
      print('First done')
      mycursor.execute(transaction)
      mydb.commit()
      return 'Values Inserted'
   except :
      return 'Please Check your details.'

def dborder(form) :
   mydb = mysql.connector.connect(
      host="localhost",
      user="administrator",
      passwd="Ujju@8860",
      database="ERP"
   )

   mycursor = mydb.cursor()

   try :
      rid = form['RawID'][0]
      name = form["ProducName"][0]
      cat = form['Category'][0]
      qnt = int(form['Quantity'][0])
      print(rid,name,cat,qnt)
      mycursor.execute("select Quantity from Transaction where Name='"+name+"' AND Raw_ID="+str(rid)+";")
   except :
      return 'Entry Not Found. Please Check Your Details'
   res = mycursor.fetchall()
   if len(res):
      for x in res:
         val = x[0]
         print(val)
      if val<qnt:
         return 'Insuffucient Quantity, Order sent to Accounts department to approve'
      else :
         mycursor.execute('UPDATE Transaction SET Quantity='+str(val-qnt)+' WHERE Raw_ID='+str(rid)+';')
         mydb.commit()
         return 'Order placed. Please collect your order from Inventory department.'
   else :
      return 'Entry Not Found. Please Check Your Details'


@app.route('/order',methods = ['POST', 'GET'])
def order():
   if request.method == 'POST':
      error = None
      # return jsonify(request.form)
      print(request.form.to_dict(flat=False))
      error = dborder(request.form.to_dict(flat=False))
      data = showTable('Master')
      return render_template('index.html',error=error, data=data)
   else:
      data = showTable('Master')
      return render_template('index.html',data=data)

@app.route('/inventory',methods = ['POST', 'GET'])
def inventory():
   if request.method == 'POST':
      error = None
      # return jsonify(request.form)
      print(request.form.to_dict(flat=False))
      error = addinventory(request.form.to_dict(flat=False))
      data = showTable('Transaction')
      return render_template('inventory.html',error=error,data=data)
   else:
      data = showTable('Transaction')
      return render_template('inventory.html',data=data)

@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      error = None
      # return jsonify(request.form)
      res = request.form.to_dict(flat=False)
      if res['username'][0] == 'InventoryModule' and res['password'][0] == 'password':
         return redirect('/inventory')
      else:
         error = 'Invalid username or password. Please try again!'
      return render_template('login.html',error=error)
   else:
      return render_template('login.html')

if __name__ == '__main__':
   app.secret_key = os.urandom(24)
   app.run(debug = True, port=5656)

   