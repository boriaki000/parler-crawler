import requests

requests.packages.urllib3.disable_warnings()

class Parler():

    def __init__(self, mst, jst, headers = False, log = False):
        self.mst = mst
        self.jst = jst
        self.log = log
        self.version = 'v1'
        self.base = f'https://api.parler.com/{self.version}'

        self.cookies = {
            'mst': self.mst,
            'jst': self.jst
        }

        self.headers = headers if headers else {
            'Accept': 'application/json, text/plain, */*',
            'Host': 'api.parler.com',
            'Referer': 'https://parler.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)

    def post(self, body, links = [], sensitive = False, state = 4):
        """
            POST /v1/post/async

            Creates a post

            note: if body is empty and parent is set... this is an echo
            note: if body is set and parent is set... this is a comment echo

            @param body - String
            @param links - Array of links?
            @param parent - String of a PostId, will make this an echo comment
            @param sensitive - Boolean if you are a bitch or not
            @param state - Number tf? default 4
        """
        endpoint = f'{self.base}/post/async'

        params = {
            'body': body,
            'links': links,
            'sensitive': sensitive,
            'state': state
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def deletePost(self, postId):
        """
            POST /v1/post/delete

            Deletes a post or echo

            @param id - String of a PostId
        """
        endpoint = f'{self.base}/post/delete?id={postId}'

        params = {
            'id': postId,
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def echo(self, postId, links = [], sesitive = False, state = 4):
        """
            POST /v1/post/async

            echos a post

            @param parent - String of a PostId, will make this an echo comment

        """
        endpoint = f'{self.base}/post/async'

        params = {
            'parent': postId,
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def commentEcho(self, postId, body = '', links = [], sensitive = False, state = 4):
        """
            POST /v1/post/async

            echos a post with a comment

            note: if body is empty and parent is set... this is an echo
            note: if body is set and parent is set... this is a comment echo

            @param body - String
            @param links - Array of links?
            @param parent - String of a PostId, will make this an echo comment
            @param sensitive - Boolean if you are a bitch or not
            @param state - Number tf? default 4

        """
        endpoint = f'{self.base}/post/async'

        params = {
            'parent': postId,
            'body': body,
            'links': links,
            'sensitive': sensitive,
            'state': state
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def comment(self, postId, body = '', links = [], sensitive = False):
        """
            POST /v1/comment/async

            Posts a comment to the PostId

            @param body - String text of the comment
            @param links - Array of links?
            @param parent - String of the PostId
            @param sensitive - Boolean of if the comment is sensitive or not
        """
        endpoint = f'{self.base}/comment/async'

        params = {
            'body': body,
            'links': links,
            'parent': postId,
            'sensitive': sensitive,
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def deleteComment(self, postId):
        """
            POST /v1/comment/delete

            Deletes a comment on a post

            @param id - String of the PostId
        """
        endpoint = f'{self.base}/comment/delete?id={postId}'

        params = {
            'id': postId,
        }

        if self.log:
            print(endpoint)

        return self.session.post(endpoint, data=params).json()

    def postVote(self, postId):
        """
            POST /v1/post/upvote

            Upvotes a post

            @param id - String of the PostId
            @param up - Boolean to upvote (true) or downvote (false)
        """
        endpoint = f'{self.base}/post/upvote'

        params = {
            'id': postId
        }

        if self.log:
            print(endpoint)

        return self.session.post(endpoint, data=params).json()

    def deletePostUpvote(self, postId):
        """
            POST /v1/post/upvote/delete

            Deletes an upvote for a post

            @param id - String of the PostId
        """
        endpoint = f'{self.base}/post/upvote/delete?id={postId}'

        params = {
            'id': postId
        }

        if self.log:
            print(endpoint)

        return self.session.post(endpoint, data=params).json()

    def commentVote(self, postId, up = True):
        """
            POST /v1/comment/vote

            Votes a comment on a post

            @param id - String of the PostId
            @param up - Boolean to upvote (true) or downvote (false)
        """
        endpoint = f'{self.base}/comment/vote'

        params = {
            'id': postId,
            'up': up
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def deleteCommentVote(self, postId):
        """
            POST /v1/comment/vote/delete

            Deletes a 'vote' for a comment given the postId

            @param id - String of the PostId
        """
        endpoint = f'{self.base}/comment/vote/delete?id={postId}'

        params = {}

        if self.log:
            print(endpoint)

        return self.session.post(endpoint, data=params).json()

    def profile(self, username = False):
        """
            GET /v1/profile

            Gets user profile information. If username is not defined,
            return the logged in user's information.

            @param username - String @ of the user to get information for

        """
        endpoint = f'{self.base}/profile'

        if username:
            endpoint = f'{endpoint}?username={username}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def follow(self, username):
        """
            GET /v1/follow

            Follow the username

            @param username - String @ of the user to follow
        """
        endpoint = f'{self.base}/follow?username={username}'

        params = {
            'username': username
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def unfollow(self, username):
        """
            POST /v1/follow/delete

            Unfollows a user by their username

            @param username - String @ of the user to unfollow
        """
        endpoint = f'{self.base}/follow/delete?username={username}'

        params = {
            'username': username
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def block(self, username):
        """
            POST /v1/user/block

            Blocks a username

            @param username - String @ of the user to block
        """
        endpoint = f'{self.base}/user/block'

        params = {
            'username': username
        }

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def unblock(self, userId):
        """
            POST /v1/user/block/delete

            Unblocks a user by their userId

            @param id - String of a user ID
        """
        endpoint = f'{self.base}/user/block/delete?id={userId}'

        if self.log:
            print(endpoint)

        return self.session.post(endpoint).json()

    def settings(self):
        """
            GET /v1/profile/settings

            Gets the settings for the logged in user
        """
        endpoint = f'{self.base}/profile/settings'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def updateProfile(self, bio = False, location = False, name = False, title = False, username = False, accountColor = False):
        """
            POST /v1/profile/update

            Updates the logged in user's profile information

            @param bio - String
            @param location - String
            @param name - String
            @param title - String
            @param username - String
            @param accountColor - String hex html value of color
        """
        endpoint = f'{self.base}/profile/update'

        params = {}

        if bio:
            params['bio'] = bio

        if location:
            params['location'] = location

        if name:
            params['name'] = name

        if title:
            params['title'] = title

        if username:
            params['username'] = username

        if accountColor:
            params['accountColor'] = accountColor

        if self.log:
            print(endpoint)
            print(params)

        return self.session.post(endpoint, data=params).json()

    def getPostsOfUserId(self, userId, limit = 10, startKey = False):
        """
            GET /v1/post/creator

            Gets the posts for the userId with a specified limit

            @param id - String of the ID of the user
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/post/creator?id={userId}'

        if limit:
            endpoint = f'{endpoint}&limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def getLikesOfUserId(self, userId, limit = 10, startKey = False):
        """
            GET /v1/post/creator/liked

            Gets the liked posts by a userId

            @param id - String of the ID of the user
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/post/creator/liked?id={userId}'

        if limit:
            endpoint = f'{endpoint}&limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def getCommentsOfUser(self, username, limit = 10, startKey = False):
        """
            GET /v1/comment/creator

            Gets the comments of the given username

            @param username - String @ of the username
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/comment/creator?username={username}'

        if limit:
            endpoint = f'{endpoint}&limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def getFollowingOfUserId(self, userId, limit = 10, startKey = False):
        """
            GET /v1/follow/following

            Gets the following list of the userId

            @param id - String of the ID of the user
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/follow/following?id={userId}'

        if limit:
            endpoint = f'{endpoint}&limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def getFollowersOfUserId(self, userId, limit = 10, startKey = False):
        """
            GET /v1/follow/followers

            Gets the list of user who the user is following

            @param id - String of the ID of the user
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/follow/followers?id={userId}'

        if limit:
            endpoint = f'{endpoint}&limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def userSearch(self, username = ''):
        """
            GET /v1/users

            Gets a list of user details given the username, if no username
            is defined, return a list of shit users they promote.

            @param search - String of a username
        """
        endpoint = f'{self.base}/users?search={username}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def hashtagSearch(self, hashtag = ''):
        """
            GET /v1/hashtag

            Gets a list of hashtags and their associated counts given a
            hashtag. If no hashtag is defined, it returns what is trending.

            @param search - String of a hashtag (no #)
        """
        endpoint = f'{self.base}/hashtag?search={hashtag}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json();

    def getFeed(self, limit = 10, startKey = False, hideEchos = False, onlySubscribed = False):
        """
            GET /v1/feed

            Returns the 'feed' of the currently logged in user.

            @param hideEchoes - Boolean if the feeds should hide echos
            @param onlySubscribed - Boolean if the feeds should only show users you subscribed to
            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/feed'

        if limit:
            endpoint = f'{endpoint}?limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if hideEchos:
            endpoint = f'{endpoint}&hideEchoes=true'

        if onlySubscribed:
            endpoint = f'{endpoint}&onlySubscribed=true'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def getNotifications(self, limit = 10, startKey = False):
        """
            GET /v1/notification

            Gets the logged in user's notifications

            @param limit - Number of results to return
            @param startKey - Timestamp used for paging
        """
        endpoint = f'{self.base}/notification'

        if limit:
            endpoint = f'{endpoint}?limit={limit}'

        if startKey:
            endpoint = f'{endpoint}&startKey={startKey}'

        if self.log:
            print(endpoint)

        return self.session.get(endpoint).json()

    def deleteAllNotifcations(self):
        """
            POST /v1/notification/all/delete

            Deletes all the notifications for the logged in user

            note: id is an empty string
        """
        endpoint = f'{self.base}/notification/all/delete'

        if self.log:
            print(endpoint)

        return self.session.post(endpoint, data={ 'id': '' }).json()

    def uploadImage(self, image):
        """
            POST /v2/upload/image

            TODO: Uploads an image (or maybe something else?) to parlers cdn

            multipart/form-data

            @param file - Data
            @param filename - String of the name of the uploaded file
        """
        endpoint = f'https://api.parler.com/v2/upload/image'

        return True
