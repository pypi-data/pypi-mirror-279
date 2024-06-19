import numpy as np
import os
import cv2
import skimage
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
from collections import Counter

class ImageExplorer:
    """
    A class for exploring images in a directory, providing metadata, and visualizing data.

    Attributes:
    - root_dir (str): The root directory containing image files.
    - class_names (dict): Mapping of class indices to class names.
    - paths (list): List of paths to all image files.
    - labels (list): List of labels corresponding to each image.
    - heights (list): List of heights for each image.
    - widths (list): List of widths for each image.
    - extensions (list): List of file extensions present in the dataset.

    Methods:
    - show_sample_images(size=(5, 5), nrow=5, ncol=5, return_fig=False):
      Displays a grid of sample images with their labels.

    - show_class_distribution():
      Displays a bar chart showing the distribution of classes in the dataset.

    - show_summary():
      Displays a summary table with statistics about the dataset, including the number
      of images, distribution of file extensions, and image dimensions statistics.
    """

    _opencv_extensions = ['jpg', 'jpeg', 'jpe', 'png', 'bmp', 'ppm', 'pbm', 'pgm', 'sr', 'ras']
    _skimage_extensions = ['tif', 'tiff']
    _pil_extensions = ['webp']
    _supported_extensions = _opencv_extensions + _skimage_extensions + _pil_extensions

    def __init__(self, root_dir):
        """
        Initialize the ImageExplorer instance with the root directory.

        Args:
        - root_dir (str): The root directory containing image files.

        Raises:
        - ValueError: If the provided root directory does not exist.
        """
        if not os.path.exists(root_dir):
            raise ValueError(f"{root_dir} does not exist")
        self.root_dir = root_dir
        self.__class_names, self.__paths, self.__labels, self.__heights, self.__widths, self.__extensions = self.__load_metada()

    def __load_metada(self):
        """
        Load metadata such as class names, paths, labels, image dimensions, and extensions from the dataset directory.
        """
        cwd = os.getcwd()
        paths = []
        class_names = {}
        labels = []
        extensions = []
        widths = []
        heights = []

        for root, _, files in os.walk(self.root_dir):
            class_name = os.path.basename(root)
            for file in files:
                if file.endswith(tuple(self._supported_extensions)):
                    _, extension = os.path.splitext(file)
                    path = os.path.join(cwd, root.lstrip('./'), file)
                    extensions.append(extension.lstrip('.'))
                    paths.append(path)
                    if class_name not in class_names.values():
                        class_names[len(class_names)] = class_name
                    labels.append(len(class_names)-1)
                    if file.endswith(tuple(self._opencv_extensions)):
                        image = cv2.imread(path)
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    elif file.endswith(tuple(self._skimage_extensions)):
                        image = skimage.io.imread(path)
                    elif file.endswith(tuple(self._pil_extensions)):
                        image = Image.open(path)
                    heights.append(image.shape[0])
                    widths.append(image.shape[1])

        return class_names, paths, labels, widths, heights, extensions

    @property
    def paths(self):
        """
        Get the paths to all images in the dataset.

        Returns:
        - list: List of paths to image files.
        """
        return self.__paths

    @property
    def labels(self):
        """
        Get the labels corresponding to each image in the dataset.

        Returns:
        - list: List of integer labels.
        """
        return self.__labels

    @property
    def class_names(self):
        """
        Get the mapping of class indices to class names.

        Returns:
        - dict: Mapping of class indices to class names.
        """
        return self.__class_names

    @property
    def heights(self):
        """
        Get the heights of all images in the dataset.

        Returns:
        - list: List of integer heights.
        """
        return self.__heights

    @property
    def widths(self):
        """
        Get the widths of all images in the dataset.

        Returns:
        - list: List of integer widths.
        """
        return self.__widths

    @property
    def extensions(self):
        """
        Get the file extensions present in the dataset.

        Returns:
        - list: List of file extensions.
        """
        return self.__extensions

    def __get_image(self, idx):
        """
        Load and return the image at the specified index.

        Args:
        - idx (int): Index of the image to load.

        Returns:
        - ndarray or Image: Loaded image object (using OpenCV, scikit-image, or PIL).
        """
        path = self.paths[idx]
        if path.endswith(tuple(self._opencv_extensions)):
            image = cv2.imread(path)
        elif path.endswith(tuple(self._skimage_extensions)):
            image = skimage.io.imread(path)
        elif path.endswith(tuple(self._pil_extensions)):
            image = Image.open(path)
        return image

    @property
    def images(self):
        """
        Get all images in the dataset as a list.

        Returns:
        - list: List of image objects (ndarray or Image).
        """
        images = []
        for idx, _ in tqdm(enumerate(self.paths)):
            images.append(self.__get_image(idx))
        return images

    def show_sample_images(self, size=(5, 5), nrow=5, ncol=5, return_fig=False):
        """
        Display a grid of sample images with their labels.

        Args:
        - size (tuple): Figure size (width, height) in inches.
        - nrow (int): Number of rows in the grid.
        - ncol (int): Number of columns in the grid.
        - return_fig (bool): Whether to return the figure and axes objects.

        Returns:
        - (fig, axs) tuple: Figure and axes objects if return_fig=True.
        """
        total_images = nrow * ncol
        fig, axs = plt.subplots(nrow, ncol, figsize=size)
        for i in range(nrow):
            for j in range(ncol):
                img_num = random.randint(0, len(self.paths)-1)
                axs[i, j].imshow(self.__get_image(img_num))
                axs[i, j].axis('off')
                axs[i, j].set_title(f'{self.labels[img_num]} - {self.class_names[self.labels[img_num]]}')
        if return_fig:
            plt.close()
            return fig, axs
        else:
            plt.show()

    def show_class_distribution(self):
        """
        Display a bar chart showing the distribution of classes in the dataset.
        """
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.bar(self.class_names.values(), np.bincount(self.labels))
        plt.legend(self.class_names.values())
        plt.show()

    def show_summary(self):
        """
        Display a summary table with statistics about the dataset, including number of images,
        distribution of file extensions, and image dimension statistics.
        """
        extensions = dict(Counter(self.extensions))
        summary_data = {
            "Number of images": len(self.paths),
            "Extensions": str(extensions),
            "Height": "",
            "Minimum height": np.min(self.heights),
            "Maximum height": np.max(self.heights),
            "Mean height": np.mean(self.heights),
            "Median height": np.median(self.heights),
            "Width": "",
            "Minimum width": np.min(self.widths),
            "Maximum width": np.max(self.widths),
            "Mean width": np.mean(self.widths),
            "Median width": np.median(self.widths),
            "Aspect ratio": "",
            "Mean aspect ratio": np.mean(self.heights) / np.mean(self.widths),
            "Median aspect ratio": np.median(self.heights) / np.median(self.widths),
        }

        # Convert summary data to table format
        table_data = list(summary_data.items())
        rows = len(table_data)
        cols = 2

        # Create a new figure and axis for plotting
        fig, ax = plt.subplots()

        # Hide axes
        ax.axis('off')

        # Create the table
        table = ax.table(cellText=table_data,
                         loc='center',
                         colLabels=['Description', 'Value'],
                         cellLoc='left',
                         colColours=['lightgray', 'lightgray'],
                         colWidths=[0.4, 0.6])

        # Adjust table properties for better layout
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)  # Adjust height of rows for better visibility

        rows_to_color = [0, 3, 8, 13]  # Example: rows to color (0-indexed)
        for row in rows_to_color:
            for col in range(cols):
                table[(row, col)].set_facecolor('#CCCCCC')  # Set background color

        plt.show()
