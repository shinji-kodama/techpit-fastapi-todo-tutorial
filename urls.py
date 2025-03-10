from controllers import *


# FastAPIのルーティング用関数
app.add_api_route('/', index)
app.add_api_route('/admin', admin)  # new
app.add_api_route('/register', register, methods=['GET', 'POST']) 
app.add_api_route('/todo/{username}/{year}/{month}/{day}', detail)
app.add_api_route('/done', done, methods=['POST'])  # new!
app.add_api_route('/add', add, methods=['POST'])  # new
app.add_api_route('/delete/{t_id}', delete)  # new


# JSONで返すAPI
app.add_api_route('/get', get)  # new
app.add_api_route('/add_task', insert, methods=['POST'])  # new