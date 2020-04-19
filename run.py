from blog import app, manager
if __name__=='__main__':
    app.secret_key='secret'
    #manager.run()
    app.run(debug=True)