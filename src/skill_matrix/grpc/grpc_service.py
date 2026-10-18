import grpc
from concurrent import futures

from src.skill_matrix.grpc import matching_pb2, matching_pb2_grpc
from src.skill_matrix.database import SessionLocal
from src.skill_matrix import crud


class MatchingService(matching_pb2_grpc.MatchingServiceServicer):
    def FindCandidates(self, request, context):

        print(f"Запрос: skill_id={request.skill_id}, "f"project_id={request.project_id}, min_level={request.min_level}")
        db = SessionLocal()
        try:
            candidates = crud.find_candidates_for_project(
                db,
                skill_id=request.skill_id,
                project_id=request.project_id,
                min_level=request.min_level,
            )

            print(f"Найдено кандидатов: {len(candidates)}")
            response = matching_pb2.FindCandidatesResponse()
            for user in candidates:
                print(f"{user.username} (id={user.user_id})")
                candidate = matching_pb2.Candidate(
                    user_id=user.user_id,
                    username=user.username,
                    email=user.email,
                    level=0,
                    role_id=user.role_id,  
                    department=user.department or "",
                )
                response.candidates.append(candidate)
            return response
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matching_pb2_grpc.add_MatchingServiceServicer_to_server(
        MatchingService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()