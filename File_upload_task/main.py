from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import string

app = Flask(__name__)

UPLOAD = "upload"
DOWNLOAD = "download"
IMG = ['png', 'jpg', 'gif', 'svg']

def change_name_to_png(fname):
    parts = fname.split('.')
    parts[-1] = 'png'
    return '.'.join(parts)


def download_link(filename):
    pngfilename = change_name_to_png(filename)
    return "Ваше фото: <a href='{0}'>{1}</a> Уменьшенное: <a href='{2}'>{3}</a>".format(url_for('uploaded_file', filename=filename), filename,
                                                                                        url_for('uploaded_file', filename='small'+pngfilename),
                                                                                            pngfilename)

def convert_image(filename):
    pngfilename = change_name_to_png(filename)
    os.system("convert '{0}' -resize 450x450! '{1}/small{2}'".format(filename, DOWNLOAD, pngfilename.split('/')[-1]))
    os.system("mv '{0}' '{1}/{2}'".format(filename, DOWNLOAD, filename.split('/')[-1]))

def process_folder(folder):
    imgs = []
    for f in os.listdir(folder):
        if f.split('.')[-1] in IMG:
            convert_image(folder + '/' + f)
            imgs.append(download_link(f))
    if imgs:
        return '<br>'.join(imgs)
    else:
        return 'EMPTY'

def process_zip(filename):
    folder = "".join(filename.split('.')[:-1])
    os.system("unzip -o {0}/{1} -d {0}/{2}".format(UPLOAD, filename, folder))
    return process_folder(UPLOAD + '/' + folder)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file:
            filename = file.filename
            if not set(filename).issubset(set(string.ascii_letters + string.digits + '._-' )):
                return 'ATTACK DETECTED'
            file.save(os.path.join(UPLOAD, filename))
            file_type = filename.split('.')[-1]
            if file_type == 'zip':
                return process_zip(filename)
            if file_type in IMG:
                print(filename)
                convert_image(UPLOAD + '/' + filename)
                return download_link(filename)
            return "BAD FORMAT"
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
       return send_from_directory(DOWNLOAD, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
