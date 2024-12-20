from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Count
from .models import Post

class PostListView(APIView, LimitOffsetPagination):
    def get(self, request):
        # Fetch posts with comment count
        posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-timestamp')
        
        # Debugging posts existence
        if not posts.exists():
            print("No posts available")
            return Response({"message": "No posts available."}, status=200)
        
        # Paginate the results
        results = self.paginate_queryset(posts, request, view=self)
        if results is None:
            print("Pagination returned None")
            return Response({"message": "No results to paginate."}, status=200)

        # Prepare response data
        data = []
        for post in results:
            comments = post.comments.all().order_by('-timestamp')[:3]
            data.append({
                "post_id": str(post.id),
                "post_text": post.text,
                "timestamp": post.timestamp,
                "author": getattr(post.user, "username", "Anonymous"),
                "comment_count": post.comment_count,
                "comments": [
                    {
                        "comment_id": str(comment.id),
                        "comment_text": comment.text,
                        "timestamp": comment.timestamp,
                        "author": getattr(comment.user, "username", "Anonymous")
                    }
                    for comment in comments
                ]
            })
        
        # Debugging response data
        print("Prepared data:", data)
        
        # Return the paginated response
        return self.get_paginated_response(data)
