from flask import Flask, redirect, url_for, request, render_template,jsonify, flash
import mysql.connector
import os
app = Flask(__name__)

def dborder(form) :
   mydb = mysql.connector.connect(
      host="localhost",
      user="administrator",
      passwd="Ujju@8860",
      database="ERP"
   )

   mycursor = mydb.cursor()

   rid = form['RawID'][0]
   name = form["ProducName"][0]
   cat = form['Category'][0]
   qnt = int(form['Quantity'][0])
   print(rid,name,cat,qnt)

   mycursor.execute("select Quantity from Transaction where Name='"+name+"' AND Raw_ID="+str(rid)+";")

   res = mycursor.fetchall()
   if len(res):
      for x in res:
         val = x[0]
         print(val)
      if val<qnt:
         return 'Insuffucient Quantity, Order sent to Accounts department to approve'
      else :
         mycursor.execute('UPDATE Transaction SET Quantity='+str(200)+' WHERE Raw_ID='+str(rid)+';')
         mydb.commit()
         print('Order placed. Please collect your order from Inventory department.')
   else :
      return 'Entry Not Found'


@app.route('/order',methods = ['POST', 'GET'])
def order():
   if request.method == 'POST':
      # return jsonify(request.form)
      print(request.form.to_dict(flat=False))
      return dborder(request.form.to_dict(flat=False))
   else:
      return render_template('index.html')

@app.route('/inventory',methods = ['POST', 'GET'])
def inventory():
   if request.method == 'POST':
      # return jsonify(request.form)
      print(request.form.to_dict(flat=False))
      return jsonify(request.form)
   else:
      return render_template('inventory.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      error = None
      # return jsonify(request.form)
      res = request.form.to_dict(flat=False)
      if res['username'][0] == 'InventoryModule' and res['password'][0] == 'password':
         flash('You were succesfully logged in.')
         return redirect('/inventory')
      else:
         error = 'Invalid username or password. Please try again!'
      return render_template('login.html',error=error)
   else:
      return render_template('login.html')

if __name__ == '__main__':
   app.secret_key = os.urandom(24)
   app.run(debug = True, port=5656)

   