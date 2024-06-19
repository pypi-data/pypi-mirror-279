# geeft
Google Earth Engine Fourier Transform 

# Installation
```bash
# From source
pip install git+https://github.com/Wetlands-NWRC/geeft.git
```


# Usasge
```python
import geeft

dataset = (
    ee.ImageCollection()
    .filterBounds(aoi)
    .filterDate('2013', '2018')
    .map(cloud_mask)
    .map(add_ndvi)
)

fourier_transform = geeft.compute(dataset, 'NDVI', 4)
```