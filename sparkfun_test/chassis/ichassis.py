class IChassis:
    def go_forward(self, speed): raise NotImplementedError

    def go_backward(self, speed): raise NotImplementedError

    def turn_left(self, speed, angle): raise NotImplementedError

    def turn_right(self, speed, angle): raise NotImplementedError

    def stop_gradually(self):
        ''' stop slowly '''
        raise NotImplementedError

    def stop_now(self):
        ''' stop immediately '''
        raise NotImplementedError
