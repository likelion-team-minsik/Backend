from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from collections import defaultdict
from .models import Choice, TestResult, Question
from rest_framework.generics import ListAPIView
from .serializers import QuestionSerializer, TestResultSerializer
# Create your views here.

#질문-선지 목록 가져오기
class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.prefetch_related('choices').all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

#선택한 답변 계산, 유형 분석, 결과 db저장
class SubmitTestView(APIView):
    permission_classes = [AllowAny]

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

        # 결과 저장
        #회원가입 유저일 때: DB저장
        if request.user.is_authenticated:
            TestResult.objects.create(
                user=request.user,
                result_type=result_type,
                scores=dict(type_scores)
            )
        else:
            #비로그인 유저일 때: 세션 저장
            request.session['last_test_result'] = {
                "result_type": result_type,
                "score_details": dict(type_scores)
            }

        return Response({
            "result_type": result_type,
            "score_details": type_scores
        })

class QuestionListAPIView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#분석 결과 불러오기
class MyTestResultsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TestResultSerializer

    def get(self, request):
        if request.user.is_authenticated:
            latest_result = TestResult.objects.filter(user=request.user).order_by('-created_at').first()
            if latest_result:
                serializer = TestResultSerializer(latest_result)
                return Response(serializer.data)
            else:
                return Response({"detail": "결과가 없습니다."}, status=404)

        # 비로그인 사용자용 - 세션에서 가져오기
        last_result = request.session.get('last_test_result')
        if last_result:
            return Response(last_result)  # 리스트 아님
        else:
            return Response({"detail": "저장된 결과가 없습니다."}, status=404)
