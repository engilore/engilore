

def check_if_admin_or_guardian(self):
        if self.email == self.ADMIN_EMAIL:
            self.is_admin = True
            self.is_guardian = True
        else:
            self.is_admin = False
            self.is_guardian = False
