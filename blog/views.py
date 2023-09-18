from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# Create your views here.
def blogHome(request): 
    allPosts= Post.objects.all()
    print("avinash",allPosts)
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    post.views= post.views +1
    post.save()

    post_tags = Post.tags.all()
    similar_posts=Post.objects.filter(tags__in=post_tags)
    print("avinash")
    similar_posts=similar_posts.annotate(tag_count=Count('tags')).order_by('-tag_count', 'slug')
    print("avinash")
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict, 'similar_posts' : similar_posts}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")



def send_email(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        message = request.POST.get('message')
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(sno=post_id)
        except Post.DoesNotExist:
            messages.error(request, 'Post does not exist.')
            return redirect(f"/blog/{post.slug}")
        subject = f'Sharing a post: {post.title}'
        post_url = request.build_absolute_uri(f'/post/{post_id}/')  
        email_message = f'Check out this post: {post.title}\n\n{message}\n\n{post_url}'
        send_mail(subject, email_message, 'your_email@example.com', [recipient_email])
        messages.success(request, 'Email sent successfully.')
        return redirect(f"/blog/{post.slug}")
    return redirect(f"/blog/{post.slug}")












