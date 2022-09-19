#! encoding: utf-8

import os
import random
import argparse

class GeneratePairs:
    """
    Generate the pairs.txt file that is used for training face classifier when calling python `src/train_softmax.py`.
    Or others' python scripts that needs the file of pairs.txt.

    Doc Reference: http://vis-www.cs.umass.edu/lfw/README.txt
    """

    def __init__(self, data_dir, pairs_filepath, img_ext):
        """
        Parameter data_dir, is your data directory.
        Parameter pairs_filepath, where is the pairs.txt that belongs to.
        Parameter img_ext, is the image data extension for all of your image data.
        """
        self.data_dir = data_dir
        self.pairs_filepath = pairs_filepath
        self.img_ext = img_ext


    def generate(self):
        for i in range(10):
            self._generate_matches_pairs()
            self._generate_mismatches_pairs()


    def _generate_matches_pairs(self):
        """
        Generate all matches pairs
        """
        for name in os.listdir(self.data_dir):
            if name == ".DS_Store":
                continue
            if name == "property":
                continue
            if name.endswith(".idx"):
                continue
            if name.endswith(".lst"):
                continue
            if name.endswith(".rec"):
                continue
            if name.endswith('.txt'):
                continue
            if name.endswith('.bin'):
                continue

            a = []
            for file in os.listdir(os.path.join(self.data_dir, name)):
                if file == ".DS_Store" or file == "property" or file.endswith(".idx") or file.endswith(".lst") or file.endswith(".rec") or file.endswith(".txt"):
                    continue
                a.append(file)

            with open(self.pairs_filepath, "a") as f:
                for i in range(3):
                    try:
                        temp = random.choice(a).split("_") # This line may vary depending on how your images are named
                    except:
                        import ipdb; ipdb.set_trace()
                    w = temp[0]
                    try:
                        # l = random.choice(a).split("_")[2].lstrip("0").rstrip(self.img_ext)
                        # r = random.choice(a).split("_")[2].lstrip("0").rstrip(self.img_ext)

                        l = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)
                        r = random.choice(a).split("_")[-1].lstrip("0").rstrip(self.img_ext)

                        f.write(w + "\t" + l + "\t" + r + "\n")
                    except:
                        import ipdb; ipdb.set_trace()

    def get_dirs(self, cur_list):
        [f_n for f_n in cur_list if f_n != ".DS_Store"]
        dirs_list = []

        for item in cur_list:
            if not item.endswith('.DS_Store') and not item.endswith('property') and not item.endswith('.idx') and not item.endswith('.lst') and not item.endswith('.rec'):
                dirs_list.append(item)

        return dirs_list


    def get_images(self, name):
        path = os.path.join(self.data_dir, name)
        paths_list = os.listdir(path)

        another_list = []

        for item in paths_list:
            if item.endswith('.jpg') or item.endswith('.jpeg'):
                another_list.append(os.path.join(self.data_dir, item))

        return another_list

    def filter_some_shit(self):
        whole = os.listdir(self.data_dir)
        result = []

        for it in whole:
            if it == ".DS_Store":
                continue
            if it.endswith("property"):
                continue
            if it.endswith(".idx"):
                continue
            if it.endswith(".lst"):
                continue
            if it.endswith(".rec"):
                continue
            if it.endswith('.txt'):
                continue
            if it.endswith('.bin'):
                continue

            result.append(it)

        return result

    def _generate_mismatches_pairs(self):
        """
        Generate all mismatches pairs
        """
        for i, name in enumerate(os.listdir(self.data_dir)):
            if name == ".DS_Store":
                continue
            if name.endswith("property"):
                continue
            if name.endswith(".idx"):
                continue
            if name.endswith(".lst"):
                continue
            if name.endswith(".rec"):
                continue
            if name.endswith('.txt'):
                continue
            if name.endswith('.bin'):
                continue

            # remaining = os.listdir(self.data_dir)
            remaining = self.filter_some_shit()
            # remaining = [f_n for f_n in remaining if f_n != ".DS_Store"]
            remaining = self.get_dirs(remaining)
            # del remaining[i] # deletes the file from the list, so that it is not chosen again
            try:
                other_dir = random.choice(remaining)
            except:
                import ipdb; ipdb.set_trace()
            with open(self.pairs_filepath, "a") as f: 
                for i in range(3):
                    # file1 = random.choice(os.listdir(os.path.join(self.data_dir, name)))
                    file1 = random.choice(self.get_images(name))
                    # print('first', file1, name)
                    try:
                        # file2 = random.choice(os.listdir(os.path.join(self.data_dir, other_dir)))
                        file2 = random.choice(self.get_images(other_dir))
                    except:
                        import ipdb; ipdb.set_trace()
                    # print('second', file2, other_dir)
                    # number_1 = file1.split("_")[2].lstrip("0").rstrip(self.img_ext)
                    # number_2 = file2.split("_")[2].lstrip("0").rstrip(self.img_ext)
                    number_1 = file1.split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    number_2 = file2.split("_")[-1].lstrip("0").rstrip(self.img_ext)
                    
                    # print(number_1, number_2)
                    # f.write(name + "\t" + file1.split("_")[2].lstrip("0").rstrip(self.img_ext) + "\n")
                    f.write(name + "\t" + number_1 + "\t" + other_dir + "\t" + number_2 + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename images in the folder according to LFW format: Name_Surname_0001.jpg, Name_Surname_0002.jpg, etc.')
    parser.add_argument('--data-dir', default='', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    parser.add_argument('--txt-file', default='', help='Full path to the directory with peeople and their names, folder should denote the Name_Surname of the person')
    # reading the passed arguments
    args = parser.parse_args()
    data_dir = args.data_dir    # "out_data_crop/"
    pairs_filepath = args.txt_file         # "pairs_1.txt"
    
    img_ext = ".jpg"
    generatePairs = GeneratePairs(data_dir, pairs_filepath, img_ext)
    generatePairs.generate()

