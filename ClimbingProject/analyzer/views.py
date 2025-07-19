from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from collections import defaultdict
from .models import Choice, TestResult, Question
from rest_framework.generics import ListAPIView
from .serializers import QuestionSerializer, TestResultSerializer
# Create your views here.

#질문-선지 목록 가져오기
class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.prefetch_related('choices').all()
        print("✅ questions:", questions)
        serializer = QuestionSerializer(questions, many=True)
        print("✅ serializer data:", serializer.data)
        return Response(serializer.data)

#선택한 답변 계산, 유형 분석, 결과 db저장
class SubmitTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answers = request.data.get("answers", [])
        type_scores = defaultdict(int)  # {"재미형": 5, "계획형": 3, ...}

        for answer in answers:
            choice_id = answer.get("choice_id")
            try:
                choice = Choice.objects.get(id=choice_id)
                type_scores[choice.type] += choice.score
            except Choice.DoesNotExist:
                continue  # 유효하지 않은 선택지는 무시

        if not type_scores:
            return Response({"error": "유효한 선택지가 없습니다."}, status=400)

        # 최고 점수인 유형 결정
        result_type = max(type_scores.items(), key=lambda x: x[1])[0]

        # 결과 저장 (선택)
        TestResult.objects.create(
            user=request.user,
            result_type=result_type,
            scores=dict(type_scores)
        )

        return Response({
            "result_type": result_type,
            "score_details": type_scores
        })

class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#분석 결과 불러오기
class MyTestResultsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestResultSerializer

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user).order_by('-created_at')