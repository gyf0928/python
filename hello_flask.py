from flask import Flask,render_template,request,escape,session
from vsearch import search4letters
from check_logged_in import check_logged_in
app=Flask(__name__)
def log_request(req: 'flask_request',res: str) ->None:
    with open('vsearch.log','a') as log:
        print(req.form,req.remote_addr,req.user_agent,res,file=log,sep='|')

@app.route('/search4',methods=['POST'])
def do_search() ->'html':
    phrase=request.form['phrase']
    letters=request.form['letters']
    results=str(search4letters(phrase,letters))
    title="Here are your results:"
    log_request(request,results)
    return render_template('results.html',the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)
@app.route('/')
@app.route('/entry')
def entry_page() ->'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')
@app.route('/login')
def do_login() ->str:
    session['logged_in']=True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() ->str:
    session.pop('logged_in')
    return 'You are now logged out.'

@app.route('/viewlog')
@check_logged_in
def view_the_log() ->'html':
    contents=[]
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles=('Form Data','Remote_addr','User_agent','Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)
app.secret_key='YouWillNeverGuessMySecretKey'

if __name__=='__main__':
    app.run(debug=True)

