# HyperCornAPI

HyperCornAPI, developed by Hypercorn, is a foundational API designed to seamlessly integrate with HyperApp, an advanced application tailored for crop classification. This documentation provides comprehensive guidance on endpoints, methods, and best practices for developers seeking to harness HyperCornAPI's powerful capabilities in image and spectrum processing. Visite us in github [HyperCorn](https://github.com/HyperCorn) or check out the FastAPI-based documentation at [Docs](https://hypercornapi-4oojabxrfa-rj.a.run.app/docs)

# Suport 
Do you need access keys for limited queries? Does your business or project depend on HyperCornAPI? Reach out to us at [hypercorncordoba@gmail.com](mailto:hypercorncordoba@gmail.com) for support and to discuss your needs.

## Index

1. [Instalation](#instalation)

## Instalation

To start using the API, you first need to install the hyperapp package, which is available on PyPI. You can easily install it using pip, Python's package manager. Open your terminal and run the following command:


```bash
$ pip install hypercorn_api
```

## Uses
Before using the functionalities, initialize HyperCornAPI with your credentials. If you don't have them,  [contact us for support](#suport).However, in this version there is no authentication.
```python
from hypercorn_api import HyperCornAPI

# Initialize the API with your credentials
hypercorn_api = HyperCornAPI()
```
In a update we will put authentication.

### Images 
This tag is for operations to retrieve images from different sources.

#### Satellite Images - NDVI
To retrieve satellite images with NDVI (Normalized Difference Vegetation Index) using HyperCornAPI, use the following function call:


```python
images_satelite_ndvi = hypercorn_api.images_satelite_ndvi( (46.16, -16.15),(46.51, -15.58),"2024-06-06" )
```


The `images_satelite_ndvi` function takes the following parameters:

1. **Min Coords (tuple)**: Specifies the minimum coordinates for the bottom-left corner of the area of interest.
   - In the Example: `(46.16, -16.15)`

2. **Max Coords (tuple)**: Specifies the maximum coordinates for the top-right corner of the area of interest.
   - In the Example: `(46.51, -15.58)`

3. **Date (string)**: Specifies the date for which you want to retrieve the satellite image.
   - In the Example: `"2024-06-06"`

The function returns a dictionary with the following structure:

- **image_list (list)**: A list containing the retrieved satellite images. The values of the pixels are in the ranges (0,1)

### Segmentation
This tag is for operations to retrieve segmented images

#### Kmeans
Operation for segmenting images using the k-means algorithm in HyperCornAPI. To retrieve the segmented images, use the following function call:
```python
segmented_image = hypercorn_api.segmentation_kmeans("path/to/your/image.jpg",False,"avg")
```

The `segmentation_kmeans` function in HyperCornAPI takes the following parameters:

1. **image_path (string)**: Specifies the file path to the image that you want to segment.
   - In the Example: `"path/to/your/image.jpg"`

2. **is_gray (bool)**: Specifies whether the image is grayscale or not. Is gray if the extension is .tif, otherwise is non gray
   - In the Example: `True`

3. **kind (string)**: Specifies the method of merging pixels for k-means segmentation. The two options are "avg" (average color) and "overlay" (overlay all pixels).
   - In the Example: `"avg"`

The function returns a dictionary with the following structure:

- **segmented_image (list)**: A list representing the segmented image, where each element corresponds to a segment.


#### Binarize
Operation for segmenting images using a simple cuttof in HyperCornAPI. To retrieve the segmented images, use the following function call:
```python
segmented_image = hypercorn_api.segmentation_binarize("path/to/your/tif_image",0.5)
```

The `segmentation_binarize` function in HyperCornAPI takes the following parameters:

1. **image_path (string)**: Specifies the file path to the image that you want to segment. The file must be in .tif format and their pixels must be in the ranges (0,1).
   - In the Example: `"path/to/your/tif_image"`

3. **sensibility (float)**: Specifies the cutoff value for binarization. Pixels with values less than the sensibility are set to 0, and pixels with values greater than or equal to the sensibility are set to 1, resulting in a binary (black and white) image.
   - In the Example: `0.5`

The function returns a dictionary with the following structure:

- **segmented_image (list)**: A list representing the segmented binary image, where each element is either 0 or 1 based on the specified sensibility cutoff.



