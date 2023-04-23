import random
import time

from flask import Flask, redirect, send_from_directory, session

PORT = 3000

app = Flask(__name__,
            static_url_path="", static_folder="ref")
app.secret_key = 'top secret key'

@app.route('/event/glastonbury-2023-deposits/worthy-farm/2500000')
def send_page_content():
    if session.get('success'):
        session['success'] = session['success'] - 1
        return send_from_directory('ref', 'Buy tickets for Glastonbury 2023 - Glastonbury.html')
    r = random.random()
    print('r', r)
    if r < 0.80:
        print('waiting page')
        time.sleep(0.1)
        return send_from_directory('ref', 'Buy tickets for Glastonbury 2023 Waiting Page- Glastonbury.html')
    elif r < 0.95:
        print('chrome error page')
        time.sleep(random.random() * 5)
        return redirect('http://localhost:3001')
    else:
        print('successful page')
        session['success'] = 5
        time.sleep(0.1)
        return send_from_directory('ref', 'Buy tickets for Glastonbury 2023 - Glastonbury.html')


app.run(port=PORT, debug=True)
