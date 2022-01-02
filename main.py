import yadisk
import shutil
import sys
import os
import posixpath
from datetime import date
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    dir = sys.argv[1]
    arch_name = f'{os.path.basename(os.path.abspath(dir))}_{date.today().strftime("%d-%m-%Y")}'
    shutil.make_archive(arch_name, 'zip', dir)

    y = yadisk.YaDisk(os.getenv('APP_ID'), os.getenv('APP_SECRET'))
    url = y.get_code_url()

    print("Go to the following url: %s" % url)
    code = input("Enter the confirmation code: ")

    try:
        response = y.get_token(code)
    except yadisk.exceptions.BadRequestError:
        print("Bad code")
        sys.exit(1)

    y.token = response.access_token

    if y.check_token():
        print("Sucessfully received token!")
    else:
        print("Something went wrong. Not sure how though...")
        sys.exit(1)

    try:
        y.mkdir('python_backups')
    except yadisk.exceptions.PathExistsError:
        pass

    y.upload(f'{arch_name}.zip', posixpath.join('python_backups', f'{arch_name}.zip'), overwrite=True, timeout=(6000.0, 9000))