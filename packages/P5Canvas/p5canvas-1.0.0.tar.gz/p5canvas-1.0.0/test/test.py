import os
import sys
sys.path.append(os.path.join(os.curdir, '../P5Canvas'))
import P5Canvas


class MyCanvas(P5Canvas):
    def setup(self, p5):
        self.x = 100
        self.y = 100
        p5.createCanvas(300, 300)

    def draw(self, p5):
        p5.background(128)
        p5.fill(255, 0, 0)
        p5.ellipse(self.x, self.y, 50, 50)

        if p5.keyIsDown(p5.LEFT_ARROW):
            self.x -= 1
        if p5.keyIsDown(p5.RIGHT_ARROW):
            self.x += 1
        if p5.keyIsDown(p5.UP_ARROW):
            self.y -= 1
        if p5.keyIsDown(p5.DOWN_ARROW):
            self.y += 1


MyCanvas().run()
