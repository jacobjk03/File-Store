from flask import Flask, request
import os
import shutil

app = Flask(__name__)
store_path = os.path.join(os.getcwd(), 'store')

@app.route('/add', methods=['POST'])
def add_file():
    try:
        for file in request.files.getlist('files'):
            filename = file.filename
            filepath = os.path.join(store_path, filename)
            flag = 0
            if os.path.exists(filepath):
                return f"File '{filename}' already exists in the store"
            
            # Content is already on the server in another file
            for savedFile in os.listdir(store_path):
                savedFilePath = os.path.join(store_path, savedFile)
                with open(savedFilePath, 'r') as fp:
                    file_content = file.read().decode('utf-8')
                    fp_content = fp.read()
                    if fp_content == file_content:
                        flag = 1
                        shutil.copyfile(savedFilePath, filepath)
                        break
                    
            # If file is not there or file content is not there in another file
            if (flag == 0):
                file.seek(0)
                file.save(filepath)
        return "Files added successfully"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/ls')
def list_files():
    try:
        files = os.listdir(store_path)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/rm', methods=['POST'])
def remove_file():
    try:
        filename = request.form.get('filename')
        filepath = os.path.join(store_path, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return f"File '{filename}' removed successfully"
        return f"Error: File '{filename}' not found in the store"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/update', methods=['POST'])
def update_file():
    try:
        for file in request.files.getlist('files'):
            filename = file.filename
            filepath = os.path.join(store_path, filename)
            file.save(filepath)
        return "File(s) updated successfully"
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/wc')
def word_count():
    try:
        word_count = 0

        for filename in os.listdir(store_path):
            file_path = os.path.join(store_path, filename)
            with open(file_path, 'r') as file:
                word_count += len(file.read().split())
                file.close()

        response = {'word_count': word_count}
        return str(response['word_count'])
    except Exception as e:
        return {'error': str(e)}

@app.route('/freq-words')
def frequent_words():
    try:
        limit = int(request.form.get('limit', 10))
        order = request.form.get('order', 'dsc')
        if order not in ['asc', 'dsc']:
            return {'error': 'Invalid order parameter. Must be "asc" or "dsc".'}

        word_counts = {}
        
        for filename in os.listdir(store_path):
            file_path = os.path.join(store_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    words = file.read().split()
                    for word in words:
                        if word in word_counts:
                            word_counts[word] += 1
                        else:
                            word_counts[word] = 1
        
        frequent_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=(order == 'dsc'))[:limit]
        frequent_words = [word for word, _ in frequent_words]
        
        response = ' '.join(frequent_words)
        return response
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    app.run(debug=True)
