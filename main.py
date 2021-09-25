import os
from dotenv import load_dotenv
load_dotenv()

from app import app


if __name__ == '__main__':
    try:
        cur_path = os.getcwd()
        if not os.path.isdir(f'{cur_path}/app/nltk_data'):
            import nltk
            nltk.set_proxy('http://192.168.1.128:8080')
            nltk.download('punkt', f'{cur_path}/app/nltk_data/')
            nltk.download('wordnet', f'{cur_path}/app/nltk_data/')
    except Exception as e:
        print(e)
    app.run()