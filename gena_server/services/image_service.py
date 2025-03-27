import uuid

'''
class image_service:

    def create_image(self, link, time, rating):
        try:
            image = gena_server.Image.objects.crate(imageID = uuid.uuid4(), link_to_image = link, createdAt = time, rating = rating)
            return image
        except Exception as e:
            print(f"Error with creating an image object: ", e)

    def delete_image(self, image_id):
        try:
            image = gena_server.Image.objects(imageID = image_id)
            image.delete()
            return image
        except Exception as e:
            print(f"Error with deleting an image: ", e)

    def update_image(self, image_id, link=None, rating=None):
        try:
            image = gena_server.Image.objects(imageID = image_id)
            image.link_to_image = link
            image.rating = rating
        except Exception as e:
            print(f"Error with deleting an image: ", e)
'''