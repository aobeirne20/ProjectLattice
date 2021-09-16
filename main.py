import ImageGen

generatedImage = ImageGen.ImageGen(size=(2000, 2000))
generatedImage.background(background_colors=(255, 255, 255, 255), background_img=None)
generatedImage.generate(generator_name="G1_TransitMap", gparams={})
generatedImage.render(renderer_name="R1_LondonMapModern", rparams={})
generatedImage.show()

ImageGen.py()
