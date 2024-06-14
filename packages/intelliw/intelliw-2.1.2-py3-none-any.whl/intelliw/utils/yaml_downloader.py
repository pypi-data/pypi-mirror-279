import sys
from intelliw.utils import iuap_request


def download(url, path):
    resp = iuap_request.get(url, timeout=10.0)
    resp.raise_for_status()
    with open(path, "wb") as fp:
        fp.write(resp.content)
    return


if __name__ == '__main__':
    file_url = sys.argv[1]
    save_path = sys.argv[2]
    download(file_url, save_path)
