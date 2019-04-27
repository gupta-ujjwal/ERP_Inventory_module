import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="administrator",
  passwd="Ujju@8860",
  database="ERP"
)

mycursor = mydb.cursor()

cat = "Raw"
name = "Woolen"
rid = 3
qnt = 2000

mycursor.execute("select Quantity from Transaction where Name='"+name+"' AND Raw_ID="+str(rid)+";")

res = mycursor.fetchall()
if len(res):
  for x in res:
    val = x[0]
    print(val)
  if val<qnt:
    print('Insuffucient Quantity, Order sent to Accounts department to approve')
  else :
    print('Order placed. Please collect your order from Inventory department.')
    mycursor.execute('UPDATE Transaction SET Quantity='+str(200)+' WHERE Raw_ID='+str(rid)+';')
    print(mycursor.rowcount)
    mydb.commit()
else :
  print('Entry Not Found')

