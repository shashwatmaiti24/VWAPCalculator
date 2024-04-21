import gzip
import shutil
from urllib.request import urlretrieve
from urllib.parse import urljoin
from pathlib import Path

itch_url_prefix = 'https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/'
download_file_name = '01302019.NASDAQ_ITCH50.gz'
data_path = Path('data')
url = urljoin(itch_url_prefix, download_file_name)

filename = data_path / url.split('/')[-1]
if not data_path.exists():
    print('Creating directory')
    data_path.mkdir()
else:
    print('Directory already exists')
if not filename.exists():
    print('Downloading...', url)
    urlretrieve(url, filename)
else:
    print('File already exists')
unzipped = data_path / (filename.stem + '.bin')
if not unzipped.exists():
    print('Unzipping to', unzipped)
    with gzip.open(str(filename), 'rb') as f_in:
        with open(unzipped, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print('Unzipped')
else:
    print('File already unziped')
