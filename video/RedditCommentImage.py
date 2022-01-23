from PIL import Image, ImageOps

class RedditCommentImage:
    def __init__(self, redditComment) -> None:
        self.img = Image.open(redditComment.pngPath)
        self.w, self.h = self.img.size
        self.redditComment = redditComment

    def resizeCommentImage(self, rescaleFactor):

        print(f"prevH: {self.h}")
        print(f"prevW: {self.w}")

        self.h = int(self.h*rescaleFactor)
        self.w = int(self.w*rescaleFactor)

        print(f"newH: {self.h}")
        print(f"newW: {self.w}")

        f1 = ImageOps.fit(self.img, (self.w, self.h))

        return f1