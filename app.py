from flask import Flask, request, render_template, jsonify
import subprocess
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_train_data', methods=['POST'])
def get_train_data():
    train_number = request.form.get('train_number')
    date = request.form.get('date')

    # Define the cURL command with user inputs
    curl_command = [
        "curl", "https://primes.indianrail.gov.in/newtemplatebasedmis/webapi/typeOne/call_charting",
        "-H", "Accept: application/json",
        "-H", "Accept-Language: en-US,en;q=0.9",
        "-H", "Access-Control-Allow-Origin: *",
        "-H", "Authorization: Basic RFlDQ05CNTVBOmE3ZDFlNGQxYzhjMjVmOGRmOGZlYzQ3MDU0OThmNGRiNTI4NTI4ZWQxZTM0NTFjYWQ4MThjM2NlZjEyNGM4ODc=",
        "-H", "Connection: keep-alive",
        "-H", "Content-Type: application/json",
        "-H", 'Cookie: TS018f73f5=01ea7166bccbee28704f766efc41635e3726ce5da147aaeb12ddd48e35436502d7436b03a7a468a13baf36da59ab2dbb0e83ff2aa536c9308a09adfbc3fab3d0e7221b4347; MYSESSIONID="bHv3wAPCk59YzUcUWlNlgqbRlpBFsRV8scNstx_i.master:ap01-server3"',
        "-H", "Origin: https://primes.indianrail.gov.in",
        "-H", "Referer: https://primes.indianrail.gov.in/PRIMES/psgnDetailsAfterCharting",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "--data-raw", json.dumps({
            "reportCode": "PSGNDETAILSAFTERCHARTING",
            "params": [train_number, date, "all"],
            "webUrl": "/newtemplatebasedmis/webapi/typeOne/call_charting",
            "userName": "DYCCNB55A"
        })
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response_data = json.loads(result.stdout)

        # Extract column names and records from the response
        columns = response_data["data"]["columnNames"]
        records = response_data["data"]["records"]

        # Create a DataFrame and render it as HTML
        df = pd.DataFrame(records, columns=columns)
        table_html = df.to_html(classes="table table-striped", index=False)

        return table_html
    except subprocess.CalledProcessError as e:
        return f"cURL Error: {e.stderr}", 500
    except KeyError:
        return "Unexpected response format.", 500
    except json.JSONDecodeError:
        return "Failed to parse JSON response.", 500

if __name__ == '__main__':
    app.run(debug=True)
