from flask import Flask, redirect, url_for, request, render_template,jsonify
import mysql.connector
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
def login():
   if request.method == 'POST':
      # return jsonify(request.form)
      print(request.form.to_dict(flat=False))
      return dborder(request.form.to_dict(flat=False))
   else:
      return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True, port=5656)

   