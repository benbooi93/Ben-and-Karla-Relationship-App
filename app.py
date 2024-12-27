from flask import Flask, render_template, request, jsonify
from simple_caller import SimpleCaller

app = Flask(__name__)
caller = SimpleCaller()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_call', methods=['POST'])
def make_call():
    data = request.json
    phone = data.get('phone')
    objective = data.get('objective')
    
    call_sid = caller.make_call(phone, objective)
    
    return jsonify({
        'success': bool(call_sid),
        'call_sid': call_sid,
        'message': f"Call initiated! SID: {call_sid}" if call_sid else "Failed to make call"
    })

@app.route('/check_status/<call_sid>')
def check_status(call_sid):
    status = caller.check_call_status(call_sid)
    return jsonify({'status': status})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌎 Web interface available at: http://localhost:3000")
    print("="*50 + "\n")
    app.run(port=3000) 