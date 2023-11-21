from flask import Flask,redirect,url_for,render_template,request
### WSGI Application
app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/products_list')
def products_list():
    return render_template('products_list.html')

@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/success')
def success():
    return render_template('contactSuccess.html')


@app.route('/fail/<int:score>')
def fail(score):
    return "Sorry. the score is "+ str(score)

### result checker
@app.route('/results/<int:marks>')
def results(marks):
    result=""
    if marks<50:
        result='fail'
    else:
        result='success'
    return redirect(url_for(result,score=marks))

@app.route('/submit',methods=['POST','GET'])
def submit():
    contactInfo = ''
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        message=request.form['message']
        contactInfo = 'First: ' + fname + '\nLast: ' + lname + '\nEmail: ' + email + '\nMessage: ' + message
        print(contactInfo)
    return redirect(url_for('success'))

if __name__=='__main__':
    app.run(debug=True)