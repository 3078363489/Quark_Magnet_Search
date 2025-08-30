from article.models import Site_Information,Downloads,Friendship_Link

def get_article_type(request):
    return {"Site_Information":  Site_Information.objects.first()}

def get_Downloads(request):
    return {"Downloads": Downloads.objects.first()}
def get_Friendship_Link(request):
    return {"Friendship_Link": Friendship_Link.objects.all()}