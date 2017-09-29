import os
from array import array
import OpenImageIO as oiio
import PyOpenColorIO as ocio
from .UpdateImageMetadata import UpdateImageMetadata
from ...Template import Template
from ..Task import Task

class ColorTransformation(Task):
    """
    Applies a color transformation to an image using open color io and open image io.

    Required Options: "sourceColorSpace" and "targetColorSpace".
    """

    def _perform(self):
        """
        Perform the task.
        """
        sourceColorSpace = self.option('sourceColorSpace')
        targetColorSpace = self.option('targetColorSpace')
        metadata = {
            'sourceColorSpace': sourceColorSpace,
            'targetColorSpace': targetColorSpace
        }

        for pathCrawler in self.pathCrawlers():
            yield pathCrawler

            # open color configuration
            config = ocio.GetCurrentConfig()

            # source image
            sourceImage = oiio.ImageInput.open(pathCrawler.var('filePath'))
            spec = sourceImage.spec()
            spec.set_format(oiio.FLOAT)

            pixels = sourceImage.read_image()
            sourceImage.close()

            transformedPixels = config.getProcessor(
                sourceColorSpace,
                targetColorSpace
            ).applyRGB(pixels)

            targetFilePath = self.filePath(pathCrawler)

            # trying to create the directory automatically in case it does not exist
            try:
                os.makedirs(os.path.dirname(targetFilePath))
            except OSError:
                pass

            targetImage = oiio.ImageOutput.create(targetFilePath)

            # umedia metadata information
            UpdateImageMetadata.updateUmediaMetadata(
                spec,
                pathCrawler,
                metadata
            )

            success = targetImage.open(
                targetFilePath,
                spec,
                oiio.Create
            )

            # saving target image
            if success:
                writePixels = array('d')
                writePixels.fromlist(transformedPixels)
                targetImage.write_image(writePixels)
            else:
                raise Exception(oiio.geterror())


# registering task
Task.register(
    'colorTransformation',
    ColorTransformation
)