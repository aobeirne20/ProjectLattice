import ImageGen

generatedImage = ImageGen.ImageGen(size=(2000, 2000))
generatedImage.background(background_colors=(255, 255, 255, 255), background_img=None)
generatedImage.generate(generator_name="G2_TransitMapv2", gparams={})
generatedImage.render(renderer_name="R2_LondonMapModernv2", rparams={})
generatedImage.show()
generatedImage.invert()
generatedImage.grayscale()
generatedImage.goldscale()
generatedImage.brightline()

