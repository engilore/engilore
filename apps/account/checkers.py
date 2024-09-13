

def check_if_admin_or_guardian(self):
    if self.email == self.ADMIN_EMAIL:
        self.is_admin = True
        self.is_guardian = True
    else:
        if not self.is_admin:
            self.is_admin = False
        if not self.is_guardian:
            self.is_guardian = False
