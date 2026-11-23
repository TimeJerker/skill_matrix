import grpc

from src.skill_matrix.config import settings
from src.skill_matrix.grpc import matching_pb2, matching_pb2_grpc


def find_candidates(skill_id: int, project_id: int, min_level: int = 1):
    channel = grpc.insecure_channel(settings.GRPC_ADDRESS())
    stub = matching_pb2_grpc.MatchingServiceStub(channel)
    request = matching_pb2.FindCandidatesRequest(
        skill_id=skill_id,
        project_id=project_id,
        min_level=min_level,
    )
    response = stub.FindCandidates(request)
    return response.candidates
