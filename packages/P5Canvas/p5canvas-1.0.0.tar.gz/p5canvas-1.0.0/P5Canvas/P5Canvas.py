class P5Canvas:
    def __init__(self):
        self.p5 = None

    def _setup(self):
        self.setup(self.p5)

    def setup(self, p5):
        pass

    def _draw(self):
        self.draw(self.p5)

    def draw(self, p5):
        pass

    def preload(self):
        pass

    def key_pressed(self, event):
        pass

    def key_released(self, event):
        pass

    def key_typed(self, event):
        pass

    def mouse_moved(self, event):
        pass

    def mouse_dragged(self, event):
        pass

    def mouse_pressed(self, event):
        pass

    def mouse_released(self, event):
        pass

    def mouse_clicked(self, event):
        pass

    def double_clicked(self, event):
        pass

    def mouse_wheel(self, event):
        pass

    def request_pointer_lock(self):
        pass

    def exit_pointer_lock(self):
        pass

    def run(self):
        import js # type: ignore # noqa

        def start(p5):
            self.p5 = p5
            p5.setup = self._setup
            p5.draw = self._draw
            p5.preload = self.preload
            p5.keyPressed = self.key_pressed
            p5.keyReleased = self.key_released
            p5.keyTyped = self.key_typed
            p5.mouseMoved = self.mouse_moved
            p5.mouseDragged = self.mouse_dragged
            p5.mousePressed = self.mouse_pressed
            p5.mouseReleased = self.mouse_released
            p5.mouseClicked = self.mouse_clicked
            p5.doubleClicked = self.double_clicked
            p5.mouseWheel = self.mouse_wheel
            p5.requestPointerLock = self.request_pointer_lock
            p5.exitPointerLock = self.exit_pointer_lock

        p5Start = js.window.Function("func", "new p5((p) => {func(p)})")
        p5Start(start)
