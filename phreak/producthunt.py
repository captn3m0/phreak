import requests

ACCESS_TOKEN = "9471cd3235687f1f20263f064997376cb7ec16493eb46a580293da5d0825fd30"
API_ROOT = "https://api.producthunt.com/v1/"

class ProductHunt:
    etag = False
    posts = []
    @staticmethod
    def getPosts():
        headers = {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json',
            'Authorization':'Bearer '+ACCESS_TOKEN,
            'Accept-Encoding': '' # To disable auto gzip decompression
        }
        if ProductHunt.etag!=False:
            headers['If-None-Match'] = ProductHunt.etag

        r = requests.get(API_ROOT + "posts/all?per_page=10", headers=headers)

        if r.status_code == 304 and ProductHunt.posts!= []:
            return ProductHunt.posts

        ProductHunt.posts = r.json()['posts']
        ProductHunt.etag  = r.headers.get('etag')
        return ProductHunt.posts
