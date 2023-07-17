import requests
import argparse

base_url = 'http://localhost:5000'

def add_files(files):
    url = f'{base_url}/add'
    response = requests.post(url, files=files)
    print(response.text)

def list_files():
    url = f'{base_url}/ls'
    response = requests.get(url)
    print(response.text)

def remove_file(filename):
    url = f'{base_url}/rm'
    data = {'filename': filename}
    response = requests.post(url, data=data)
    print(response.text)

def update_files(files):
    url = f'{base_url}/update'
    response = requests.post(url, files=files)
    print(response.text)

def word_count():
    try:
        url = f'{base_url}/wc'
        response = requests.get(url)
        print(f"Total word count: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

def frequent_words(limit, order):
    try:
        url = f'{base_url}/freq-words'
        data = {'limit': limit, 'order': order}
        response = requests.get(url, data=data)
        frequent_words = response.text.split()
        print("Frequent words:")
        for word in frequent_words:
            print(word)

    except Exception as e:
        print(f"Error: {str(e)}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='File Store through commands passed on CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('files', nargs='+', help='Files to add to the store')

    subparsers.add_parser('ls')

    rm_parser = subparsers.add_parser('rm')
    rm_parser.add_argument('filename', help='File to remove from the store')

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('files', nargs='+', help='Files to update in the store')

    subparsers.add_parser('wc')

    freq_words_parser = subparsers.add_parser('freq-words')
    freq_words_parser.add_argument('--limit', '-n', type=int, default=10, help='Number of frequent words to retrieve')
    freq_words_parser.add_argument('--order', choices=['asc', 'dsc'], default='dsc', help='Order of frequent words (asc or dsc)')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.command == 'add':
        all_Files = [('files', open(file, 'r')) for file in args.files] #files are list of tuples : files, file object where file object is opened file in binary format
        add_files(all_Files)
    elif args.command == 'ls':
        list_files()
    elif args.command == 'rm':
        remove_file(args.filename)
    elif args.command == 'update':
        all_Files = [('files', open(file, 'r')) for file in args.files]
        update_files(all_Files)
    elif args.command == 'wc':
        word_count()
    elif args.command == 'freq-words':
        frequent_words(args.limit, args.order)
