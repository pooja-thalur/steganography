from flask import Flask, render_template, request
import os
from pathlib import Path
import sys
import jinja2

root_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
app = Flask(__name__.split('.')[0], root_path=root_path)
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(str(root_path / 'templates')))
dir_name = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, template_folder='')

# Dummy function for image encryption
def encrypt_image(image_path, message):
    # Replace this with your image encryption logic
    encrypted_image = f"Image encrypted with message: {message}"
    return encrypted_image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files:
            uploaded_image = request.files['image']
            if uploaded_image.filename != '':
                # Save the uploaded image (if required)
                # For simplicity, let's assume it's saved as 'uploaded_image.jpg'
                uploaded_image.save('uploaded_image.jpg')
                return render_template('/template/encrypt.html', image_path='uploaded_image.jpg')
        elif 'message' in request.form:
            message = request.form['message']
            image_path = request.form['image_path']
            encrypted_image = encrypt_image(image_path, message)
            return render_template('/template/result.html', encrypted_image=encrypted_image)
    print(os.getcwd())
    ##C:\Users\Pooja\projects\steno\Steno\steno\views
    return render_template("C:\\Users\\Pooja\\projects\\steno\\Steno\\steno\\templates\\index.html")
    ##return render_template(dir_name+'\\index.html')

if __name__ == '__main__':
    app.run(debug=True)
