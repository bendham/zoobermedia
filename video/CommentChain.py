
from asyncio.windows_events import NULL


from RedditComment import RedditComment

class CommentChain:

    def __init__(self) -> None:
        self.top = NULL
        self.count = 0
    
    def addComment(self, comment: RedditComment):
        self.count += 1

        if self.top is NULL:
            self.top = comment
            return

        cur = self.top
        while(cur.nextComment):
            cur = cur.nextComment
        
        cur.next = comment



    # def populateChildComments(self):
    #     isStillGoodComments = True
    #     clickedContinueThread = False
    #     commentCount = 1
    #     compareScore = self.com.score

    #     replies = self.com.replies
    #     if(len(replies)): # Is this right?
    #         child = self.com.replies[0]
    #         threadId = child.id
    #         if(type(child)==MoreComments): # I dont deal with this case for right now...
    #             isStillGoodComments = False
    #     else:
    #         isStillGoodComments = False

    #     while(isStillGoodComments):
    #         if(child.score/compareScore >= self.PERCENT_TO_BEAT and commentCount < self.MAX_CHILD_COMMENTS):
    #             if(len(child.body.split(" ")) < self.MAX_AMOUNT_OF_WORDS):

    #                 if(commentCount == 2):
    #                     try:
    #                         # Is this the problem?
    #                         threadElm = WebDriverWait(self.drv, self.timeout).until(
    #                         lambda x: x.find_element(By.XPATH, f"//div[@id='continueThread-t1_{threadId}']/div[2]/a"))
                            
    #                         threadElm.click()

    #                         newCmt = WebDriverWait(self.drv, 10*self.timeout).until(EC.visibility_of_element_located((By.ID, f"t1_{child.id}")))
            
    #                         self.drv.execute_script("arguments[0].scrollIntoView();", newCmt)
                            
    #                     except TimeoutException:
    #                         isStillGoodComments = False
    #                         print("Page load timed out, could not continue the thread...")
    #                         break
    #                     else:
    #                         clickedContinueThread = True

    #                 redditChildComment = RedditComment(self.speechEngine, self.drv, child, self.identifier + str(commentCount), self.urlToUse)
    #                 if(redditChildComment.goodToUse == True):
    #                     self.childComments.append(redditChildComment)
    #                     compareScore = child.score
    #                     child = child.replies[0]

    #                     commentCount += 1
    #                 else: # Maybe add
    #                     isStillGoodComments = False
    #             else:
    #                 isStillGoodComments = False
    #         else:
    #             isStillGoodComments = False

    #     if(clickedContinueThread):
    #         self.drv.execute_script("window.history.go(-1)")
    #         #self.drv.get(self.urlToUse)

    # def buildVideoFrames(self):

    #     bgBase = Image.open(BACKGROUND_FILE_DIR)
    #     bgX, bgY = bgBase.size

        
        
    #     totalCommentHeight = 0
    #     commentList = []
    #     commentImg = RedditCommentImage(self)
    #     commentList.append(commentImg)
    #     totalCommentHeight += commentImg.h
    #     for comment in self.childComments:
    #         if(comment.goodToUse): # There has to be a better way
    #             commentImg = RedditCommentImage(comment)
    #             commentList.append(commentImg)
    #             totalCommentHeight += commentImg.h
    #         else:
    #             break
                
    #     totalHeightSpace = bgY*0.8
    #     scaleFactor = totalHeightSpace/totalCommentHeight
    #     usedScaleFactor = scaleFactor

    #     if(scaleFactor*commentList[0].w > bgX):
    #         usedScaleFactor = (bgX*0.95)/commentList[0].w

    #     newTotalHeight = 0
    #     for comment in commentList:
    #         newTotalHeight += comment.h*usedScaleFactor

    #     prevCommentH = 0
    #     hOffset = 0
    #     for idx, comment in enumerate(commentList):
            
    #         f1 = comment.resizeCommentImage(usedScaleFactor)
    #         bgBase.paste(f1, ((bgX-f1.width)//2, math.floor((bgY-newTotalHeight)//2 + hOffset)))
    #         comment.redditComment.commentFrameDir = os.path.join(COMMENT_PNG_FRAME_DIR, f"f{str(idx+1)}_{self.getId()}.png")
    #         bgBase.save(os.path.join(COMMENT_PNG_FRAME_DIR, comment.redditComment.commentFrameDir))

    #         prevCommentH = f1.height

    #         hOffset += prevCommentH