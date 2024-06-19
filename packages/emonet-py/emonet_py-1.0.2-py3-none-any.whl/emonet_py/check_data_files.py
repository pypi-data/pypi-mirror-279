"""
Check data files exist; if not, download.

.. codeauthor:: Laurent Mertens <laurent.mertens@kuleuven.be>
"""
import os.path
from gitlab import Gitlab


class CheckDataFiles:
    PROJECT_ID = '39472331'  # GitLab EmoNet project ID
    URL_START = f'https://gitlab.com/api/v4/projects/{PROJECT_ID}/repository/files/data%2F'
    URL_END = '/raw?ref=master'

    @classmethod
    def check_and_download(cls):
        # Check data folder exists; if not, create
        abs_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(abs_dir, '../data')
        b_data_folder_exists = os.path.isdir(data_dir)

        if not b_data_folder_exists:
            os.makedirs(data_dir)

        # Check expected files exist; if not, download
        expected_files = [
            'conv1.bias.txt.bz2',
            'conv1.weights.txt.bz2',
            'conv2.bias.txt.bz2',
            'conv2.weights.txt.bz2',
            'conv3.bias.txt.bz2',
            'conv3.weights.txt.bz2',
            'conv4.bias.txt.bz2',
            'conv4.weights.txt.bz2',
            'conv5.bias.txt.bz2',
            'conv5.weights.txt.bz2',
            'demo_big.jpg',
            'demo_small.jpg',
            'emonet.pth',
            'fc1.bias.txt.bz2',
            'fc1.weights.txt.bz2',
            'fc2.bias.txt.bz2',
            'fc2.weights.txt.bz2',
            'fc3.bias.txt.bz2',
            'fc3.weights.txt.bz2',
            'img_mean.txt'
        ]

        gl = None
        for file in expected_files:
            # Check file exists and download if not
            path_file = os.path.join(data_dir, file)
            if not (os.path.isfile(path_file)):
                print(f"Attempting to download file {file} from GitLab...", end='', flush=True)
                # Instantiate Gitlab API, if not yet done; this way we don't create an instance, unless one is needed
                if gl is None:
                    gl = Gitlab()
                # Download file
                f = gl.http_get(path=f'{cls.URL_START}{file}{cls.URL_END}')
                with open(path_file, 'wb') as fout:
                    fout.write(f.content)

                print(f" done!\n\tFile saved to: {path_file}")


if __name__ == '__main__':
    CheckDataFiles.check_and_download()
