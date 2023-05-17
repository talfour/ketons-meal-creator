from django.urls import path
from .views import CategoryListView, QuestionCreateView, QuestionDetailView, QuestionListView, like_unlike_question, check_if_exists, mark_as_best_answer
# CategoryCreateView
app_name = 'questions'

urlpatterns = [
    path("", CategoryListView.as_view(), name="question-categories"),
    path("create/", QuestionCreateView.as_view(), name="question-create"),
    path("category/<slug>/", QuestionListView.as_view(), name="questions"),
#     path("create_category/", CategoryCreateView.as_view(),
     #     name="question-category-create"),
    path("details/<slug>/", QuestionDetailView.as_view(),
         name="question-detail-view"),
    path("marked/", mark_as_best_answer, name="mark-best-answer"),
    path("check_if_exists", check_if_exists, name="check_if_exists"),
    path("vote-system", like_unlike_question, name="vote_like")

]
