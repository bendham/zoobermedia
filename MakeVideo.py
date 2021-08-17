from video.RedditVideoInterface import RedditVideoInterface

if __name__ == "__main__":

    print("Generating new compilation...\n")

    newCompilation = RedditVideoInterface("contagiouslaughter")
    newCompilation.generateVideoList()