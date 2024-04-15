from flask import Flask, render_template, request

app = Flask(__name__)

# Variable to store the message
message = ""

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def home():
    global message

    if request.method == 'POST':
        # Get the message from the form
        new_message = request.form.get('message')
        if new_message:
            # Save the new message
            message = new_message
        else:
            # Show an error if the message is empty
            return render_template('index.html', error='Please enter a message.')

    elif request.method == 'DELETE':
        # Delete the message
        message = ""

    # Log the message to the console if a GET request is made
    if request.method == 'GET':
        print("Current message:", message)

    # Render the template with the message
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
