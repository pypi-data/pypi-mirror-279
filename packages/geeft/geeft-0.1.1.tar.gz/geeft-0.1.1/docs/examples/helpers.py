import ee

AOI = ee.Geometry.Point([-121.059, 37.924])
DATES: tuple[str, str] = ("2013", "2018")


class LandSAT8SR(ee.ImageCollection):
    def __init__(self):
        super().__init__("LANDSAT/LC08/C02/T1_L2")

    def addNDVI(self):
        return self.map(
            lambda x: x.addBands(
                x.normalizedDifference(["SR_B5", "SR_B4"]).rename("NDVI").float()
            )
        )

    def applyCloudMask(self):
        return self.map(self.cloud_mask)

    @staticmethod
    def cloud_mask(image: ee.Image) -> ee.Image:
        qaMask = image.select("QA_PIXEL").bitwiseAnd(int("11111", 2)).eq(0)
        saturationMask = image.select("QA_RADSAT").eq(0)
        opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
        thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
        return (
            image.addBands(opticalBands, None, True)
            .addBands(thermalBands, None, True)
            .updateMask(qaMask)
            .updateMask(saturationMask)
        )
