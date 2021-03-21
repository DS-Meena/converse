from friends.models import FriendRequest

# to determine if two users are friends
# if they are friends true else return false
def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False