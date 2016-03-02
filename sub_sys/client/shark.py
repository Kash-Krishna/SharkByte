class Shark:
    """ Sharks //users of SharkByte
    Attributtes:
    
    uid: unique id for each user x0000 to xFFFF
    sub_list: list of user's subscription
    
    """
    def __init__(self, unique_id):
        self.display_name = ""
        self.uid = unique_id
        self.sub_list = [] #list of other users the current user is subscribe to
        self.group_tags = [] #same as subs, but for tracker/friend groups
        return

    def __eq__(self, other):
        return self.uid == other.uid
    
    def printSharkInfo(self):
        print "Display Name: " + self.display_name
        print "uid: " + self.uid
        return

    def follow_the_shark(self, other):
        if other not in self.sub_list:
            self.sub_list.append(other)
        return

    def follow_the_shiver(self, shiver):
        if shiver not in self.group_tags:
            self.group_tags.append(shiver)
        return
